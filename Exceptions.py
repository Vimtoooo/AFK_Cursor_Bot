class BotAlreadyActivatedError(Exception):
    def __init__(self, error: str):
        super().__init__(error)

class BotAlreadyDeactivatedError(Exception):
    def __init__(self, error: str):
        super().__init__(error)

class ThreadNotStartedError(Exception):
    def __init__(self, error: str):
        super().__init__(error)

class HotkeyAlreadyDefinedError(Exception):
    def __init__(self, error: str):
        super().__init__(error)