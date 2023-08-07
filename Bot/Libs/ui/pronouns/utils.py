from typing import List

from .structs import PronounsWordsEntry


def parse_opinion(opinion: str) -> str:
    data = {
        "yes": "\U00002764",
        "jokingly": "\U0001f61b",
        "close": "\U0001f465",
        "meh": "\U0001f44c",
        "no": "\U0001f6ab",
    }
    return data[opinion]


def determine_bold(value: str, opinion: str) -> str:
    if "yes" in opinion:
        return f"**{value}**"
    return f"{value}"


def parse_words(words: List[PronounsWordsEntry]) -> str:
    result = ""
    for word in words:
        if word.header is not None:
            result += f"\n**{word.header}**\n"
        else:
            result += "\n"
        result += ", ".join(
            [
                f"{determine_bold(value.value, value.opinion)} ({parse_opinion(value.opinion)})"
                for value in word.values
            ]
        )
        result += "\n"
    return result
