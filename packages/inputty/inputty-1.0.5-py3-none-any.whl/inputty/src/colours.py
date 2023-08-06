
from colorama import Fore, Back, init, Style

init()  # colorama


def get_colour_map(colours: dict[str, tuple]) -> dict[str, str]:
    selected_colours = {
        'text-fore': Fore.BLACK,
        'text-style': Style.NORMAL,
        'text-back': Back.RESET,

        'cues-fore': Fore.BLACK,
        'cues-style': Style.NORMAL,
        'cues-back': Back.RESET,
    }
    if 'text' in colours:
        if len(colours['text']) > 0:
            selected_colours['text-fore'] = _colour_map(colours['text'][0], 'fore')
        if len(colours['text']) > 1:
            selected_colours['text-style'] = _colour_map(colours['text'][1], 'style')
        if len(colours['text']) > 2:
            selected_colours['text-back'] = _colour_map(colours['text'][3], 'back')

        if len(colours['cues']) > 0:
            selected_colours['cues-fore'] = _colour_map(colours['cues'][0], 'fore')
        if len(colours['cues']) > 1:
            selected_colours['cues-style'] = _colour_map(colours['cues'][1], 'style')
        if len(colours['cues']) > 2:
            selected_colours['cues-back'] = _colour_map(colours['cues'][2], 'back')

    return selected_colours


def _colour_map(colour, item):
    map = {
        'fore': {
            'black': Fore.BLACK,
            'red': Fore.RED,
            'green': Fore.GREEN,
            'yellow': Fore.YELLOW,
            'blue': Fore.BLUE,
            'magenta': Fore.MAGENTA,
            'cyan': Fore.CYAN,
            'white': Fore.WHITE,
        },

        'style': {
            'dim': Style.DIM,
            'bright': Style.BRIGHT,
            'normal': Style.NORMAL,
        },

        'back': {
            'black': Back.BLACK,
            'red': Back.RED,
            'green': Back.GREEN,
            'yellow': Back.YELLOW,
            'blue': Back.BLUE,
            'magenta': Back.MAGENTA,
            'cyan': Back.CYAN,
            'white': Back.WHITE,
        }
    }
    return map[item][colour]


DEFAULT_COLOURS = {
    'text': ('black', 'dim'),
    'cues': ('blue', 'bright', 'blue'),
}

"""
Fore.RED
Fore.GREEN
Fore.YELLOW
Fore.BLUE
Fore.MAGENTA
Fore.CYAN
Fore.WHITE
"""
