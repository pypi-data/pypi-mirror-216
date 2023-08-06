from typing import List, Tuple, Union
from .ansi import Fg, Bg, Frmt, ESC, RESET, bg_hex, bg_rgb, fg_hex, fg_rgb


def style(text: str,
          fg: Fg | str | Tuple[int, int, int] |
          List[Union[int, int, int]] = Fg.DEFAULT,
          bg: Bg | str | Tuple[int, int, int] |
          List[Union[int, int, int]] = Bg.DEFAULT,
          frmt: List[Frmt] = None) -> str:
    """ Styles string using ANSI escape codes.

    Args:
        text (str): String to style.
        fg (Fg | str | Tuple[int, int, int] | List[int, int, int], optional): Foreground color.
            Either a Fg enum, a hex color string, or an RGB tuple or list.
        bg (Bg | str | Tuple[int, int, int] | List[int, int, int], optional): Background color.
            Either a Bg enum, a hex color string, or an RGB tuple or list.
        frmt (Frmt[Style], optional): List of formatting to apply.

    Returns:
        str: Styled text.
    """

    if fg is None:
        fg = Fg.DEFAULT
    if isinstance(fg, str):
        fore = fg_hex(fg)
    if isinstance(fg, tuple):
        fore = fg_rgb(fg)
    if isinstance(fg, Fg):
        fore = fg.value

    if bg is None:
        bg = Bg.DEFAULT
    if isinstance(bg, str):
        back = bg_hex(bg)
    if isinstance(bg, tuple):
        back = bg_rgb(bg)
    if isinstance(bg, Bg):
        back = bg.value

    if frmt is None:
        frmt = []
    else:
        frmt.sort()

    frmt_string = ''
    for frmt in frmt:
        frmt_string += f';{frmt.value}'

    return f'{ESC}{fore};{back}{frmt_string}m{text}{RESET}'
