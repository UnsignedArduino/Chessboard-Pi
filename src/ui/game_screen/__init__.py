from typing import Never

import chess
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from chessboard import manager_enums
from chessboard.manager import ChessboardManagerSingleton
from utils.chessboard_helpers import get_chessboard_preview


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, name="game_screen")
        self.last_state = None

        # TODO: Rotate UI for black player
        self.vlayout = BoxLayout(orientation="vertical")

        self.chessboard_preview = Image(fit_mode="contain", size=(240, 240),
                                        size_hint=(None, None))
        self.vlayout.add_widget(self.chessboard_preview)

        self.confirm_move_button = Button(text="White, make a move", disabled=True)
        self.confirm_move_button.bind(on_press=self.confirm_move)

        self.outcome_label = Label(text="Game ended")
        # update_ui will add or remove the confirm move button and outcome label

        self.more_actions_button = Button(text="More actions")
        self.more_actions_button.bind(on_press=self.open_more_menu)
        # update_ui will readd more_actions_button

        self.update_ui()
        self.add_widget(self.vlayout)

    def on_pre_enter(self, *args):
        """
        Called when the screen is entered. Starts updating the UI.
        """
        super().on_pre_enter(*args)
        Clock.schedule_interval(self.update_ui, 1 / 20)

    def on_pre_leave(self, *args):
        """
        Called when the screen is left. Stops updating the UI.
        """
        super().on_pre_leave(*args)
        Clock.unschedule(self.update_ui)

    def update_ui(self, _: Never = None):
        manager = ChessboardManagerSingleton()
        if manager.state == manager_enums.State.GAME_IN_PROGRESS:
            # Game just started
            if self.last_state != manager.state:
                self.vlayout.add_widget(self.confirm_move_button)
                self.vlayout.remove_widget(self.outcome_label)
                # Readd to keep the button under the confirm move button
                self.vlayout.remove_widget(self.more_actions_button)
                self.vlayout.add_widget(self.more_actions_button)
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
        elif manager.state == manager_enums.State.GAME_OVER:
            # Game just ended
            if self.last_state != manager.state:
                self.vlayout.remove_widget(self.confirm_move_button)
                self.vlayout.add_widget(self.outcome_label)
                # Readd to keep the button under the outcome label
                self.vlayout.remove_widget(self.more_actions_button)
                self.vlayout.add_widget(self.more_actions_button)
            self.confirm_move_button.disabled = True
            self.outcome_label.text = manager.outcome_as_text
        self.last_state = manager.state
        # Update preview
        core_img = get_chessboard_preview(manager.physical_board, 240)
        self.chessboard_preview.texture = core_img.texture

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

    def open_more_menu(self, _):
        # TODO: Actually pause the game by calling the manager
        self.manager.transition.direction = "left"
        self.manager.current = "more_actions_screen"
