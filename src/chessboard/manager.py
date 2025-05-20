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
    _possible_move: Optional[chess.Move]
    _outcome: Optional[chess.Outcome]
    _claim_draw: bool

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
        self._outcome = None
        self._claim_draw = False
        self._interface = interface

    @property
    def state(self) -> manager_enums.State:
        """
        Returns the current state of the manager.

        :return: The current state of the manager.
        """
        return self._state

    @property
    def physical_board(self) -> chess.Board:
        """
        Returns the physical board.

        :return: The physical board.
        """
        return self._interface.board.copy()

    @property
    def possible_move(self) -> Optional[chess.Move]:
        """
        Returns the possible move detected by the interface. If not None, then there is
        a legal move on the board which can be confirmed.

        :return: The possible move detected by the interface.
        """
        return self._possible_move

    @property
    def outcome(self) -> Optional[chess.Outcome]:
        """
        Returns the outcome of the game. If not None, then the game is over.

        :return: The outcome of the game.
        """
        return self._outcome

    @property
    def can_claim_draw(self) -> bool:
        """
        Returns True if the player to move can claim a draw. (ex. 3-fold repetition)

        :return: True if the player to move can claim a draw.
        """
        return self.physical_board.can_claim_draw()

    def claim_draw(self):
        """
        Claim a draw. (ex. 3-fold repetition)
        """
        if self._state != manager_enums.State.GAME_IN_PROGRESS:
            raise manager_exceptions.ChessboardManagerStateError(
                f"Cannot claim draw in state \"{self._state}\".")
        if not self.can_claim_draw:
            raise manager_exceptions.ChessboardManagerStateError(
                "Cannot claim draw, no draw available.")
        logger.debug(
            f"{'White' if self.physical_board.turn == chess.WHITE else 'Black'} "
            f"claiming draw")
        self._claim_draw = True

    def confirm_possible_move(self,
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
        if promoteTo is not None and self._possible_move.promotion is not None:
            logger.debug(f"Promoting to {promoteTo.name} ({promoteTo.value[0]})")
            self._possible_move.promotion = promoteTo.value[0]
        logger.debug(f"Confirming possible move: {self._possible_move} "
                     f"({self.physical_board.san(self._possible_move)})")
        self._interface.add_move(self._possible_move)
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
        self._outcome = None
        self._claim_draw = False

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
        self._outcome = None
        self._claim_draw = False
        self._interface.reset_board()

    def update(self):
        """
        Update the manager. This should be called as often as possible to keep the game
        state in sync with the physical board.
        """
        if self._state == manager_enums.State.GAME_IN_PROGRESS:
            self._possible_move = self._interface.check_for_possible_move()
            self._outcome = self._interface.board.outcome(claim_draw=self._claim_draw)
            if self._outcome is not None:
                self._state = manager_enums.State.GAME_OVER
                self._possible_move = None
