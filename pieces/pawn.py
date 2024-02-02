from pieces.piece import Piece
import pygame

white_pawn = pygame.image.load("pieces/assets/White_Pawn.png")
black_pawn = pygame.image.load("pieces/assets/Black_Pawn.png")
pawns = [white_pawn, black_pawn]

# Piece Square Table
white_pawn_eval_table = [
    [0,  0,  0,  0,  0,  0,  0,  0],
    [50,  50,  50,  50,  50,  50,  50,  50],
    [10,  10,  20,  30,  30,  20,  10,  10],
    [5,  5,  10,  25,  25,  10,  5,  5],
    [0,  0,  0,  20,  20,  0,  0,  0],
    [5, -5, -10,  0,  0, -10, -5,  5],
    [5,  10, 10,  -20, -20,  10,  10,  5],
    [0,  0,  0,  0,  0,  0,  0,  0]
]

black_pawn_eval_table = white_pawn_eval_table[::-1]

class Pawn(Piece):
    def __init__(self, row, col, color, direction):
        super().__init__(row, col, color)
        self.row = row
        self.col = col
        self.color = color
        self.direction = direction
        self.vulnerable_to_en_passant = True
        self.valid_moves = []

    def update_valid_moves(self, board, move_log):
        self.valid_moves = self.get_valid_moves(board,  move_log)
        return self.valid_moves

    def get_valid_moves(self, board, move_log):
        moves = []

        if self.direction == "Up":
            if 0 < self.col < 7:
                # Moving straight
                if board[self.row][self.col - 1] == 0:
                    moves.append((self.row, self.col - 1))
                if self.col == 6:
                    if board[self.row][self.col - 1] == 0 and board[self.row][self.col - 2] == 0:
                        moves.append((self.row, self.col - 2))

                # Capturing on Diagonals
                if self.row < 7:
                    if board[self.row + 1][self.col - 1] != 0:
                        piece = board[self.row + 1][self.col - 1]
                        if piece.color != self.color:
                            moves.append((self.row + 1, self.col - 1))

                if self.row > 0:
                    if board[self.row - 1][self.col - 1] != 0:
                        piece = board[self.row - 1][self.col - 1]
                        if piece.color != self.color:
                            moves.append((self.row - 1, self.col - 1))

                # En Passant Rule
                if self.col == 3:
                    if self.row == 0:
                        piece = board[self.row + 1][self.col]
                        if isinstance(piece, Pawn) and piece.color != self.color and move_log[-1] == "b5":
                            self.add_en_passant_move(piece, move_log, moves, "Up")

                    elif self.row == 7:
                        piece = board[self.row - 1][self.col]
                        if isinstance(piece, Pawn) and piece.color != self.color and move_log[-1] == "g5":
                            self.add_en_passant_move(piece, move_log, moves, "Up")
                    else:
                        pieces = [board[self.row + 1][self.col], board[self.row - 1][self.col]]
                        for piece in pieces:
                            if isinstance(piece, Pawn) and piece.color != self.color and \
                                    move_log[-1] in ["a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5"]:
                                self.add_en_passant_move(piece, move_log, moves, "Up")

        else:
            if 0 < self.col < 7:
                if board[self.row][self.col + 1] == 0:
                    moves.append((self.row, self.col + 1))
                if self.col == 1:
                    if board[self.row][self.col + 1] == 0 and board[self.row][self.col + 2] == 0:
                        moves.append((self.row, self.col + 2))

                # Capturing on Diagonals
                if self.row < 7:
                    if board[self.row + 1][self.col + 1] != 0:
                        piece = board[self.row + 1][self.col + 1]
                        if piece.color != self.color:
                            moves.append((self.row + 1, self.col + 1))

                if self.row > 0:
                    if board[self.row - 1][self.col + 1] != 0:
                        piece = board[self.row - 1][self.col + 1]
                        if piece.color != self.color:
                            moves.append((self.row - 1, self.col + 1))

                # En Passant Rule
                if self.col == 4:
                    if self.row == 0:
                        piece = board[self.row + 1][self.col]
                        if isinstance(piece, Pawn) and piece.color != self.color and move_log[-1] == "b4":
                            self.add_en_passant_move(piece, move_log, moves, "Down")

                    elif self.row == 7:
                        piece = board[self.row - 1][self.col]
                        if isinstance(piece, Pawn) and piece.color != self.color and move_log[-1] == "g4":
                            self.add_en_passant_move(piece, move_log, moves, "Down")
                    else:
                        pieces = [board[self.row + 1][self.col], board[self.row - 1][self.col]]
                        for piece in pieces:
                            if isinstance(piece, Pawn) and piece.color != self.color and \
                                    move_log[-1] in ["a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4"]:
                                self.add_en_passant_move(piece, move_log, moves, "Down")

        return moves

    def get_row(self, letter):
        if letter == "a":
            return 0
        elif letter == "b":
            return 1
        elif letter == "c":
            return 2
        elif letter == "d":
            return 3
        elif letter == "e":
            return 4
        elif letter == "f":
            return 5
        elif letter == "g":
            return 6
        elif letter == "h":
            return 7
        else:
            pass

    def add_en_passant_move(self, piece, move_log, moves, direction):
        if direction == "Up":
            if piece.row == self.get_row(move_log[-1][0]) and piece.col == abs(int(move_log[-1][1]) - 8):
                if piece.vulnerable_to_en_passant:
                    moves.append((piece.row, piece.col - 1))
        else:
            if piece.row == self.get_row(move_log[-1][0]) and piece.col == abs(int(move_log[-1][1]) - 8):
                if piece.vulnerable_to_en_passant:
                    moves.append((piece.row, piece.col + 1))
        return moves
