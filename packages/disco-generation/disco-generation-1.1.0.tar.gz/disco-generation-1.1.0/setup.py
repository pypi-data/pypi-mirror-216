# disco
# Copyright (C) 2022-present NAVER Corp.
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0 license

from setuptools import setup, find_packages

setup(
    name='disco-generation',
    version='1.1.0',
    description='A toolkit for distributional control of generative models',
    url='https://github.com/naver/disco',
    author='Naver Labs Europe', author_email='jos.rozen@naverlabs.com',
    license='Creative Commons Attribution-NonCommercial-ShareAlike 4.0',
    long_description="""The 🕺🏽 **disco** toolkit allows to control language models and other generative systems to match human preferences while avoiding catastrophic forgetting.

To achieve this, **disco** decouples the problem of expressing _what_ properties the model should have from _how_ to actually get the desired model as separate steps.

**Step 1: ⚓ We express how the target distribution *should* be**

First, we define some feature over the generated samples that matters to us. It can be anything we can compute. For example, on a language model it can be as simple as whether the generated text contains a certain word or as complex as the compilability of some generated piece of code. Importantly, there is no need for the feature to be differentiable.

Then, we can express our preferences on the target distribution by deciding how prevalent the feature should be. For example, we might want to ask that a certain word appears 50% of the time when sampling from the model; or that 100% of the generated code is compilable. The resulting target distribution is expressed as an energy-based model or EBM, which is an unnormalized probability distribution that respects the desired moments while avoiding catastrophic forgetting, as a result of having minimal KL divergence to the original model.

The resulting representation of the target distribution can *score* samples, but cannot directly be used to *generate* them.

**Step 2: 🎯 Approximate the target distribution**

To generate samples from the target distribution we can tune a model to approximate it. We do this by minimizing the divergence to the target distribution. While techniques such as reinforcement learning from human feedback (RLHF) are restricted to using one kind of divergence only (specifically, reverse KL divergence), **disco** is more general, allowing the use of the full class of f-divergences, including both forward and reverse KL divergence, Jensen-Shannon, and total variation distance.

**Step 3: 💬 Generate content that matches the preferences**

The resulting model can generate samples directly from a close approximation of the target distribution. Furthermore, it can be used jointly with Quasi-Rejection Sampling (QRS), a Monte Carlo sampling technique that allows the generation of samples that are even more representative of the target distribution.
Alternatively, it is then possible to use decoding methods such as nucleus sampling, top-k sampling, or beam search, which would return samples from a further updated target distribution.""",
    long_description_content_type='text/markdown',
    packages=find_packages(include=['disco', 'disco.*']),
    python_requires='>=3.8, <3.11',
    install_requires=['torch', 'transformers',
            'numpy', 'scipy',
            'datasets', 'spacy',
            'notebook',
            'neptune-client', 'wandb'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Science/Research',
        'License :: Free for non-commercial use',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
