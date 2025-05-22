from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import Screen


class MainScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, name="main_screen")
        layout = BoxLayout(orientation="vertical")

        new_game_button = Button(text="New game")
        new_game_button.bind(on_press=self.switch_to_new_game_screen)
        layout.add_widget(new_game_button)

        # TODO: Implement resume game functionality
        resume_game_button = Button(text="Resume game", disabled=True)
        resume_game_button.bind(on_press=self.switch_to_resume_game_screen)
        layout.add_widget(resume_game_button)

        # TODO: Implement completed games functionality
        completed_games_button = Button(text="View completed games", disabled=True)
        completed_games_button.bind(on_press=self.switch_to_completed_games_screen)
        layout.add_widget(completed_games_button)

        settings_button = Button(text="Settings")
        settings_button.bind(on_press=self.open_settings_screen)
        layout.add_widget(settings_button)

        self.add_widget(layout)

    def switch_to_new_game_screen(self, _):
        self.manager.transition.direction = "left"
        self.manager.current = "new_game_screen"

    def switch_to_resume_game_screen(self, _):
        # TODO: Implement resume game functionality
        pass

    def switch_to_completed_games_screen(self, _):
        # TODO: Implement view completed games functionality
        pass

    def open_settings_screen(self, _):
        self.manager.transition.direction = "left"
        self.manager.current = "settings_screen"
