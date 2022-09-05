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

def redrawGameWindow(board):
    display.fill((255, 255, 255))

    board.draw(display, images)

    surf = pygame.transform.scale(display, (WIDTH, HEIGHT))
    surf_rect = surf.get_rect(center=(WIDTH/2, HEIGHT/2))
    screen.blit(surf, surf_rect)

    pygame.display.update()

def main():
    running = True

    n = Network()

    board = n.get_board()
    color = n.get_color()

    board.center_board(WIDTH/2, HEIGHT/2)

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

                n.send(["select", mouse_pos])

                if (result := n.send(["checkmate"])):
                    redrawGameWindow(board)
                    if result == "s":
                        print("WHITE" if color == "w" else "BLACK", "stalemate.")
                    elif result == "d":
                        print("DRAW")
                    else:
                        print("WHITE" if result == "w" else "BLACK", "has won!")
                    pygame.time.delay(2000)
                    running = False

        redrawGameWindow(board)
    pygame.quit()

if __name__ == "__main__":
    main()