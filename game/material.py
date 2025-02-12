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

  def draw_captured(self, window, color):
    # Draw captured black pieces
    for piece in range(len(self.captured_black_pieces)):

      if isinstance(self.captured_black_pieces[piece], Pawn):
        image = pygame.transform.scale(pawns[1], (32, 32))

      elif isinstance(self.captured_black_pieces[piece], Knight):
        image = pygame.transform.scale(knights[1], (32, 32))

      elif isinstance(self.captured_black_pieces[piece], Bishop):
        image = pygame.transform.scale(bishops[1], (32, 32))

      elif isinstance(self.captured_black_pieces[piece], Rook):
        image = pygame.transform.scale(rooks[1], (32, 32))

      else:
        image = pygame.transform.scale(queens[1], (32, 32))

      if color == "White":
        if piece < 8:
          window.blit(image, (480 + piece * 25, 410))
        else:
          window.blit(image, (480 + (piece - 8) * 25, 435))
      else:
        if piece < 8:
          window.blit(image, (480 + piece * 25, 35))
        else:
          window.blit(image, (480 + (piece - 8) * 25, 55))

    # Draw captured white pieces
    for piece in range(len(self.captured_white_pieces)):
      if isinstance(self.captured_white_pieces[piece], Pawn):
        image = pygame.transform.scale(pawns[0], (32, 32))

      elif isinstance(self.captured_white_pieces[piece], Knight):
        image = pygame.transform.scale(knights[0], (32, 32))

      elif isinstance(self.captured_white_pieces[piece], Bishop):
        image = pygame.transform.scale(bishops[0], (32, 32))

      elif isinstance(self.captured_white_pieces[piece], Rook):
        image = pygame.transform.scale(rooks[0], (32, 32))

      else:
        image = pygame.transform.scale(queens[0], (32, 32))

      if color == "White":
        if piece < 8:
          window.blit(image, (480 + piece * 25, 25))
        else:
          window.blit(image, (480 + (piece - 8) * 25, 45))
      else:
        if piece < 8:
          window.blit(image, (480 + piece * 25, 400))
        else:
          window.blit(image, (480 + (piece - 8) * 25, 425))

  def draw_advantages(self, window, color):
    if self.white_advantage > self.black_advantage:
      text = my_font.render("+" + str(self.white_advantage), True, (0, 0, 0))
      self.captured_black_pieces.append(text)

      for piece in range(len(self.captured_black_pieces)):
        if not isinstance(self.captured_black_pieces[piece], (Pawn, Knight, Bishop, Rook, Queen)):

          if color == "White":
            if piece <= 8:
              window.blit(
                self.captured_black_pieces[piece], (460 + (piece + 1) * 25, 420))
            else:
              window.blit(
                self.captured_black_pieces[piece], (460 + (piece - 7) * 25, 445))

          else:
            if piece <= 8:
              window.blit(
                self.captured_black_pieces[piece], (460 + (piece + 1) * 25, 45))
            else:
              window.blit(
                self.captured_black_pieces[piece], (460 + (piece - 7) * 25, 70))

          self.captured_black_pieces.pop(-1)

    elif self.black_advantage > self.white_advantage:
      text = my_font.render("+" + str(self.black_advantage), True, (0, 0, 0))
      self.captured_white_pieces.append(text)

      for piece in range(len(self.captured_white_pieces)):
        if not isinstance(self.captured_white_pieces[piece], (Pawn, Knight, Bishop, Rook, Queen)):

          if color == "White":
            if piece <= 8:
              window.blit(
                self.captured_white_pieces[piece], (460 + (piece + 1) * 25, 35))
            else:
              window.blit(
                self.captured_white_pieces[piece], (460 + (piece - 7) * 25, 60))

          else:
            if piece <= 8:
              window.blit(
                self.captured_white_pieces[piece], (460 + (piece + 1) * 25, 410))
            else:
              window.blit(
                self.captured_white_pieces[piece], (460 + (piece - 7) * 25, 435))

          self.captured_white_pieces.pop(-1)

  def update_advantages(self, board):
    black_adv = 0
    white_adv = 0

    for row in board.board:
      for piece in row:
        if isinstance(piece, (Pawn, Knight, Bishop, Rook, Queen, King)):
          if piece.color == "White":
            if isinstance(piece, Pawn):
              white_adv += 1

            elif isinstance(piece, Knight) or isinstance(piece, Bishop):
              white_adv += 3

            elif isinstance(piece, Rook):
              white_adv += 4

            elif isinstance(piece, Queen):
              white_adv += 9

          else:
            if isinstance(piece, Pawn):
              black_adv += 1

            elif isinstance(piece, Knight) or isinstance(piece, Bishop):
              black_adv += 3

            elif isinstance(piece, Rook):
              black_adv += 4

            elif isinstance(piece, Queen):
              black_adv += 9

    if white_adv > black_adv:
      self.white_advantage = white_adv - black_adv
      self.black_advantage = 0

    elif black_adv > white_adv:
      self.black_advantage = black_adv - white_adv
      self.white_advantage = 0

    else:
      self.white_advantage = 0
      self.black_advantage = 0

  def add_to_captured_pieces(self, piece, capture_list):
    # Insert pawns to start of list
    if isinstance(piece, Pawn):
      capture_list.insert(0, piece)

    # Insert knights at the start of list, or after last pawn
    elif isinstance(piece, Knight):
      if len(capture_list) == 0 or not isinstance(capture_list[0], Pawn):
        capture_list.insert(0, piece)
      else:
        for i in range(len(capture_list)):
          curr = capture_list[i]
          if not isinstance(curr, Pawn):
            capture_list.insert(i, piece)
            break
          if i == len(capture_list) - 1:
            capture_list.insert(i + 1, piece)

    # Insert bishops at the start of the list, or after last pawn / knight
    elif isinstance(piece, Bishop):
      if len(capture_list) == 0 or (not isinstance(capture_list[0], Pawn)
                                    and not isinstance(capture_list[0], Knight)):
        capture_list.insert(0, piece)
      else:
        for i in range(len(capture_list)):
          curr = capture_list[i]
          if not isinstance(curr, Pawn) and not isinstance(curr, Knight):
            capture_list.insert(i, piece)
            break
          if i == len(capture_list) - 1:
            capture_list.insert(i + 1, piece)

    # Insert rooks at the end of the list, or after before queen
    elif isinstance(piece, Rook):
      if len(capture_list) == 0 or not isinstance(capture_list[-1], Queen):
        capture_list.append(piece)
      else:
        capture_list.insert(len(capture_list) - 1, piece)

    # Insert queen at the end of the list
    elif isinstance(piece, Queen):
      capture_list.append(piece)
