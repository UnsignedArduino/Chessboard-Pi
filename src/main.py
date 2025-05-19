import logging
from argparse import ArgumentParser

from chessboard import manager_dataclasses, manager_enums
from chessboard.interface import ChessboardInterface
from chessboard.manager import ChessboardManager
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

interface = ChessboardInterface()
interface.connect(args.port)
manager = ChessboardManager(interface)
manager.new_game(
    white_player=manager_dataclasses.PlayerConfiguration(
        player_type=manager_enums.PlayerType.HUMAN),
    black_player=manager_dataclasses.PlayerConfiguration(
        player_type=manager_enums.PlayerType.HUMAN)
)
try:
    while True:
        manager.update()
except KeyboardInterrupt:
    interface.disconnect()
