import chess


def square_set_from_board(b: chess.Board) -> chess.SquareSet:
    """
    Converts a chess board to a square set.

    :param b: The chess board to convert.
    :return: The square set representing the chess pieces on the board.
    """
    ss = chess.SquareSet()
    for color in (chess.WHITE, chess.BLACK):
        for piece in chess.PIECE_TYPES:
            piece_squares = b.pieces(piece, color)
            ss |= chess.SquareSet(piece_squares)
    return ss
