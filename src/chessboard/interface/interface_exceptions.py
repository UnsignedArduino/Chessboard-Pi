class ChessboardInterfaceError(Exception):
    """
    Base class for exceptions in the chessboard interface module.
    """
    pass


class ChessboardInterfaceConnectionError(ChessboardInterfaceError):
    """
    Raised when an error occurs related to the connection to the chessboard.
    """


class ChessboardInterfaceBadResponseError(ChessboardInterfaceError):
    """
    Raised when the chessboard returns an unexpected response.
    """
