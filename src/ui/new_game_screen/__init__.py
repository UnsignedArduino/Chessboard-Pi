from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen

from chessboard.manager_enums import PlayerType


class NewGameScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, name="new_game_screen")
        layout = BoxLayout(orientation="vertical")

        start_game_button = Button(text="Start game", disabled=True)
        layout.add_widget(start_game_button)

        self.white_player_type = PlayerType.HUMAN
        self.white_player_config_button = Button()
        self.update_white_player_config_button()
        self.white_player_config_button.bind(
            on_press=self.switch_to_white_player_config_screen)
        layout.add_widget(self.white_player_config_button)

        self.black_player_type = PlayerType.HUMAN
        self.black_player_config_button = Button()
        self.update_black_player_config_button()
        self.black_player_config_button.bind(
            on_press=self.switch_to_black_player_config_screen)
        layout.add_widget(self.black_player_config_button)

        go_back_button = Button(text="Go back")
        go_back_button.bind(on_press=self.switch_to_main_screen)
        layout.add_widget(go_back_button)

        self.add_widget(layout)

    def switch_to_main_screen(self, _):
        self.manager.transition.direction = "right"
        self.manager.current = "main_screen"

    def switch_to_white_player_config_screen(self, _):
        self.manager.transition.direction = "left"
        self.manager.current = "white_player_config_screen"

    def update_white_player_config_button(self):
        if self.white_player_type == PlayerType.HUMAN:
            self.white_player_config_button.text = "White player: human"
        else:
            self.white_player_config_button.text = "White player: engine"

    def switch_to_black_player_config_screen(self, _):
        self.manager.transition.direction = "left"
        self.manager.current = "black_player_config_screen"

    def update_black_player_config_button(self):
        if self.black_player_type == PlayerType.HUMAN:
            self.black_player_config_button.text = "Black player: human"
        else:
            self.black_player_config_button.text = "Black player: engine"
