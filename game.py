import pygame
from board import Board
from network import Network
import const, os

pygame.display.set_caption("Chess Game")
WIDTH, HEIGHT = 750, 500
screen = pygame.display.set_mode((WIDTH, HEIGHT))
display = pygame.Surface((WIDTH, HEIGHT))

clock = pygame.time.Clock()

def load_images(path):#Loads multi depth directory of images into a dictionary
    images = {}

    for (dirpath, dirnames, filenames) in os.walk(path):
        current_dir = images
        if dirpath != path:
            for dir in dirpath.split(path)[1].split("/")[1:]:
                current_dir = current_dir[dir]

        for dirname in dirnames:
            current_dir[dirname] = {}
        
        for filename in filenames:
            if filename.split(".")[1] == "png":
                current_dir[filename.split(".")[0]] = const.load_image(dirpath+"/"+filename).convert_alpha()
    
    return images

images = load_images(const.IMAGE_PATH)

def word_color(color):
    return "WHITE" if color == "w" else "BLACK"

def send_board(n, data):
    board = n.send(data)

    board.center_board(WIDTH/2, HEIGHT/2)

    return board


def redrawGameWindow(board, color):
    display.fill((255, 255, 255))

    board.draw(display, images, color)

    surf = pygame.transform.scale(display, (WIDTH, HEIGHT))
    surf_rect = surf.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(surf, surf_rect)

    pygame.display.update()

def main():
    running = True

    n = Network()

    board, color = n.connect()
    
    # board = Board(0, 0)
    # color = "w"

    print('You are', word_color(color))

    board.center_board(WIDTH/2, HEIGHT/2)
    offset = [board.board_rect.x, board.board_rect.y]

    mouse_pos = [0, 0]
    while running:
        clock.tick(const.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN and color == board.turn:
                mouse_pos = pygame.mouse.get_pos()

                mouse_pos = [mouse_pos[0]-offset[0], mouse_pos[1]-offset[1]]

                board = send_board(n, ["select", mouse_pos])
                print(board)

                if (result := n.send(["checkmate"])):
                    redrawGameWindow(board, color)
                    if result == "s":
                        print(word_color(color), "stalemate.")
                    elif result == "d":
                        print("DRAW")
                    else:
                        print(word_color(result), "has won!")
                    pygame.time.delay(2000)
                    running = False
    
        if color != board.turn:
            board = send_board(n, "board")

        redrawGameWindow(board, color)
    pygame.quit()

if __name__ == "__main__":
    main()