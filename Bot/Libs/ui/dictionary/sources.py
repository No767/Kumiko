from attrs import asdict
from discord.ext import menus
from Libs.cog_utils.dictionary import JapaneseDictEntry


class EnglishDefinePageSource(menus.ListPageSource):
    async def format_page(self, menu, entries):
        definitions = []
        for idx, entry in enumerate(entries.definitions[0], start=0):
            defaultText = f"{idx + 1}. {entry['definition']}"
            if "example" in entry:
                defaultText = f"{idx}. {entry['definition']}\n--- *{entry['example']}*"

            definitions.append(defaultText)
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
        dictEntries = asdict(entries)
        firstJpnEntry = dictEntries["word"][0]
        if "word" and "reading" in firstJpnEntry:
            if firstJpnEntry["word"] == firstJpnEntry["reading"]:
                word_str += f"**{firstJpnEntry['word']}**\n"
            else:
                word_str += (
                    f"**{firstJpnEntry['word']}** ({firstJpnEntry['reading']})\n"
                )
        elif "word" not in firstJpnEntry:
            word_str += f"**{firstJpnEntry['reading']}**\n"

        # getTags = ", ".join([item for item in dictEntries["tags"]]).rstrip(",")
        # get_readings = ", ".join([item for item in dictEntries]).rstrip(",")
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

        # header_desc = f"**{entries.part_of_speech}** {' • '.join([item['text'] for item in entries.phonetics]).rstrip('*')}\n\n"
        menu.embed.description = "\n".join(definitions)
        return menu.embed
