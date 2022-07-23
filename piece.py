import pygame
import os
import const

class Piece:
    img = ""

    def __init__(self, row, column, color, pieces):
        self.row = row
        self.column = column
        self.color = color
        self.moved = False
        self.selected = False
        self.attacked = False
        self.changed = False
        self.move_list = []
        self.king = False
        self.pawn = False

        self.image = pieces[self.color][self.img]

        self.outline = []
        self.update_outline()

    def get_x(self):
        return self.column * const.TILE_SIZE

    def get_y(self):
        return (self.row-1) * const.TILE_SIZE

    def is_selected(self):
        return self.selected

    def update_valid_moves(self, board):
        self.move_list = self.valid_moves(board)

    def draw(self, display, offset):
        if offset != [0, 0]:
            self.update_outline(offset)

        if self.changed:
            pygame.draw.lines(display, const.LAST_MOVE_COLOR, False, self.outline, 5)
        if self.selected:
            pygame.draw.lines(display, const.OUTLINE_COLOR, False, self.outline, 5)
        if self.attacked:
            pygame.draw.lines(display, const.WARNING_COLOR, False, self.outline, 5)

        display.blit(self.image, (self.get_x() + offset[0], self.get_y() + offset[1]))

    def update_outline(self, offset=[0, 0]):
        image_mask = pygame.mask.from_surface(self.image)

        self.outline = [(p[0]+ self.get_x() + offset[0], p[1]+ self.get_y() + offset[1]) for p in image_mask.outline()]

    def get_pos(self):
        return (self.row, self.column)

    def change_pos(self, pos):
        self.row = pos[0]
        self.column = pos[1]

        self.update_outline()

    def __str__(self):
        return str(self.img) + " " + str(self.color) + " " + str(self.column) + " " + str(self.row)

# ---------------------------------------- PAWN ----------------------------------------

class Pawn(Piece):
    img = "pawn"

    def __init__(self, row, column, color, pieces):
        super().__init__(row, column, color, pieces)
        self.queen = False
        self.pawn = True

    def valid_moves(self, board):
        r = self.row
        c = self.column

        moves = []
        if self.color == "b":
            dir = 1
        else:
            dir = -1

        try:
            if r < 7:
                p = board[r + dir][c]
                if p == None:
                    moves.append((r + dir, c))
        except:
            pass

        # DIAGONAL
        try:
            if c < 7:
                p = board[r + dir][c + 1]
                if p != None:
                    if p.color != self.color:
                        moves.append((r + dir, c + 1))

            if c > 0:
                p = board[r + dir][c - 1]
                if p != None:
                    if p.color != self.color:
                        moves.append((r + dir, c - 1))
        except:
            pass

        try:
            if not self.moved:
                p = board[r + (2*dir)][c]
                if p == None:
                    if board[r + dir][c] == None:
                        moves.append((r + (2*dir), c))
        except:
            pass

        return moves
    
    def attack_moves(self, board):
        r = self.row
        c = self.column

        moves = []
        if self.color == "b":
            dir = 1
        else:
            dir = -1

        # DIAGONAL
        try:
            if c < 7:
                p = board[r + dir][c + 1]
                moves.append((r + dir, c + 1))

            if c > 0:
                p = board[r + dir][c - 1]
                moves.append((r + dir, c - 1))
        except:
            pass

        return moves

# ---------------------------------------- ROOK ----------------------------------------

class Rook(Piece):
    img = "rook"

    def valid_moves(self, board):
        r = self.row
        c = self.column

        moves = []

        # UP
        for y in range(r - 1, -1, -1):
            p = board[y][c]
            if p == None:
                moves.append((y, c))
            elif p.color != self.color:
                moves.append((y, c))
                break
            else:
                break

        # DOWN
        for y in range(r + 1, 8, 1):
            p = board[y][c]
            if p == None:
                moves.append((y, c))
            elif p.color != self.color:
                moves.append((y, c))
                break
            else:
                break

        # LEFT
        for x in range(c - 1, -1, -1):
            p = board[r][x]
            if p == None:
                moves.append((r, x))
            elif p.color != self.color:
                moves.append((r, x))
                break
            else:
                break

        # RIGHT
        for x in range(c + 1, 8, 1):
            p = board[r][x]
            if p == None:
                moves.append((r, x))
            elif p.color != self.color:
                moves.append((r, x))
                break
            else:
                break

        return moves
    
    def attack_moves(self, board):
        r = self.row
        c = self.column

        moves = []

        # UP
        for y in range(r - 1, -1, -1):
            p = board[y][c]
            if p == None:
                moves.append((y, c))
            elif p.color != self.color:
                moves.append((y, c))
                if p.king:
                    if y != 0:
                        moves.append((y-1, c))
                else:
                    break
            else:
                break

        # DOWN
        for y in range(r + 1, 8, 1):
            p = board[y][c]
            if p == None:
                moves.append((y, c))
            elif p.color != self.color:
                moves.append((y, c))
                if p.king:
                    if y != 7:
                        moves.append((y+1, c))
                else:
                    break
            else:
                break

        # LEFT
        for x in range(c - 1, -1, -1):
            p = board[r][x]
            if p == None:
                moves.append((r, x))
            elif p.color != self.color:
                moves.append((r, x))
                if p.king:
                    if x != 0:
                        moves.append((r, x-1))
                else:
                    break
            else:
                break

        # RIGHT
        for x in range(c + 1, 8, 1):
            p = board[r][x]
            if p == None:
                moves.append((r, x))
            elif p.color != self.color:
                moves.append((r, x))
                if p.king:
                    if x != 7:
                        moves.append((r, x+1))
                else:
                    break
            else:
                break

        return moves

