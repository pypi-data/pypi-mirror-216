from setuptools import setup
from setuptools import find_packages

setup(
    name="genagg",
    version="1.0.0",
    packages=find_packages(),
    install_requires=["torch", "torch_scatter", "torch_geometric", "pandas", "gym", "wandb"],
    author="Ryan Kortvelesy",
    description="A Learnable, Generalised Aggregation Module",
)
