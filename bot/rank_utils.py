# The equations are these:
#
# Calculating Rank from Petals: 0.12 * ∛petals
# Calculating Petals from Rank: (rank / 0.12) ^ 3
#
# These may be subject to change. We'll see later if they change.


def calc_rank(petals: int) -> int:
    """Calculates the current rank of the user

    Args:
        petals (int): The amount of petals currently owned in the user

    Returns:
        int: The calculated rank. Always rounded down since it's always faster to round down than up
    """
    cube_root = pow(petals, (1 / 3))
    return round(0.12 * cube_root)


def calc_petals(rank: int) -> int:
    """Calculates the amount of petals needed to reach the next rank

    Args:
        rank (int): The current rank of the user

    Returns:
        int: _description_
    """
    return round(pow((rank / 0.12), 3))
