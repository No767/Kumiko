from typing import Dict, List, Union


def format_job_options(rows: Union[List[Dict[str, str]], None]) -> str:
    """Format the rows to be sent to the user

    Args:
        rows (Union[List[Dict[str, str]], None]): Rows to format

    Returns:
        str: _Formatted string
    """
    if rows is None or len(rows) == 0:
        return "Job not found"

    names = "\n".join([row["name"] for row in rows])
    return f"Job not found. Did you mean:\n{names}"
