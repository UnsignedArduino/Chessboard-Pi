from kivy.uix.screenmanager import Screen
from kivy.uix.settings import InterfaceWithSpinner, Settings

from ui.config import SettingsConfigSingleton


class SettingsScreen(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs, name="settings_screen")
        conf = SettingsConfigSingleton().config
        s = Settings(interface_cls=InterfaceWithSpinner)
        s.on_close = self.on_close
        s.add_json_panel("Display", conf, data="""
[
  {
    "type": "options",
    "title": "Transition speed",
    "desc": "Choose how fast the screen transitions.",
    "section": "display",
    "key": "transition_speed",
    "options": [
      "Slow",
      "Fast"
    ]
  },
  {
    "type": "options",
    "title": "Rotation speed",
    "desc": "Choose how fast the screen rotates. Select None for no rotation.",
    "section": "display",
    "key": "rotation_speed",
    "options": [
      "None",
      "Slow",
      "Fast",
      "Instant"
    ]
  }
]
        """)
        self.add_widget(s)

    def on_close(self, *args):
        """
        Called when the settings screen is closed.
        """
        super().on_pre_leave(*args)
        SettingsConfigSingleton().reload()
        self.manager.transition.direction = "right"
        self.manager.current = "main_screen"
