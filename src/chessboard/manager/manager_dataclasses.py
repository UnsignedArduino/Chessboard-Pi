from dataclasses import dataclass

from chessboard.manager import manager_enums


@dataclass
class PlayerConfiguration:
    """
    Configuration for a player in the chessboard manager.
    """
    player_type: manager_enums.PlayerType
    # TODO: Add engine configuration settings
    # TODO: Add time control settings
