from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="wordify",
    version="1.0.0",
    author="Fathi Abdelmalek",
    author_email="abdelmalek.fathi.2001@gmail.com",
    url="https://github.com/FathiMalek/wordify.git",
    description="A Python module to convert numerical values into their word representation.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=['wordify'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
