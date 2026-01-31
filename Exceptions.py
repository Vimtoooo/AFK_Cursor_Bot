class BotAlreadyActivatedError(Exception):
    def __init__(self, error: str):
        super().__init__(error)

class BotAlreadyDeactivatedError(Exception):
    def __init__(self, error: str):
        super().__init__(error)

class ThreadNotStartedError(Exception):
    def __init__(self, error: str):
        super().__init__(error)

class HotkeyNotDefinedError(Exception):
    def __init__(self, error: str):
        super().__init__(error)

class InvalidDataTypeError(Exception):
    def __init__(self, error: str):
        super().__init__(error)

class ParametersOutOfBoundsError(Exception):
    def __init__(self, error: str):
        super().__init__(error)

class InvalidArgumentsError(Exception):
    def __init__(self, error: str):
        super().__init__(error)