
# BUG: Test and identify bugs within the Cursor Bot!

from AFK_Cursor_Bot import CursorBot
import time

class Test_Cases:

    @staticmethod
    def terminate_via_hotkey():
        bot1: CursorBot = CursorBot()
        bot1.add_hotkey_listener("esc")
        bot1.activate_bot()
        # User presses the desired hotkey at any time...

    @staticmethod
    def terminate_via_method_call() -> bool:
        bot2: CursorBot = CursorBot()
        bot2.add_hotkey_listener("esc")
        bot2.activate_bot()
        time.sleep(5) # Sleeps for 5 seconds...
        bot2.deactivate_bot()
        return True

    @staticmethod
    def stopwatch_tracking() -> bool:
        bot3: CursorBot = CursorBot()
        bot3.add_hotkey_listener("esc")
        bot3.activate_bot()
        time.sleep(3)
        bot3.deactivate_bot()
        print(bot3)
        return True
    
    @staticmethod
    def auto_setting_movement_area() -> bool:
        bot4: CursorBot = CursorBot()
        bot4.add_hotkey_listener("esc")
        bot4.auto_set_movement_area("custom")
        bot4.activate_bot()
        time.sleep(5)
        bot4.deactivate_bot()
        return True

    @staticmethod
    def afk_testing() -> bool:
        return True

    @staticmethod
    def testing_custom_hotkey() -> bool:
        return True

if __name__ == "__main__":
    Test_Cases.auto_setting_movement_area()