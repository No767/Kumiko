from typing import List, Union

import msgspec


class PronounsProfileCircleEntry(msgspec.Struct):
    username: str
    avatar: str
    mutual: bool
    relationship: str


class PronounsValuesEntry(msgspec.Struct):
    value: str
    opinion: str


class PronounsWordsEntry(msgspec.Struct):
    header: Union[str, None]
    values: List[PronounsValuesEntry]


class PronounsProfileEntry(msgspec.Struct):
    username: str
    avatar: str
    locale: str
    names: List[PronounsValuesEntry]
    pronouns: List[PronounsValuesEntry]
    description: str
    age: Union[int, None]
    links: List[str]
    flags: List[str]
    words: List[PronounsWordsEntry]
    timezone: Union[str, None]
    circle: Union[List[PronounsProfileCircleEntry], None]
