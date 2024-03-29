import pygame

PORT = 4000

IMAGE_PATH = "assets/images"

FPS = 24

TILE_SIZE = 48
BOARD_SIZE = 134
BOARD_BORDER = 9

OUTLINE_COLOR = (240, 224, 48)
WARNING_COLOR = (255, 55, 33)
LAST_MOVE_COLOR = (66, 135, 245)

IMAGE_MULTIPLIER = 3

def invert_color(color):
    return "b" if color == "w" else "w"

def load_image(path):
    image = pygame.image.load(path)

    return pygame.transform.scale(image, (image.get_width()*IMAGE_MULTIPLIER, image.get_height()*IMAGE_MULTIPLIER))