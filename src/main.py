import logging
from argparse import ArgumentParser

from utils.logger import create_logger, set_all_stdout_logger_levels

logger = create_logger(name=__name__, level=logging.DEBUG)

parser = ArgumentParser(
    description="Raspberry Pi firmware for a magnetic-piece-tracking digital chessboard! WIP")
parser.add_argument("--port", "-p", required=True,
                    help="Serial port to connect to the chessboard.")
parser.add_argument("--debug", action="store_true",
                    help="Enable debug logging.")
args = parser.parse_args()
debug = bool(args.debug)
if debug:
    set_all_stdout_logger_levels(logging.DEBUG)
logger.debug(f"Received arguments: {args}")
