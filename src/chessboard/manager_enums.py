from enum import Enum


class State(Enum):
    IDLE = "IDLE"
    GAME_IN_PROGRESS = "GAME_IN_PROGRESS"


class PlayerType(Enum):
    HUMAN = "HUMAN"
    ENGINE = "ENGINE"
