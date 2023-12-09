import logging

from rich.console import Console
from rich.logging import RichHandler

logging.basicConfig(
    format="%(message)s",
    level=logging.DEBUG,
    handlers=[RichHandler(console=Console(stderr=True, width=120))],
)
