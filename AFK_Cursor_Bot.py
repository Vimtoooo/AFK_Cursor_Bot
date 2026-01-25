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
        self._start_time: float = 0
        self._elapsed_time: float = 0

        self._threads: list[threading.Thread] = []
        self._is_active: bool = False
        self._hotkey: str = "esc"

    def activate_bot(self):
        
        if self._is_active:
            raise BotAlreadyActivatedError("The bot has already been activated!")
        
        self._is_active = True

        thread: threading.Thread = threading.Thread(target=self._run_bot_logic)
        self._threads.append(thread)
        thread.start()
        self._start_time = time.perf_counter()


    def deactivate_bot(self):
        
        if not self._is_active:
            raise BotAlreadyDeactivatedError("The bot has already been deactivated!")
        
        self._is_active = False
        print("The bot has been terminated")

        end_time: float = time.perf_counter()
        self._elapsed_time = round(end_time - self._start_time, 3)
        print(f"Bot elapsed time: {self._elapsed_time: ,.} seconds")

        try:
            for t in self._threads:
                t.join()

        except RuntimeError:
            raise ThreadNotStartedError("The thread was not currently being executed for the bot to terminate")
        
        finally:
            self._threads.clear()
            self._start_time = 0
            self._elapsed_time = 0

    def set_movement_area(self, x: int, y: int, width: int, height: int):
        pass

    def perform_random_click(self):
        pass

    def add_hotkey_listener(self, key: str = "esc"):

        if self._hotkey == key.lower() and self._hotkey is not None:
            raise HotkeyAlreadyDefinedError(f"The '{key}' keybind has already been defined as a hotkey!")
        
        self._hotkey = key

        k.add_hotkey(self._hotkey, self.deactivate_bot)

    def _run_bot_logic(self):
            
        while self._is_active:
            random_x: int = r.randint(0, self._x_axis)
            random_y: int = r.randint(0, self._y_axis)

            pag.moveTo(random_x, random_y, duration=self._duration)

    def __str__(self) -> str:
        current_status: str = "Running" if self._is_active else "Inactive"
        if self._is_active:
            end_time_temporary: float = time.perf_counter()
            current_elapsed_time: float = round(end_time_temporary - self._start_time, 3)
            return f"Current Status: {self._is_active}"
        return f""