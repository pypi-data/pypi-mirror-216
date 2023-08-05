from mwtokenizer.tokenizer import Tokenizer

TEST_NWS_SENTENCES = {
    "ja": "こんにちは世界。",  # "Hello world."
    "th": "สวัสดีชาวโลก",  # "Hello world."
    "cr": "ᐄᔨᔫ/ᐄᓅ ᐊᔅᒌ (ᔖᐗᓅᑖᐊᒡ ᐊᔨᒧᐎᓐ",
}
# Format: {language_code: [passage, expected_tokens_without_abbreviation,
# expected_tokens_with_abbreviation]}
TEST_WS_SENTENCES = {
    "en": [
        "During the conference, Dr. Appledora gave the keynote. It was excellent!",
        [
            "During",
            " ",
            "the",
            " ",
            "conference",
            ",",
            " ",
            "Dr",
            ".",
            " ",
            "Appledora",
            " ",
            "gave",
            " ",
            "the",
            " ",
            "keynote",
            ".",
            " ",
            "It",
            " ",
            "was",
            " ",
            "excellent",
            "!",
        ],
        [
            "During",
            " ",
            "the",
            " ",
            "conference",
            ",",
            " ",
            "Dr.",
            " ",
            "Appledora",
            " ",
            "gave",
            " ",
            "the",
            " ",
            "keynote",
            ".",
            " ",
            "It",
            " ",
            "was",
            " ",
            "excellent",
            "!",
        ],
    ]
}


def test_simple_whitespaced_word_segmentations():
    for lang_code, passage in TEST_WS_SENTENCES.items():
        tokenizer = Tokenizer(language_code=lang_code)
        expected = passage[1]
        words = [w for w in tokenizer.word_tokenize(passage[0], use_abbreviation=False)]
        assert words == expected


def test_simple_whitespaced_word_segmentations_with_abbr():
    for lang_code, passage in TEST_WS_SENTENCES.items():
        tokenizer = Tokenizer(language_code=lang_code)
        expected = passage[2]
        words = [w for w in tokenizer.word_tokenize(passage[0], use_abbreviation=True)]
        assert words == expected


def test_nonwhitespace_word_segmentations():
    for lang_code, passage in TEST_NWS_SENTENCES.items():
        tokenizer = Tokenizer(language_code=lang_code)
        words = [w for w in tokenizer.word_tokenize(passage, use_abbreviation=False)]
        # taking a guardrail approach here, since the tokenizer is not
        # guaranteed to return exactly these tokens
        # 1. there are more than 1 token and the number of tokens is less than the number of characters
        assert len(words) > 1 and len(words) < len(passage)

        # 2. check if rejoining the tokens gives the original passage
        assert "".join(words).replace("▁", " ").lstrip() == passage
