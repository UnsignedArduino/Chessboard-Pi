import logging
from typing import Optional

import chess

from chessboard import manager_dataclasses, manager_enums, manager_exceptions
from chessboard.interface import ChessboardInterface
from utils.logger import create_logger
from utils.singleton import Singleton

logger = create_logger(name=__name__, level=logging.DEBUG)


class ChessboardManagerSingleton(metaclass=Singleton):
    """
    Handles main logic for the digital chessboard. Is a singleton.
    """

    _state: manager_enums.State

    _interface: ChessboardInterface
    _board: chess.Board

    _white_player_config: manager_dataclasses.PlayerConfiguration
    _black_player_config: manager_dataclasses.PlayerConfiguration

    def __init__(self, interface: Optional[ChessboardInterface] = None):
        """
        :param interface: As the class is a singleton, the interface must be passed in
         when the class is instantiated for the first time. Subsequent calls to the
         class never end up calling this constructor again, so it's optional to appease
         the linter.
        """
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

    @property
    def board(self) -> chess.Board:
        """
        Returns the current board.

        :return: The current board.
        """
        return self._board.copy()

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
        self._state = manager_enums.State.GAME_IN_PROGRESS
        self._white_player_config = white_player
        self._black_player_config = black_player
        self._board.reset()

    def pause_and_exit(self):
        """
        Pauses the game and exits. State must be GAME_IN_PROGRESS.
        """
        if self._state != manager_enums.State.GAME_IN_PROGRESS:
            raise manager_exceptions.ChessboardManagerStateError(
                f"Cannot pause and exit in state \"{self._state}\".")
        logger.debug("Pausing game and exiting.")
        self._state = manager_enums.State.IDLE
        self._board.reset()

    def update(self):
        """
        Update the manager. This should be called as often as possible to keep the game
        state in sync with the physical board.
        """
        self._interface.update()
