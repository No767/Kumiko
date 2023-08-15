from .structs import PronounsInclusiveEntry, PronounsNounsEntry, PronounsTermsEntry


class PronounsTermsEmbedEntry:
    __slots__ = ("term", "original", "definition", "locale", "flags", "category")

    def __init__(self, entry: PronounsTermsEntry):
        self.term = entry.term
        self.original = entry.original
        self.definition = entry.definition
        self.locale = entry.locale
        self.flags = entry.flags
        self.category = entry.category

    def to_dict(self):
        parsed_flags = str(self.flags) if len(self.flags) > 0 else "None"
        data = {
            "title": self.term,
            "description": self.definition,
            "fields": [
                {"name": "Original", "value": self.original or "None", "inline": True},
                {"name": "Flags", "value": parsed_flags, "inline": True},
                {"name": "Category", "value": self.category, "inline": True},
            ],
        }
        return data


class PronounsInclusiveEmbedEntry:
    __slots__ = ("instead_of", "say", "because", "categories", "clarification")

    def __init__(self, entry: PronounsInclusiveEntry):
        self.instead_of = entry.instead_of
        self.say = entry.say
        self.because = entry.because
        self.categories = entry.categories
        self.clarification = entry.clarification

    def to_dict(self):
        desc = f"Instead of [{self.instead_of}], you should say [{self.say}] because [{self.because}]."
        data = {
            "title": f"Instead of ..., say {self.say}",
            "description": desc,
            "fields": [
                {
                    "name": "Clarification",
                    "value": self.clarification or "None",
                    "inline": True,
                },
                {
                    "name": "Categories",
                    "value": self.categories or "None",
                    "inline": True,
                },
            ],
        }
        return data


class PronounsNounsEmbedEntry:
    __slots__ = ("masc", "fem", "neutr", "masc_plural", "fem_plural", "neutr_plural")

    def __init__(self, entry: PronounsNounsEntry):
        self.masc = entry.masc
        self.fem = entry.fem
        self.neutr = entry.neutr
        self.masc_plural = entry.masc_plural
        self.fem_plural = entry.fem_plural
        self.neutr_plural = entry.neutr_plural

    def to_dict(self):
        desc = f"**Masc**: {self.masc}\n**Fem**: {self.fem}\n**Neutr**: {self.neutr}\n"
        desc += f"**Masc Plural**: {self.masc_plural}\n**Fem Plural**: {self.fem_plural}\n**Neutr Plural**: {self.neutr_plural}"
        data = {
            "title": f"{self.masc} -- {self.fem} -- {self.neutr}",
            "description": desc,
        }
        return data
