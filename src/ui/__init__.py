import logging
from typing import Never

import chess
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.screenmanager import ScreenManager

from chessboard.manager import ChessboardManagerSingleton, manager_enums
from ui.game_screen import GameScreen
from ui.game_screen.black_promoting_to_screen import BlackPromotingToScreen
from ui.game_screen.confirm_offer_draw_screen import ConfirmOfferDrawScreen
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
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._player_showing_to = chess.WHITE
        self._last_player_to_show = chess.WHITE

        self.scatter_root = ScatterLayout(do_rotation=False, do_scale=False,
                                          do_translation=False)

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
            ConfirmResignationScreen,
            ConfirmOfferDrawScreen
        )
        for s in screens:
            sm.add_widget(s())

        self.scatter_root.add_widget(sm)

    def build(self):
        return self.scatter_root

    @property
    def player_showing_to(self) -> chess.WHITE | chess.BLACK:
        """
        Returns the player that is currently showing the screen.

        :return: The player that is currently showing the screen.
        """
        return self._player_showing_to

    def on_start(self):
        Clock.schedule_interval(self.update_rotation, 1 / 20)

    def on_stop(self):
        Clock.unschedule(self.update_rotation)

    def update_rotation(self, _: Never = None):
        """
        Updates the rotation of the chessboard based on the current player to show.
        """
        manager = ChessboardManagerSingleton()
        app = App.get_running_app()
        self._player_showing_to = chess.WHITE
        if manager.game is not None and manager.state == manager_enums.State.GAME_IN_PROGRESS:
            self._player_showing_to = manager.game.board.turn
        if self._last_player_to_show != self._player_showing_to:
            if self._player_showing_to == chess.WHITE:
                app.set_rotation_to_0()
            else:
                app.set_rotation_to_180()
            self._last_player_to_show = self._player_showing_to

    def set_rotation_to_0(self):
        """
        Sets the rotation of the scatter root to 0 degrees.
        """
        anim = Animation(rotation=0, duration=0.5, t="out_quad")
        anim.start(self.scatter_root)

    def set_rotation_to_180(self):
        """
        Sets the rotation of the scatter root to 180 degrees.
        """
        anim = Animation(rotation=180, duration=0.5, t="out_quad")
        anim.start(self.scatter_root)
