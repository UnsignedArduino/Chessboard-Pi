from os import environ

environ["KIVY_NO_ARGS"] = "1"

import logging
import threading
from argparse import ArgumentParser
from time import sleep

from kivy.core.window import Window

from chessboard.interface import ChessboardInterface
from chessboard.manager import ChessboardManagerSingleton
from ui import ChessboardApp
from utils.logger import create_logger, set_all_stdout_logger_levels

logger = create_logger(name=__name__, level=logging.DEBUG)

parser = ArgumentParser(
    description="Raspberry Pi firmware for a magnetic-piece-tracking digital chessboard! WIP")
parser.add_argument("--port", "-p", required=True,
                    help="Serial port to connect to the chessboard.")
parser.add_argument("--no-fullscreen", action="store_true",
                    help="Disable fullscreen mode.")
parser.add_argument("--debug", action="store_true",
                    help="Enable debug logging.")
args = parser.parse_args()
debug = bool(args.debug)
if debug:
    set_all_stdout_logger_levels(logging.DEBUG)
logger.debug(f"Received arguments: {args}")

Window.size = (240, 320)
Window.resizable = False
if not args.no_fullscreen:
    logger.debug("Fullscreen mode enabled")
    Window.fullscreen = True

interface = ChessboardInterface()
interface.connect(args.port)
manager = ChessboardManagerSingleton(interface)


def update_loop():
    while not stop_event.is_set():
        manager.update()
        sleep(0.01)


stop_event = threading.Event()
update_thread = threading.Thread(target=update_loop, daemon=True)
update_thread.start()
logger.debug("Started update thread")

app = ChessboardApp()
app.run()

stop_event.set()
update_thread.join()
logger.debug("Stopped update thread")
