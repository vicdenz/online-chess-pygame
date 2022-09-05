import const
from piece import *
import pygame

class Board:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, const.BOARD_SIZE, const.BOARD_SIZE)
        self.board_rect = pygame.Rect(self.rect.x+const.BOARD_BORDER, self.rect.x+const.BOARD_BORDER, self.rect.width-const.BOARD_BORDER*2, self.rect.height-const.BOARD_BORDER*2)

        self.turn = "w"

        self.rows = 8
        self.columns = 8
        self.board = [[None for x in range(self.columns)] for y in range(self.rows)]

        self.board[0][0] = Rook(0, 0, "b")
        self.board[0][1] = Knight(0, 1, "b")
        self.board[0][2] = Bishop(0, 2, "b")
        self.board[0][3] = Queen(0, 3, "b")
        self.board[0][4] = King(0, 4, "b")
        self.board[0][5] = Bishop(0, 5, "b")
        self.board[0][6] = Knight(0, 6, "b")
        self.board[0][7] = Rook(0, 7, "b")

        self.board[1][0] = Pawn(1, 0, "b")
        self.board[1][1] = Pawn(1, 1, "b")
        self.board[1][2] = Pawn(1, 2, "b")
        self.board[1][3] = Pawn(1, 3, "b")
        self.board[1][4] = Pawn(1, 4, "b")
        self.board[1][5] = Pawn(1, 5, "b")
        self.board[1][6] = Pawn(1, 6, "b")
        self.board[1][7] = Pawn(1, 7, "b")

        self.board[7][0] = Rook(7, 0, "w")
        self.board[7][1] = Knight(7, 1, "w")
        self.board[7][2] = Bishop(7, 2, "w")
        self.board[7][3] = Queen(7, 3, "w")
        self.board[7][4] = King(7, 4, "w")
        self.board[7][5] = Bishop(7, 5, "w")
        self.board[7][6] = Knight(7, 6, "w")
        self.board[7][7] = Rook(7, 7, "w")

        self.board[6][0] = Pawn(6, 0, "w")
        self.board[6][1] = Pawn(6, 1, "w")
        self.board[6][2] = Pawn(6, 2, "w")
        self.board[6][3] = Pawn(6, 3, "w")
        self.board[6][4] = Pawn(6, 4, "w")
        self.board[6][5] = Pawn(6, 5, "w")
        self.board[6][6] = Pawn(6, 6, "w")
        self.board[6][7] = Pawn(6, 7, "w")

        # Stalemate DEBUG
        # self.board[0][0] = King(0, 0, "w")
        # self.board[0][1] = Queen(0, 1, "w")
        # self.board[0][7] = Rook(0, 7, "w")
        # self.board[6][0] = Rook(6, 0, "w")
        # self.board[1][5] = Rook(1, 5, "b")
        # self.board[2][7] = Pawn(2, 7, "b")
        # self.board[7][7] = King(7, 7, "b")

        # EN PASSANT DEBUG
        # self.board[2][2] = Pawn(2, 2, "b")
        # self.board[2][3] = Pawn(2, 3, "b")
        # self.board[2][4] = Pawn(2, 4, "b")
        # self.board[5][2] = Pawn(5, 2, "w")
        # self.board[5][3] = Pawn(5, 3, "w")
        # self.board[5][4] = Pawn(5, 4, "w")

        self.selected_piece = None

        self.attack_move_list = {"b":set(), "w":set()}
        self.last_moved_piece = []

    def center_board(self, centerx, centery):
        self.rect.center = (centerx, centery)
        self.board_rect.center = (centerx, centery)
    
    def invert_color(self, color):
        return "b" if color == "w" else "w"

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

                    # EN PASSANT
                    if self.last_moved_piece != []:
                        moved_pawn = self.board[self.last_moved_piece[1][0]][self.last_moved_piece[1][1]]
                        if moved_pawn != None and moved_pawn.pawn:
                            if abs(self.last_moved_piece[0][0]-self.last_moved_piece[1][0]) == 2:
                                for side in range(self.last_moved_piece[1][1]-1, self.last_moved_piece[1][1]+2, 2):
                                    side_pawn = self.board[self.last_moved_piece[1][0]][side]

                                    if side_pawn != None and side_pawn.pawn:
                                        side_pawn.move_list.append((self.last_moved_piece[1][0]-1+2*int(moved_pawn.color == "w"), self.last_moved_piece[1][1]))

    def update_attack_move_lists(self):
        self.attack_move_list = {"b":set(), "w":set()}
        for row in self.board:
            for piece in row:
                if piece != None:
                    for move in piece.attack_moves(self.board):
                        self.attack_move_list[piece.color].add(move)

    def move_piece(self, pos, new_pos):
        self.board[pos[0]][pos[1]].change_pos(new_pos)
        self.board[new_pos[0]][new_pos[1]] = self.board[pos[0]][pos[1]]
        self.board[pos[0]][pos[1]] = None

        return self.board[new_pos[0]][new_pos[1]]

    def king_check(self, turn):
        self.update_attack_move_lists()

        king = None
        for row in self.board:
            for piece in row:
                if piece != None:
                    if piece.color == turn and piece.king:
                        king = piece

        if king.get_pos() in self.attack_move_list[self.invert_color(king.color)]:
            king.attacked = True
            return True
        return False

    # Returns which color WON, "s" if it's a stalemate, or "d" if it's a draw.
    def checkmate(self):
        self.update_move_lists()
        self.update_attack_move_lists()

        kings = []
        pieces = {"b":[], "w":[]}
        for row in self.board:
            for piece in row:
                if piece != None:
                    if piece.king:
                        kings.append(piece)
                    else:
                        pieces[piece.color].append(piece)
        
        # check if all of the moves of the king are blocked and the king is in the attack move list.
        for king in kings:
            enemy_color = self.invert_color(king.color)
            checkmate = False

            if set(king.move_list).issubset(self.attack_move_list[enemy_color]):
                if king.get_pos() in self.attack_move_list[enemy_color]:
                    checkmate = True
                else:#check if all of the remaining pieces have no moves left and the king is not in check. Returns stalemate if so.
                    for piece in pieces[king.color]:
                        if len(piece.move_list) != 0:
                            break
                    else:
                        return "s"
            
            #Check all piece if they have repeated more than 3 times
            for row in self.board:
                for piece in row:
                    if piece:
                        if piece.repetitions >= 3:
                            return "d"

            if checkmate:
                king.attacked = True
                return enemy_color

    def select(self, mouse_pos):
        mx = mouse_pos[0]
        my = mouse_pos[1]
        if self.board_rect.collidepoint(mx, my):
            m_row = (my - self.board_rect.y) // const.TILE_SIZE
            m_column = (mx - self.board_rect.x) // const.TILE_SIZE

            self.update_move_lists()
            if self.selected_piece == None:#if no piece is selected, then select that piece
                self.reset_selection()

                m_piece = self.board[m_row][m_column]
                if m_piece != None and m_piece.color == self.turn:
                    if m_piece.color == self.turn:
                        m_piece.selected = True
                        self.selected_piece = m_piece
            else:
                m_pos = (m_row, m_column)
                if m_pos in self.selected_piece.move_list:#if where the mouse clicked is a valid move, move the piece, reset the board and change turns
                    if self.board[m_row][m_column] == None or self.board[m_row][m_column].color != self.selected_piece.color:
                        start_pos = self.selected_piece.get_pos()
                        m_piece = self.board[m_row][m_column]

                        # CASTLING
                        castling = False
                        en_passant = None
                        if self.selected_piece.king and abs(start_pos[1]-m_column) == 2:
                            castling = True
                            king = self.move_piece(start_pos, m_pos)

                            rook_side = int(king.column > self.columns//2)
                            rook = self.board[m_row][rook_side*(self.columns-1)]
                            self.move_piece(rook.get_pos(), (king.row, king.column+1-rook_side*2))
                        # EN PASSANT
                        elif self.selected_piece.pawn and start_pos[1] != m_column and self.board[m_row][m_column] == None:
                            self.move_piece(start_pos, m_pos)

                            en_passent = self.board[m_row-(m_row-start_pos[0])][m_column]
                            self.board[m_row-(m_row-start_pos[0])][m_column] = None
                        else:
                            self.move_piece(start_pos, m_pos)

                        #RESET KING IF CHECKED
                        self.update_move_lists()
                        if self.king_check(self.turn):
                            start_pos, m_pos = m_pos, start_pos
                            if castling:
                                rook_side = int(king.column > self.columns//2)
                                rook = self.board[king.row][king.column+1-rook_side*2]
                                king = self.move_piece(start_pos, m_pos)

                                self.move_piece(rook.get_pos(), (rook.row, rook_side*(self.columns-1)))
                            elif en_passant:
                                self.move_piece(start_pos, m_pos)

                                self.board[m_row-(m_row-start_pos[0])][m_column] = en_passent                     
                            else:
                                self.move_piece(start_pos, m_pos)
                                self.board[start_pos[0]][start_pos[1]] = m_piece
                            
                            return self.turn

                        self.selected_piece.moved = True
                        
                        if self.selected_piece.get_pos() == self.selected_piece.last_pos:
                            self.selected_piece.repetitions += 1
                        else:
                            self.selected_piece.repetitions = 0
                        self.selected_piece.last_pos = start_pos
                        self.reset_selection()

                        self.last_moved_piece = [start_pos, m_pos]

                        self.turn = self.invert_color(self.turn)
                        return self.turn

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
        return self.turn

    def draw(self, display, images):
        display.blit(images['board'], self.rect)

        offset = [self.rect.x + const.BOARD_BORDER, self.rect.y + const.BOARD_BORDER]

        if self.selected_piece == None:
            for pos in self.last_moved_piece:
                pygame.draw.rect(display, const.LAST_MOVE_COLOR, (pos[1]*const.TILE_SIZE + offset[0], pos[0]*const.TILE_SIZE + offset[1], const.TILE_SIZE, const.TILE_SIZE))

        if self.selected_piece != None:
            for row, column in self.selected_piece.move_list:
                if self.board[row][column] == None:
                    display.blit(images['pieces'][self.selected_piece.color]['dot'], (column*const.TILE_SIZE + offset[0], row*const.TILE_SIZE + offset[1]))

        for row in range(self.rows):
            for column in range(self.columns):
                if self.board[row][column] != None:
                    if self.board[row][column] == self.selected_piece:
                        continue
                    self.board[row][column].draw(display, images, offset)

        if self.selected_piece != None:
            self.selected_piece.draw(display, images, [self.rect.x + const.BOARD_BORDER, self.rect.y + const.BOARD_BORDER])