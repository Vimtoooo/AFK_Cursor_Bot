
# BUG: Test and identify bugs within the Cursor Bot!

from AFK_Cursor_Bot import Cursor_Bot

class Test_Cases:

    @staticmethod
    def test_case1():
        bot1: Cursor_Bot = Cursor_Bot()
        bot1.add_hotkey_listener("esc")
        bot1.activate_bot()

    @staticmethod
    def test_case2():
        pass

    @staticmethod
    def test_case3():
        pass

if __name__ == "__main__":
    Test_Cases.test_case1()