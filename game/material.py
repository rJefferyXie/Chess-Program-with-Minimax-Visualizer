from pieces.pawn import Pawn, pawns
from pieces.knight import Knight, knights
from pieces.bishop import Bishop, bishops
from pieces.rook import Rook, rooks
from pieces.queen import Queen, queens
from pieces.king import King
import pygame


pygame.font.init()
my_font = pygame.font.SysFont("calibri", 15)


class Material(object):
  def __init__(self):
    self.black_advantage = 0
    self.white_advantage = 0
    self.captured_black_pieces = []
    self.captured_white_pieces = []

  def get_image(self, piece, color_index):
    image_map = {
      Pawn: pawns[color_index],
      Knight: knights[color_index],
      Bishop: bishops[color_index],
      Rook: rooks[color_index],
      Queen: queens[color_index]
    }
    image = image_map.get(type(piece))
    return pygame.transform.scale(image, (32, 32)) if image else None

  def draw_captured(self, window, color):
    positions = {
      "White": [(480, 410, 25, 0), (480, 435, 25, -8)],
      "Black": [(480, 35, 25, 0), (480, 55, 25, -8)]
    }
    color_index = 1  # Black pieces
    for idx, piece in enumerate(self.captured_black_pieces):
      image = self.get_image(piece, color_index)
      if image:
        x_offset, y_base, spacing, shift = positions[color][0 if idx < 8 else 1]
        window.blit(image, (x_offset + (idx + shift) * spacing, y_base))

    color_index = 0  # White pieces
    for idx, piece in enumerate(self.captured_white_pieces):
      image = self.get_image(piece, color_index)
      if image:
        x_offset, y_base, spacing, shift = positions[color][0 if idx < 8 else 1]
        window.blit(image, (x_offset + (idx + shift) * spacing,
                    y_base - 385 if color == "White" else 375))

  def draw_advantages(self, window, color):
    def draw_text(pieces_list, advantage, y_offsets):
      text = my_font.render(f"+{advantage}", True, (0, 0, 0))
      pieces_list.append(text)
      for piece in range(len(pieces_list)):
        if not isinstance(pieces_list[piece], (Pawn, Knight, Bishop, Rook, Queen)):
          x_offset = 460 + (piece + 1) * 25
          y_offset = y_offsets[0] if piece <= 8 else y_offsets[1]
          window.blit(pieces_list[piece], (x_offset, y_offset))
          pieces_list.pop(-1)

    if self.white_advantage > self.black_advantage:
      draw_text(self.captured_black_pieces, self.white_advantage,
                (420 if color == "White" else 45, 445 if color == "White" else 70))
    elif self.black_advantage > self.white_advantage:
      draw_text(self.captured_white_pieces, self.black_advantage,
                (35 if color == "White" else 410, 60 if color == "White" else 435))

  def update_advantages(self, board):
    value_map = {Pawn: 1, Knight: 3, Bishop: 3, Rook: 4, Queen: 9}
    black_adv, white_adv = 0, 0

    for row in board.board:
      for piece in row:
        if type(piece) in value_map:
          if piece.color == "White":
            white_adv += value_map[type(piece)]
          else:
            black_adv += value_map[type(piece)]

    self.white_advantage = max(0, white_adv - black_adv)
    self.black_advantage = max(0, black_adv - white_adv)

  def add_to_captured_pieces(self, piece, capture_list):
    priority = [Pawn, Knight, Bishop, Rook, Queen]
    piece_priority = priority.index(type(piece))

    for i, curr in enumerate(capture_list):
      if priority.index(type(curr)) > piece_priority:
        capture_list.insert(i, piece)
        return
    capture_list.append(piece)