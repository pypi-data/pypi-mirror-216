from ..src.input import Input

ANSI_COLOR_BLACK = "\033[30m"
ANSI_COLOR_GREEN = "\033[32m"
ANSI_COLOR_RESET = "\033[49m"
ANSI_COLOR_BRIGHT = "\033[1m"
ANSI_COLOR_NORMAL = "\033[22m"


def test_prompt():
    prompt = "Enter 'Y' to proceed, 'Q' to quit: "
    processes = {
        'Y': (None, []),
        'Q': (None, []),
    }
    my_input = Input(prompt, processes)
    cue_start = f'{ANSI_COLOR_GREEN}{ANSI_COLOR_BRIGHT}{ANSI_COLOR_RESET}'
    cue_stop = f'{ANSI_COLOR_BLACK}{ANSI_COLOR_NORMAL}{ANSI_COLOR_RESET}'
    yes = f'{cue_start}Y{cue_stop}'
    quit = f'{cue_start}Q{cue_stop}'
    assert my_input.prompt == f'Enter {yes} to proceed, {quit} to quit: '
