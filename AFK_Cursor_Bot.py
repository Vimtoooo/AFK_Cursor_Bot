import pyautogui as pag
import threading
import keyboard as k
import random as r
import time

from Exceptions import BotAlreadyActivatedError, BotAlreadyDeactivatedError, ThreadNotStartedError, HotkeyNotDefinedError, InvalidDataTypeError, ParametersOutOfBoundsError, InvalidArgumentsError

class CursorBot:

    def __init__(self):
        self.__screen_width, self.__screen_height = pag.size()
        self.__x: int = 0
        self.__y: int = 0
        self.__width: int = self.__screen_width
        self.__height: int = self.__screen_height
        self.__size: str = "max"
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

    def set_movement_area(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0) -> bool:
        self.__validate_coordinates(x, y, width, height)
        
        if x:
            self.__x = x

        if y:
            self.__y = y

        if width:
            self.__width = width
        
        if height:
            self.__height = height

        print("Coordinates and dimensions have been updated successfully!")
        return True

    def auto_set_movement_area(self, size: str = "medium"):
        formatted_size: str = self.__validate_size(size)
        total_width, total_height = self.__screen_width, self.__screen_height
        
        consumed_width: int = 0
        consumed_height: int = 0

        if formatted_size == "small": # Consumes 20% of available width and height
            consumed_width = total_width // 5
            consumed_height = total_height // 5

        if formatted_size == "medium": # Consumes 50% of available width and height
            consumed_width = total_width // 2
            consumed_height = total_height // 2
        
        if formatted_size == "large": # Consumes 80% of available width and height
            consumed_width = int(total_width * 0.8)
            consumed_height = int(total_height * 0.8)
        
        if formatted_size == "max": # Consumes 100% of available width and height
            consumed_width = total_width
            consumed_height = total_height
        
        if formatted_size == "custom": # Consumes a random portion of area, where the minimum must be at 10 pixels
            consumed_width = r.randint(10, total_width)
            consumed_height = r.randint(10, total_height)

        self.__width = consumed_width
        self.__height = consumed_height

        # Center the movement area
        self.__x = (total_width - self.__width) // 2
        self.__y = (total_height - self.__height) // 2
        
        print(f"Movement area set to '{formatted_size}' and centered.")

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

    def __validate_size(self, size: str) -> str:
        
        if not isinstance(size, str):
            raise InvalidDataTypeError(f"Invalid data type for 'size': {type(size)}")
        
        size = size.lower()
        
        if size not in ("small", "medium", "large", "max", "custom"):
            raise InvalidArgumentsError(f"Invalid arguments for 'size': {size}")
        
        return size

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