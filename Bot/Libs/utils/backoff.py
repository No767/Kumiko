import random


def backoff(backoff_sec: int = 5, backoff_sec_index: int = 0) -> float:
    """Helper function to calculate backoff time (exponential)

    Args:
        backoff_sec (int, optional): The init second to use. Defaults to 5.
        backoff_sec_index (int, optional): The index to use. Defaults to 0.

    Returns:
        float: Backoff time (seconds)
    """
    sleepAmt = backoff_sec * 2**backoff_sec_index + random.uniform(  # nosec
        0, 1
    )  # nosec
    if sleepAmt > 60:
        return float(60)
    return sleepAmt
