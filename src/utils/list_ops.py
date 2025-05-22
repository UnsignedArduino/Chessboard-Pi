def remove_adjacent_duplicates(l: list):
    """
    Removes adjacent duplicates from a list. Modifies the list in place.

    :param l: The list to remove duplicates from.
    """
    i = 0
    while True:
        first = l[i]
        second = l[i + 1] if i + 1 < len(l) else None
        if second is None:
            break
        elif first == second:
            l.pop(i + 1)
        else:
            i += 1