# ------------------------------------------------------------ KNIGHT ------------------------------------------------------------

class Knight(Piece):
    img = "knight"

    def valid_moves(self, board):
        r = self.row
        c = self.column

        moves = []

        # DOWN LEFT
        if r < 6 and c > 0:
            p = board[r + 2][c - 1]
            if p == None or p.color != self.color:
                moves.append((r + 2, c - 1))
            elif p.color != self.color:
                moves.append((r + 2, c - 1))

        # UP LEFT
        if r > 1 and c > 0:
            p = board[r - 2][c - 1]
            if p == None:
                moves.append((r - 2, c - 1))
            elif p.color != self.color:
                moves.append((r - 2, c - 1))

        # DOWN RIGHT
        if r < 6 and c < 7:
            p = board[r + 2][c + 1]
            if p == None:
                moves.append((r + 2, c + 1))
            elif p.color != self.color:
                moves.append((r + 2, c + 1))

        # UP RIGHT
        if r > 1 and c < 7:
            p = board[r - 2][c + 1]
            if p == None:
                moves.append((r - 2, c + 1))
            elif p.color != self.color:
                moves.append((r - 2, c + 1))

        if r > 0 and c > 1:
            p = board[r - 1][c - 2]
            if p == None:
                moves.append((r - 1, c - 2))
            elif p.color != self.color:
                moves.append((r - 1, c - 2))

        if r > 0 and c < 6:
            p = board[r - 1][c + 2]
            if p == None:
                moves.append((r - 1, c + 2))
            elif p.color != self.color:
                moves.append((r - 1, c + 2))

        if r < 7 and c > 1:
            p = board[r + 1][c - 2]
            if p == None:
                moves.append((r + 1, c - 2))
            elif p.color != self.color:
                moves.append((r + 1, c - 2))

        if r < 7 and c < 6:
            p = board[r + 1][c + 2]
            if p == None:
                moves.append((r + 1, c + 2))
            elif p.color != self.color:
                moves.append((r + 1, c + 2))

        return moves
    
    def attack_moves(self, board):
        return self.valid_moves(board)

# ---------------------------------------- BISHOP ----------------------------------------

