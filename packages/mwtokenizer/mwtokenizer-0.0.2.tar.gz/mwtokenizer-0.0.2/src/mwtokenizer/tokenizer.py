import json
from importlib.resources import open_text, path
from typing import Any, Iterator, List, Set

import regex as re  # https://pypi.org/project/regex/
import sentencepiece as spm

from mwtokenizer.config.symbols import ALL_UNICODE_PUNCTUATION as PUNCTUATIONS
from mwtokenizer.config.symbols import (
    GLOBAL_SENTENCE_TERMINATORS as SENTENCE_TERMINATORS,
)
from mwtokenizer.config.symbols import NON_WHITESPACE_LANGUAGES_SPC_MAPPING as NWL
from mwtokenizer.utils import capture_trailing_space

# the `(?<=...)` is a positive lookbehind assertion, which means that
# the regex engine will only match if the pattern is preceded by the given pattern.
# the `[%s]`` is a character class, which means that the regex engine
# will match any of the characters in the SENTENCE_TERMINATORS character group.
# the `\s+` is a quantifier, which means that the regex engine will
# match a whitespace character 1 or more times. Using the parenthesis we capture
# these whitespaces as a group

global_sent_split_pattern = re.compile(
    r"(?<=[%s])(\s+)" % "".join(SENTENCE_TERMINATORS)
)


def whitespace_word_tokenization(
    text: str = "", abbreviations: Set[str] = None
) -> Iterator[str]:
    """
    This function tokenizes a text string into a list of tokens using whitespace as a delimiter.
    Tokens can be any sequence of consecutive whitespace characters,
    any sequence of consecutive puntuations, single punctuation characters not
    surrounded by word characters, or any sequence of word characters (which may include internal
    punctuation). For example, the text "I'm a sentence. \n" will be tokenized into
    ["I'm", " ", "a", " ", "sentence", ".", " \n"].

    :param text: The text string to be tokenized
    :type text: str
    :param abbreviations: A set of abbreviations to be used for tokenization
    :type abbreviations: Set[str]
    :return: A list of tokens
    :rtype: List[str]
    """
    # Initialize an empty string to hold the current word being processed
    current_word = ""
    idx = 0
    while idx < len(text):
        char = text[idx]
        # If the character is a whitespace character
        if char.isspace():
            # If there is a current word being processed, first yield it as a token
            if current_word:
                yield current_word
                current_word = ""

            # Yield the consecutive whitespace character(s) as a single token
            start_idx = idx
            while idx + 1 < len(text) and text[idx + 1].isspace():
                idx += 1
            yield text[start_idx : idx + 1]

        # If the character is a unicode punctuation character
        elif char in PUNCTUATIONS:
            # current character is not the last character of the string
            if idx != len(text) - 1:
                start_idx = idx
                if text[idx + 1] in PUNCTUATIONS or text[idx + 1].isspace():
                    # check if the punctuation is followed by consecutive punctuation character
                    while idx + 1 < len(text) and text[idx + 1] in PUNCTUATIONS:
                        idx += 1

                    # check if the consecutive punctuations are at the end of the string
                    if idx == len(text) - 1 or text[idx + 1].isspace():
                        # if consecutive/single punctuations are at the end of a word, e.g: " learning?!! ",
                        # or at the end of the string, e.g: "What is deep learning?!!",
                        # they are yielded as separate tokens e.g: "learning", "?!!"
                        if current_word + text[start_idx : idx + 1] in abbreviations:
                            yield current_word + text[start_idx : idx + 1]
                        else:
                            yield current_word
                            yield text[start_idx : idx + 1]
                        current_word = ""

                    elif text[start_idx - 1].isspace() or start_idx == 0:
                        # if consecutive punctuations are at the beginning of a word, e.g: "!!What is going on",
                        # they are yielded as separate tokens
                        yield text[start_idx : idx + 1]
                        current_word = ""

                    else:
                        # if consecutive punctuations are inside a word, they are not yielded as separate tokens
                        # e.g: "partic...ular" is tokenized as "partic...ular"
                        current_word = current_word + text[start_idx : idx + 1]

                else:
                    # if the punctuation is not followed by consecutive punctuation character or whitespace
                    # eg: "40.123"
                    if idx == 0 or text[idx - 1].isspace():
                        yield char
                    else:
                        current_word += char

            # if the punctuation is the last character of the text eg: "Hello?",
            # yield both the current word and the punctuation character as separate tokens
            elif idx == len(text) - 1:
                if current_word + char in abbreviations:
                    yield current_word + char
                else:
                    yield current_word
                    yield char
                current_word = ""

        else:
            current_word += char
        idx += 1
    # If the character is not a whitespace or punctuation character, add it to the current word being processed
    if current_word:
        yield current_word


