import pyautogui as pag
import threading
import keyboard as k
import random as r
import time

from Exceptions import BotAlreadyActivatedError, BotAlreadyDeactivatedError, ThreadNotStartedError, HotkeyAlreadyDefinedError

class Cursor_Bot:

    def __init__(self):
        self._x_axis: int = 1000
        self._y_axis: int = 1000
        self._width: int = 500
        self._height: int = 500
        self._duration: int | float = 3
        
        self._threads: list = []
        self._is_active: bool = False
        self._hotkey: str = "esc"

    def activate_bot(self):
        
        if self._is_active:
            raise BotAlreadyActivatedError("The bot has already been activated!")
        
        self._is_active = True

        t: threading.Thread = threading.Thread(target=self._run_bot_logic)
        self._threads.append(t)
        t.start()

    def deactivate_bot(self):
        
        if not self._is_active:
            raise BotAlreadyDeactivatedError("The bot has already been deactivated!")
        
        try:
            t: threading.Thread = self._threads.pop()
            t.join()

        except RuntimeError:
            raise ThreadNotStartedError("The thread was not currently being executed for the bot to terminate")
        
        finally:
            self._is_active = False

    def set_movement_area(self, x: int, y: int, width: int, height: int):
        pass

    def perform_random_click(self):
        pass

    def add_hotkey_listener(self, key: str = "esc"):

        if self._hotkey == key.lower():
            raise HotkeyAlreadyDefinedError(f"The '{key}' keybind has already been defined as a hotkey!")
        
        self._hotkey = key

        k.add_hotkey(self._hotkey, self.deactivate_bot)

    def _run_bot_logic(self):
            
        while self._is_active:
            random_x: int = r.randint(0, self._x_axis)
            random_y: int = r.randint(0, self._y_axis)

            pag.moveTo(random_x, random_y, duration=self._duration)

    def __str__(self) -> str:
        return f"Current Status: {self._is_active}"