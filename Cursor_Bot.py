import pyautogui as pag
import threading
import keyboard as k
import random as r
import time
from textwrap import dedent

from Exceptions import *

class CursorBot:

    def __init__(self):
        self.__screen_width, self.__screen_height = pag.size() # IDEA: It is discouraged to change the screen measurements!
        self.__x: int = 0
        self.__y: int = 0
        self.__width: int = self.__screen_width
        self.__height: int = self.__screen_height
        self.__size: str = "max"
        self.__duration: int | float = 3
        self.__start_time: float = 0
        self.__elapsed_time: float = 0
        self.__click_start_time: float = 0
        self.__click_elapsed_time: float = 0
        self.__click_overall_elapsed_time: float = 0
        self.__overall_elapsed_time: float = 0

        self.__threads: list[threading.Thread] = []
        self.__is_active: bool = False
        self.__is_clicking: bool = False
        self.__hotkey: str | None = None
        self.__failsafe = pag.FAILSAFE # By default, it is set to false

    ''' Public Methods '''

    def activate_bot(self, perform_random_click: bool = False) -> bool:
        
        if self.__is_active:
            raise BotAlreadyActivatedError("The bot has already been activated!")
        
        self.__is_active = True

        thread: threading.Thread = threading.Thread(target=self.__run_bot_logic, name="CursorMover")
        self.__threads.append(thread)
        thread.start()

        if perform_random_click:
            self.perform_random_click()

        self.__start_time = time.perf_counter()
        return True

    def deactivate_bot(self):
        
        if not self.__is_active and not self.__is_clicking:
            raise BotAlreadyDeactivatedError("The bot has already been deactivated!")
        
        end_time: float = time.perf_counter()

        if self.__is_active:
            self.__elapsed_time = round(end_time - self.__start_time, 3)
            self.__overall_elapsed_time += self.__elapsed_time
            print(f"Bot movement elapsed time: {self.__elapsed_time} seconds")

        if self.__is_clicking:
            self.__click_elapsed_time = round(end_time - self.__click_start_time, 3)
            self.__click_overall_elapsed_time += self.__click_elapsed_time
            print(f"Clicking elapsed time: {self.__click_elapsed_time} seconds")

        self.__is_active = False
        self.__is_clicking = False
        print("The bot has been terminated")

        try:
            for thread in self.__threads:
                thread.join()

        except RuntimeError:
            raise ThreadNotStartedError("The thread was not currently being executed for the bot to terminate")
        
        except KeyboardInterrupt:
            print("Autonomous clicking stopped")
        
        finally:
            self.__start_time = 0
            self.__click_start_time = 0
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
        
        self.__size = "custom"
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
        
        print(f"Movement area set to '{formatted_size}' and centered")

    def perform_random_click(self, click_duration: float | int | None = None, click_timeout: float | int | None = None) -> bool:
        if self.__is_clicking:
            raise ClickingAlreadyActiveError("Clicking is already active")
        
        self.__validate_click(click_duration, click_timeout)

        if not self.__is_active:
            self.__is_active = True
        self.__is_clicking = True
        
        clicker_thread = threading.Thread(target=self.__run_clicking_logic, args=(click_duration, click_timeout,), name="Clicker")
        self.__threads.append(clicker_thread)
        clicker_thread.start()
        print("Autonomous clicking activated")
        self.__click_start_time = time.perf_counter()
        return True

    def add_hotkey_listener(self, key: str) -> bool:

        if key is None:
            raise HotkeyNotDefinedError(f"The '{key}' hotkey has not been defined as None!")
        
        self.__hotkey = key.lower()

        k.add_hotkey(self.__hotkey, self.deactivate_bot, timeout=1000)
        return True
    
    def reset_settings(self) -> None:
        self.__init__()

    ''' Private/Helper Methods '''

    def __run_bot_logic(self) -> None:
        try:
            while self.__is_active:
                # Calculate max coordinates, ensuring they don't exceed screen boundaries
                # We subtract 1 because coordinates are 0-indexed (e.g., 0 to 1919 for 1920 width)
                max_x = min(self.__x + self.__width, self.__screen_width - 1)
                max_y = min(self.__y + self.__height, self.__screen_height - 1)

                random_x: int = r.randint(self.__x, max_x)
                random_y: int = r.randint(self.__y, max_y)

                pag.moveTo(random_x, random_y, duration=self.__duration)

        except FailSafeException:
            print("Failsafe triggered. Program stopped safely.")

        finally:
            self.deactivate_bot()

    def __run_clicking_logic(self, click_duration: float | int | None = None, click_timeout: float | int | None = None) -> None:
        if click_timeout is None:
            click_timeout = r.randint(1, 5)
        
        try:
            while self.__is_clicking:
                if click_duration is not None:
                    current_time = time.perf_counter()
                    
                    if round(current_time - self.__click_start_time, 3) >= click_duration:
                        self.__is_clicking = False
                        break

                pag.click()
                time.sleep(click_timeout)

        except Exception as e:
            print(f"An error occurred in the clicking thread: {e}")

        finally:
            self.__is_clicking = False

    def __validate_coordinates(self, x: int = 0, y: int = 0, width: int = 0, height: int = 0) -> bool:
        
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

        if x < 0 or y < 0:
            raise ParametersOutOfBoundsError(f"'X' and 'Y' axis must be non-negative integers:\nX -> {x}\nYt -> {y}")
        
        return True

    def __validate_size(self, size: str) -> str:
        
        if not isinstance(size, str):
            raise InvalidDataTypeError(f"Invalid data type for 'size': {type(size)}")
        
        size = size.lower()
        
        if size not in ("small", "medium", "large", "max", "custom"):
            raise InvalidArgumentsError(f"Invalid arguments for 'size': {size}")
        
        return size
    
    def __validate_click(self, click_duration: float | int | None, click_timeout: float | int | None) -> bool:

        if not isinstance(click_duration, (int, float)) and click_duration is not None:
            raise InvalidDataTypeError(f"Invalid data type for 'click_duration': {type(click_duration)}")
        
        if not isinstance(click_timeout, (int, float)) and click_timeout is not None:
            raise InvalidDataTypeError(f"Invalid data type for 'click_timeout': {type(click_timeout)}")
        
        if click_duration is not None and click_duration < 0:
            raise InvalidArgumentsError(f"The 'click_duration' cannot be a negative number")
        
        if click_timeout is not None and click_timeout < 0:
            raise InvalidArgumentsError(f"The 'click-timeout' cannot be a negative number")
        
        return True

    ''' Dunder Methods '''

    def __str__(self) -> str:
        current_status: str = "Running" if self.__is_active else "Inactive"
        clicking_status: str = "Running" if self.__is_clicking else "Inactive"

        if self.__is_active:
            current_elapsed_time = round(time.perf_counter() - self.__start_time, 3)
        else:
            current_elapsed_time = self.__elapsed_time

        if self.__is_clicking:
            current_elapsed_time_clicking = round(time.perf_counter() - self.__click_start_time, 3)
        else:
            current_elapsed_time_clicking = self.__click_elapsed_time

        return dedent(f"""\
            Current Status: {current_status}
            Clicking Status: {clicking_status}

            Movement elapsed time: {current_elapsed_time} seconds
            Clicking elapsed time: {current_elapsed_time_clicking} seconds
            Total movement time: {round(self.__overall_elapsed_time, 3)} seconds
            Total clicking time: {round(self.__click_overall_elapsed_time, 3)} seconds

            Active Threads: {len(self.__threads)}
            Bot Set Duration: {self.__duration} seconds

            configurations:
            Hotkey: {self.__hotkey}
            Size Set: {self.__size}

            Movement Area:
            X: {self.__x} pixels
            Y: {self.__y} pixels
            Width: {self.__width} pixels
            Height: {self.__height} pixels
        """).strip()


    ''' Property Methods '''

    @property
    def screen_width(self) -> int:
        return self.__screen_width

    @screen_width.setter
    def screen_width(self, value) -> None:
        raise IllegalModificationError("The 'screen_width' attribute is immutable.")
    
    @property
    def screen_height(self) -> int:
        return self.__screen_height

    @screen_height.setter
    def screen_height(self, value) -> None:
        raise IllegalModificationError("The 'screen_height' attribute is immutable.")
    
    @property
    def x(self) -> int:
        return self.__x
    
    @x.setter
    def x(self, value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise InvalidDataTypeError(f"X must be a non-negative integer. Got: {value}")
        
        self.__x = value

    @x.deleter
    def x(self) -> None:
        self.__x = 0
    
    @property
    def y(self) -> int:
        return self.__y
    
    @y.setter
    def y(self, value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise InvalidDataTypeError(f"Y must be a non-negative integer. Got: {value}")
        
        self.__y = value

    @y.deleter
    def y(self) -> None:
        self.__y = 0
    
    @property
    def width(self) -> int:
        return self.__width
    
    @width.setter
    def width(self, value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise InvalidDataTypeError(f"Width must be a non-negative integer. Got: {value}")
        
        self.__width = value

    @width.deleter
    def width(self) -> None:
        self.__width = self.__screen_width
    
    @property
    def height(self) -> int:
        return self.__height
    
    @height.setter
    def height(self, value: int) -> None:
        if not isinstance(value, int) or value < 0:
            raise InvalidDataTypeError(f"Height must be a non-negative integer. Got: {value}")
        
        self.__height = value

    @height.deleter
    def height(self) -> None:
        self.__height = self.__screen_height
    
    @property
    def size(self) -> str:
        return self.__size
    
    @size.setter
    def size(self, value: str) -> None:
        self.__size = self.__validate_size(value)

    @size.deleter
    def size(self) -> None:
        self.__size = "max"
    
    @property
    def duration(self) -> int | float:
        return self.__duration
    
    @duration.setter
    def duration(self, value: int | float) -> None:
        if not isinstance(value, (int, float)) or value <= 0:
            raise InvalidDataTypeError(f"Duration must be a positive number. Got: {value}")
        
        self.__duration = value

    @duration.deleter
    def duration(self) -> None:
        self.__duration = 3
    
    @property
    def start_time(self) -> float:
        return self.__start_time

    @start_time.setter
    def start_time(self, value) -> None:
        raise IllegalModificationError("The 'start_time' attribute is managed internally and cannot be modified.")

    @property
    def elapsed_time(self) -> float:
        return self.__elapsed_time
    
    @elapsed_time.setter
    def elapsed_time(self, value) -> None:
        raise IllegalModificationError("The 'elapsed_time' attribute is managed internally and cannot be modified.")
    
    @property
    def overall_elapsed_time(self) -> float:
        return self.__overall_elapsed_time
    
    @overall_elapsed_time.setter
    def overall_elapsed_time(self, value) -> None:
        raise IllegalModificationError("The 'overall_elapsed_time' attribute is managed internally and cannot be modified.")
    
    @property
    def threads(self) -> list[threading.Thread]:
        return self.__threads
    
    @property
    def is_active(self) -> bool:
        return self.__is_active
    
    @property
    def hotkey(self) -> str | None:
        return self.__hotkey

    @hotkey.setter
    def hotkey(self, value) -> None:
        raise IllegalModificationError("Please use the 'add_hotkey_listener' method to change the hotkey.")
    
    @property
    def failsafe(self) -> bool:
        return self.__failsafe
    
    @failsafe.setter
    def failsafe(self, value: bool) -> None:
        if not isinstance(value, bool):
            raise IllegalModificationError(f"Failsafe must be a boolean type. Got {value}")

        self.__failsafe = value
        pag.FAILSAFE = value
    
    @failsafe.deleter
    def failsafe(self) -> None:
        self.__failsafe = True