from itertools import product, permutations as _permutations
from typing import Generator


def permutations(string: str,
                 max_len: int = None,
                 min_len: int = 1,
                 allow_repetition: bool = False) -> Generator[str, None, None]:
    """Generates all permutations of a string.

    Args:
        string (str): String to permute.
        max_len (int, optional): Maximum length of permutations. Defaults to length of the string.

    Yields:
        str: Permutations of the string.
    """
    if max_len is None:
        max_len = len(string)
    else:
        max_len = min(max_len, len(string))

    min_len = min(min_len, max_len)

    if min_len <= 0:
        min_len = 1

    if allow_repetition:
        for i in range(min_len, max_len + 1):
            for p in product(string, repeat=max_len):
                yield ''.join(p)
        return

    for i in range(min_len, max_len + 1):
        for p in _permutations(string, i):
            yield ''.join(p)
