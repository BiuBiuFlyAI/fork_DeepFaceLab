import pathlib
from typing import List, Optional


def input_path(prompt: str, must_exist: bool = False, default: Optional[pathlib.Path] = None) -> pathlib.Path:
    label = f"{prompt}: "

    while True:
        value = input(label).strip()
        value = pathlib.Path(value)

        if not value and default is not None:
            return default

        value = pathlib.Path(value)

        if must_exist and not value.exists():
            print("Error: Path does not exist, please try again.")
        else:
            return value


def input_int(prompt: str, default: Optional[int] = None) -> int:
    label = f"{prompt}{f' (default {default})' if default is not None else ''}: "

    while True:
        value = input(label).strip()

        if not value and default is not None:
            return default

        try:
            return int(value)
        except ValueError:
            print("Error: Please enter a valid integer.")


def input_float(prompt: str, default: Optional[float] = None) -> float:
    label = f"{prompt}{f' (default {default})' if default is not None else ''}: "

    while True:
        value = input(label).strip()

        if not value and default is not None:
            return default

        try:
            return float(value)
        except ValueError:
            print("Error: Please enter a valid float.")


def input_str(prompt: str, default: Optional[str] = None) -> str:
    label = f"{prompt}{f' (default {default})' if default is not None else ''}: "

    value = input(label).strip()

    if not value and default is not None:
        return default

    return value


def input_bool(prompt: str, default: Optional[bool] = False) -> bool:
    default_label = "Y/n" if default else "y/N"
    label = f"{prompt} ({default_label}): "

    while True:
        value = input(label).strip().lower()

        if value == "" and default is not None:
            return default
        elif value in ["y", "yes", "1", "true"]:
            return True
        elif value in ["n", "no", "0", "false"]:
            return False
        else:
            print("Error: Please enter 'y' or 'n'.")


def input_choice(prompt: str, choices: List[str], default: Optional[str] = None) -> str:
    choices_str = "/".join(choices)
    label = f"{prompt} [{choices_str}]{f' (default {default})' if default else ''}: "

    while True:
        value = input(label).strip()

        if not value and default is not None:
            return default
        elif value in choices:
            return value
        else:
            print(f"Error: Invalid input, please choose from {choices_str}.")
