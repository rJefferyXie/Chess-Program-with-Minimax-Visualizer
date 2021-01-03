import pygame

# The width and height of the window
width, height = 720, 640

# An 8 x 8 board is the standard size for chess
num_rows, num_cols = 8, 8

# The size of each square on the board
square_size = 640 // 8 - 20

# Possible themes for the chess board
blue_theme = (204, 229, 255), (153, 204, 255)
red_theme = (255, 153, 153), (255, 204, 204)
purple_theme = (229, 204, 255), (204, 153, 255)
themes = [blue_theme, purple_theme, red_theme]

# Used for promotion menu
light_gray = (230, 230, 230)

# The background images
blue_image = pygame.transform.scale(pygame.image.load("game/themes/blue_theme.png"), (square_size, square_size))
purple_image = pygame.transform.scale(pygame.image.load("game/themes/purple_theme.png"), (square_size, square_size))
red_image = pygame.transform.scale(pygame.image.load("game/themes/red_theme.png"), (square_size, square_size))
images = [blue_image, purple_image, red_image]
