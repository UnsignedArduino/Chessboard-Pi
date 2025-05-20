from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from chessboard import manager_enums
from chessboard.manager import ChessboardManagerSingleton


class WhitePromotingToScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, name="white_promoting_to_screen")
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(Label(text="White pawn is promoting to..."))

        for piece in (manager_enums.PromotionPiece.QUEEN,
                      manager_enums.PromotionPiece.ROOK,
                      manager_enums.PromotionPiece.BISHOP,
                      manager_enums.PromotionPiece.KNIGHT):
            button = Button(text=f"A {piece.name.lower()}")
            button.bind(on_press=self.promote_to_piece)
            layout.add_widget(button)

        self.add_widget(layout)

    def promote_to_piece(self, button):
        piece = button.text.split(" ")[1].upper()
        manager = ChessboardManagerSingleton()
        pieces = {
            "QUEEN": manager_enums.PromotionPiece.QUEEN,
            "ROOK": manager_enums.PromotionPiece.ROOK,
            "BISHOP": manager_enums.PromotionPiece.BISHOP,
            "KNIGHT": manager_enums.PromotionPiece.KNIGHT
        }
        manager.confirm_possible_move(promoteTo=pieces[piece])
        self.manager.transition.direction = "right"
        self.manager.current = "game_screen"
