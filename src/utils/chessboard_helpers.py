from io import BytesIO, StringIO

import chess
import chess.svg
from kivy.core.image import Image as CoreImage
from reportlab.graphics import renderPM
from svglib.svglib import svg2rlg


def get_chessboard_preview(board: chess.Board, size: int) -> CoreImage:
    """
    Returns a preview of the chessboard as a PNG image.

    :param board: The chessboard to get a preview of.
    :param size: The size of the chessboard in pixels.
    :return: The chessboard preview texture.
    """
    last_move = board.peek() if len(board.move_stack) > 0 else None
    fill = {}
    checkers = board.checkers()
    if checkers:
        # Get a piece that is checking the king (although multiple checkers are
        # possible, they should all be the same color)
        a_checking_piece = board.piece_at(checkers.pop())
        side_in_check = not a_checking_piece.color
        # Get the king that is in check
        check_square = board.king(side_in_check)
        fill[check_square] = "#CC0000CC"
    svg = chess.svg.board(board, size=size, lastmove=last_move,
                          # check=check_square  # svglib doesn't like the gradient used
                          # for check so we use fill
                          fill=fill)
    drawing = svg2rlg(StringIO(svg))
    png_buf = BytesIO()
    renderPM.drawToFile(drawing, png_buf, fmt="PNG")
    png_buf.seek(0)
    return CoreImage(png_buf, ext="png")