def non_whitespace_word_tokenization(
    text: str = "", spc_model: Any = None
) -> Iterator[str]:
    # add sphinx style docstring
    """
    This function tokenizes a text string into a list of tokens using a sentencepiece model
    as a tokenizer. The model is trained on a corpus of wikipedia articles extracted from multiple
    non-whitespace language projects, such as Chinese, Japanese, Laos, Thai, etc.

    :param text: The text string to be tokenized
    :type text: str
    :param spc_model: The sentencepiece model to be used for tokenization
    :type spc_model: Any
    :return: A list of tokens
    :rtype: List[str]
    """

    tokens = spc_model.tokenize(text, out_type=str)
    for token in tokens:
        yield token


class Tokenizer:
    def __init__(
        self,
        language_code: str = "en",
        abbreviations_file_name: str = "dict_abbr_filtered.json",
    ) -> None:
        """
        :param language_code: The language code of the language to be tokenized
        :type language_code: str
        :param abbreviations_file_name: The name of the json file containing the abbreviations
        :type abbreviations_file_path: str
        """

        self.language_code = language_code
        try:
            with open_text("mwtokenizer.assets", abbreviations_file_name) as fin:
                all_abbreviations = json.load(fin)
            self.abbreviations = all_abbreviations[self.language_code + "wiki"]
        except Exception:
            self.abbreviations = set()
        if language_code in NWL.keys():
            sentencepiece_model_name = NWL[language_code]
            with path(
                "mwtokenizer.assets.spcmodels", sentencepiece_model_name
            ) as model_path:
                self.nws_word_tokenizer = spm.SentencePieceProcessor(
                    model_file=str(model_path)
                )
        else:
            self.nws_word_tokenizer = None

    def incorporate_abbreviations(self, split_sentence: List[str]) -> List[str]:
        # add documentation in sphinx format
        """
        This method implements an algorithm to consider abbreviations during sentence segmentations
        to avoid splitting sentences at the end of an abbreviation.
        If a sentence's last word is contained in the set of abbreviations,
        we concatenate the next sentence.
        :params split_sentences: The list of splitted sentence from the sentence segmenter.
        :type split_sentence: List of sentence segments


        :return: A list of :class: `str` objects
        :rtype: List[str]

        """
        final_sentences = []
        idx = 0
        num_sentences = len(split_sentence)

        if num_sentences == 1:
            return split_sentence

        while idx < num_sentences:
            current_sentence = split_sentence[idx]
            last_word = current_sentence.rsplit(maxsplit=1)[-1]

            while last_word in self.abbreviations and idx + 1 < num_sentences:
                idx += 1
                current_sentence += split_sentence[idx]  # adding the following sentence
                if (
                    split_sentence[idx].strip() != ""
                ):  # this check is likely not needed, but just in case
                    last_word = current_sentence.rsplit(maxsplit=1)[-1]
            idx += 1
            final_sentences.append(current_sentence)
        return final_sentences

    def sentence_tokenize(
        self, text: str = "", use_abbreviation: bool = True
    ) -> Iterator[str]:
        # add documentation in sphinx format so we can later on use it for readthedocs
        """
        Naive rule-based implementation to split plaintext to sentences.
        Steps:
            1. Split the text on the global_sent_split_pattern
            2. Post-process the split sentences, if use_abbreviation is True
            3. Yield the split sentences
            4. for each sentence, we preserve the sentence-termination symbol and any trailing whitespaces such that
            joining the sentences recovers the original text as a single string

        :params text: the plaintext that would be segmented.
        :type text: str
        :params use_abbreviation: whether or not to use compiled list of abbreviations for
        post processing the split sentences, after a naive segmentation
        :type use_abbreviation: boolean


        :return: A generator of :class: `str` objects
        :rtype: List[str]
        """
        split_sentences = capture_trailing_space(
            re.split(global_sent_split_pattern, text)
        )

        if use_abbreviation and len(self.abbreviations) > 0:
            split_sentences = self.incorporate_abbreviations(split_sentences)

        for sentence in split_sentences:
            yield sentence

    def word_tokenize(
        self, text: str = "", use_abbreviation: bool = True
    ) -> Iterator[str]:
        """
        Tokenize a text string into a list of tokens. The type of tokenizer to use is determined by the language code.
        :param text: The text string to be tokenized
        :type text: str
        :param use_abbreviation: Whether or not to use compiled list of abbreviations for
        post processing the split tokens, after a naive segmentation
        :type use_abbreviation: bool

        :return: A list of tokens
        :rtype: List[str]
        """
        abbreviations = self.abbreviations
        if not use_abbreviation:
            abbreviations = set()

        if self.language_code not in NWL.keys():
            word_tokens = whitespace_word_tokenization(
                text=text, abbreviations=abbreviations
            )

        else:
            word_tokens = non_whitespace_word_tokenization(
                text=text, spc_model=self.nws_word_tokenizer
            )

        for token in word_tokens:
            yield token

    def tokens_to_string(self, tokens: List[str]) -> str:
        """
        Merge tokens into the original text.
        :param tokens: The list of tokens to be merged
        :type tokens: List[str]
        :return: The original text to be tokenized
        :rtype: str
        """
        return "".join(tokens)
