from os import environ

environ["KIVY_NO_ARGS"] = "1"

from kivy.config import Config

Config.set("graphics", "resizable", "0")
Config.set("graphics", "width", "240")
Config.set("graphics", "height", "320")

import logging
from argparse import ArgumentParser

from ui import ChessboardApp
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

app = ChessboardApp()
app.run_with_args(args.port)
