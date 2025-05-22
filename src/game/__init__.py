import logging
from typing import Optional

import chess

from game.chess_game_enums import ChessGameOutcomeType
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


class ChessGame:
    _board: chess.Board
    _claim_draw: bool
    _offered_draw: Optional[chess.WHITE | chess.BLACK] = None
    _ended_to_agreed_draw: bool = False
    _ended_to_resignation: bool = False

    def __init__(self):
        self._board = chess.Board()
        self._claim_draw = False
        self._offered_draw = None
        self._ended_to_agreed_draw = False
        self._ended_to_resignation = False

    @property
    def board(self) -> chess.Board:
        """
        Returns the board instance.

        :return: The board instance.
        """
        return self._board

    @property
    def outcome(self) -> Optional[ChessGameOutcomeType]:
        """
        Returns the outcome of the game. If None, the game is still in progress.

        :return: The outcome of the game.
        """
        if self._ended_to_resignation:
            return ChessGameOutcomeType.RESIGNATION_BY_WHITE if self.board.turn == chess.WHITE else ChessGameOutcomeType.RESIGNATION_BY_BLACK
        elif self._ended_to_agreed_draw:
            return ChessGameOutcomeType.AGREED_DRAW
        o = self._board.outcome(claim_draw=self._claim_draw)
        if o is None:
            return None
        if o.termination == chess.Termination.CHECKMATE:
            return ChessGameOutcomeType.CHECKMATE_BY_WHITE if o.winner == chess.WHITE else ChessGameOutcomeType.CHECKMATE_BY_BLACK
        elif o.termination == chess.Termination.STALEMATE:
            return ChessGameOutcomeType.STALEMATE
        elif o.termination == chess.Termination.INSUFFICIENT_MATERIAL:
            return ChessGameOutcomeType.INSUFFICIENT_MATERIAL
        elif o.termination == chess.Termination.SEVENTYFIVE_MOVES:
            return ChessGameOutcomeType.FORCED_SEVENTYFIVE_MOVES
        elif o.termination == chess.Termination.FIVEFOLD_REPETITION:
            return ChessGameOutcomeType.FORCED_FIVEFOLD_REPETITION
        elif o.termination == chess.Termination.FIFTY_MOVES:
            return ChessGameOutcomeType.CLAIMED_FIFTY_MOVES
        elif o.termination == chess.Termination.THREEFOLD_REPETITION:
            return ChessGameOutcomeType.CLAIMED_THREEFOLD_REPETITION
        return None

    @property
    def can_claim_draw(self) -> bool:
        """
        Returns True if the player can claim a draw, False otherwise.

        :return: True if the player can claim a draw, False otherwise.
        """
        return self._board.can_claim_draw()

    def claim_draw(self):
        """
        Claims a draw. This is only possible if the player can claim a draw.
        """
        if self.can_claim_draw:
            self._claim_draw = True
            logger.debug(f"{'White' if self.board.turn == chess.WHITE else 'Black'} "
                         f"claiming draw")
        else:
            raise ValueError("Cannot claim draw")

    @property
    def offered_draw(self) -> Optional[chess.WHITE | chess.BLACK]:
        """
        Returns the color of the player who offered a draw. If None, no draw has been offered.

        :return: The color of the player who offered a draw.
        """
        return self._offered_draw

    def offer_draw(self):
        """
        The current player offers a draw.
        """
        if self._offered_draw is None:
            self._offered_draw = self.board.turn
            logger.debug(f"{'White' if self.board.turn == chess.WHITE else 'Black'} "
                         f"offering draw")
        else:
            raise ValueError("Draw already offered")

    def accept_offered_draw(self):
        """
        Accepts the offered draw. This is only possible if a draw has been offered.
        """
        if self._offered_draw is not None:
            self._offered_draw = None
            self._ended_to_agreed_draw = True
            logger.debug(f"{'White' if self.board.turn == chess.BLACK else 'Black'} "
                         f"accepting draw")
        else:
            raise ValueError("No draw offered")

    def decline_offered_draw(self):
        """
        Declines the offered draw. This is only possible if a draw has been offered.
        """
        if self._offered_draw is not None:
            self._offered_draw = None
            logger.debug(f"{'White' if self.board.turn == chess.BLACK else 'Black'} "
                         f"declining draw")
        else:
            raise ValueError("No draw offered")

    def resign(self):
        """
        The current player resigns the game. The game is over and the other player wins.
        """
        self._ended_to_resignation = True
        logger.debug(f"{'White' if self.board.turn == chess.WHITE else 'Black'} "
                     f"resigning")
