from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen

from chessboard.manager_enums import PlayerType


class BlackPlayerConfigScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs,
                         name="black_player_config_screen")
        layout = BoxLayout(orientation="vertical")

        layout.add_widget(
            Label(text="Black pieces player will be..."))

        set_as_human_button = Button(text="...a human")
        set_as_human_button.bind(
            on_press=self.set_as_human_and_switch_to_new_game_screen)
        layout.add_widget(set_as_human_button)

        # Not implemented yet.
        set_as_engine_button = Button(text="...an engine", disabled=True)
        set_as_engine_button.bind(
            on_press=self.set_as_engine_and_switch_to_new_game_screen)
        layout.add_widget(set_as_engine_button)

        go_back_button = Button(text="Go back")
        go_back_button.bind(on_press=self.switch_to_new_game_screen)
        layout.add_widget(go_back_button)

        self.add_widget(layout)

    def set_as_human_and_switch_to_new_game_screen(self, _):
        new_game_screen = self.manager.get_screen("new_game_screen")
        new_game_screen.black_player_type = PlayerType.HUMAN
        new_game_screen.update_black_player_config_button()
        self.switch_to_new_game_screen(_)

    def set_as_engine_and_switch_to_new_game_screen(self, _):
        new_game_screen = self.manager.get_screen("new_game_screen")
        new_game_screen.black_player_type = PlayerType.ENGINE
        new_game_screen.update_black_player_config_button()
        self.switch_to_new_game_screen(_)

    def switch_to_new_game_screen(self, _):
        self.manager.transition.direction = "right"
        self.manager.current = "new_game_screen"
