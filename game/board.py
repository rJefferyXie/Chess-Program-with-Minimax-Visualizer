import pygame
from game.constants import square_size, num_rows, num_cols, light_gray, images
from pieces.pawn import Pawn, pawns
from pieces.knight import Knight, knights
from pieces.bishop import Bishop, bishops
from pieces.rook import Rook, rooks
from pieces.queen import Queen, queens
from pieces.king import King, kings
from game.material import Material

pygame.font.init()


PIECE_IMAGES = {
    "Pawn": (pawns[0], pawns[1]),
    "Knight": (knights[0], knights[1]),
    "Bishop": (bishops[0], bishops[1]),
    "Rook": (rooks[0], rooks[1]),
    "Queen": (queens[0], queens[1]),
    "King": (kings[0], kings[1])
}


class Board(object):
  def __init__(self, player_color):
    self.player_color = player_color
    self.material = Material()
    self.move_notation = ""
    self.show_valid_moves = True
    self.show_AI_calculations = False
    self.AI_speed = "Fast"
    self.previous_move = None
    self.prev_square = None
    self.piece = None
    self.target = None
    self.captured_piece = 0
    self.hash = None
    self.board = [
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]
    ]

  def move(self, piece, row, col):
    self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
    piece.move(row, col)

  def get_piece(self, row, col):
    return self.board[row][col]

  def initiate_pieces(self):
    if self.player_color == "White":
      # Place Black pieces on top row (row 0 to 1)
      pieces = [
          Rook(0, 0, "Black"), Knight(0, 1, "Black"), Bishop(
              0, 2, "Black"), Queen(0, 3, "Black"),
          King(0, 4, "Black"), Bishop(0, 5, "Black"), Knight(
              0, 6, "Black"), Rook(0, 7, "Black"),
          Pawn(1, 0, "Black", "Down"), Pawn(
              1, 1, "Black", "Down"), Pawn(1, 2, "Black", "Down"),
          Pawn(1, 3, "Black", "Down"), Pawn(
              1, 4, "Black", "Down"), Pawn(1, 5, "Black", "Down"),
          Pawn(1, 6, "Black", "Down"), Pawn(1, 7, "Black", "Down"),

          # Place White pieces on bottom row (row 6 to 7)
          Rook(7, 0, "White"), Knight(7, 1, "White"), Bishop(
              7, 2, "White"), Queen(7, 3, "White"),
          King(7, 4, "White"), Bishop(7, 5, "White"), Knight(
              7, 6, "White"), Rook(7, 7, "White"),
          Pawn(6, 0, "White", "Up"), Pawn(
              6, 1, "White", "Up"), Pawn(6, 2, "White", "Up"),
          Pawn(6, 3, "White", "Up"), Pawn(
              6, 4, "White", "Up"), Pawn(6, 5, "White", "Up"),
          Pawn(6, 6, "White", "Up"), Pawn(6, 7, "White", "Up")
      ]
    else:
      # Place White pieces on top row (row 0 to 1)
      pieces = [
          Rook(0, 0, "White"), Knight(0, 1, "White"), Bishop(
              0, 2, "White"), Queen(0, 3, "White"),
          King(0, 4, "White"), Bishop(0, 5, "White"), Knight(
              0, 6, "White"), Rook(0, 7, "White"),
          Pawn(1, 0, "White", "Down"), Pawn(
              1, 1, "White", "Down"), Pawn(1, 2, "White", "Down"),
          Pawn(1, 3, "White", "Down"), Pawn(
              1, 4, "White", "Down"), Pawn(1, 5, "White", "Down"),
          Pawn(1, 6, "White", "Down"), Pawn(1, 7, "White", "Down"),

          # Place Black pieces on bottom row (row 6 to 7)
          Rook(7, 0, "Black"), Knight(7, 1, "Black"), Bishop(
              7, 2, "Black"), Queen(7, 3, "Black"),
          King(7, 4, "Black"), Bishop(7, 5, "Black"), Knight(
              7, 6, "Black"), Rook(7, 7, "Black"),
          Pawn(6, 0, "Black", "Up"), Pawn(
              6, 1, "Black", "Up"), Pawn(6, 2, "Black", "Up"),
          Pawn(6, 3, "Black", "Up"), Pawn(
              6, 4, "Black", "Up"), Pawn(6, 5, "Black", "Up"),
          Pawn(6, 6, "Black", "Up"), Pawn(6, 7, "Black", "Up")
      ]

    for piece in pieces:
      self.board[piece.row][piece.col] = piece

  def create_board(self, window, theme):
    my_font = pygame.font.SysFont("calibri", 15)
    letters = ["a", "b", "c", "d", "e", "f", "g", "h"]

    # Draw squares and background
    window.fill(theme[0])
    for row in range(num_rows):
      for col in range(num_cols):
        if (row + col) % 2 == 0:
          pygame.draw.rect(
            window, theme[1], (row * square_size, col * square_size, square_size, square_size))

    # Draw board letters and numbers
    for i in range(0, 8):
      text = my_font.render(letters[i], True, (0, 0, 0))
      window.blit(text, (square_size * i + 2,
                  square_size * 7 + square_size - 20))

      text = my_font.render(str(8 - i), True, (0, 0, 0))
      window.blit(text, (square_size * 0 + 2, square_size * i + 5))

    # Draw move history
    pygame.draw.rect(window, (255, 255, 255), (10, 490, 700, 140))

  def draw(self, window, board):
    for row in board.board:
      for piece in row:
        if isinstance(piece, (Pawn, Knight, Bishop, Rook, Queen, King)):
          piece_image = PIECE_IMAGES[type(piece).__name__]
          image = piece_image[0] if piece.color == "White" else piece_image[1]
          piece.draw(window, image)

  def promotion_menu(self, color, window):
    if color == "White":
      self.draw_promotion_window(
        queens[0], rooks[0], bishops[0], knights[0], window)
    else:
      self.draw_promotion_window(
        queens[1], rooks[1], bishops[1], knights[1], window)

  def draw_promotion_window(self, queen, rook, bishop, knight, window):
    for i, piece in enumerate([queen, rook, bishop, knight]):
      pygame.draw.rect(window, light_gray, (540 + i % 2 * square_size,
                                            180 + i // 2 * square_size, square_size, square_size))
      window.blit(piece, (540 + i % 2 * square_size,
                          180 + i // 2 * square_size))

  def draw_theme_window(self, window):
    # Blue
    window.blit(images[0], (500, 115))

    # Purple
    window.blit(images[1], (570, 115))

    # Red
    window.blit(images[2], (640, 115))

  def draw_game_buttons(self, window, theme):
    my_font = pygame.font.SysFont("calibri", 13)
    buttons = [
        ("Resign/Quit", (483, 328, 74, 39), (485, 330, 70, 35)),
        ("Visualize AI", (563, 328, 74, 39), (565, 330, 70, 35)),
        ("Speed", (563, 373, 74, 39), (565, 375, 70, 35)),
        ("Highlight Valid Moves", (643, 328, 74, 39), (645, 330, 70, 35))
      ]

    for label, button_rect, draw_rect in buttons:
      text = my_font.render(label, True, (0, 0, 0))
      pygame.draw.rect(window, [0, 0, 0], button_rect)
      pygame.draw.rect(window, [255, 255, 255], draw_rect)
      window.blit(text, (draw_rect[0] + 3, draw_rect[1] + 10))

  def draw_valid_moves(self, moves, window):
    for move in moves:
      row, col = move
      self.draw_move_square(col, row, [128, 5, 242], window)

  def draw_previous_move(self, window):
    if self.previous_move is not None:
      for move in self.previous_move:
        row, col = move
        self.draw_move_square(col, row, [21, 35, 230], window)

  def draw_move_square(self, row, col, color, window):
    pygame.draw.rect(window, color, (row * square_size, col *
                     square_size, square_size + 1, square_size + 1), 2)

  def get_all_pieces(self, color):
    pieces = []
    for row in self.board:
      for piece in row:
        if isinstance(piece, (Pawn, Knight, Bishop, Rook, Queen, King)) and piece.color == color:
          pieces.append(piece)
    return pieces
