from typing import Dict, List, Union


def format_options(rows: Union[List[Dict[str, str]], None]) -> str:
    """Format the rows to be sent to the user

    Args:
        rows (Union[List[Dict[str, str]], None]): Rows to format

    Returns:
        str: Formatted string
    """
    if rows is None or len(rows) == 0:
        return "Pin not found"

    names = "\n".join([row["name"] for row in rows])
    return f"Pin not found. Did you mean:\n{names}"
