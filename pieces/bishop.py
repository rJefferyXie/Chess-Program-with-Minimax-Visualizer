from pieces.piece import Piece
import pygame

white_bishop = pygame.image.load("pieces/assets/White_Bishop.png")
black_bishop = pygame.image.load("pieces/assets/Black_Bishop.png")
bishops = [white_bishop, black_bishop]


# Piece Square Table
white_bishop_table = [[-20, -10, -10, -10, -10, -10, -10, -20],
                [-10,  0,  0,  0,  0,  0,  0, -10],
                [-10,  0,  5,  10,  10,  5,  0, -10],
                [-10,  5,  5,  10,  10,  5,  5, -10],
                [-10,  0,  10,  10,  10,  10,  0, -10],
                [-10,  10,  10,  10,  10,  10,  10, -10],
                [-10,  5,  0,  0,  0,  0,  5, -10],
                [-20, -10, -10, -10, -10, -10, -10, -20]]

black_bishop_table = white_bishop_table[::-1]
bishop_tables = [white_bishop_table, black_bishop_table]


class Bishop(Piece):
    def __init__(self, row, col, color):
        super().__init__(row, col, color)
        self.row = row
        self.col = col
        self.color = color
        self.valid_moves = []
        self.letter = "B"

    def update_valid_moves(self, board):
        self.valid_moves = self.get_valid_moves(board)
        return self.valid_moves

    def get_valid_moves(self, board):
        moves = []

        # Up Right Moves
        index = 0
        while self.col - index > 0 and self.row + index < 7:
            index += 1
            piece = board[self.row + index][self.col - index]
            if piece != 0:
                if piece.color != self.color:
                    moves.append((piece.row, piece.col))
                break
            moves.append((self.row + index, self.col - index))

        # Up Left Moves
        index = 0
        while self.col - index > 0 and self.row - index > 0:
            index += 1
            piece = board[self.row - index][self.col - index]
            if piece != 0:
                if piece.color != self.color:
                    moves.append((piece.row, piece.col))
                break
            moves.append((self.row - index, self.col - index))

        # Down Left Moves
        index = 0
        while self.col + index < 7 and self.row - index > 0:
            index += 1
            piece = board[self.row - index][self.col + index]
            if piece != 0:
                if piece.color != self.color:
                    moves.append((piece.row, piece.col))
                break
            moves.append((self.row - index, self.col + index))

        # Down Right Moves
        index = 0
        while self.col + index < 7 and self.row + index < 7:
            index += 1
            piece = board[self.row + index][self.col + index]
            if piece != 0:
                if piece.color != self.color:
                    moves.append((piece.row, piece.col))
                break
            moves.append((self.row + index, self.col + index))

        return moves
