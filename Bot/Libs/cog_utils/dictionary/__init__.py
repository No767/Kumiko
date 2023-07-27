from typing import Dict, List, Optional

from attrs import define


@define
class EnglishDef:
    definition: str
    synonyms: List[str]
    antonyms: List[str]
    example: str


@define
class EnglishDictEntry:
    word: str
    phonetics: List[Dict[str, str]]
    part_of_speech: str
    definitions: List[EnglishDef]


@define
class JapaneseEntryDef:
    english_definitions: List[str]
    parts_of_speech: List[str]
    tags: List[str]


@define
class JapaneseWordEntry:
    word: Optional[str]
    reading: Optional[str]


@define
class JapaneseDictEntry:
    word: List[JapaneseWordEntry]
    definitions: List[JapaneseEntryDef]
    is_common: Optional[bool]
    tags: Optional[List[str]]
    jlpt: Optional[List[str]]
