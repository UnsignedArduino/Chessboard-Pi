from typing import Never

import chess
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

from chessboard import manager_enums
from chessboard.manager import ChessboardManagerSingleton
from utils.chessboard_helpers import get_chessboard_preview


class GameScreen(Screen):
    last_state: manager_enums.State

    def __init__(self, **kwargs):
        super().__init__(**kwargs, name="game_screen")
        self.last_state = manager_enums.State.IDLE
        # TODO: Rotate UI for black player
        vlayout = BoxLayout(orientation="vertical")

        self.chessboard_preview = Image(fit_mode="contain", size=(240, 240),
                                        size_hint=(None, None))
        vlayout.add_widget(self.chessboard_preview)

        self.confirm_move_button = Button(text="White, make a move", disabled=True)
        self.confirm_move_button.bind(on_press=self.confirm_move)
        vlayout.add_widget(self.confirm_move_button)

        self.hlayout = BoxLayout(orientation="horizontal")
        vlayout.add_widget(self.hlayout)

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
        if manager.state == manager_enums.State.GAME_IN_PROGRESS:
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

            if self.last_state != manager.state:
                self.hlayout.clear_widgets()
                # TODO: Implement draw offer
                draw_button = Button(text="Offer draw", disabled=True)

                self.hlayout.add_widget(draw_button)
                # TODO: Implement resign
                resign_button = Button(text="Resign", disabled=True)

                self.hlayout.add_widget(resign_button)
                pause_button = Button(text="Pause")
                pause_button.bind(on_press=self.pause)
                self.hlayout.add_widget(pause_button)
        elif manager.state == manager_enums.State.GAME_OVER:
            self.confirm_move_button.disabled = True
            outcome = manager.outcome
            text = "Game ended"
            if outcome.termination == chess.Termination.CHECKMATE:
                text = f"{'White' if outcome.winner == chess.WHITE else 'Black'} wins by checkmate"
            elif outcome.termination == chess.Termination.STALEMATE:
                text = "Stalemate"
            elif outcome.termination == chess.Termination.INSUFFICIENT_MATERIAL:
                text = "Insufficient material"
            elif outcome.termination == chess.Termination.SEVENTYFIVE_MOVES:
                text = "Forced 75 move rule draw"
            elif outcome.termination == chess.Termination.FIVEFOLD_REPETITION:
                text = "Forced 5-fold repetition draw"
            elif outcome.termination == chess.Termination.FIFTY_MOVES:
                text = "Claimed 50 move rule draw"
            elif outcome.termination == chess.Termination.THREEFOLD_REPETITION:
                text = "Claimed 3-fold repetition draw"
            self.confirm_move_button.text = text

            if self.last_state != manager.state:
                self.hlayout.clear_widgets()
                exit_button = Button(text="Exit")
                exit_button.bind(on_press=self.exit_to_main_screen)
                self.hlayout.add_widget(exit_button)

        self.last_state = manager.state

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

    def offer_draw(self, _):
        """
        Called when the offer draw button is pressed. Offers a draw.
        """
        pass

    def resign(self, _):
        """
        Called when the resign button is pressed. Resigns the game.
        """
        pass

    def pause(self, _):
        # TODO: Actually pause the game by calling the manager
        self.manager.transition.direction = "left"
        self.manager.current = "pause_screen"

    def exit_to_main_screen(self, _):
        """
        Exits the game and goes back to the main screen. The game is not saved.
        """
        manager = ChessboardManagerSingleton()
        manager.exit()
        self.manager.transition.direction = "right"
        self.manager.current = "main_screen"
