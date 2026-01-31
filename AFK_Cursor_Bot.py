import pyautogui as pag
import threading
import keyboard as k
import random as r
import time

from Exceptions import BotAlreadyActivatedError, BotAlreadyDeactivatedError, ThreadNotStartedError, HotkeyNotDefinedError, InvalidDataTypeError, ParametersOutOfBoundsError

class CursorBot:

    def __init__(self):
        self.__screen_width, self.__screen_height = pag.size()
        self.__x: int = 0
        self.__y: int = 0
        self.__width: int = self.__screen_width
        self.__height: int = self.__screen_height
        self.__size: str = "medium"
        self.__duration: int | float = 3
        self.__start_time: float = 0
        self.__elapsed_time: float = 0
        self.__overall_elapsed_time: float = 0

        self.__threads: list[threading.Thread] = []
        self.__is_active: bool = False
        self.__hotkey: str | None = None

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
            for thread in self.__threads:
                thread.join()

        except RuntimeError:
            raise ThreadNotStartedError("The thread was not currently being executed for the bot to terminate")
        
        finally:
            self.__overall_elapsed_time += self.__elapsed_time
            self.__start_time = 0
            self.__elapsed_time = 0
            self.__threads.clear()

    def set_movement_area(self, x: int, y: int, width: int, height: int):
        self.__validate_coordinates(x, y, width, height)
        
        self.__x = x
        self.__y = y
        self.__width = width
        self.__height = height

    def auto_set_movement_area(self, size: str = "medium"):
        pass

    def perform_random_click(self):
        pass

    def add_hotkey_listener(self, key: str):

        if key is None:
            raise HotkeyNotDefinedError(f"The '{key}' hotkey has not been defined as None!")
        
        self.__hotkey = key.lower()

        k.add_hotkey(self.__hotkey, self.deactivate_bot, timeout=1000)

    def __run_bot_logic(self):
            
        while self.__is_active:
            # Calculate max coordinates, ensuring they don't exceed screen boundaries
            # We subtract 1 because coordinates are 0-indexed (e.g., 0 to 1919 for 1920 width)
            max_x = min(self.__x + self.__width, self.__screen_width - 1)
            max_y = min(self.__y + self.__height, self.__screen_height - 1)

            random_x: int = r.randint(self.__x, max_x)
            random_y: int = r.randint(self.__y, max_y)

            pag.moveTo(random_x, random_y, duration=self.__duration)

    def __validate_coordinates(self, x: int, y: int, width: int, height: int) -> bool:
        
        if not isinstance(x, int):
            raise InvalidDataTypeError(f"Invalid data type for 'x': {type(x)}")
        
        if not isinstance(y, int):
            raise InvalidDataTypeError(f"Invalid data type for 'y': {type(y)}")
        
        if not isinstance(width, int):
            raise InvalidDataTypeError(f"Invalid data type for 'width': {type(width)}")
        
        if not isinstance(height, int):
            raise InvalidDataTypeError(f"Invalid data type for 'height': {type(height)}")
        
        if width < 0 or height < 0:
            raise ParametersOutOfBoundsError(f"Width and height must be non-negative integers:\nWidth -> {width}\nHeight -> {height}")
        
        return True

    def __str__(self) -> str:
        current_status: str = "Running" if self.__is_active else "Inactive"
        
        if self.__is_active:
            end_time_temporary: float = time.perf_counter()
            current_elapsed_time: float = round(end_time_temporary - self.__start_time, 3)
            
            return f"Current Status: {current_status}\n\n\
                    Current elapsed Time: {current_elapsed_time} seconds\n\
                    Overall elapsed Time: {self.__overall_elapsed_time} seconds"
        
        return f"Current Status: {current_status}\n\n\
                Overall elapsed Time: {self.__overall_elapsed_time} seconds"