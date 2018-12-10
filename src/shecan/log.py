import logging
from typing import Any


def setup_logging(args: Any) -> logging.StreamHandler:
    ch = logging.StreamHandler()
    formatter = logging.Formatter("%(asctime)s %(levelname)s: %(message)s")
    ch.setFormatter(formatter)
    logger = logging.getLogger("shecan")
    logger.setLevel(logging.DEBUG if args.debug else logging.INFO)
    logger.addHandler(ch)
    return ch
