from pieces.piece import Piece
import pygame

white_rook = pygame.image.load("pieces/assets/White_Rook.png")
black_rook = pygame.image.load("pieces/assets/Black_Rook.png")
rooks = [white_rook, black_rook]


# Piece Square Table
white_rook_eval_table = [
  0, 0, 0, 0, 0, 0, 0, 0,
  5, 10, 10, 10, 10, 10, 10, 5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  -5, 0, 0, 0, 0, 0, 0, -5,
  0, 0, 0, 5, 5, 0, 0, 0
]

black_rook_eval_table = white_rook_eval_table[::-1]


class Rook(Piece):
  def __init__(self, row, col, color):
    super().__init__(row, col, color)
    self.valid_moves = []
    self.can_castle = True
    self.letter = "R"

  def update_valid_moves(self, board):
    self.valid_moves = self.get_valid_moves(board)
    return self.valid_moves

  def get_valid_moves(self, board):
    moves = []
    # Direction vectors for Up, Down, Left, Right
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for d in directions:
      row, col = self.row, self.col
      while True:
        row += d[0]
        col += d[1]
        if not (0 <= row < 8 and 0 <= col < 8):
          break

        piece = board[row][col]
        if piece != 0:
          if piece.color != self.color:
            moves.append((row, col))
          break

        moves.append((row, col))

    return moves
