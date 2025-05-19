import logging
from typing import Optional

import chess
import serial.serialutil
from serial import Serial

from chessboard import interface_exceptions
from chessboard.helpers import square_set_from_board
from chessboard.interface_dataclasses import AddPieceDifference, MovePieceDifference, \
    PieceDifferencesToMatch, RemovePieceDifference, SquareDifferencesToMatch
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


class ChessboardInterface:
    """
    Handles interfacing with the serial connection to the chessboard.
    """
    _conn: Optional[Serial]
    _curr_board: chess.Board

    def __init__(self):
        self._conn = None
        self._curr_board = chess.Board()
        self._curr_board.clear()

    def connect(self, port: str):
        """
        Connect to the chessboard via the specified serial port.

        :param port: The serial port to connect to.
        """
        try:
            self._conn = Serial(port, baudrate=9600, timeout=1)
            logger.debug(f"Connected to chessboard on port {port}")
            # Clear command buffer
            self._conn.write(b"\r\n\r\n")
        except serial.serialutil.SerialException:
            raise interface_exceptions.ChessboardInterfaceConnectionError(
                f"Failed to connect to chessboard on port {port}")

    def disconnect(self):
        """
        Disconnect from the chessboard.
        """
        if self._conn:
            self._conn.close()
            logger.debug(f"Disconnected from chessboard on port {self._conn.port}")
            self._conn = None
        else:
            raise interface_exceptions.ChessboardInterfaceConnectionError(
                "No connection to disconnect")

    def _get_curr_board_square_set(self) -> chess.SquareSet:
        """
        Gets the square set for the pieces of the current board in memory, NOT the
        physical board.

        :return: The current square set representing the chess pieces on the board.
        """
        return square_set_from_board(self._curr_board)

    def _get_physical_square_set(self) -> chess.SquareSet:
        """
        Gets the square set for the pieces on the physical board, NOT the board in
        memory. Expects an open serial connection.

        :return: The current square set representing the chess pieces on the board.
        """
        self._conn.write(b"print\r\n")
        first_line = self._conn.readline()
        if first_line != b"Printing pieces\r\n":
            raise interface_exceptions.ChessboardInterfaceBadResponseError(
                f"Unexpected first line response from chessboard when querying for "
                f"current bitboard: {first_line}")
        ss = chess.SquareSet()
        for row in range(8):
            line = self._conn.readline().strip().split(b" ")
            for col, col_char in enumerate(line):
                # Oddly enough "0" is a piece, "." is empty
                if col_char == b"0":
                    ss.add(chess.square(col, 7 - row))
                elif col_char == b".":
                    continue
                else:
                    raise interface_exceptions.ChessboardInterfaceBadResponseError(
                        f"Unexpected piece character in row {row} col {col}: {col_char}")
        return ss

    def update(self):
        """
        Update the chessboard state by querying the chessboard. With some logic we can
        track pieces based on what bits change. Must be called as often as possible to
        keep the board state up to date.
        """
        if not self._conn:
            raise interface_exceptions.ChessboardInterfaceConnectionError(
                "No connection to update from")
        square_diffs = self.differences_to_current()
        removals = square_diffs.to_remove
        additions = square_diffs.to_add
        # Single piece movement
        if len(removals) == 1 and len(additions) == 1:
            removed_square = removals.pop()
            added_square = additions.pop()
            try:
                move = self._curr_board.find_move(removed_square, added_square)
                if move:
                    self._curr_board.push(move)
            except chess.IllegalMoveError:
                pass
        # First time startup and all pieces present
        elif len(removals) == 0 and len(additions) == 32:
            self._curr_board.reset()

    def differences_to_current(self) -> SquareDifferencesToMatch:
        """
        Finds the differences needed to match the current board to the physical board.

        :return: A SquareDifferencesToMatch object containing the differences.
        """
        curr_square_set = self._get_curr_board_square_set()
        physical_square_set = self._get_physical_square_set()
        to_add = physical_square_set - curr_square_set
        to_remove = curr_square_set - physical_square_set
        return SquareDifferencesToMatch(to_add, to_remove)

    def differences_to_target(self, target: chess.Board) -> PieceDifferencesToMatch:
        """
        Finds the piece differences needed to match the current board to the target board.

        :param target: The target board to compare against.
        :return: A PieceDifferencesToMatch object containing the differences.
        """
        if self._curr_board == target:
            return PieceDifferencesToMatch([], [], [])
        to_add = []
        to_remove = []
        to_move = []

        curr_square_set = self._get_curr_board_square_set()
        target_square_set = square_set_from_board(target)
        removals = curr_square_set - target_square_set
        additions = target_square_set - curr_square_set
        for removal in removals:
            piece = self._curr_board.piece_at(removal)
            if piece:
                to_remove.append(RemovePieceDifference(piece=piece, square=removal))
        for addition in additions:
            piece = target.piece_at(addition)
            if piece:
                to_add.append(AddPieceDifference(piece=piece, square=addition))
        # Simplify - if piece is removed and added, it's a move
        # Must iterate backwards to avoid index errors
        for to_remove_index in range(len(to_remove) - 1, 0, -1):
            for to_add_index in range(len(to_add) - 1, 0, -1):
                r = to_remove[to_remove_index]
                a = to_add[to_add_index]
                if r.piece == a.piece:
                    to_move.append(
                        MovePieceDifference(piece=r.piece, from_square=r.square,
                                            to_square=a.square))
                    to_remove.pop(to_remove_index)
                    to_add.pop(to_add_index)

        return PieceDifferencesToMatch(to_add, to_remove, to_move)
