from itertools import permutations as _permutations
from typing import Generator


def permutations(string: str,
                 max_len: int = None) -> Generator[str, None, None]:
    """Generates all permutations of a string.

    Args:
        string (str): String to permute.
        max_len (int, optional): Maximum length of permutations. Defaults to length of the string.

    Yields:
        str: Permutations of the string.
    """
    if max_len is None:
        max_len = len(string)

    for i in range(1, max_len + 1):
        for p in _permutations(string, i):
            yield ''.join(p)
