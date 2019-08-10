def is_asc_sorted(lst: list) -> bool:
    """
    Utility that tells whether a given list is already ascendentally sorted
    with every item in the list greater than the previous.
    :param lst: list to check
    :return: true if and only if the given list is ascendentally sorted
    """
    return all(lst[i+1] > lst[i] for i in range(0, len(lst) - 2))
