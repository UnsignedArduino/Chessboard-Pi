from typing import Never

from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from chessboard import manager_enums
from chessboard.manager import ChessboardManagerSingleton


class MoreActionsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, name="more_actions_screen")

        self.claimed_draw = False

        layout = BoxLayout(orientation="vertical")
        self.status_label = Label(text="Game paused")
        layout.add_widget(self.status_label)

        self.resume_button = Button(text="Resume")
        self.resume_button.bind(on_press=self.resume_or_go_back)
        layout.add_widget(self.resume_button)

        # TODO: Implement draw offer
        self.draw_button = Button(text="Offer draw", disabled=True)
        self.draw_button.bind(on_press=self.claim_or_offer_draw)
        layout.add_widget(self.draw_button)

        self.resign_button = Button(text="Resign")
        self.resign_button.bind(on_press=self.resign)
        layout.add_widget(self.resign_button)

        # TODO: Implement save game functionality so it can be resumed later
        exit_button = Button(text="Exit without saving")
        exit_button.bind(on_press=self.exit_to_main_screen)
        layout.add_widget(exit_button)

        self.update_ui()

        self.add_widget(layout)

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
            self.status_label.text = "Game paused"
            self.resume_button.text = "Resume"
            if manager.game.can_claim_draw:
                self.draw_button.disabled = False
                self.draw_button.text = "Claim draw"
            else:
                # TODO: Implement draw offer
                self.draw_button.disabled = True
                self.draw_button.text = "Offer draw"
            self.resign_button.disabled = False
        elif manager.state == manager_enums.State.GAME_OVER:
            self.status_label.text = manager.game.outcome.value
            self.resume_button.text = "Go back to game"
            self.draw_button.disabled = True
            self.resign_button.disabled = True

    def resume_or_go_back(self, _):
        """
        Resumes or goes back to the game by going back to the game screen.
        """
        self.manager.transition.direction = "right"
        self.manager.current = "game_screen"

    def claim_or_offer_draw(self, _):
        """
        Claims or offers a draw.
        """
        manager = ChessboardManagerSingleton()
        if manager.game.can_claim_draw:
            manager.game.claim_draw()
            self.draw_button.disabled = True
        else:
            # TODO: Implement draw offer
            pass

    def resign(self, _):
        """
        The current player resigns the game.
        """
        self.manager.transition.direction = "left"
        self.manager.current = "confirm_resignation_screen"

    def exit_to_main_screen(self, _):
        """
        Exits the game and goes back to the main screen. The game is not saved.
        """
        # TODO: Implement save game functionality
        manager = ChessboardManagerSingleton()
        manager.exit()
        self.manager.transition.direction = "right"
        self.manager.current = "main_screen"
