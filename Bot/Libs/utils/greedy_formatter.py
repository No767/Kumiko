from typing import List


def format_greedy(list: List[str]) -> str:
    """Formats a Greedy list into a human-readable string

    For example, if we had a list of ["a", "b", "c"], it would return "a, b, and c".
    If we had a list of ["a", "b"], it would return "a and b".
    If we had a list of ["a"], it would return "a".
    If we had a list of [], it would return "".

    Args:
        list: The list of strings to format

    Returns:
        str: The formatted string
    """
    if len(list) >= 3:
        return f"{', '.join(list[:-1])}, and {list[-1]}"
    elif len(list) == 2:
        return " and ".join(list)
    return "".join(list)
