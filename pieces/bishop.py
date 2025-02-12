from pieces.piece import Piece
import pygame

white_bishop = pygame.image.load("pieces/assets/White_Bishop.png")
black_bishop = pygame.image.load("pieces/assets/Black_Bishop.png")
bishops = [white_bishop, black_bishop]

# Piece Square Table
white_bishop_eval_table = [
    [-20, -10, -10, -10, -10, -10, -10, -20],
    [-10, 0, 0, 0, 0, 0, 0, -10],
    [-10, 0, 5, 10, 10, 5, 0, -10],
    [-10, 5, 5, 10, 10, 5, 5, -10],
    [-10, 0, 10, 10, 10, 10, 0, -10],
    [-10, 10, 10, 10, 10, 10, 10, -10],
    [-10, 5, 0, 0, 0, 0, 5, -10],
    [-20, -10, -10, -10, -10, -10, -10, -20]
]

black_bishop_eval_table = white_bishop_eval_table[::-1]


class Bishop(Piece):
  def __init__(self, row, col, color):
    super().__init__(row, col, color)
    self.valid_moves = []
    self.letter = "B"

  def update_valid_moves(self, board):
    self.valid_moves = self.get_valid_moves(board)
    return self.valid_moves

  def get_valid_moves(self, board):
    moves = []
    # Up-Left, Up-Right, Down-Left, Down-Right
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for dx, dy in directions:
      row, col = self.row, self.col
      while True:
        row += dx
        col += dy

        if not (0 <= row < 8 and 0 <= col < 8):
          break

        piece = board[row][col]
        if piece != 0:
          if piece.color != self.color:
            moves.append((row, col))
          break

        moves.append((row, col))

    return moves
