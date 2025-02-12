from pieces.piece import Piece
import pygame

white_knight = pygame.image.load("pieces/assets/White_Knight.png")
black_knight = pygame.image.load("pieces/assets/Black_Knight.png")
knights = [white_knight, black_knight]

# Piece Square Table
white_knight_eval_table = [
    [-50, -40, -30, -30, -30, -30, -40, -50],
    [-40, -20, 0, 0, 0, 0, -20, -40],
    [-30, 0, 10, 15, 15, 10, 0, -30],
    [-30, 5, 15, 20, 20, 15, 5, -30],
    [-30, 0, 15, 20, 20, 15, 0, -30],
    [-30, 5, 10, 15, 15, 10, 5, -30],
    [-40, -20, 0, 5, 5, 0, -20, -40],
    [-50, -40, -30, -30, -30, -30, -40, -50]
]

black_knight_eval_table = white_knight_eval_table[::-1]


class Knight(Piece):
  def __init__(self, row, col, color):
    super().__init__(row, col, color)
    self.valid_moves = []
    self.letter = "N"

  def update_valid_moves(self, board):
    self.valid_moves = self.get_valid_moves(board)
    return self.valid_moves

  def get_valid_moves(self, board):
    moves = []

    # All possible moves for a knight
    knight_moves = [
        (-2, -1), (-2, 1), (-1, -2), (-1, 2),
        (1, -2), (1, 2), (2, -1), (2, 1)
    ]

    for move in knight_moves:
      new_row = self.row + move[0]
      new_col = self.col + move[1]

      if 0 <= new_row < 8 and 0 <= new_col < 8:  # Ensure within board bounds
        piece = board[new_row][new_col]
        if piece == 0 or piece.color != self.color:  # Empty or opponent's piece
          moves.append((new_row, new_col))

    return moves
