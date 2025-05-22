import chess
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from chessboard.manager import ChessboardManagerSingleton


class ConfirmResignationScreen(Screen):
    def __init__(self):
        super().__init__(name="confirm_resignation_screen")
        layout = BoxLayout(orientation="vertical")
        self.title_label = Label(text="Resign?")
        layout.add_widget(self.title_label)

        yes_button = Button(text="Yes, resign")
        yes_button.bind(on_press=self.confirm_resignation)
        layout.add_widget(yes_button)

        no_button = Button(text="No, go back")
        no_button.bind(on_press=self.cancel_resignation)
        layout.add_widget(no_button)

        self.add_widget(layout)

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        manager = ChessboardManagerSingleton()
        self.title_label.text = f"{'White' if manager.game.board.turn == chess.WHITE else 'Black'}, resign?"

    def confirm_resignation(self, _):
        manager = ChessboardManagerSingleton()
        manager.game.resign()
        self.manager.transition.direction = "right"
        self.manager.current = "game_screen"

    def cancel_resignation(self, _):
        self.manager.transition.direction = "right"
        self.manager.current = "more_actions_screen"
