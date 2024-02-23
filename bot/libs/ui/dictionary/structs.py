from typing import Dict, List, Optional

import msgspec


class EnglishDef(msgspec.Struct):
    definition: str
    synonyms: List[str]
    antonyms: List[str]
    example: Optional[str]


class EnglishDictEntry(msgspec.Struct):
    word: str
    phonetics: List[Dict[str, str]]
    part_of_speech: str
    definitions: List[List[EnglishDef]]


class JapaneseEntryDef(msgspec.Struct):
    english_definitions: List[str]
    parts_of_speech: List[str]
    tags: List[str]


class JapaneseWordEntry(msgspec.Struct):
    word: Optional[str]
    reading: Optional[str]


class JapaneseDictEntry(msgspec.Struct):
    word: List[JapaneseWordEntry]
    definitions: List[JapaneseEntryDef]
    is_common: Optional[bool]
    tags: Optional[List[str]]
    jlpt: Optional[List[str]]