class Bishop(Piece):
    img = "bishop"

    def valid_moves(self, board):
        r = self.row
        c = self.column

        moves = []

        # TOP RIGHT
        djL = c + 1
        djR = c - 1
        for di in range(r - 1, -1, -1):
            if djL < 8:
                p = board[di][djL]
                if p == None:
                    moves.append((di, djL))
                elif p.color != self.color:
                    moves.append((di, djL))
                    break
                else:
                    break
            else:
                break

            djL += 1

        # TOP LEFT
        for di in range(r - 1, -1, -1):
            if djR > -1:
                p = board[di][djR]
                if p == None:
                    moves.append((di, djR))
                elif p.color != self.color:
                    moves.append((di, djR))
                    break
                else:
                    break
            else:
                break

            djR -= 1

        # BOTTOM RIGHT
        djL = c + 1
        djR = c - 1
        for di in range(r + 1, 8):
            if djL < 8:
                p = board[di][djL]
                if p == None:
                    moves.append((di, djL))
                elif p.color != self.color:
                    moves.append((di, djL))
                    break
                else:
                    break
            else:
                break
            djL += 1
        
        # BOTTOM LEFT
        for di in range(r + 1, 8):
            if djR > -1:
                p = board[di][djR]
                if p == None:
                    moves.append((di, djR))
                elif p.color != self.color:
                    moves.append((di, djR))
                    break
                else:
                    break
            else:
                break

            djR -= 1

        return moves
    
    def attack_moves(self, board):
        r = self.row
        c = self.column

        moves = []

        # TOP RIGHT
        djL = c + 1
        djR = c - 1
        for di in range(r - 1, -1, -1):
            if djL < 8:
                p = board[di][djL]
                if p == None:
                    moves.append((di, djL))
                elif p.color != self.color:
                    moves.append((di, djL))
                    if p.king:
                        if di != 0 and djL != 7:
                            moves.append((di-1, djL+1))
                    else:
                        break
                else:
                    break
            else:
                break

            djL += 1

        # TOP LEFT
        for di in range(r - 1, -1, -1):
            if djR > -1:
                p = board[di][djR]
                if p == None:
                    moves.append((di, djL))
                elif p.color != self.color:
                    moves.append((di, djL))
                    if p.king:
                        if di != 0 and djR != 0:
                            moves.append((di-1, djR-1))
                    else:
                        break
                else:
                    break
            else:
                break

            djR -= 1

        # BOTTOM RIGHT
        djL = c + 1
        djR = c - 1
        for di in range(r + 1, 8):
            if djL < 8:
                p = board[di][djL]
                if p == None:
                    moves.append((di, djL))
                elif p.color != self.color:
                    moves.append((di, djL))
                    if p.king:
                        if di != 7 and djL != 7:
                            moves.append((di+1, djL+1))
                    else:
                        break
                else:
                    break
            else:
                break
        
            djL += 1
        
        # BOTTOM LEFT
        for di in range(r + 1, 8):
            if djR > -1:
                p = board[di][djR]
                if p == None:
                    moves.append((di, djL))
                elif p.color != self.color:
                    moves.append((di, djL))
                    if p.king:
                        if di != 7 and djR != 0:
                            moves.append((di+1, djL-1))
                    else:
                        break
                else:
                    break
            else:
                break

            djR -= 1

        return moves

# ---------------------------------------- QUEEN ----------------------------------------

