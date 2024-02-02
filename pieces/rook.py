from pieces.piece import Piece
import pygame

white_rook = pygame.image.load("pieces/assets/White_Rook.png")
black_rook = pygame.image.load("pieces/assets/Black_Rook.png")
rooks = [white_rook, black_rook]


# Piece Square Table
white_rook_eval_table = [
    [ 0,  0,  0,  0,  0,  0,  0,  0],
    [ 5,  10,  10,  10,  10,  10,  10,  5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [-5,  0,  0,  0,  0,  0,  0, -5],
    [ 0,   0, 0,  5,  5,  0,  0,  0]
]

black_rook_eval_table = white_rook_eval_table[::-1]

class Rook(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.row = row
        self.col = col
        self.color = color
        self.valid_moves = []
        self.can_castle = True
        self.letter = "R"

    def update_valid_moves(self, board):
        self.valid_moves = self.get_valid_moves(board)
        return self.valid_moves

    def get_valid_moves(self, board):
        moves = []

        # Up Moves
        index = 0
        while self.col - index > 0:
            index += 1
            piece = board[self.row][self.col - index]
            if piece != 0:
                if piece.color != self.color:
                    moves.append((piece.row, piece.col))
                break
            moves.append((self.row, self.col - index))

        # Down Moves
        index = 0
        while self.col + index < 7:
            index += 1
            piece = board[self.row][self.col + index]
            if piece != 0:
                if piece.color != self.color:
                    moves.append((piece.row, piece.col))
                break
            moves.append((self.row, self.col + index))

        # Left Moves
        index = 0
        while self.row - index > 0:
            index += 1
            piece = board[self.row - index][self.col]
            if piece != 0:
                if piece.color != self.color:
                    moves.append((piece.row, piece.col))
                break
            moves.append((self.row - index, self.col))

        # Right Moves
        index = 0
        while self.row + index < 7:
            index += 1
            piece = board[self.row + index][self.col]
            if piece != 0:
                if piece.color != self.color:
                    moves.append((piece.row, piece.col))
                break
            moves.append((self.row + index, self.col))

        return moves
