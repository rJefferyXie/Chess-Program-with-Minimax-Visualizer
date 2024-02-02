from pieces.piece import Piece
from pieces.rook import Rook
import pygame


white_king = pygame.image.load("pieces/assets/White_King.png")
black_king = pygame.image.load("pieces/assets/Black_King.png")
kings = [white_king, black_king]

# Piece Square Table
white_king_eval_table = [
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-30, -40, -40, -50, -50, -40, -40, -30],
    [-20, -30, -30, -40, -40, -30, -30, -20],
    [-10, -20, -20, -20, -20, -20, -20, -10],
    [ 20,  20,  0,  0,  0,  0,  20,  20],
    [ 20,  30,  10,  0,  0,  10,  30,  20]
]

black_king_eval_table = white_king_eval_table[::-1]

class King(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.row = row
        self.col = col
        self.color = color
        self.valid_moves = []
        self.can_castle = True
        self.is_checked = False
        self.letter = "K"

    def update_valid_moves(self, board):
        self.valid_moves = self.get_valid_moves(board)
        return self.valid_moves

    def get_valid_moves(self, board):
        moves = []

        # Up Left
        if self.row - 1 >= 0 and self.col - 1 >= 0:
            piece = board[self.row - 1][self.col - 1]
            if piece == 0:
                moves.append((self.row - 1, self.col - 1))
            elif piece.color != self.color:
                moves.append((piece.row, piece.col))

        # Up
        if self.col - 1 >= 0:
            piece = board[self.row][self.col - 1]
            if piece == 0:
                moves.append((self.row, self.col - 1))
            elif piece.color != self.color:
                moves.append((piece.row, piece.col))

        # Up Right
        if self.row + 1 <= 7 and self.col - 1 >= 0:
            piece = board[self.row + 1][self.col - 1]
            if piece == 0:
                moves.append((self.row + 1, self.col - 1))
            elif piece.color != self.color:
                moves.append((piece.row, piece.col))

        # Right
        if self.row + 1 <= 7:
            piece = board[self.row + 1][self.col]
            if piece == 0:
                moves.append((self.row + 1, self.col))
            elif piece.color != self.color:
                moves.append((piece.row, piece.col))

        # Down Right
        if self.row + 1 <= 7 and self.col + 1 <= 7:
            piece = board[self.row + 1][self.col + 1]
            if piece == 0:
                moves.append((self.row + 1, self.col + 1))
            elif piece.color != self.color:
                moves.append((piece.row, piece.col))

        # Down
        if self.col + 1 <= 7:
            piece = board[self.row][self.col + 1]
            if piece == 0:
                moves.append((self.row, self.col + 1))
            elif piece.color != self.color:
                moves.append((piece.row, piece.col))

        # Down Left
        if self.row - 1 >= 0 and self.col + 1 <= 7:
            piece = board[self.row - 1][self.col + 1]
            if piece == 0:
                moves.append((self.row - 1, self.col + 1))
            elif piece.color != self.color:
                moves.append((piece.row, piece.col))

        # Left
        if self.row - 1 >= 0:
            piece = board[self.row - 1][self.col]
            if piece == 0:
                moves.append((self.row - 1, self.col))
            elif piece.color != self.color:
                moves.append((piece.row, piece.col))

        # Castling
        if self.can_castle and not self.is_checked:
            # Check if the path to the a rook is empty
            if board[self.row - 1][self.col] == 0 and board[self.row - 2][self.col] == 0 and \
                    board[self.row - 3][self.col] == 0 and isinstance(board[self.row - 4][self.col], Rook):
                piece = board[self.row - 4][self.col]
                if piece.can_castle:
                    moves.append((piece.row, piece.col))

            # Check if path to the h rook is empty
            if board[self.row + 1][self.col] == 0 and board[self.row + 2][self.col] == 0 and \
                    isinstance(board[self.row + 3][self.col], Rook):
                piece = board[self.row + 3][self.col]
                if isinstance(piece, Rook):
                    if piece.can_castle:
                        moves.append((piece.row, piece.col))

        return moves
