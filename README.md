# The AFK Cursor Bot

## Overview:

Ever needed a self-functioning AFK cursor bot to actively dislocate your cursor from time to time, without having to worry about getting kicked out of an online session, or even preventing your computer from going to sleep mode? Well, this project will cover all of these requirements just for the user!

## Breakdown of the Project:

We will go through the various methods, libraries and illustrate what each process of the program will do to achieve every criteria.

### Libraries Used:

- `pyautogui`: The primary library which will handle the logical thinking of moving the cursor, bringing the bot to live.
- `random`: Picks the randomly generated number to be one of the required coordinates (for the x-axis and the y-axis).
- `time`: Provides a short cool-down, giving the ability to prevent the active spam of constant cursor dislocation.

#### Methods:

* `__init__(self)`: The constructor provides instance attributes, whether the user would like to alter the default coordinates, the speed of the cursor, and optionally, the time of cool-down. Later on, property methods (setter, getter and deleter) will be made.
* `activate_bot(self)`: Activates the bot, executing a **while-loop**.
* `deactivate_bot(self)`: Deactivates the bot, breaking the **while-loop**.