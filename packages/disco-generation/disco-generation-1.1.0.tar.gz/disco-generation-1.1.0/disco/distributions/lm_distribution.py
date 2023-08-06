# disco
# Copyright (C) 2022-present NAVER Corp.
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 license

import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, AutoModelForSeq2SeqLM

from collections import namedtuple

from .base_distribution import BaseDistribution
from disco.utils.helpers import get_token_first_indices


TextSample = namedtuple('TextSample', ['token_ids', 'text'])

class LMDistribution(BaseDistribution):
    """
    Language model distribution class, a core class for all NLP
    use-cases, relying on Huggingface's Transformers library.
    """

    def __init__(self,
            model="gpt2", tokenizer=None, auto=AutoModelForCausalLM, freeze=True,
            length=40, device="cpu",
            **config
        ):
        """
        Parameters
        ----------
        model: string
            Transformers' name of a causal or seq2seq language model 
        tokenizer: string
            Transformers' name for the related tokenizer
        auto: class
            auto class from Transformers, default is AutoModelForCausalLM
            but AutoModelForSeq2SeqLM is also valid
        freeze: boolean
            flag to eventually (not) freeze the network's parameters
        length: int
            number of tokens in the samples
        device: string
            reference of the computing device
        config: kwarg
            parameters and values passed to transformers' ```generate(…)```
        """

        self.tokenizer= AutoTokenizer.from_pretrained(tokenizer if tokenizer else model)
        assert auto in [AutoModelForCausalLM, AutoModelForSeq2SeqLM], "only AutoModel, AutoModelForCausalLM and AutoModelForSeq2SeqLM are valid options."
        self._load_network(auto, model)
    
        self.device = device
        self.network.to(self.device)
        self.network.eval() # to make sure scoring is consistent
        if freeze:
            self.freeze(True)

        self.length = length

        default_params = {
            "top_k": 0,
            "top_p": 1.0,
            "typical_p": 1.0,
            "temperature": 1.0,
            "num_beams": 1
        }
        self.params = default_params.copy()
        self.params.update(config)

        self.scorable = True if all(\
                [default_params[k] == self.params[k] for k in default_params.keys()]\
            ) else False

    def _load_network(self, auto, model):
        self.network = auto.from_pretrained(model)
        if not self.network.config.is_encoder_decoder:
            self.tokenizer.pad_token = self.tokenizer.eos_token
            self.network.config.pad_token_id = self.tokenizer.eos_token_id

    def to(self, device):
        self.device = device
        self.network.to(self.device)

    def freeze(self, frozen=True):
        """Freeze (or unfreeze) parameters for gradient computation.

        Parameters
        ----------
        frozen: boolean (True)
            state to transition to, default is to freeze
        """
 
        self.network.requires_grad_(not frozen)

    def log_score(self, samples, context="", grad=False, sum=True):
        """Computes log-probabilities for the samples according
        to the language model network in the given context

        Parameters
        ----------
        samples: list(Sample)
            samples to (log-)score as a list()
        context: text
            context for which to (log-)score the samples
        grad: boolean
            flag to eventually compute the gradients, e.g. when fitting
        sum: boolean
            flag to eventually return token-level tensor of scores

        Returns
        -------
        tensor of log-probabilities
        """

        assert self.scorable, "this distribution's parameters make it unscorable."
        shapes = set([s.token_ids.shape for s in samples])
        assert 1 == len(shapes), "sequences of token_ids should have the same shape, but got: {shapes}."

        device = self.device

        if not self.network.config.is_encoder_decoder:
            context = self.tokenizer.bos_token if "" == context else context
        tokenized_context = self.tokenizer([context] * len(samples), return_tensors="pt", add_special_tokens=True)
        tokenized_context["input_ids"] = tokenized_context["input_ids"].to(device)
        tokenized_context["attention_mask"] = tokenized_context["attention_mask"].to(device)

        tokenized_samples = dict()
        tokenized_samples["input_ids"] = torch.stack([sample.token_ids for sample in samples]).to(device)

        first_eos_indices = get_token_first_indices(
                tokenized_samples["input_ids"],
                self.tokenizer.eos_token_id
            )
        tokenized_samples["attention_mask"] = torch.where(
                self.tokenizer.pad_token_id == tokenized_samples["input_ids"],
                0, 1
            )
        for i, ix in enumerate(first_eos_indices):
            if None != self.network.config.forced_bos_token_id and\
                self.network.config.forced_bos_token_id == tokenized_samples["input_ids"][i][0]:
                    tokenized_samples["attention_mask"][i][0] = 0
            else:
                tokenized_samples["attention_mask"][i][0] = 1  # at least score one token
            if ix != -1:  # if there is an eos token
                tokenized_samples["attention_mask"][i][ix] = 1  # score first eos token
                tokenized_samples["attention_mask"][i][ix + 1:] = 0  # ignore everything after it
        tokenized_samples["attention_mask"] = tokenized_samples["attention_mask"].to(device)

        if self.network.config.is_encoder_decoder:
            shift = None
            last = None
            inputs = tokenized_context
            labels = tokenized_samples["input_ids"]
        else:
            shift = tokenized_context["input_ids"].shape[-1] - 1
            last = -1
            inputs = {
                "input_ids": torch.cat((tokenized_context["input_ids"], tokenized_samples["input_ids"]), 1),
                "attention_mask": torch.cat((tokenized_context["attention_mask"], tokenized_samples["attention_mask"]), 1)
            }
            labels = inputs["input_ids"]

        if grad:
            outputs = self.network(**inputs, labels=labels)
        else:
            with torch.no_grad():
                outputs = self.network(**inputs, labels=labels)
    
        all_logprobs = outputs.logits[:, shift:last, :].log_softmax(-1) # [n_samples, length, vocab]
        seq_logprobs = torch.gather(
                all_logprobs, 2, tokenized_samples["input_ids"][:, :, None]
            ).squeeze(-1) # [n_samples, length]

        seq_logprobs = torch.where(1 == tokenized_samples["attention_mask"], seq_logprobs, torch.tensor(0.).to(device))

        return seq_logprobs.sum(dim=1) if sum else seq_logprobs 

    def sample(self, context="", sampling_size=32, sum=True):
        """Samples sequences from the language model in the given context
        
        Parameters
        ----------
        context: text
            contextual text for which to sample
        sampling_size: int
            number of sequences to sample
        sum: Boolean
            flag to eventually return token-level tensor of scores
        
        Returns
        -------
        tuple of (list of Sample(tokens, text), tensor of logprobs)
        """
    
        if not self.network.config.is_encoder_decoder and not context:
            context = self.tokenizer.bos_token
        input_ids = self.tokenizer([context] * sampling_size, return_tensors="pt", add_special_tokens=True).input_ids.to(self.device)
        n_context_tokens = input_ids.shape[-1]

        if self.network.config.is_encoder_decoder:
            shift = 1
            last = None
        else:
            shift = n_context_tokens
            last = None

        outputs = self.network.generate(input_ids,
            output_scores=True, return_dict_in_generate=True,
            max_new_tokens=self.length,
            do_sample=True, **self.params)

        all_logprobs = torch.stack(outputs.scores, dim=1).log_softmax(-1)  # [sampling_size, length, vocab]
        token_seq_logprobs = torch.gather(
                all_logprobs, 2, outputs.sequences[:, shift:last][:, :, None]
            ).squeeze(-1) # [sampling_size, length]

        # we need to zero the (log-)scores of extra <eos>
        first_eos_indices = get_token_first_indices(
                outputs.sequences[:, shift:last],  # starting at 1 to skip an eventual bos token
                self.tokenizer.eos_token_id
            )
        non_pad_tokens = torch.cat(
                (outputs.sequences[:, shift:last][:, 0].unsqueeze(1),
                torch.where(
                        self.tokenizer.pad_token_id == outputs.sequences[:, shift:last][:, 1:],
                        -1,
                        outputs.sequences[:, shift:last][:, 1:])
                    ),
                dim=1
            )
        non_pad_log_scores = torch.where(-1 != non_pad_tokens, token_seq_logprobs, torch.tensor(0.).to(self.device))
        for i, ix in enumerate(first_eos_indices):
            non_pad_log_scores[i][0] = token_seq_logprobs[i][0]  # at least score one token
            if ix != -1: # if there an eos token
                non_pad_log_scores[i][ix] = token_seq_logprobs[i][ix]  # keep the first eos scores
                non_pad_log_scores[i][ix + 1:] = 0. # ignore everything after eos
        
        seq_logprobs = non_pad_log_scores.sum(dim=1) if sum else non_pad_log_scores

        output_tokens = outputs.sequences[:, shift:] # [sampling_size, length]

        return (
                [TextSample(ots, self.tokenizer.decode(ots)) for ots in output_tokens],
                seq_logprobs
            )
