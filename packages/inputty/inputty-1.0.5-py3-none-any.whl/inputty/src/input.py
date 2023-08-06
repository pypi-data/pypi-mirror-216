"""Provide an Input class to handle CLI inputs."""

from typing import List, Tuple
from termcolor import cprint

from .colours import get_colour_map

__all__ = ['Input']

MODULE_COLOUR = 'blue'
ERROR_COLOUR = 'red'
INVALID_SPEC_MSG = 'Invalid specification for process:'
INVALID_INPUT_MSG = 'Invalid input.'
USE_ONE_OF_MSG = 'Use one of'
INTEGER_RANGE_MSG = 'Integer outside valid range:'

DEFAULT_COLOURS = {
    'text': ('black',),
    'cues': ('green', 'bright'),
}

RETURN = '<RTN>'
STRING = '<STRING>'
INTEGER_SELECTION = '<INTEGERS>'
INTEGER_BASE = 1


class Input():
    """
    The class takes a prompt string and a list of processes that
    define allowed inputs and the relevant process to be called.

    Attributes
    ----------

    prompt: str
        The prompt is the string that appears in the input statement. E.g.

            prompt = f"'S' to synchronise {len(files_to_copy)} files, 'Q' to quit: "

    process: dict[str, Tuple[object, list]] or dict[str, Tuple[object, list, tuple]]
        The process object is the function to be called when the input is the key
        the list contains the parameters to be passed to the function.
        The second definition includes a two-ple for min_integer and max_integer

        An example process:

            processes = {
                '<INTEGERS>': (function_one, [arg], (min_integer, max_integer)),
                '<RTN>': (function_two, []),
                'S': (function_three, [files_to_copy]),
                'Q': (quit, []),
            }
        If the process key is <RTN> (RETURN) then a null input will invoke the associated process.

        If the process key is <INTEGERS> (INTEGER_SELECTION) then a valid input is created for
        integers in the range (min_integer to the max_integer) and
        the call is to function_one with the first parameter the integer that has been input.)


    validation: dict[str, x]
        experimental

    Methods
    -------

    process_response:
        Returns the method associated with a valid input.

    Example Usage
    -----

        Input(prompt, processes)()
    or,
        my_input = Input(prompt, processes)
        my_input()
    """
    def __init__(self, prompt: str,
                 processes: dict[str, Tuple[object, List[object]]],
                 validation: dict[str, object] = {},
                 colours: dict[str, str] = DEFAULT_COLOURS):
        self.prompt = self.colorize_prompt(prompt, processes, colours)
        self.processes = self._generate_processes(processes)
        self.validation = validation
        self.message_list = self._get_message_list(processes)
        self .response = None
        self.error_colour = ERROR_COLOUR
        # Are valid inputs to be included in the error message?
        self.include_valid_in_error = True
        self._input_error_message = self._get_input_error_message()

        self.process_response = self.invoke

    def __call__(self):
        self.invoke()

    def invoke(self) -> object:
        # Return the result of a valid input
        response = self._get_input()

        self.response = response
        if response not in self.processes:
            return response

        if not self.processes[response]:
            return True

        process = self.processes[response]
        if not process[0]:
            return response

        return process[0](*process[1])

    def _get_input(self) -> str:
        # Return a valid input string
        while True:
            response = input(self.prompt)

            # Handle null input
            if not response:
                if RETURN in self.processes:
                    return RETURN
                continue

            if response in self.processes:
                return response

            # Capture string
            if STRING in self.processes:
                return response

            if self.validation:
                return self.validate_input(response)
            cprint(f"{self._input_error_message}", self.error_colour)

    def validate_input(self, response):
        # Return a valid input string having validated input.
        if 'integer' in self.validation:
            return self.validate_integer(response)
        return False

    def validate_integer(self, response):
        # Validate an integer  response.
        if not response.isnumeric():
            return False
        integer = int(response)
        min_, max_ = self.validation['integer']['min'], self.validation['integer']['max']
        if integer < min_ or integer > max_:
            cprint(f"{INTEGER_RANGE_MSG} {min_} to {max_}", ERROR_COLOUR)
            return False
        return response

    def _get_message_list(self, processes) -> List[str]:
        # Return a list of valid inputs for use in error message
        message_list = []
        for key in processes:
            if key == INTEGER_SELECTION:
                (min_, max_) = Input._get_integers_min_max(processes[key])
                message_list.append(f'an integer({min_}-{max_})')
            else:
                message_list.append(key)
        return message_list

    def _generate_processes(self, processes) -> dict[Tuple[object, list[object]]]:
        self._validate_processes(processes)
        case_processes = self._get_case_processes(processes)
        integer_processes = self._get_integer_processes(processes)
        return {**processes, **case_processes, **integer_processes}

    @staticmethod
    def _validate_processes(processes):
        for key, item in processes.items():
            try:
                _ = len(item)
            except TypeError:
                err_msg = f'{INVALID_SPEC_MSG} {key}. No parameters.'
                raise TypeError(err_msg)
            if not isinstance(item[1], list):
                err_msg = f'{INVALID_SPEC_MSG} {key}. Parameters not a list.'
                raise TypeError(err_msg)

    @staticmethod
    def _get_case_processes(processes):
        case_processes = {}
        for key in processes:
            if not key.isnumeric() and key not in [INTEGER_SELECTION, RETURN]:
                if key.upper() in processes:
                    case_processes[key.lower()] = processes[key]
                elif key.lower() in processes:
                    case_processes[key.upper()] = processes[key]
        return case_processes

    @staticmethod
    def _get_integer_processes(processes):
        integer_processes = {}
        for key in processes:
            if key == INTEGER_SELECTION:
                Input._validate_integers(key, processes[key])
                (min_, max_) = Input._get_integers_min_max(processes[key])
                integer_range = range(min_, max_+1)
                for index in integer_range:
                    args = [index]
                    if processes[key][1]:
                        args = [index] + processes[key][1]
                    integer_processes[str(index)] = (processes[key][0], args)
        return integer_processes

    @staticmethod
    def _get_integers_min_max(process):
        if isinstance(process[2], int):
            return (INTEGER_BASE, process[2])
        else:
            return process[2]

    @staticmethod
    def _validate_integers(key, process):
        if len(process) <= 2:
            err_msg = f'{INVALID_SPEC_MSG} {key}. No integer range.'
            raise ValueError(err_msg)
        if isinstance(process[2], int):
            return
        if not isinstance(process[2], tuple):
            err_msg = f'{INVALID_SPEC_MSG} {key}. Range not a tuple.'
            raise TypeError(err_msg)
        if len(process[2]) == 0:
            err_msg = f'{INVALID_SPEC_MSG} {key}. Range empty.'
            raise TypeError(err_msg)

    def _get_input_error_message(self) -> str:
        # Return the error message for the input
        if self.include_valid_in_error:
            valid_responses_list = self.message_list
            valid_responses = ', '.join(valid_responses_list)
            if len(valid_responses_list) >= 1:
                return f'{INVALID_INPUT_MSG} {USE_ONE_OF_MSG} {valid_responses}'
        return INVALID_INPUT_MSG

    def colorize_prompt(self, prompt, processes, colours) -> str:
        colours = get_colour_map(colours)
        prompt = prompt.strip() + ' '
        for key, item in processes.items():
            if f"'{key}'" in prompt:
                prompt = prompt.replace(f"'{key}'", key)
            if f"{key}" in prompt:
                prompt = prompt.replace(f"{key}", self.colorize_key(key, colours))
        return prompt

    @staticmethod
    def colorize_key(key: str, colours) -> str:
        text_fore = colours['text-fore']
        text_style = colours['text-style']
        text_back = colours['text-back']
        text_format = f'{text_fore}{text_style}{text_back}'

        cues_fore = colours['cues-fore']
        cues_style = colours['cues-style']
        cues_back = colours['cues-back']
        cues_format = f'{cues_fore}{cues_style}{cues_back}'

        return f"{cues_format}{key}{text_format}"

    def __str__(self) -> str:
        return f'Input: {self.prompt} {[key for key in self.processes]}'
