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
        # self.board[7][2] = Bishop(7, 2, "w", pieces)
        # self.board[7][3] = Queen(7, 3, "w", pieces)
        self.board[7][4] = King(7, 4, "w", pieces)
        # self.board[7][5] = Bishop(7, 5, "w", pieces)
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
            for column in range(self.columns):
                if self.board[row][column] != None:
                    self.board[row][column].selected = False
                    self.board[row][column].attacked = False
    
    def update_move_lists(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if self.board[row][column] != None:
                    self.board[row][column].update_valid_moves(self.board)

                    # CASTLING
                    if self.board[row][column].king and not self.board[row][column].moved and not self.king_check(self.board[row][column].color):
                        for rook_col in (0, -1):
                            rook = self.board[row][rook_col]
                            if type(rook) == Rook and not rook.moved:
                                for col in range(rook.column+1+rook_col*2, self.board[row][column].column, 1+rook_col*2):
                                    if self.board[row][col] != None:
                                        break
                                else:
                                    self.board[row][column].move_list.append((row, col-1-rook_col*2))

    def move_piece(self, pos, new_pos):
        self.board[pos[0]][pos[1]].change_pos(new_pos)
        self.board[new_pos[0]][new_pos[1]] = self.board[pos[0]][pos[1]]
        self.board[pos[0]][pos[1]] = None

        return self.board[new_pos[0]][new_pos[1]]
    
    def move_board(self, pos, new_pos):
        # CASTLING
        if self.board[pos[0]][pos[1]].king and abs(pos[1]-new_pos[1]) == 2:
            self.move_piece(pos, new_pos)

            rook_side = int(self.board[new_pos[0]][new_pos[1]].col > self.columns//2)
            self.move_piece((pos[0], rook_side*(self.columns-1)), (pos[0], new_pos[1]-1+rook_side*2))
        else:
            self.move_piece(pos, new_pos)

    def king_check(self, turn):
        king = None
        attack_move_list = []
        for row in self.board:
            for piece in row:
                if piece != None:
                    if piece.color == turn and piece.king:
                        king = piece
                    elif piece.color != turn:
                        attack_move_list += piece.attack_moves(self.board)
        
        if king.get_pos() in attack_move_list:
            king.attacked = True
            return True
        return False

    def select(self, turn, mouse_pos):
        mx = mouse_pos[0]
        my = mouse_pos[1]
        if self.board_rect.collidepoint(mx, my):
            m_row = (my - self.board_rect.y) // const.TILE_SIZE
            m_column = (mx - self.board_rect.x) // const.TILE_SIZE

            self.update_move_lists()
            if self.selected_piece == None:#if no piece is selected, then select that piece
                self.reset_selection()

                m_piece = self.board[m_row][m_column]
                if m_piece != None and m_piece.color == turn:
                    if m_piece.color == turn:
                        m_piece.selected = True
                        self.selected_piece = m_piece
            else:
                m_pos = (m_row, m_column)
                if m_pos in self.selected_piece.move_list:#if where the mouse clicked is a valid move, move the piece, reset the board and change turns
                    if self.board[m_row][m_column] == None or self.board[m_row][m_column].color != self.selected_piece.color:
                        start_pos = self.selected_piece.get_pos()
                        m_piece = self.board[m_row][m_column]

                        # CASTLING
                        if self.board[start_pos[0]][start_pos[1]].king and abs(start_pos[1]-m_column) == 2:
                            king = self.move_piece(start_pos, m_pos)

                            rook_side = int(king.column > self.columns//2)
                            rook = self.board[m_row][rook_side*(self.columns-1)]
                            self.move_piece((rook.row, rook.column), (king.row, king.column+1-rook_side*2))
                        else:
                            self.move_piece(start_pos, m_pos)

                        #RESET KING IF CHECKED
                        if self.king_check(turn):
                            self.move_piece(m_pos, start_pos)
                            self.board[m_row][m_column] = m_piece
                            return turn

                        self.selected_piece.moved = True
                        self.reset_selection()
                        if turn == "b":
                            return "w"
                        else:
                            return "b"
                elif self.board[m_row][m_column] == self.selected_piece:#reset the board if you click on the same piece
                    self.reset_selection()
                elif self.board[m_row][m_column] != None and self.board[m_row][m_column].color == self.selected_piece.color:#if you click on a different piece of your color, change the selected piece
                    self.reset_selection()
                    self.board[m_row][m_column].selected = True
                    self.selected_piece = self.board[m_row][m_column]

            if self.selected_piece != None:
                for row, column in self.selected_piece.move_list:
                    if self.board[row][column] != None and self.board[row][column].color != self.selected_piece.color:
                        self.board[row][column].attacked = True
            return turn

    def draw(self, display):
        display.blit(self.board_image, self.rect)

        offset = [self.rect.x + const.BOARD_BORDER, self.rect.y + const.BOARD_BORDER]

        if self.selected_piece != None:
            for row, column in self.selected_piece.move_list:
                if self.board[row][column] == None:
                    display.blit(self.dot_images[self.selected_piece.color], (column*const.TILE_SIZE + offset[0], row*const.TILE_SIZE + offset[1]))

        for row in range(self.rows):
            for column in range(self.columns):
                if self.board[row][column] != None:
                    if self.board[row][column] == self.selected_piece:
                        continue
                    self.board[row][column].draw(display, offset)

        if self.selected_piece != None:
            self.selected_piece.draw(display, [self.rect.x + const.BOARD_BORDER, self.rect.y + const.BOARD_BORDER])