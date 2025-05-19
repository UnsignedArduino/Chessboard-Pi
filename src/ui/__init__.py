import logging
import threading
import time

from kivy.app import App
from kivy.uix.screenmanager import ScreenManager

from chessboard.interface import ChessboardInterface
from chessboard.manager import ChessboardManager
from ui.main_screen import MainScreen
from ui.new_game_screen import NewGameScreen
from ui.new_game_screen.black_player_config_screen import BlackPlayerConfigScreen
from ui.new_game_screen.white_player_config_screen import WhitePlayerConfigScreen
from utils.logger import create_logger

logger = create_logger(name=__name__, level=logging.DEBUG)


class ChessboardApp(App):
    port: str

    interface: ChessboardInterface
    manager: ChessboardManager

    _update_thread: threading.Thread
    _stop_event: threading.Event

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def build(self):
        sm = ScreenManager()
        sm.add_widget(MainScreen())
        sm.add_widget(NewGameScreen())
        sm.add_widget(WhitePlayerConfigScreen())
        sm.add_widget(BlackPlayerConfigScreen())
        return sm

    def run_with_args(self, port: str):
        self.port = port
        super().run()

    def update_loop(self):
        while not self._stop_event.is_set():
            self.manager.update()
            time.sleep(0.1)

    def on_start(self):
        self.interface = ChessboardInterface()
        self.interface.connect(self.port)
        self.manager = ChessboardManager(self.interface)

        self._stop_event = threading.Event()
        self._update_thread = threading.Thread(target=self.update_loop, daemon=True)
        self._update_thread.start()
        logger.debug("Started update thread")

    def on_stop(self):
        self._stop_event.set()
        self._update_thread.join()
        logger.debug("Stopped update thread")

        self.interface.disconnect()
