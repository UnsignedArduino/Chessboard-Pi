class ChessboardManagerError(Exception):
    """
    Base class for all exceptions raised by the ChessboardManager.
    """
    pass


class ChessboardManagerStateError(ChessboardManagerError):
    """
    Raised when an operation is attempted in an invalid state.
    """
