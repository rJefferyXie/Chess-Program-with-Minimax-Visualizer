from pieces.piece import Piece
import pygame

white_pawn = pygame.image.load("pieces/assets/White_Pawn.png")
black_pawn = pygame.image.load("pieces/assets/Black_Pawn.png")
pawns = [white_pawn, black_pawn]

# Piece Square Table
white_pawn_eval_table = [
  0, 0, 0, 0, 0, 0, 0, 0,
  50, 50, 50, 50, 50, 50, 50, 50,
  10, 10, 20, 30, 30, 20, 10, 10,
  5, 5, 10, 25, 25, 10, 5, 5,
  0, 0, 0, 20, 20, 0, 0, 0,
  5, -5, -10, 0, 0, -10, -5, 5,
  5, 10, 10, -20, -20, 10, 10, 5,
  0, 0, 0, 0, 0, 0, 0, 0
]

black_pawn_eval_table = white_pawn_eval_table[::-1]


class Pawn(Piece):
  def __init__(self, row, col, color, direction):
    super().__init__(row, col, color)
    self.direction = direction
    self.vulnerable_to_en_passant = False
    self.valid_moves = []

  def update_valid_moves(self, board, move_log):
    self.valid_moves = self.get_valid_moves(board, move_log)
    return self.valid_moves

  def get_valid_moves(self, board, move_log):
    moves = []

    # Direction mapping for Up and Down
    dir_map = {
        "Up": {"move": -1, "start": 6},
        "Down": {"move": 1, "start": 1}
    }
    direction = dir_map[self.direction]
    move = direction["move"]

    # Moving forward
    if 0 <= self.row + move < 8 and board[self.row + move][self.col] == 0:
      moves.append((self.row + move, self.col))
      # Two-square move from the start
      if self.row == direction["start"] and 0 <= self.row + (2 * move) < 8 and board[self.row + (2 * move)][self.col] == 0:
        moves.append((self.row + (2 * move), self.col))

    # Capturing diagonally
    for dx in [-1, 1]:
      new_row, new_col = self.row + move, self.col + dx
      if 0 <= new_row < 8 and 0 <= new_col < 8:
        target = board[new_row][new_col]
        if target != 0 and target.color != self.color:
          moves.append((new_row, new_col))

    # En Passant
    if move_log:
      for dx in [-1, 1]:
        new_col = self.col + dx
        if 0 <= new_col < 8:
          adjacent = board[self.row][new_col]
          if isinstance(adjacent, Pawn) and adjacent.color != self.color and adjacent.vulnerable_to_en_passant \
          and new_col == self.get_row(move_log[-1][0]) and self.row == abs(int(move_log[-1][-1]) - 8):
            moves.append((self.row + move, new_col))

    return moves

  def get_row(self, letter):
    return {'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7}.get(letter)
