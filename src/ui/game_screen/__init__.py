from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.screenmanager import Screen

from chessboard.manager import ChessboardManagerSingleton
from utils.chessboard_helpers import get_chessboard_preview


class GameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, name="game_screen")
        vlayout = BoxLayout(orientation="vertical")

        self.chessboard_preview = Image(fit_mode="contain", size=(240, 240),
                                        size_hint=(None, None))
        self.update_preview()
        vlayout.add_widget(self.chessboard_preview)

        hlayout = BoxLayout(orientation="horizontal")
        pause_and_exit_button = Button(text="Pause and exit")
        pause_and_exit_button.bind(on_press=self.pause_and_switch_to_main_screen)
        hlayout.add_widget(pause_and_exit_button)
        vlayout.add_widget(hlayout)

        self.add_widget(vlayout)

    def update_preview(self):
        manager = ChessboardManagerSingleton()
        core_img = get_chessboard_preview(manager.board, 240)
        self.chessboard_preview.texture = core_img.texture

    def pause_and_switch_to_main_screen(self, _):
        manager = ChessboardManagerSingleton()
        manager.pause_and_exit()
        self.manager.transition.direction = "right"
        self.manager.current = "main_screen"
