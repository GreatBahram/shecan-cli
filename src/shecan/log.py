import logging
from typing import Any


def setup_logging(args: Any) -> logging.StreamHandler:
    console_handler = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    console_handler.setFormatter(formatter)
    logger = logging.getLogger("shecan")
    logger.setLevel(logging.DEBUG if args.debug else logging.INFO)
    logger.addHandler(console_handler)
    return console_handler
