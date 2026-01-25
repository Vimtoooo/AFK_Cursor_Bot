import pyautogui as pag
import threading
import keyboard as k
import random as r
import time

from Exceptions import BotAlreadyActivatedError, BotAlreadyDeactivatedError, ThreadNotStartedError, HotkeyNotDefinedError

class Cursor_Bot:

    def __init__(self):
        self.__x_axis: int = 1000
        self.__y_axis: int = 1000
        self.__width: int = 500
        self.__height: int = 500
        self.__duration: int | float = 3
        self.__start_time: float = 0
        self.__elapsed_time: float = 0

        self.__threads: list[threading.Thread] = []
        self.__is_active: bool = False
        self.__hotkey: str = "esc"
        k.add_hotkey(self.__hotkey, self.deactivate_bot)

    def activate_bot(self):
        
        if self.__is_active:
            raise BotAlreadyActivatedError("The bot has already been activated!")
        
        self.__is_active = True

        thread: threading.Thread = threading.Thread(target=self.__run_bot_logic)
        self.__threads.append(thread)
        thread.start()
        self.__start_time = time.perf_counter()


    def deactivate_bot(self):
        
        if not self.__is_active:
            raise BotAlreadyDeactivatedError("The bot has already been deactivated!")
        
        self.__is_active = False
        print("The bot has been terminated")

        end_time: float = time.perf_counter()
        self.__elapsed_time = round(end_time - self.__start_time, 3)
        print(f"Bot elapsed time: {self.__elapsed_time} seconds")

        try:
            for t in self.__threads:
                t.join()

        except RuntimeError:
            raise ThreadNotStartedError("The thread was not currently being executed for the bot to terminate")
        
        finally:
            self.__threads.clear()
            self.__start_time = 0
            self.__elapsed_time = 0

    def set_movement_area(self, x: int, y: int, width: int, height: int):
        pass

    def perform_random_click(self):
        pass

    def add_hotkey_listener(self, key: str):

        if self.__hotkey is None or key is None:
            raise HotkeyNotDefinedError(f"The '{key}' hotkey has not been defined!")
        
        self.__hotkey = key.lower()

        k.add_hotkey(self.__hotkey, self.deactivate_bot)

    def __run_bot_logic(self):
            
        while self.__is_active:
            random_x: int = r.randint(0, self.__x_axis)
            random_y: int = r.randint(0, self.__y_axis)

            pag.moveTo(random_x, random_y, duration=self.__duration)

    def __str__(self) -> str:
        current_status: str = "Running" if self.__is_active else "Inactive"
        if self.__is_active:
            end_time_temporary: float = time.perf_counter()
            _current_elapsed_time: float = round(end_time_temporary - self.__start_time, 3)
            return f"Current Status: {self.__is_active}"
        return f""