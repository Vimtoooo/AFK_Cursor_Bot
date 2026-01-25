
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
    def terminate_via_method_call():
        bot2: CursorBot = CursorBot()
        bot2.add_hotkey_listener("esc")
        bot2.activate_bot()
        time.sleep(5) # Sleeps for 5 seconds...
        bot2.deactivate_bot()

    @staticmethod
    def stopwatch_tracking():
        bot3: CursorBot = CursorBot()
        bot3.add_hotkey_listener("esc")
        bot3.activate_bot()
        time.sleep(3)
        bot3.deactivate_bot()
        print(bot3)

    @staticmethod
    def afk_testing():
        pass

    @staticmethod
    def testing_custom_hotkey():
        pass

if __name__ == "__main__":
    Test_Cases.terminate_via_hotkey()