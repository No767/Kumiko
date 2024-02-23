from discord.ext import menus

from .structs import EnglishDictEntry, JapaneseDictEntry


class EnglishDefinePageSource(menus.ListPageSource):
    async def format_page(self, menu, entries: EnglishDictEntry):
        definitions = []
        for defs in entries.definitions:
            for idx, entry in enumerate(defs, start=0):
                default_text = f"{idx + 1}. {entry.definition}"
                if entry.example is not None:
                    default_text = f"{idx}. {entry.definition}\n--- *{entry.example}*"

                definitions.append(default_text)
        maximum = self.get_max_pages()
        menu.embed.title = f"{entries.word}"

        if maximum > 1:
            footer = (
                f"Page {menu.current_page + 1}/{maximum} ({len(self.entries)} entries)"
            )
            menu.embed.set_footer(text=footer)

        header_desc = f"**{entries.part_of_speech}** {' • '.join([item['text'] for item in entries.phonetics if 'text' in item]).rstrip('*')}\n"
        menu.embed.description = header_desc + "\n".join(definitions)
        return menu.embed


class JapaneseDefPageSource(menus.ListPageSource):
    async def format_page(self, menu, entries: JapaneseDictEntry):
        word_str = ""
        first_jpn_entry = entries.word[0]
        jpn_word = first_jpn_entry.word
        jpn_reading = first_jpn_entry.reading
        if jpn_word and jpn_reading is not None:
            if jpn_word == jpn_reading:
                word_str += f"**{jpn_word}**\n"
            else:
                word_str += f"**{jpn_word}** ({jpn_reading})\n"
        elif jpn_reading is None:
            word_str += f"**{jpn_word}**\n"
        elif jpn_word is None:
            word_str += f"**{jpn_reading}**\n"

        definitions = []
        for idx, entry in enumerate(entries.definitions, start=0):
            parse_defs = ", ".join([item for item in entry.english_definitions]).rstrip(
                ","
            )
            parse_pos = ", ".join([item for item in entry.parts_of_speech]).rstrip(",")
            parse_tags = ", ".join([item for item in entry.tags]).rstrip(",")
            text = f"(**{parse_pos}**)\n{idx + 1}. {parse_defs}\n"
            if len(entry.tags) != 0:
                text = f"(**{parse_pos}**)\n{idx + 1}. {parse_defs} ({parse_tags})\n"
            definitions.append(text)

        maximum = self.get_max_pages()
        menu.embed.title = f"{word_str}"

        if maximum > 1:
            footer = (
                f"Page {menu.current_page + 1}/{maximum} ({len(self.entries)} entries)"
            )
            menu.embed.set_footer(text=footer)

        menu.embed.description = "\n".join(definitions)
        return menu.embed
