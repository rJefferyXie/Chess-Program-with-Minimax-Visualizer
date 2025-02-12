import random


class ZobristHashing:
  def __init__(self, rows, cols, piece_types, colors):
    self.rows = rows
    self.cols = cols
    self.piece_types = piece_types
    self.colors = colors
    self.zobrist_table = self._initialize_zobrist_table()

  def _initialize_zobrist_table(self):
    table = {}
    for row in range(self.rows):
      for col in range(self.cols):
        for piece_type in self.piece_types:
          for color in self.colors:
            table[(row, col, piece_type, color)] = random.getrandbits(64)
    return table

  def calculate_hash(self, board):
    h = 0
    for row in board.board:
      for piece in row:
        if piece != 0:
          h ^= self.zobrist_table[(
            piece.row, piece.col, type(piece).__name__, piece.color)]
    return h

  def update_hash(self, h, piece, old_position, new_position):
    piece_type = type(piece).__name__
    piece_color = piece.color
    if old_position:
      h ^= self.zobrist_table[(
        old_position[0], old_position[1], piece_type, piece_color)]
    if new_position:
      h ^= self.zobrist_table[(
        new_position[0], new_position[1], piece_type, piece_color)]
    return h
