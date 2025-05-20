from enum import Enum

import chess


class State(Enum):
    IDLE = "IDLE"
    GAME_IN_PROGRESS = "GAME_IN_PROGRESS"


class PlayerType(Enum):
    HUMAN = "HUMAN"
    ENGINE = "ENGINE"


class PromotionPiece(Enum):
    QUEEN = chess.QUEEN,
    KNIGHT = chess.KNIGHT,
    BISHOP = chess.BISHOP,
    ROOK = chess.ROOK,
