from typing import Never

import chess
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

from chessboard.manager import ChessboardManagerSingleton
from utils.chessboard_helpers import get_chessboard_preview


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, name="game_screen")
        # TODO: Rotate UI for black player
        vlayout = BoxLayout(orientation="vertical")

        self.chessboard_preview = Image(fit_mode="contain", size=(240, 240),
                                        size_hint=(None, None))
        vlayout.add_widget(self.chessboard_preview)

        hlayout = BoxLayout(orientation="horizontal")
        self.confirm_move_button = Button(text="White, make a move", disabled=True)
        self.confirm_move_button.bind(on_press=self.confirm_move)
        hlayout.add_widget(self.confirm_move_button)
        vlayout.add_widget(hlayout)

        self.update_ui()
        self.add_widget(vlayout)

    def on_enter(self, *args):
        """
        Called when the screen is entered. Starts updating the UI.
        """
        super().on_enter(*args)
        Clock.schedule_interval(self.update_ui, 1 / 20)

    def on_leave(self, *args):
        """
        Called when the screen is left. Stops updating the UI.
        """
        super().on_leave(*args)
        Clock.unschedule(self.update_ui)

    def update_ui(self, _: Never = None):
        manager = ChessboardManagerSingleton()
        # Update preview
        core_img = get_chessboard_preview(manager.physical_board, 240)
        self.chessboard_preview.texture = core_img.texture
        # Check for possible move
        self.confirm_move_button.disabled = manager.possible_move is None
        player_to_move = "White" if manager.physical_board.turn == chess.WHITE else "Black"
        if manager.possible_move is not None:
            san_move = manager.physical_board.san(manager.possible_move)
            if manager.possible_move.promotion is not None:
                san_move = san_move.split("=")[0] + "=..."
            self.confirm_move_button.text = f"{player_to_move}, confirm move {san_move}"
        else:
            self.confirm_move_button.text = f"{player_to_move}, make a move"

    def confirm_move(self, _):
        """
        Called when the confirm move button is pressed. Confirms the possible move.
        """
        manager = ChessboardManagerSingleton()
        if manager.possible_move is not None:
            if manager.possible_move.promotion is not None:
                self.manager.transition.direction = "left"
                self.manager.current = "white_promoting_to_screen" if manager.physical_board.turn == chess.WHITE else "black_promoting_to_screen"
            else:
                manager.confirm_possible_move()

    def pause_and_exit_to_main_screen(self, _):
        manager = ChessboardManagerSingleton()
        manager.pause_and_exit()
        self.manager.transition.direction = "right"
        self.manager.current = "main_screen"
