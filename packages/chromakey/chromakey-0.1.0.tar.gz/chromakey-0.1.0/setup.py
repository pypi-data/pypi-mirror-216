from setuptools import find_packages, setup

setup(
    name="chromakey",
    version="0.1.0",
    packages=find_packages(),
    install_requires=["Pillow", "scipy", "numpy"],
)
