import pygame
from game.board import Board
from pieces.pawn import Pawn
from pieces.knight import Knight
from pieces.bishop import Bishop
from pieces.rook import Rook
from pieces.queen import Queen
from pieces.king import King
from game.move_history import MoveHistory
from game.constants import themes
from players.human_player import Human
from players.computer_player import Computer


class Game(object):
  def __init__(self, window, player_color, theme):
    self.window = window
    self.theme = theme
    self.move_history = MoveHistory()
    self.human = Human(player_color, self)
    self.board = Board(player_color)
    self.computer = Computer("Black" if player_color == "White" else "White")
    self.turn = "White"

    # Game Over Conditions
    self.checkmate_win = False
    self.stalemate_draw = False
    self.threefold_draw = False
    self.no_captures_50 = False
    self.insufficient_material_draw = False
    self.resign = False

  def game_over(self):
    return any([self.checkmate_win, self.stalemate_draw, self.threefold_draw,
                self.no_captures_50, self.insufficient_material_draw, self.resign])

  def update_screen(self, valid_moves, board):
    # Draw Board
    self.board.create_board(self.window, themes[self.theme])

    # Draw Previous Move
    self.board.draw_previous_move(self.window)

    # Draw all valid moves for selected piece
    if self.board.show_valid_moves:
      self.board.draw_valid_moves(valid_moves, self.window)

    # Draw change theme buttons
    self.board.draw_theme_window(self.window)

    # Draw Game Buttons
    self.board.draw_game_buttons(self.window, themes[self.theme])

    # Draw Move Log
    self.move_history.draw_move_log(self.window)

    # Draw captured and advantages
    self.board.material.draw_captured(self.window, self.human.color)
    self.board.material.draw_advantages(self.window, self.human.color)

    # Draw the chess pieces
    self.board.draw(self.window, board)

    # Draw Promotion Menu
    if self.human.promoting:
      self.board.promotion_menu(self.human.color, self.window)

    # Update the screen
    pygame.display.update()

  def update_game(self):
    self.board.material.update_advantages(self.board)
    self.change_turn()
    self.update_all_valid_moves()

  def check_game_status(self):
    if self.king_checked():
      self.checkmate()
    self.stalemate()
    self.threefold_repetition()
    self.insufficient_material()
    self.no_captures_in_50()

  def update_all_valid_moves(self):
    for row in self.board.board:
      for piece in row:
        if isinstance(piece, (Knight, Bishop, Rook, Queen, King)):
          piece.update_valid_moves(self.board.board)
        elif isinstance(piece, Pawn):
          piece.update_valid_moves(
            self.board.board, self.move_history.move_log)

  def get_dangerous_squares(self):
    dangerous_squares = []
    for row in self.board.board:
      for piece in row:
        if isinstance(piece, (Pawn, Knight, Bishop, Rook, Queen, King)):
          if piece.color != self.turn:
            dangerous_squares.extend(piece.valid_moves)

    return dangerous_squares

  def king_checked(self):
    self.update_all_valid_moves()
    king = None
    dangerous_squares = self.get_dangerous_squares()
    king_pos = (None, None)
    for row in self.board.board:
      for piece in row:
        if isinstance(piece, King) and piece.color == self.turn:
          king_pos = (piece.row, piece.col)
          king = piece
          break

    if king_pos in dangerous_squares:
      king.is_checked = True
      return True

    king.is_checked = False
    return False

  def checkmate(self):
    for row in self.board.board:
      for piece in row:

        # Get all pieces that are the same color as the king in check
        if isinstance(piece, (Pawn, Knight, Bishop, Rook, Queen, King)) and piece.color == self.turn:
          prev_row, prev_col = piece.row, piece.col

          # Try all the moves available for each piece to see if they can escape check
          for move in piece.valid_moves:
            target = self.board.board[move[0]][move[1]]

            # If capturing an enemy piece
            if isinstance(target, (Pawn, Knight, Bishop, Rook, Queen, King)) and target.color != self.turn:
              self.board.board[move[0]][move[1]] = 0
              self.board.move(piece, move[0], move[1])

              # If king is still checked, undo move and go next
              if self.king_checked():
                self.board.move(piece, prev_row, prev_col)
                self.board.board[move[0]][move[1]] = target

              # If king is no longer checked, then there is no checkmate yet
              else:
                self.board.move(piece, prev_row, prev_col)
                self.board.board[move[0]][move[1]] = target
                return False

            # If moving to an empty square
            else:
              self.board.move(piece, move[0], move[1])

              # If king is still checked, undo move and go next
              if self.king_checked():
                self.board.move(piece, prev_row, prev_col)

              # If king is no longer checked, then there is no checkmate yet
              else:
                self.board.move(piece, prev_row, prev_col)
                return False

    self.update_screen(self.human.valid_moves, self.board)
    self.checkmate_win = True

  def threefold_repetition(self):
    # Check for threefold repetition in the move history
    unique_moves = set(self.move_history.move_log[-9:])
    if len(self.move_history.move_log) > 9 and len(unique_moves) == 4:
      self.update_screen(self.human.valid_moves, self.board)
      self.threefold_draw = True

  def stalemate(self):
    all_valid_moves = []
    dangerous_squares = self.get_dangerous_squares()

    for row in self.board.board:
      for piece in row:
        # Get all pieces that are the same color as the current player's team
        if isinstance(piece, (Pawn, Knight, Bishop, Rook, Queen, King)) and piece.color == self.turn:

          # Go through all possible moves to see if any are legal
          if isinstance(piece, King):
            for move in piece.valid_moves:
              if move not in dangerous_squares:
                all_valid_moves.append(move)
          else:
            for move in piece.valid_moves:
              all_valid_moves.append(move)

    # If there were no legal moves for the current player, its a stalemate
    if not all_valid_moves:
      self.update_screen(self.human.valid_moves, self.board)
      self.stalemate_draw = True

  def no_captures_in_50(self):
    if len(self.move_history.move_log) > 50:
      moves = self.move_history.move_log[-50:]
      captures = [move for move in moves if "x" in move]
      if len(captures) == 0:
        self.no_captures_50 = True

  def insufficient_material(self):
    white_material = {"Knights": 0, "Bishops": 0}
    black_material = {"Knights": 0, "Bishops": 0}

    for row in self.board.board:
      for piece in row:

        # If there is a pawn, rook, or queen on the board, the game is still winnable
        if isinstance(piece, (Pawn, Rook, Queen)):
          return False

        if isinstance(piece, Knight):
          white_material["Knights"] += 1 if piece.color == "White" else 0
          black_material["Knights"] += 1 if piece.color == "Black" else 0
        if isinstance(piece, Bishop):
          white_material["Bishops"] += 1 if piece.color == "White" else 0
          black_material["Bishops"] += 1 if piece.color == "Black" else 0

    white_pieces = sum(white_material.values())
    black_pieces = sum(black_material.values())

    if white_pieces * 3 <= 3 and black_pieces * 3 <= 3:
      self.update_screen(self.human.valid_moves, self.board)
      self.insufficient_material_draw = True

  def move_creates_check(self, move):
    self.change_turn()
    if self.king_checked():
      move += "+"
    self.change_turn()
    return move

  def change_turn(self):
    self.human.valid_moves = []
    self.turn = "Black" if self.turn == "White" else "White"

  def capture(self, piece):
    if piece.color == "Black":
      self.board.material.add_to_captured_pieces(piece, self.board.material.captured_black_pieces)
    if piece.color == "White":
      self.board.material.add_to_captured_pieces(piece, self.board.material.captured_white_pieces)

  def castle(self, king, rook, row, col, dangerous_squares, board):
    # Long Castle
    if row == 0:
      if ((col + 1) and (row, col + 2) and (row, col + 3)) not in dangerous_squares:
        board.move(rook, 0, 3)
        board.move(king, 0, 2)
        board.move_notation = "O-O-O"
      else:
        return False

    # Short Castle
    elif row == 7:
      if (row, col - 1) and (row, col - 2) not in dangerous_squares:
        board.move(rook, 7, 5)
        board.move(king, 7, 6)
        board.move_notation = "O-O"
      else:
        return False

    king.can_castle = False
    return True

  def detect_promotion(self, piece):
    # If a pawn reaches the other side of the board (any promotion square, let player choose how to promote)
    if isinstance(piece, Pawn):
      if (piece.color == "White" and piece.row == 0) or (piece.color == "Black" and piece.row == 7):
        return True
    return False
