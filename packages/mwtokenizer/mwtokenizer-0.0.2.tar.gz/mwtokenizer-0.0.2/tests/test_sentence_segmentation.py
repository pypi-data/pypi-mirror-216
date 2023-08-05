

from mwtokenizer.tokenizer import Tokenizer

tokenizer = Tokenizer(language_code="en")


def test_simple_naive_sentence():
    passage = "During the conference, Dr. Appledora gave the keynote. It was excellent!"
    expected = ["During the conference, Dr. ", "Appledora gave the keynote. ", "It was excellent!"]
    sentences = [s for s in tokenizer.sentence_tokenize(passage, use_abbreviation=False)]
    assert sentences == expected


def test_abbr_sentence():
    passage = "During the conference, Dr. Appledora gave the keynote. It was excellent!"
    expected = ["During the conference, Dr. Appledora gave the keynote. ", "It was excellent!"]
    sentences = [s for s in tokenizer.sentence_tokenize(passage, use_abbreviation=True)]
    assert sentences == expected
