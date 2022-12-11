import importlib.util
import inspect
import logging
import pathlib
import shutil
import sys
from typing import Callable, Optional, Sequence

from .arguments import parse_arguments

INPUT_EXTENSION = ".txt"
RUN_FUNCTION = "run"


def _input_file_path(year: str, day: str, is_small: bool) -> pathlib.Path:
    input_path = pathlib.Path("input") / year

    suffix = "_small" if is_small else ""

    return input_path / f"day{day}{suffix}{INPUT_EXTENSION}"


def _runner(year: str, day: str) -> Callable:
    file_path = pathlib.Path(year) / f"day{day}.py"
    module_name = "puzzle"

    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    try:
        return getattr(module, RUN_FUNCTION)
    except AttributeError as e:
        raise NotImplementedError(
            f"`{RUN_FUNCTION}` function is not implemented for {year} day {day}"
        ) from e


def run(*, year: int, day: int, is_small: bool) -> None:
    """Run the test case for the given year and day."""
    input_file = _input_file_path(year, day, is_small)

    try:
        with open(input_file, "r", encoding="utf-8") as file:
            solutions = _runner(year, day)(file)
    except FileNotFoundError:
        logging.error(f"No input or solution file found for {year} day {day}")
        return

    logging.info(f"Solutions: {solutions}")


def stub(*, year: str, day: str) -> None:
    """Create two stub input files and copy `template.py` into a solution file."""

    for is_small in [True, False]:
        input_file = _input_file_path(year, day, is_small)

        input_file.parent.mkdir(parents=True, exist_ok=True)

        logging.debug(f"Creating '{input_file.name}'")
        input_file.touch()

    solution_path = pathlib.Path(year)
    solution_path.mkdir(parents=True, exist_ok=True)

    solution_file = solution_path / f"day{day}.py"
    if not solution_file.is_file():
        logging.info(f"Stubbing solution file in '{solution_path.resolve()}'")

        logging.debug(f"Creating '{solution_file.name}'")
        shutil.copyfile("aoc/template.py", solution_file)


def real_main(argv: Optional[Sequence[str]] = None) -> int:
    """Entry point into the module."""
    args = parse_arguments(argv)

    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # If the command string passed to the function is not found, this will raise an exception.
    # No need to whitelist the function lookup below.
    try:
        function = getattr(sys.modules[__name__], str(args.subcommand))
    except KeyError as e:
        raise NotImplementedError(f"Command '{args.subcommand}' not implemented") from e

    # Get the arguments required by the function from the command line. Each method
    # specifies key-word only arguments that must be passed in.
    arguments = {arg: getattr(args, arg) for arg in inspect.getfullargspec(function).kwonlyargs}

    function(**arguments)

    return 0


def main(argv: Optional[Sequence[str]] = None) -> int:
    """Enter into the main module and catch any exceptions.

    All exceptions are caught here to swallow the stack trace.
    """
    try:
        return real_main(argv)
    except KeyboardInterrupt:
        logging.error("Interrupted by user. Goodbye")
        return 0
    except Exception as e:  # pylint: disable=broad-except
        logging.error(f"python -m five: error: {e}", exc_info=__debug__)
        return 1
