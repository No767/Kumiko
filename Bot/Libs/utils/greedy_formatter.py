from typing import List


def formatGreedy(list: List[str]) -> str:
    if len(list) >= 3:
        return f"{', '.join(list[:-1])}, and {list[-1]}"
    elif len(list) == 2:
        return " and ".join(list)
    return "".join(list)
