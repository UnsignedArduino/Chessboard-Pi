import logging
from typing import Never

import chess
from kivy.animation import Animation
from kivy.app import App
from kivy.clock import Clock
from kivy.config import ConfigParser
from kivy.uix.scatterlayout import ScatterLayout
from kivy.uix.screenmanager import ScreenManager

from chessboard.manager import ChessboardManagerSingleton, manager_enums
from ui.config import SettingsConfigSingleton
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
from ui.settings_screen import SettingsScreen
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


class ChessboardApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self._player_showing_to = chess.WHITE
        self._last_player_to_show = None

        self._transition_speed = 0.4
        self._rotation_speed = 0.5

        self.config = ConfigParser()
        self.config.read("settings.ini")

        self.scatter_root = ScatterLayout(do_rotation=False, do_scale=False,
                                          do_translation=False)

        self.screen_manager = ScreenManager()
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
            ConfirmOfferDrawScreen,
            SettingsScreen
        )
        for s in screens:
            self.screen_manager.add_widget(s())
        self._update_transition_speed()

        cbs = SettingsConfigSingleton().on_reload_callbacks
        cbs.append(self._update_transition_speed)
        cbs.append(self._update_rotation_speed)

        self.scatter_root.add_widget(self.screen_manager)

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
        self._player_showing_to = chess.WHITE
        if manager.game is not None and manager.state == manager_enums.State.GAME_IN_PROGRESS:
            self._player_showing_to = manager.game.board.turn
        if self._last_player_to_show != self._player_showing_to:
            if self._player_showing_to == chess.WHITE:
                self.set_rotation_to_0(no_animate=self._last_player_to_show is None)
            else:
                self.set_rotation_to_180(no_animate=self._last_player_to_show is None)
            self._last_player_to_show = self._player_showing_to

    def set_rotation_to_0(self, no_animate: bool = False):
        """
        Sets the rotation of the scatter root to 0 degrees with a rotating animation.

        :param no_animate: If True, the rotation is set without animation.
        """
        angle = 0
        self._set_rotation(angle, no_animate)

    def set_rotation_to_180(self, no_animate: bool = False):
        """
        Sets the rotation of the scatter root to 180 degrees with a rotating animation.

        :param no_animate: If True, the rotation is set without animation.
        """
        angle = 180
        self._set_rotation(angle, no_animate)

    def _set_rotation(self, angle: float, no_animate: bool = False):
        """
        Sets the rotation of the scatter root to the specified angle with a rotating animation.

        :param angle: The angle to set the rotation to.
        :param no_animate: If True, the rotation is set without animation.
        """
        if no_animate or self._rotation_speed == 0:
            self.scatter_root.rotation = angle
        else:
            anim = Animation(rotation=angle, duration=self._rotation_speed,
                             t="out_quad")
            anim.start(self.scatter_root)

    def _update_transition_speed(self):
        self.screen_manager.transition.duration = {
            "slow": 0.4,
            "fast": 0.1
        }[SettingsConfigSingleton().config["display"]["transition_speed"].lower()]

    def _update_rotation_speed(self):
        self._rotation_speed = {
            "slow": 0.5,
            "fast": 0.1,
            "instant": 0
        }[SettingsConfigSingleton().config["display"]["rotation_speed"].lower()]
        self.scatter_root.rotation = self._rotation_speed
