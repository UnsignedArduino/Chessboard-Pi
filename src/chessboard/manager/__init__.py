import logging
from typing import Optional

import chess

from chessboard.interface import ChessboardInterface
from chessboard.manager import manager_dataclasses, manager_enums, manager_exceptions
from game import ChessGame
from utils.logger import create_logger
from utils.singleton import Singleton

logger = create_logger(name=__name__, level=logging.DEBUG)


class ChessboardManagerSingleton(metaclass=Singleton):
    """
    Handles main logic for the digital chessboard. Is a singleton.
    """

    _state: manager_enums.State
    _possible_move: Optional[chess.Move]
    _game: Optional[ChessGame]

    _interface: ChessboardInterface

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
        self._possible_move = None
        self._game = None
        self._interface = interface

    @property
    def state(self) -> manager_enums.State:
        """
        Returns the current state of the manager.

        :return: The current state of the manager.
        """
        return self._state

    @property
    def game(self) -> Optional[ChessGame]:
        """
        Returns the current game instance.

        :return: The current game instance.
        """
        return self._game

    @property
    def possible_move(self) -> Optional[chess.Move]:
        """
        Returns the possible move detected by the interface. If not None, then there is
        a legal move on the board which can be confirmed.

        :return: The possible move detected by the interface.
        """
        return self._possible_move

    def confirm_possible_move(self, *,
                              promoteTo: Optional[manager_enums.PromotionPiece] = None):
        """
        Confirms the possible move detected by the interface, adding it to the current
        board. This should be called when the user confirms the move on the UI.

        :param promoteTo: The piece to promote to, if the move is a promotion.
        """
        if self._state != manager_enums.State.GAME_IN_PROGRESS:
            raise manager_exceptions.ChessboardManagerStateError(
                f"Cannot confirm possible move in state \"{self._state}\".")
        if self._possible_move is None:
            raise manager_exceptions.ChessboardManagerStateError(
                "No possible move to confirm.")
        # If a draw was offered and it's currently the other players turn, then the move
        # is a decline of the draw offer
        if self.game.offered_draw is not None and self.game.offered_draw != self.game.board.turn:
            self.game.decline_offered_draw()
        if promoteTo is not None and self._possible_move.promotion is not None:
            logger.debug(f"Promoting to {promoteTo.name} ({promoteTo.value[0]})")
            self._possible_move.promotion = promoteTo.value[0]
        logger.debug(f"Confirming possible move: {self._possible_move} "
                     f"({self.game.board.san(self._possible_move)})")
        self._interface.add_move(self._possible_move)
        self.game.board.push(self._possible_move)
        self._possible_move = None

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
        self._interface.reset_board()
        self._game = ChessGame()

    def exit(self):
        """
        Pauses the game and exits. State must be GAME_IN_PROGRESS.
        """
        if self._state not in (manager_enums.State.GAME_IN_PROGRESS,
                               manager_enums.State.GAME_OVER):
            raise manager_exceptions.ChessboardManagerStateError(
                f"Cannot pause and exit in state \"{self._state}\".")
        logger.debug("Exiting.")
        self._state = manager_enums.State.IDLE
        self._possible_move = None
        self._interface.reset_board()
        self._game = None

    def update(self):
        """
        Update the manager. This should be called as often as possible to keep the game
        state in sync with the physical board.
        """
        if self._state == manager_enums.State.GAME_IN_PROGRESS:
            self._possible_move = self._interface.check_for_possible_move()
            if self.game is not None:
                o = self.game.outcome
                if o is not None:
                    self._state = manager_enums.State.GAME_OVER
                    self._possible_move = None
