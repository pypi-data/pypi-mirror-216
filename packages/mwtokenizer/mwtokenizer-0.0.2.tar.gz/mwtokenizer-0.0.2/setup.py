import codecs
import os

from setuptools import find_packages, setup

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "README.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = "0.0.2"
DESCRIPTION = "Wikipedia Tokenizer Utility"
LONG_DESCRIPTION = """A language-agnostic NLP toolkit for processing Wikipedia
articles with adequate performance out-of-the-box."""

# Dev dependencies
EXTRAS_REQUIRE = {
    "tests": ["pytest>=6.2.5"],
    "pre-commit": ["pre-commit"],
    "typing": ["mypy>=0.961"],
    "benchmarking": ["pandas"],
}

EXTRAS_REQUIRE["dev"] = (
    EXTRAS_REQUIRE["tests"]
    + EXTRAS_REQUIRE["pre-commit"]
    + EXTRAS_REQUIRE["typing"]
    + EXTRAS_REQUIRE["benchmarking"]
)

# Setting up
setup(
    name="mwtokenizer",
    version=VERSION,
    author="Appledora & Isaac Johnson & Martin Gerlach",
    author_email="<isaac@wikimedia.org>",
    url="https://gitlab.wikimedia.org/repos/research/wiki-nlp-tools/",
    license="MIT License",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=["regex", "requests", "sentencepiece"],
    keywords=["python", "wikipedia", "nlp", "tokenizer"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ],
    extras_require=EXTRAS_REQUIRE,
    package_data={
        "mwtokenizer": [
            "assets/spcmodels/*.model",
            "assets/spcmodels/*.vocab",
            "assets/dict_abbr_filtered.json",
        ]
    },
    include_package_data=True,
    zip_safe=False,
)
