from enum import Enum


class ChessGameOutcomeType(Enum):
    # Checkmates
    CHECKMATE_BY_WHITE = "White wins by checkmate"
    CHECKMATE_BY_BLACK = "Black wins by checkmate"
    # Draws
    AGREED_DRAW = "Agreed upon draw"
    STALEMATE = "Stalemate"
    INSUFFICIENT_MATERIAL = "Insufficient material"
    FORCED_SEVENTYFIVE_MOVES = "Forced 75 move rule draw"
    FORCED_FIVEFOLD_REPETITION = "Forced 5 fold repetition draw"
    CLAIMED_FIFTY_MOVES = "Claimed 50 move rule draw"
    CLAIMED_THREEFOLD_REPETITION = "Claimed 3 fold repetition draw"
    # Resignation
    RESIGNATION_BY_WHITE = "Resignation by white"
    RESIGNATION_BY_BLACK = "Resignation by black"
