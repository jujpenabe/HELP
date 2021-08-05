import enum

class State(enum.Enum):
    MENU = 0
    FADE_IN = 1
    PLAY = 2
    FADE_OUT = 3
    QUIT = 4