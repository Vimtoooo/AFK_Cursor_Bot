# The AFK Cursor Bot

## Overview:

Ever needed a self-functioning AFK cursor bot to actively dislocate your cursor from time to time, without having to worry about getting kicked out of an online session, or even preventing your computer from going to sleep mode? Well, this project will cover all of these requirements just for the user!

## Breakdown of the Project:

We will go through the various methods, libraries and illustrate what each process of the program will do to achieve every criteria.

> [!NOTE]
> This is a still "working on" project, so not everything has been implemented yet or correctly.

### Libraries Used:

- `pyautogui`: The primary library which will handle the logical thinking of moving the cursor, bringing the bot to live.
- `threading`: Solves any blocking loop issues that are executed by the main bot's logic in a separate thread, from not only keeping your main program responsive to having control to terminate the bot or call various methods, making the experience more dynamic.
- `random`: Picks the randomly generated number to be one of the required coordinates (for the x-axis and the y-axis).
- `time`: Provides a short cool-down, giving the ability to prevent the active spam of constant cursor dislocation, but also keeping track of how long the bot has been running for.

#### Methods:

* `__init__(self)`: The constructor provides instance attributes, whether the user would like to alter the default coordinates, the speed of the cursor, and optionally, the time of cool-down. Later on, property methods (setter, getter and deleter) will be made.
* `activate_bot(self)`: Activates the bot, executing a **while-loop**.
* `deactivate_bot(self)`: Deactivates the bot, breaking the **while-loop**.
* `set_movement_area(self, x, y, width, height)`: Deposits the coordinates of movement areas for the bot itself.
* `auto_set_movement_area(self)`: Automatically sets the coordinates of movement for you, based on the size of your screen.
* `perform_random_click(self)`: Executes a right-click, just for fun `:)` (later, there will be a feature to specify which button to press).
* `__str__(self)`: A string dunder method that returns the status of the current bot.
* `add_hotkey_listener(self, key="esc")`: A simple but advanced feature which uses the library `keyboard` to listen for global hotkeys like the **"esc"**, to instantly deactivate the bot, regardless of what you're doing (can be used as an emergency button!).