from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="SimpleSplit",
    version="0.1.1",
    author="GitHub @fakerybakery",
    author_email="me@mrfake.name",
    description="Split and re-combine large binary files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fakerybakery/simplesplit",
    packages=["simplesplit"],
    install_requires=["tqdm"],
    entry_points={
        "console_scripts": [
            "simplesplit = simplesplit.main:main",
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    platforms=["Any"],
)