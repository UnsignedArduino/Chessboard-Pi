from enum import Enum

import chess


class State(Enum):
    IDLE = "IDLE"
    GAME_IN_PROGRESS = "GAME_IN_PROGRESS"
    GAME_OVER = "GAME_OVER"


class PlayerType(Enum):
    HUMAN = "HUMAN"
    ENGINE = "ENGINE"


class PromotionPiece(Enum):
    QUEEN = chess.QUEEN,
    KNIGHT = chess.KNIGHT,
    BISHOP = chess.BISHOP,
    ROOK = chess.ROOK,
