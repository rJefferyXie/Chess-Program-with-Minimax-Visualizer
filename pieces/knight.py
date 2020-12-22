from pieces.piece import Piece
import pygame

white_knight = pygame.image.load("pieces/assets/White_Knight.png")
black_knight = pygame.image.load("pieces/assets/Black_Knight.png")
knights = [white_knight, black_knight]

# Piece Square Table
white_knight_table = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20,  0,  0,  0,  0, -20, -40],
    [-30,  0,  10,  15,  15,  10,  0, -30],
    [-30,  5,  15,  20,  20,  15,  5, -30],
    [-30,  0,  15,  20,  20,  15,  0, -30],
    [-30,  5,  10,  15,  15,  10,  5, -30],
    [-40, -20,  0,  5,  5,  0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
]

black_knight_table = white_knight_table[::-1]
knight_tables = [white_knight_table, black_knight_table]


class Knight(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.row = row
        self.col = col
        self.color = color
        self.valid_moves = []
        self.letter = "N"

    def update_valid_moves(self, board):
        self.valid_moves = self.get_valid_moves(board)
        return self.valid_moves

    def get_valid_moves(self, board):
        moves = []

        # up two one left
        if self.row - 1 >= 0 and self.col - 2 >= 0:
            piece = board[self.row - 1][self.col - 2]
            if piece == 0:
                moves.append((self.row - 1, self.col - 2))
            elif piece.color != self.color:
                moves.append((piece.row, piece.col))

        # up two one right
        if self.row + 1 <= 7 and self.col - 2 >= 0:
            piece = board[self.row + 1][self.col - 2]
            if piece == 0:
                moves.append((self.row + 1, self.col - 2))
            elif piece.color != self.color:
                moves.append((piece.row, piece.col))

        # up one two left
        if self.row - 2 >= 0 and self.col - 1 >= 0:
            piece = board[self.row - 2][self.col - 1]
            if piece == 0:
                moves.append((self.row - 2, self.col - 1))
            elif piece.color != self.color:
                moves.append((piece.row, piece.col))

        # up one two right
        if self.row + 2 <= 7 and self.col - 1 >= 0:
            piece = board[self.row + 2][self.col - 1]
            if piece == 0:
                moves.append((self.row + 2, self.col - 1))
            elif piece.color != self.color:
                moves.append((piece.row, piece.col))

        # down one two right
        if self.row + 2 <= 7 and self.col + 1 <= 7:
            piece = board[self.row + 2][self.col + 1]
            if piece == 0:
                moves.append((self.row + 2, self.col + 1))
            elif piece.color != self.color:
                moves.append((piece.row, piece.col))

        # down one two left
        if self.row - 2 >= 0 and self.col + 1 <= 7:
            piece = board[self.row - 2][self.col + 1]
            if piece == 0:
                moves.append((self.row - 2, self.col + 1))
            elif piece.color != self.color:
                moves.append((piece.row, piece.col))

        # down two one right
        if self.row + 1 <= 7 and self.col + 2 <= 7:
            piece = board[self.row + 1][self.col + 2]
            if piece == 0:
                moves.append((self.row + 1, self.col + 2))
            elif piece.color != self.color:
                moves.append((piece.row, piece.col))

        # down two one left
        if self.row - 1 >= 0 and self.col + 2 <= 7:
            piece = board[self.row - 1][self.col + 2]
            if piece == 0:
                moves.append((self.row - 1, self.col + 2))
            elif piece.color != self.color:
                moves.append((piece.row, piece.col))

        return moves
