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


class PronounsTermsEntry(msgspec.Struct):
    term: str
    original: Union[str, None]
    definition: str
    locale: str
    flags: str
    category: str


class PronounsInclusiveEntry(msgspec.Struct):
    instead_of: str
    say: str
    because: str
    categories: str
    clarification: Union[str, None]


class PronounsNounsEntry(msgspec.Struct):
    masc: str
    fem: str
    neutr: str
    masc_plural: str
    fem_plural: str
    neutr_plural: str
