import discord
from discord.ext import commands
from Libs.utils.pages import KumikoPages

from .sources import EnglishDefinePageSource, JapaneseDefPageSource
from .structs import (
    EnglishDef,
    EnglishDictEntry,
    JapaneseDictEntry,
    JapaneseEntryDef,
    JapaneseWordEntry,
)


class DictPages(KumikoPages):
    def __init__(self, entries, *, ctx: commands.Context, per_page=1):
        converted = [
            EnglishDictEntry(
                word=entry["word"],
                phonetics=entry["phonetics"],
                part_of_speech=entry["meanings"][0]["partOfSpeech"],
                definitions=[
                    [
                        EnglishDef(
                            definition=adef["definition"],
                            synonyms=adef["synonyms"],
                            antonyms=adef["antonyms"],
                            example=adef["example"] if "example" in adef else None,
                        )
                        for adef in item["definitions"]
                    ]
                    for item in entry["meanings"]
                ],
            )
            for entry in entries
        ]
        super().__init__(
            EnglishDefinePageSource(converted, per_page=per_page), ctx=ctx, compact=True
        )
        self.embed = discord.Embed(colour=discord.Colour.og_blurple())


class JapaneseDictPages(KumikoPages):
    def __init__(self, entries, *, ctx: commands.Context, per_page=1):
        converted = [
            JapaneseDictEntry(
                word=[
                    JapaneseWordEntry(
                        word=word["word"] if "word" in word else word["reading"],
                        reading=word["reading"] if "reading" in word else None,
                    )
                    for word in entry["japanese"]
                ],
                definitions=[
                    JapaneseEntryDef(
                        english_definitions=item["english_definitions"],
                        parts_of_speech=item["parts_of_speech"],
                        tags=item["tags"],
                    )
                    for item in entry["senses"]
                ],
                is_common=entry["is_common"] if "is_common" in entry else None,
                tags=entry["tags"],
                jlpt=entry["jlpt"],
            )
            for entry in entries
        ]
        super().__init__(
            JapaneseDefPageSource(converted, per_page=per_page), ctx=ctx, compact=True
        )
        self.embed = discord.Embed(colour=discord.Colour.light_grey())
