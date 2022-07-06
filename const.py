import pygame

BOARD_IMAGE_PATH = "assets/images/board.png"
PIECES_PATH = "assets/images/pieces"

TILE_SIZE = 48
BOARD_BORDER = 9

OUTLINE_COLOR = (255, 55, 33)
LAST_MOVE_COLOR = (66, 135, 245)

IMAGE_MULTIPLIER = 3

def load_image(path):
    image = pygame.image.load(path)

    return pygame.transform.scale(image, (image.get_width()*IMAGE_MULTIPLIER, image.get_height()*IMAGE_MULTIPLIER))