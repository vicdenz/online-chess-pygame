import pygame
from board import Board
import const, os

pygame.display.set_caption("Chess Game")
WIDTH, HEIGHT = 750, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
display = pygame.Surface((WIDTH, HEIGHT))

clock = pygame.time.Clock()

pieces = {}
for color in os.listdir(const.PIECES_PATH):
    color_dir = const.PIECES_PATH+"/"+color

    pieces[color] = {}
    for filename in os.listdir(color_dir):
        file_path = color_dir+"/"+filename
        pieces[color][filename.split(".")[0]] = const.load_image(file_path).convert()
        pieces[color][filename.split(".")[0]].set_colorkey((0, 0, 0))

board = Board(0, 0, pieces)
board.center_board(WIDTH/2, HEIGHT/2)
turn = "w"

def redrawGameWindow():
    display.fill((255, 255, 255))

    board.draw(display)

    # surf = pygame.transform.scale(display, (WIDTH*const.IMAGE_MULTIPLIER, HEIGHT*const.IMAGE_MULTIPLIER))
    # surf_rect = surf.get_rect(center=(WIDTH/2, HEIGHT/2))
    # screen.blit(surf, surf_rect)
    screen.blit(display, (0, 0))
    pygame.display.update()

running = True
while running:
    clock.tick(const.FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LCTRL:
                running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            turn = board.select(turn, mouse_pos)
            if (result := board.checkmate()):
                print(result)
                redrawGameWindow()
                if result == "s":
                    print("WHITE" if turn == "w" else "BLACK", "stalemate.")
                else:
                    print("WHITE" if result == "w" else "BLACK", "has won!")
                pygame.time.delay(2000)
                running = False

    redrawGameWindow()
pygame.quit()