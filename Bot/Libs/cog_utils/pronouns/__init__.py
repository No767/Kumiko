from typing import List


def parse_pronouns(entry: List[str]):
    fullPronouns = {
        "he": "he/him",
        "she": "she/her",
        "it": "it/its",
        "they": "they/them",
    }
    for idx, item in enumerate(entry):
        if item in fullPronouns:
            entry[idx] = fullPronouns[item]

    return ", ".join(entry).rstrip(",")
