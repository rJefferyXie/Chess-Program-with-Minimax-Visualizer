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
    [20, 20, 0, 0, 0, 0, 20, 20],
    [20, 30, 10, 0, 0, 10, 30, 20]
]

black_king_eval_table = white_king_eval_table[::-1]


class King(Piece):
  def __init__(self, row, col, color):
    super().__init__(row, col, color)
    self.valid_moves = []
    self.can_castle = True
    self.is_checked = False
    self.letter = "K"

  def update_valid_moves(self, board):
    self.valid_moves = self.get_valid_moves(board)
    return self.valid_moves

  def get_valid_moves(self, board):
    moves = []
    directions = [
        (-1, -1), (-1, 0), (-1, 1),  # Up-Left, Up, Up-Right
        (0, -1), (0, 1),  # Left, Right
        (1, -1), (1, 0), (1, 1)  # Down-Left, Down, Down-Right
    ]

    # Standard King Moves
    for dx, dy in directions:
      new_row, new_col = self.row + dx, self.col + dy
      if 0 <= new_row < 8 and 0 <= new_col < 8:  # Stay within board
        piece = board[new_row][new_col]
        if piece == 0 or piece.color != self.color:  # Empty or Opponent's piece
          moves.append((new_row, new_col))

    if self.can_castle and not self.is_checked:
      # Queenside Castle
      if all(board[self.row][self.col - i] == 0 for i in range(1, 3)):
        rook = board[self.row][self.col - 4]
        if isinstance(rook, Rook) and rook.can_castle:
          moves.append((self.row, self.col - 4))

      # Kingside Castle
      if all(board[self.row][self.col + i] == 0 for i in range(1, 2)):
        rook = board[self.row][self.col + 3]
        if isinstance(rook, Rook) and rook.can_castle:
          moves.append((self.row, self.col + 3))

    return moves
