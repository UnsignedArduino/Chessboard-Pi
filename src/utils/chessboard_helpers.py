from functools import lru_cache
from io import BytesIO

import chess
import chess.svg
from cairosvg import svg2png
from kivy.core.image import Image as CoreImage


@lru_cache(maxsize=16)
def svg_to_core_image(svg: str) -> CoreImage:
    """
    Converts an SVG string to a CoreImage.

    :param svg: The SVG string to convert.
    :return: The CoreImage object.
    """
    png_buf = BytesIO()
    svg2png(bytestring=svg.encode("utf-8"), write_to=png_buf)
    png_buf.seek(0)
    return CoreImage(png_buf, ext="png")


def get_chessboard_preview(board: chess.Board, possible_move: chess.Move,
                           orientation: chess.WHITE | chess.BLACK = chess.WHITE,
                           size: int = 240) -> CoreImage:
    """
    Returns a preview of the chessboard as a PNG image.

    :param board: The chessboard to get a preview of.
    :param possible_move: The possible move to highlight.
    :param size: The size of the chessboard in pixels.
    :return: The chessboard preview texture.
    """
    last_move = board.peek() if len(board.move_stack) > 0 else None
    check_square = None
    checkers = board.checkers()
    if checkers:
        # Get a piece that is checking the king (although multiple checkers are
        # possible, they should all be the same color)
        a_checking_piece = board.piece_at(checkers.pop())
        side_in_check = not a_checking_piece.color
        # Get the king that is in check
        check_square = board.king(side_in_check)
    svg = chess.svg.board(board, size=size, lastmove=last_move, check=check_square,
                          orientation=orientation,
                          arrows=[chess.svg.Arrow(possible_move.from_square,
                                                  possible_move.to_square,
                                                  color="green")] if possible_move is not None else [])
    return svg_to_core_image(svg)
