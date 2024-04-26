import sys
from pathlib import Path

from dotenv import load_dotenv

path = Path(__file__).parents[2].joinpath("Bot")
sys.path.append(str(path))

load_dotenv()

from libs.ui.dictionary import (
    EnglishDef,
    EnglishDictEntry,
    JapaneseDictEntry,
    JapaneseEntryDef,
    JapaneseWordEntry,
)


def test_japanese_word_entry():
    word = "桜"
    reading = "さくら"
    entry = JapaneseWordEntry(word=word, reading=reading)
    assert entry.word == word
    assert entry.reading == reading


def test_english_def():
    # github copilot generated these lol
    definition = "a tree that bears pale pink flowers"
    synonyms = ["cherry", "cherry tree", "Prunus avium"]
    antonyms = ["Prunus serotina", "black cherry", "rum cherry", "rum cherry tree"]
    example = "the cherry trees were in full bloom"

    entry = EnglishDef(
        definition=definition, synonyms=synonyms, antonyms=antonyms, example=example
    )
    assert (
        (entry.definition == definition)
        and (entry.synonyms == synonyms)
        and (entry.antonyms == antonyms)
        and (entry.example == example)
    )


def test_english_dict_entry():
    word = "nice"
    phonetics = []
    part_of_speech = "nouns"
    definition = "a tree that bears pale pink flowers"
    synonyms = ["cherry", "cherry tree", "Prunus avium"]
    antonyms = ["Prunus serotina", "black cherry", "rum cherry", "rum cherry tree"]
    example = "the cherry trees were in full bloom"
    entry = EnglishDef(
        definition=definition, synonyms=synonyms, antonyms=antonyms, example=example
    )

    edict = EnglishDictEntry(
        word=word,
        phonetics=phonetics,
        part_of_speech=part_of_speech,
        definitions=[entry],
    )
    assert (
        (edict.word == word)
        and (edict.phonetics == phonetics)
        and (edict.part_of_speech == part_of_speech)
        and (edict.definitions == [entry])
    )


def test_japanese_entry_def():
    english_definitions = ["cherry", "cherry tree", "Prunus avium"]
    parts_of_speech = ["nouns"]
    tags = ["cherry", "cherry tree", "Prunus avium"]
    entry = JapaneseEntryDef(
        english_definitions=english_definitions,
        parts_of_speech=parts_of_speech,
        tags=tags,
    )
    assert (
        (entry.english_definitions == english_definitions)
        and (entry.parts_of_speech == parts_of_speech)
        and (entry.tags == tags)
    )


def test_japanese_dict_entry():
    word = "桜"
    reading = "さくら"
    word_entry = JapaneseWordEntry(word=word, reading=reading)
    english_definitions = ["cherry", "cherry tree", "Prunus avium"]
    parts_of_speech = ["nouns"]
    tags = ["cherry", "cherry tree", "Prunus avium"]
    entry_es = JapaneseEntryDef(
        english_definitions=english_definitions,
        parts_of_speech=parts_of_speech,
        tags=tags,
    )
    entry = JapaneseDictEntry(
        word=[word_entry],
        definitions=[entry_es],
        is_common=False,
        tags=tags,
        jlpt=["N5"],
    )
    assert (
        (entry.definitions == [entry_es])
        and (entry.tags == tags)
        and (entry.jlpt == ["N5"])
        and (entry.is_common is False)
        and (entry.word == [word_entry])
    )
