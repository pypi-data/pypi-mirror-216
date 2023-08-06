from typing import Iterable


def del_duplicates(x: Iterable, /, keep_order: bool = False) -> Iterable:
    r"""
    The function del_duplicates takes an iterable x as input and removes duplicate elements from it.
    It returns a new iterable with the duplicates removed.

    The function accepts an optional keyword argument keep_order, which is set to False by default.
    If keep_order is set to False, the function tries to convert the input iterable x into a set,
    which automatically removes duplicates. If the conversion to a set is successful,
    the function converts the set to the original dtype and returns the set.

    If the conversion to a set fails due to a TypeError, indicating that the elements of x are
    unhashable, the function sets keep_order to True.

    If keep_order is set to True, the function iterates over the elements of x
    and creates a temporary dictionary (tmpdict) to store the unique elements.
    If an element is hashable, it is used as the key and value in tmpdict.
    If an element is unhashable, its string representation concatenated with
    its repr() representation is used as the key and the element itself is used as the value.

    Finally, the function constructs a new iterable of unique elements based on
    the content of tmpdict. If keep_order is True, the function, converts the values in
    tmpdict to the original dtype,
    returns the values of tmpdict in the order they were encountered in the input iterable x.
    Otherwise, it returns the values of tmpdict in an arbitrary order.

    Note: The function checks whether x is an instance of dict, set, or frozenset.
    If it is, it immediately returns x without performing any duplicate removal,
    as these types inherently handle duplicate elimination.


    Args:
        x (Iterable): The input iterable from which duplicates will be removed.
        keep_order (bool, optional): Specifies whether to preserve the original order of elements.
        Defaults to False.

    Returns:
        Iterable: A new iterable containing the unique elements from the input iterable.

    Raises:
        None

    Notes:
        - If `x` is an instance of `dict`, `set`, or `frozenset`, it is returned as is since these types inherently handle duplicate elimination.
        - If `keep_order` is False (default), the function attempts to convert `x` into a set to remove duplicates.
        - If the conversion to a set fails due to unhashable elements, `keep_order` is automatically set to True.
        - If `keep_order` is True, the function creates a temporary dictionary to store unique elements, preserving the order of their occurrence.
        - For unhashable elements, their string representation concatenated with their `repr()` representation is used as the dictionary key.
        - The function constructs a new iterable of unique elements based on the content of the temporary dictionary.
          If `keep_order` is True, the values are returned in the order they were encountered in the input iterable. Otherwise, the values are returned in an arbitrary order.


    """
    if isinstance(x, (dict, set, frozenset)):
        return x
    dtype = type(x)
    if not keep_order:
        try:
            return dtype(set(x))
        except TypeError:
            keep_order = True
    if keep_order:
        tmpdict = {}
        for v in x:
            try:
                tmpdict[v] = v
            except TypeError:
                tmpdict[f"{v}{repr(v)}"] = v
        return dtype([q[-1] for q in tmpdict.items()])