class Queen(Piece):
    img = "queen"

    def valid_moves(self, board):
        r = self.row
        c = self.column

        moves = []

        # TOP RIGHT
        djL = c + 1
        djR = c - 1
        for di in range(r - 1, -1, -1):
            if djL < 8:
                p = board[di][djL]
                if p == None:
                    moves.append((di, djL))
                elif p.color != self.color:
                    moves.append((di, djL))
                    break
                else:
                    break
            else:
                break

            djL += 1

        # TOP LEFT
        for di in range(r - 1, -1, -1):
            if djR > -1:
                p = board[di][djR]
                if p == None:
                    moves.append((di, djR))
                elif p.color != self.color:
                    moves.append((di, djR))
                    break
                else:
                    break
            else:
                break

            djR -= 1

        # BOTTOM RIGHT
        djL = c + 1
        djR = c - 1
        for di in range(r + 1, 8):
            if djL < 8:
                p = board[di][djL]
                if p == None:
                    moves.append((di, djL))
                elif p.color != self.color:
                    moves.append((di, djL))
                    break
                else:
                    break
            else:
                break
            djL += 1
        
        # BOTTOM LEFT
        for di in range(r + 1, 8):
            if djR > -1:
                p = board[di][djR]
                if p == None:
                    moves.append((di, djR))
                elif p.color != self.color:
                    moves.append((di, djR))
                    break
                else:
                    break
            else:
                break

            djR -= 1

        # UP
        for y in range(r - 1, -1, -1):
            p = board[y][c]
            if p == None:
                moves.append((y, c))
            elif p.color != self.color:
                moves.append((y, c))
                break
            else:
                break

        # DOWN
        for y in range(r + 1, 8, 1):
            p = board[y][c]
            if p == None:
                moves.append((y, c))
            elif p.color != self.color:
                moves.append((y, c))
                break
            else:
                break

        # LEFT
        for x in range(c - 1, -1, -1):
            p = board[r][x]
            if p == None:
                moves.append((r, x))
            elif p.color != self.color:
                moves.append((r, x))
                break
            else:
                break

        # RIGHT
        for x in range(c + 1, 8, 1):
            p = board[r][x]
            if p == None:
                moves.append((r, x))
            elif p.color != self.color:
                moves.append((r, x))
                break
            else:
                break

        return moves
    
    def attack_moves(self, board):
        r = self.row
        c = self.column

        moves = []

        # TOP RIGHT
        djL = c + 1
        djR = c - 1
        for di in range(r - 1, -1, -1):
            if djL < 8:
                p = board[di][djL]
                if p == None:
                    moves.append((di, djL))
                elif p.color != self.color:
                    moves.append((di, djL))
                    if p.king:
                        if di != 0 and djL != 7:
                            moves.append((di-1, djL+1))
                    else:
                        break
                else:
                    break
            else:
                break

            djL += 1

        # TOP LEFT
        for di in range(r - 1, -1, -1):
            if djR > -1:
                p = board[di][djR]
                if p == None:
                    moves.append((di, djL))
                elif p.color != self.color:
                    moves.append((di, djL))
                    if p.king:
                        if di != 0 and djR != 0:
                            moves.append((di-1, djR-1))
                    else:
                        break
                else:
                    break
            else:
                break

            djR -= 1

        # BOTTOM RIGHT
        djL = c + 1
        djR = c - 1
        for di in range(r + 1, 8):
            if djL < 8:
                p = board[di][djL]
                if p == None:
                    moves.append((di, djL))
                elif p.color != self.color:
                    moves.append((di, djL))
                    if p.king:
                        if di != 7 and djL != 7:
                            moves.append((di+1, djL+1))
                    else:
                        break
                else:
                    break
            else:
                break
        
            djL += 1
        
        # BOTTOM LEFT
        for di in range(r + 1, 8):
            if djR > -1:
                p = board[di][djR]
                if p == None:
                    moves.append((di, djL))
                elif p.color != self.color:
                    moves.append((di, djL))
                    if p.king:
                        if di != 7 and djR != 0:
                            moves.append((di+1, djL-1))
                    else:
                        break
                else:
                    break
            else:
                break

            djR -= 1

        # UP
        for y in range(r - 1, -1, -1):
            p = board[y][c]
            if p == None:
                moves.append((y, c))
            elif p.color != self.color:
                moves.append((y, c))
                if p.king:
                    if y != 0:
                        moves.append((y-1, c))
                else:
                    break
            else:
                break

        # DOWN
        for y in range(r + 1, 8, 1):
            p = board[y][c]
            if p == None:
                moves.append((y, c))
            elif p.color != self.color:
                moves.append((y, c))
                if p.king:
                    if y != 7:
                        moves.append((y+1, c))
                else:
                    break
            else:
                break

        # LEFT
        for x in range(c - 1, -1, -1):
            p = board[r][x]
            if p == None:
                moves.append((r, x))
            elif p.color != self.color:
                moves.append((r, x))
                if p.king:
                    if x != 0:
                        moves.append((r, x-1))
                else:
                    break
            else:
                break

        # RIGHT
        for x in range(c + 1, 8, 1):
            p = board[r][x]
            if p == None:
                moves.append((r, x))
            elif p.color != self.color:
                moves.append((r, x))
                if p.king:
                    if x != 7:
                        moves.append((r, x+1))
                else:
                    break
            else:
                break

        return moves

# ---------------------------------------- KING ----------------------------------------

class King(Piece):
    img = "king"

    def __init__(self, row, column, color, pieces):
        super().__init__(row, column, color, pieces)
        self.king = True

    def valid_moves(self, board):
        r = self.row
        c = self.column

        moves = []

        if r > 0:
            # TOP LEFT
            if c > 0:
                p = board[r - 1][c - 1]
                if p == None or p.color != self.color:
                    moves.append((r - 1, c - 1))

            # TOP MIDDLE
            p = board[r - 1][c]
            if p == None or p.color != self.color:
                moves.append((r - 1, c))

            # TOP RIGHT
            if c < 7:
                p = board[r - 1][c + 1]
                if p == None or p.color != self.color:
                    moves.append((r - 1, c + 1))

        if r < 7:
            # BOTTOM LEFT
            if c > 0:
                p = board[r + 1][c - 1]
                if p == None or p.color != self.color:
                    moves.append((r + 1, c - 1))

            # BOTTOM MIDDLE
            p = board[r + 1][c]
            if p == None or p.color != self.color:
                moves.append((r + 1, c))

            # BOTTOM RIGHT
            if c < 7:
                p = board[r + 1][c + 1]
                if p == None or p.color != self.color:
                    moves.append((r + 1, c + 1))

        # MIDDLE LEFT
        if c > 0:
            p = board[r][c - 1]
            if p == None or p.color != self.color:
                moves.append((r, c - 1))

        # MIDDLE RIGHT
        if c < 7:
            p = board[r][c + 1]
            if p == None or p.color != self.color:
                moves.append((r, c + 1))

        return moves
    
    def attack_moves(self, board):
        return self.valid_moves(board)