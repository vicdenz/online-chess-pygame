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

        if self.selected:
            pygame.draw.lines(display, const.OUTLINE_COLOR, False, self.outline, 5)

        display.blit(self.image, (self.get_x() + offset[0], self.get_y() + offset[1]))

    def update_outline(self, offset=[0, 0]):
        image_mask = pygame.mask.from_surface(self.image)

        self.outline = [(p[0]+ self.get_x() + offset[0], p[1]+ self.get_y() + offset[1]) for p in image_mask.outline()]

    def get_pos(self):
        return (self.column, self.row)

    def change_pos(self, pos):
        self.row = pos[1]
        self.column = pos[0]
        self.moved = True

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
        i = self.row
        j = self.column

        moves = []
        if self.color == "b":
            dir = 1
        else:
            dir = -1

        try:
            print(1)
            if i < 7:
                p = board[i + dir][j]
                if p == None:
                    moves.append((j, i + dir))
        except:
            pass

        # DIAGONAL
        try:
            print(2)
            if j < 7:
                p = board[i + dir][j + 1]
                if p != None:
                    if p.color != self.color:
                        moves.append((j + 1, i + dir))

            if j > 0:
                p = board[i + dir][j - 1]
                if p != None:
                    if p.color != self.color:
                        moves.append((j - 1, i + dir))
        except:
            pass

        try:
            print(3)
            if not self.moved:
                p = board[i + (2*dir)][j]
                if p == None:
                    if board[i + dir][j] == None:
                        moves.append((j, i + (2*dir)))
        except:
            pass

        return moves

# ---------------------------------------- ROOK ----------------------------------------

class Rook(Piece):
    img = "rook"

    def valid_moves(self, board):
        i = self.row
        j = self.column

        moves = []

        # UP
        for x in range(i - 1, -1, -1):
            p = board[x][j]
            if p == None:
                moves.append((j, x))
            elif p.color != self.color:
                moves.append((j, x))
                break
            else:
                break

        # DOWN
        for x in range(i + 1, 8, 1):
            p = board[x][j]
            if p == None:
                moves.append((j, x))
            elif p.color != self.color:
                moves.append((j, x))
                break
            else:
                break

        # LEFT
        for x in range(j - 1, -1, -1):
            p = board[i][x]
            if p == None:
                moves.append((x, i))
            elif p.color != self.color:
                moves.append((x, i))
                break
            else:
                break

        # RIGHT
        for x in range(j + 1, 8, 1):
            p = board[i][x]
            if p == None:
                moves.append((x, i))
            elif p.color != self.color:
                moves.append((x, i))
                break
            else:
                break

        return moves

# ------------------------------------------------------------ KNIGHT ------------------------------------------------------------

class Knight(Piece):
    img = "knight"

    def valid_moves(self, board):
        i = self.row
        j = self.column

        moves = []

        # DOWN LEFT
        if i < 6 and j > 0:
            p = board[i + 2][j - 1]
            if p == None:
                moves.append((j - 1, i + 2))
            elif p.color != self.color:
                moves.append((j - 1, i + 2))

        # UP LEFT
        if i > 1 and j > 0:
            p = board[i - 2][j - 1]
            if p == None:
                moves.append((j - 1, i - 2))
            elif p.color != self.color:
                moves.append((j - 1, i - 2))

        # DOWN RIGHT
        if i < 6 and j < 7:
            p = board[i + 2][j + 1]
            if p == None:
                moves.append((j + 1, i + 2))
            elif p.color != self.color:
                moves.append((j + 1, i + 2))

        # UP RIGHT
        if i > 1 and j < 7:
            p = board[i - 2][j + 1]
            if p == None:
                moves.append((j + 1, i - 2))
            elif p.color != self.color:
                moves.append((j + 1, i - 2))

        if i > 0 and j > 1:
            p = board[i - 1][j - 2]
            if p == None:
                moves.append((j - 2, i - 1))
            elif p.color != self.color:
                moves.append((j - 2, i - 1))

        if i > 0 and j < 6:
            p = board[i - 1][j + 2]
            if p == None:
                moves.append((j + 2, i - 1))
            elif p.color != self.color:
                moves.append((j + 2, i - 1))

        if i < 7 and j > 1:
            p = board[i + 1][j - 2]
            if p == None:
                moves.append((j - 2, i + 1))
            elif p.color != self.color:
                moves.append((j - 2, i + 1))

        if i < 7 and j < 6:
            p = board[i + 1][j + 2]
            if p == None:
                moves.append((j + 2, i + 1))
            elif p.color != self.color:
                moves.append((j + 2, i + 1))

        return moves

# ---------------------------------------- BISHOP ----------------------------------------

