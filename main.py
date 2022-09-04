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
        pieces[color][filename.split(".")[0]] = const.load_image(file_path).convert_alpha()
        # pieces[color][filename.split(".")[0]].set_colorkey((0, 0, 0))

def redrawGameWindow(board):
    display.fill((255, 255, 255))

    board.draw(display)

    surf = pygame.transform.scale(display, (WIDTH, HEIGHT))
    surf_rect = surf.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(surf, surf_rect)

    pygame.display.update()

def main():
    running = True

    board = Board(0, 0)
    board.center_board(WIDTH/2, HEIGHT/2)
    turn = "w"

    board.update_pieces(pieces)

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
                # for row in board.board:
                #     print(row)
                # print("\n\n\n")
                if (result := board.checkmate()):
                    print(result)
                    redrawGameWindow(board)
                    if result == "s":
                        print("WHITE" if turn == "w" else "BLACK", "stalemate.")
                    elif result == "d":
                        print("DRAW")
                    else:
                        print("WHITE" if result == "w" else "BLACK", "has won!")
                    pygame.time.delay(2000)
                    running = False

        redrawGameWindow(board)
    pygame.quit()

main()