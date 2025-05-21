import chess
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from chessboard.manager import ChessboardManagerSingleton


class ConfirmOfferDrawScreen(Screen):
    def __init__(self):
        super().__init__(name="confirm_offer_draw_screen")
        layout = BoxLayout(orientation="vertical")
        self.title_label = Label(text="Offer draw?")
        layout.add_widget(self.title_label)

        yes_button = Button(text="Yes, offer draw")
        yes_button.bind(on_press=self.confirm_offer_draw)
        layout.add_widget(yes_button)

        no_button = Button(text="No, go back")
        no_button.bind(on_press=self.cancel_offer_draw)
        layout.add_widget(no_button)

        self.add_widget(layout)

    def on_pre_enter(self, *args):
        super().on_pre_enter(*args)
        manager = ChessboardManagerSingleton()
        self.title_label.text = f"{'White' if manager.game.board.turn == chess.WHITE else 'Black'}, offer draw?"

    def confirm_offer_draw(self, _):
        manager = ChessboardManagerSingleton()
        manager.game.offer_draw()
        self.manager.transition.direction = "right"
        self.manager.current = "game_screen"

    def cancel_offer_draw(self, _):
        self.manager.transition.direction = "right"
        self.manager.current = "more_actions_screen"
