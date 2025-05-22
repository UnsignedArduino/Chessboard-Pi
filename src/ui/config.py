import logging
from typing import Callable, Optional

from kivy.config import ConfigParser

from utils.logger import create_logger
from utils.singleton import Singleton

logger = create_logger(name=__name__, level=logging.DEBUG)


class SettingsConfigSingleton(metaclass=Singleton):
    _config: Optional[ConfigParser]
    on_reload_callbacks: list[Callable]

    def __init__(self):
        self._config = None
        self.on_reload_callbacks = []

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
            self.reload()
        return self._config

    def reload(self):
        """
        Reloads the config instance.
        """
        logger.debug("Reloading config")
        self.config.read(self.settings_path)
        for callback in self.on_reload_callbacks:
            callback()
