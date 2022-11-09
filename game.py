import pygame
from board import Board
from network import Network
import const, os, sys

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

def redrawGameWindow(board, color):
    display.fill((255, 255, 255))

    board.draw(display, images, color)

    surf = pygame.transform.scale(display, (WIDTH, HEIGHT))
    surf_rect = surf.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(surf, surf_rect)

    pygame.display.update()

def main():
    n = Network()

    board, color = n.connect()
    
    # board = Board(0, 0)
    # color = "w"
    # board.ready = True

    print('You are', word_color(color))

    board.center_board(WIDTH/2, HEIGHT/2)
    offset = [board.board_rect.x, board.board_rect.y]

    def send(n, data):
        global running

        try:
            data = n.send(data)

            if type(data) == Board:
                data.center_board(WIDTH/2, HEIGHT/2)

            return data
        except EOFError:
            print('Game over! Opponent has disconnected.')
            pygame.quit()
            sys.exit(0)

    def check_game_over(board):
        # if (result := board.checkmate()):
        if (result := send(n, "checkmate")):
            redrawGameWindow(board, color)
            if result == "s":
                print(word_color(color), "stalemate.")
            elif result == "d":
                print("DRAW")
            else:
                print(word_color(result), "has won!")
            pygame.time.delay(2000)
            pygame.quit()

    running = True
    while running:
        clock.tick(const.FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL:
                    running = False

            if event.type == pygame.MOUSEBUTTONDOWN and board.ready and color == board.turn:
                mouse_pos = pygame.mouse.get_pos()
                # board.select(mouse_pos)
                # color = board.turn

                mouse_pos = [mouse_pos[0]-offset[0], mouse_pos[1]-offset[1]]
                board = send(n, ["select", mouse_pos])

                check_game_over(board)
    
        if not board.ready or color != board.turn:
            result = n.wait()
            
            if result == "start":
                board = send(n, "board")

            elif result == "ready":
                board = send(n, "board")

                if board.ready:
                    check_game_over(board)

        redrawGameWindow(board, color)
    send(n, "quit")
    pygame.quit()

if __name__ == "__main__":
    main()