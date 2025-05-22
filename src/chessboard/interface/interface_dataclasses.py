# from dataclasses import dataclass
# from typing import Optional
#
# import chess


# from chessboard import interface_enums


# @dataclass
# class AddPieceDifference:
#     """
#     Represents a piece difference that needs to be added to the board.
#     """
#     piece: chess.Piece
#     square: chess.Square
#
#
# @dataclass
# class RemovePieceDifference:
#     """
#     Represents a piece difference that needs to be removed from the board.
#     """
#     piece: chess.Piece
#     square: chess.Square
#
#
# @dataclass
# class MovePieceDifference:
#     """
#     Represents a piece difference that needs to be moved on the board.
#     """
#     piece: chess.Piece
#     from_square: chess.Square
#     to_square: chess.Square
#
#
# @dataclass
# class PieceDifferencesToMatch:
#     """
#     Represents what piece differences need to be matched.
#     """
#     to_add: list[AddPieceDifference]
#     to_remove: list[RemovePieceDifference]
#     to_move: list[MovePieceDifference]
#
#     def __len__(self):
#         """
#         Returns the total number of piece differences.
#         """
#         return len(self.to_add) + len(self.to_remove) + len(self.to_move)
#
#     @staticmethod
#     def create_empty() -> "PieceDifferencesToMatch":
#         """
#         Creates an empty PieceDifferencesToMatch object.
#         """
#         return PieceDifferencesToMatch([], [], [])
#
#
# @dataclass
# class SquareDifferencesToMatch:
#     """
#     Represents what square differences need to be matched. (which squares should have
#     a piece added and which squares should have a piece removed)
#     """
#     to_add: chess.SquareSet
#     to_remove: chess.SquareSet
#
#     def __eq__(self, other):
#         """
#         Checks if the two SquareDifferencesToMatch objects are equal.
#         """
#         return (self.to_add == other.to_add and
#                 self.to_remove == other.to_remove)


# @dataclass
# class SquareDifference:
#     """
#     Represents a square difference.
#     """
#     square: chess.Square
#     type: interface_enums.SquareDifferenceType


# @dataclass
# class PossibleMoveResult:
#     """
#     Represents a possible move result.
#     """
#     move: Optional[chess.Move]
#     square_diffs: SquareDifferencesToMatch
