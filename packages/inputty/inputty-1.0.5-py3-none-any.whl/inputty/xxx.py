import sys
from src.input import Input


def input_Y(value):
    print(value)


# class Input():
#     def __init__(self, options):
#         option_str = ', '.join(options)
#         self.prompt = f"Enter one of {option_str}: "

#     def invoke(self):
#         return input(self.prompt)


def main():
    prompt = "Enter 'Y' to proceed, 'Q' to quit: "
    processes = {
        'Y': (input_Y, ['Y input']),
        'Q': (sys.exit, ['user quit']),
    }
    my_input = Input(prompt, processes)
    my_input()


if __name__ == '__main__':
    main()