class Bishop(Piece):
    img = "bishop"

    def valid_moves(self, board):
        i = self.row
        j = self.column

        moves = []

        # TOP RIGHT
        djL = j + 1
        djR = j - 1
        for di in range(i - 1, -1, -1):
            if djL < 8:
                p = board[di][djL]
                if p == None:
                    moves.append((djL, di))
                elif p.color != self.color:
                    moves.append((djL, di))
                    break
                else:
                    break
            else:
                break

            djL += 1

        for di in range(i - 1, -1, -1):
            if djR > -1:
                p = board[di][djR]
                if p == None:
                    moves.append((djR, di))
                elif p.color != self.color:
                    moves.append((djR, di))
                    break
                else:
                    break
            else:
                break

            djR -= 1

        # TOP LEFT
        djL = j + 1
        djR = j - 1
        for di in range(i + 1, 8):
            if djL < 8:
                p = board[di][djL]
                if p == None:
                    moves.append((djL, di))
                elif p.color != self.color:
                    moves.append((djL, di))
                    break
                else:
                    break
            else:
                break
            djL += 1
        for di in range(i + 1, 8):
            if djR > -1:
                p = board[di][djR]
                if p == None:
                    moves.append((djR, di))
                elif p.color != self.color:
                    moves.append((djR, di))
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
        i = self.row
        j = self.column

        moves = []

        # TOP RIGHT
        djL = j + 1
        djR = j - 1
        for di in range(i - 1, -1, -1):
            if djL < 8:
                p = board[di][djL]
                if p == None:
                    moves.append((djL, di))
                elif p.color != self.color:
                    moves.append((djL, di))
                    break
                else:
                    djL = 9

            djL += 1

        for di in range(i - 1, -1, -1):
            if djR > -1:
                p = board[di][djR]
                if p == None:
                    moves.append((djR, di))
                elif p.color != self.color:
                    moves.append((djR, di))
                    break
                else:
                    djR = -1

            djR -= 1

        # TOP LEFT
        djL = j + 1
        djR = j - 1
        for di in range(i + 1, 8):
            if djL < 8:
                p = board[di][djL]
                if p == None:
                    moves.append((djL, di))
                elif p.color != self.color:
                    moves.append((djL, di))
                    break
                else:
                    djL = 9
            djL += 1
        for di in range(i + 1, 8):
            if djR > -1:
                p = board[di][djR]
                if p == None:
                    moves.append((djR, di))
                elif p.color != self.color:
                    moves.append((djR, di))
                    break
                else:
                    djR = -1

            djR -= 1

        # UP
        for x in range(i - 1, -1, -1):
            p = board[x][j]
            if p == None:
                moves.append((j, x))
            elif p.color != self.color:
                moves.append((j, x))
                break
            else:
                break

        # DOWN
        for x in range(i + 1, 8, 1):
            p = board[x][j]
            if p == None:
                moves.append((j, x))
            elif p.color != self.color:
                moves.append((j, x))
                break
            else:
                break

        # LEFT
        for x in range(j - 1, -1, -1):
            p = board[i][x]
            if p == None:
                moves.append((x, i))
            elif p.color != self.color:
                moves.append((x, i))
                break
            else:
                break

        # RIGHT
        for x in range(j + 1, 8, 1):
            p = board[i][x]
            if p == None:
                moves.append((x, i))
            elif p.color != self.color:
                moves.append((x, i))
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
        i = self.row
        j = self.column

        moves = []

        if i > 0:
            # TOP LEFT
            if j > 0:
                p = board[i - 1][j - 1]
                if p == None:
                    moves.append((j - 1, i - 1,))
                elif p.color != self.color:
                    moves.append((j - 1, i - 1,))

            # TOP MIDDLE
            p = board[i - 1][j]
            if p == None:
                moves.append((j, i - 1))
            elif p.color != self.color:
                moves.append((j, i - 1))

            # TOP RIGHT
            if j < 7:
                p = board[i - 1][j + 1]
                if p == None:
                    moves.append((j + 1, i - 1,))
                elif p.color != self.color:
                    moves.append((j + 1, i - 1,))

        if i < 7:
            # BOTTOM LEFT
            if j > 0:
                p = board[i + 1][j - 1]
                if p == None:
                    moves.append((j - 1, i + 1,))
                elif p.color != self.color:
                    moves.append((j - 1, i + 1,))

            # BOTTOM MIDDLE
            p = board[i + 1][j]
            if p == None:
                moves.append((j, i + 1))
            elif p.color != self.color:
                moves.append((j, i + 1))

            # BOTTOM RIGHT
            if j < 7:
                p = board[i + 1][j + 1]
                if p == None:
                    moves.append((j + 1, i + 1))
                elif p.color != self.color:
                    moves.append((j + 1, i + 1))

        # MIDDLE LEFT
        if j > 0:
            p = board[i][j - 1]
            if p == None:
                moves.append((j - 1, i))
            elif p.color != self.color:
                moves.append((j - 1, i))

        # MIDDLE RIGHT
        if j < 7:
            p = board[i][j + 1]
            if p == None:
                moves.append((j + 1, i))
            elif p.color != self.color:
                moves.append((j + 1, i))

        return moves