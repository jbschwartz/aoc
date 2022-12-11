import argparse
from typing import Optional, Sequence


def parse_arguments(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    """Parse and return command line arguments.

    `sys.argv` will be used by default if passed `argv` is None. This allows for calling this
    function from the command line as well as from a python script.
    """
    # Top-level program parser.
    parser = argparse.ArgumentParser(prog="python -m aoc", description="Advent of Code helper")

    subcommands = parser.add_subparsers(dest="subcommand", metavar="subcommand", required=True)

    # This is a parent to all subcommand parsers. It contains the arguments which are common to all
    # of the subcommands.
    common_parser = argparse.ArgumentParser(add_help=False)
    common_parser.add_argument(dest="year", help="the year")
    common_parser.add_argument(dest="day", help="the year")
    common_parser.add_argument(
        "-v", "--verbose", action="store_true", help="enable verbose output on stderr"
    )

    _stub_parser = subcommands.add_parser("stub", help="create stub files", parents=[common_parser])

    run_parser = subcommands.add_parser("run", help="run the day's input", parents=[common_parser])

    run_parser.add_argument(
        "-s",
        "--small",
        dest="is_small",
        action="store_true",
        help="execute the small test input",
    )

    args = parser.parse_args(argv)

    return args
