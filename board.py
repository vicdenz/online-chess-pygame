import const
from piece import *
import pygame

class Board:
    def __init__(self, x, y, pieces):
        self.board_image = const.load_image(const.BOARD_IMAGE_PATH).convert()
        self.rect = self.board_image.get_rect(x=x, y=y)
        self.board_rect = pygame.Rect(self.rect.x+const.BOARD_BORDER, self.rect.x+const.BOARD_BORDER, self.rect.width-const.BOARD_BORDER*2, self.rect.height-const.BOARD_BORDER*2)

        self.dot_images = {"b": pieces['b']['dot'], "w": pieces['w']['dot']}

        self.rows = 8
        self.columns = 8
        self.board = [[None for x in range(self.columns)] for y in range(self.rows)]

        self.board[0][0] = Rook(0, 0, "b", pieces)
        self.board[0][1] = Knight(0, 1, "b", pieces)
        self.board[0][2] = Bishop(0, 2, "b", pieces)
        self.board[0][3] = Queen(0, 3, "b", pieces)
        self.board[0][4] = King(0, 4, "b", pieces)
        self.board[0][5] = Bishop(0, 5, "b", pieces)
        self.board[0][6] = Knight(0, 6, "b", pieces)
        self.board[0][7] = Rook(0, 7, "b", pieces)

        self.board[1][0] = Pawn(1, 0, "b", pieces)
        self.board[1][1] = Pawn(1, 1, "b", pieces)
        self.board[1][2] = Pawn(1, 2, "b", pieces)
        self.board[1][3] = Pawn(1, 3, "b", pieces)
        self.board[1][4] = Pawn(1, 4, "b", pieces)
        self.board[1][5] = Pawn(1, 5, "b", pieces)
        self.board[1][6] = Pawn(1, 6, "b", pieces)
        self.board[1][7] = Pawn(1, 7, "b", pieces)

        self.board[7][0] = Rook(7, 0, "w", pieces)
        self.board[7][1] = Knight(7, 1, "w", pieces)
        self.board[7][2] = Bishop(7, 2, "w", pieces)
        self.board[7][3] = Queen(7, 3, "w", pieces)
        self.board[7][4] = King(7, 4, "w", pieces)
        self.board[7][5] = Bishop(7, 5, "w", pieces)
        self.board[7][6] = Knight(7, 6, "w", pieces)
        self.board[7][7] = Rook(7, 7, "w", pieces)

        self.board[6][0] = Pawn(6, 0, "w", pieces)
        self.board[6][1] = Pawn(6, 1, "w", pieces)
        self.board[6][2] = Pawn(6, 2, "w", pieces)
        self.board[6][3] = Pawn(6, 3, "w", pieces)
        self.board[6][4] = Pawn(6, 4, "w", pieces)
        self.board[6][5] = Pawn(6, 5, "w", pieces)
        self.board[6][6] = Pawn(6, 6, "w", pieces)
        self.board[6][7] = Pawn(6, 7, "w", pieces)

        self.selected_piece = None

    def center_board(self, centerx, centery):
        self.rect.center = (centerx, centery)
        self.board_rect.center = (centerx, centery)

    def reset_selection(self):
        self.selected_piece = None

        for row in range(self.rows):
            for col in range(self.columns):
                if self.board[row][col] != None:
                    self.board[row][col].selected = False

    def check_selection(self, turn, mouse_pos):
        self.reset_selection()

        mx = mouse_pos[0]
        my = mouse_pos[1]
        if (self.board_rect.collidepoint(mx, my)):
            m_row = (my - self.board_rect.y) // const.TILE_SIZE
            m_column = (mx - self.board_rect.x) // const.TILE_SIZE

            m_piece = self.board[m_row][m_column]
            if m_piece != None and m_piece.color == turn:
                if m_piece.color == turn:
                    m_piece.selected = True
                    self.selected_piece = m_piece
    
    def move_piece(self, turn, mouse_pos):
        pass

    def draw(self, display):
        display.blit(self.board_image, self.rect)

        offset = [self.rect.x + const.BOARD_BORDER, self.rect.y + const.BOARD_BORDER]
        for row in range(self.rows):
            for col in range(self.columns):
                if self.board[row][col] != None:
                    if (self.board[row][col] == self.selected_piece):
                        continue
                    self.board[row][col].draw(display, offset)
        if (self.selected_piece != None):
            self.selected_piece.draw(display, [self.rect.x + const.BOARD_BORDER, self.rect.y + const.BOARD_BORDER])

            print(self.selected_piece.valid_moves(self.board))
            for row, col in self.selected_piece.valid_moves(self.board):
                display.blit(self.dot_images[self.selected_piece.color], (row*const.TILE_SIZE + offset[0], col*const.TILE_SIZE + offset[1]))