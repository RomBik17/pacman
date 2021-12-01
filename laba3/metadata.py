"""
This file is intended for constants
 in game as size of window,
 colors of ghost or player and etc.
"""
ROWS = 31
COLS = 28
PADDING = 50
# Screen constants
WIDTH, HEIGHT = COLS * 20 + PADDING, ROWS * 20 + PADDING
FPS = 60

MAZE_WIDTH, MAZE_HEIGHT = WIDTH - PADDING, HEIGHT - PADDING



# Colour constants
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREY = (187, 187, 187)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Font constants
START_TEXT_SIZE = 36
START_FONT = 'Impact'

# Game states
MENU = 1
GAMING = 2
GAME_OVER = 3
WINNER = 4


# Player constants
PACMAN_COLOUR = YELLOW
PACMAN_LIVES = 3
DESTINATION = (29, 29)

# Enemy constants
RANDOM = 1
DEFAULT = 2

# Map constants
WALL = 1
COIN = 2
PACMAN = 223
ENEMY = 333
DEFAULT_GHOST = 222
RANDOM_GHOST = 221
BLOCKED = 1
PASSAGE = 0
COINS_AMOUNT = 10


MINMAX = 1
EXPECT = 2
