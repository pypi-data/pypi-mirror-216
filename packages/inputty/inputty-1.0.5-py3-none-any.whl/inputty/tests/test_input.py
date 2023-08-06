import sys
import pytest
from ..src.input import Input


def input_Y(value):
    assert value == 'Y input'


def input_return(value):
    assert value == 'null input'


def test_string_input(monkeypatch):
    prompt = "Enter 'Y' to proceed, 'Q' to quit: "
    processes = {
        'Y': (input_Y, ['Y input']),
        'Q': (sys.exit, ['user quit']),
    }
    monkeypatch.setattr('builtins.input', lambda name: 'Y')
    Input(prompt, processes).invoke()


def test_string_input_lower_case(monkeypatch):
    prompt = "Enter 'Y' to proceed, 'Q' to quit: "
    processes = {
        'Y': (input_Y, ['Y input']),
        'Q': (sys.exit, ['user quit']),
    }
    monkeypatch.setattr('builtins.input', lambda name: 'y')
    Input(prompt, processes).invoke()


def test_return_input(monkeypatch):
    prompt = "Enter <RTN> to proceed, 'Q' to quit: "
    processes = {
        '<RTN>': (input_return, ['null input']),
        'Q': (sys.exit, ['user quit']),
    }
    monkeypatch.setattr('builtins.input', lambda name: '')
    Input(prompt, processes).invoke()


def test_null_input(monkeypatch):
    prompt = "Enter <RTN> to proceed, 'Q' to quit: "
    processes = {
        '<RTN>': (input_return, ['null input']),
        'Q': (sys.exit, ['user quit']),
    }

    for response in ['', 'Q']:
        monkeypatch.setattr('builtins.input', lambda name: response)
        if response == 'Q':
            with pytest.raises(SystemExit) as excinfo:
                Input(prompt, processes).invoke()
            assert excinfo.value.code == 'user quit'


def test_quit(monkeypatch):
    prompt = "Enter 'Y' to proceed, 'Q' to quit: "
    processes = {
        'Y': (input_Y, ['Y input']),
        'Q': (sys.exit, ['user quit']),
    }

    monkeypatch.setattr('builtins.input', lambda name: 'Q')
    with pytest.raises(SystemExit) as excinfo:
        Input(prompt, processes).invoke()
    assert excinfo.value.code == 'user quit'


def test_quit_lower_case(monkeypatch):
    prompt = "Enter 'Y' to proceed, 'Q' to quit: "
    processes = {
        'Y': (input_Y, ['Y input']),
        'Q': (sys.exit, ['user quit']),
    }

    monkeypatch.setattr('builtins.input', lambda name: 'q')
    with pytest.raises(SystemExit) as excinfo:
        Input(prompt, processes).invoke()
    assert excinfo.value.code == 'user quit'


def test_no_process(monkeypatch):
    prompt = "Enter 'Y' to proceed, 'Q' to quit: "
    processes = {
        'Y': (None, ['Y input']),
        'Q': (sys.exit, ['user quit']),
    }

    monkeypatch.setattr('builtins.input', lambda name: 'y')
    response = Input(prompt, processes).invoke()
    assert response == 'y'


def test_invalid(monkeypatch, capsys):
    prompt = "Enter 'Y' to proceed, 'Q' to quit: "
    processes = {
        'Y': (input_Y, ['Y input']),
        'Q': (sys.exit, ['user quit']),
    }

    for response in ['P', 'Q']:
        monkeypatch.setattr('builtins.input', lambda name: response)
        if response == 'P':
            capsys.readouterr()
            # assert captured.out.strip() == 'Invalid input'
        else:
            with pytest.raises(SystemExit) as excinfo:
                Input(prompt, processes).invoke()
            assert excinfo.value.code == 'user quit'
