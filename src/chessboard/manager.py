import logging

import chess

from chessboard import manager_dataclasses, manager_enums, manager_exceptions
from chessboard.interface import ChessboardInterface
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


class ChessboardManager:
    """
    Handles main logic for the digital chessboard.
    """

    _state: manager_enums.State

    _interface: ChessboardInterface
    _board: chess.Board

    _white_player_config: manager_dataclasses.PlayerConfiguration
    _black_player_config: manager_dataclasses.PlayerConfiguration

    def __init__(self, interface: ChessboardInterface):
        self._state = manager_enums.State.IDLE
        self._interface = interface
        self._board = chess.Board()

    @property
    def state(self) -> manager_enums.State:
        """
        Returns the current state of the manager.

        :return: The current state of the manager.
        """
        return self._state

    def new_game(self, white_player: manager_dataclasses.PlayerConfiguration,
                 black_player: manager_dataclasses.PlayerConfiguration):
        """
        Starts a new game. State must be IDLE.

        :param white_player: Configuration for the white player.
        :param black_player: Configuration for the black player.
        """
        if self._state != manager_enums.State.IDLE:
            raise manager_exceptions.ChessboardManagerStateError(
                f"Cannot start a new game in state \"{self._state}\".")
        logger.debug(f"Starting new game with players: {white_player}, {black_player}")
        self._white_player_config = white_player
        self._black_player_config = black_player
        self._state = manager_enums.State.GAME_IN_PROGRESS
        self._board.reset()

    def update(self):
        """
        Update the manager. This should be called as often as possible to keep the game
        state in sync with the physical board.
        """
        self._interface.update()
