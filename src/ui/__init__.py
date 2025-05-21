import logging
import threading

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from ui.game_screen import GameScreen
from ui.game_screen.black_promoting_to_screen import BlackPromotingToScreen
from ui.game_screen.confirm_resignation_screen import ConfirmResignationScreen
from ui.game_screen.more_actions_screen import MoreActionsScreen
from ui.game_screen.white_promoting_to_screen import WhitePromotingToScreen
from ui.main_screen import MainScreen
from ui.new_game_screen import NewGameScreen
from ui.new_game_screen.black_player_config_screen import BlackPlayerConfigScreen
from ui.new_game_screen.white_player_config_screen import WhitePlayerConfigScreen
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


class ChessboardApp(App):
    _update_thread: threading.Thread
    _stop_event: threading.Event

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        sm = ScreenManager()
        screens = (
            MainScreen,
            NewGameScreen,
            WhitePlayerConfigScreen,
            BlackPlayerConfigScreen,
            GameScreen,
            WhitePromotingToScreen,
            BlackPromotingToScreen,
            MoreActionsScreen,
            ConfirmResignationScreen
        )
        for screen in screens:
            sm.add_widget(screen())
        return sm
