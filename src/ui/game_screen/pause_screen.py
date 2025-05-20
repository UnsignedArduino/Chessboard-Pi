from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from chessboard.manager import ChessboardManagerSingleton


class PauseScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, name="pause_screen")
        layout = BoxLayout(orientation="vertical")
        layout.add_widget(Label(text="Game paused"))

        resume_button = Button(text="Resume")
        resume_button.bind(on_press=self.resume)
        layout.add_widget(resume_button)

        # TODO: Implement save game functionality so it can be resumed later
        exit_button = Button(text="Exit without saving")
        exit_button.bind(on_press=self.exit_to_main_screen)
        layout.add_widget(exit_button)

        self.add_widget(layout)

    def resume(self, _):
        """
        Resumes the game by going back to the game screen.
        """
        self.manager.transition.direction = "right"
        self.manager.current = "game_screen"

    def exit_to_main_screen(self, _):
        """
        Exits the game and goes back to the main screen. The game is not saved.
        """
        manager = ChessboardManagerSingleton()
        manager.exit()
        self.manager.transition.direction = "right"
        self.manager.current = "main_screen"
