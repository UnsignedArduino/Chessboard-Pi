from typing import Optional

from kivy.config import ConfigParser

from utils.singleton import Singleton


class SettingsConfigSingleton(metaclass=Singleton):
    _config: Optional[ConfigParser]

    def __init__(self):
        self._config = None

    @property
    def settings_path(self) -> str:
        """
        Returns the path to the settings file.

        :return: The path to the settings file.
        """
        return "settings.ini"

    @property
    def config(self) -> ConfigParser:
        """
        Returns the current config instance.

        :return: The current config instance.
        """
        if self._config is None:
            self._config = ConfigParser()
            self._config.read(self.settings_path)
        return self._config
