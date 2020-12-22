from pieces.pawn import Pawn
from pieces.knight import Knight
from pieces.bishop import Bishop
from pieces.rook import Rook
from pieces.queen import Queen
from pieces.king import King


class Human(object):
    def __init__(self, color, game):
        self.color = color
        self.game = game
        self.selected_piece = None
        self.valid_moves = []
        self.promoting = False

    def select(self, row, col, mouse_xy):
        if row < 8 and col < 8 and not self.promoting:
            if self.selected_piece:
                result = self.move(row, col)
                if not result:
                    self.selected_piece = None
                    self.valid_moves = []

            piece = self.game.board.get_piece(row, col)
            if isinstance(piece, (Pawn, Knight, Bishop, Rook, Queen, King)) and piece.color == self.game.turn:
                self.selected_piece = piece
                self.game.update_all_valid_moves()
                self.valid_moves = piece.valid_moves
                return True

        if self.promoting:
            if (row, col) == (9, 3):
                self.promote(Queen, self.selected_piece.row, self.selected_piece.col)
            elif (row, col) == (10, 3):
                self.promote(Rook, self.selected_piece.row, self.selected_piece.col)
            elif (row, col) == (9, 4):
                self.promote(Bishop, self.selected_piece.row, self.selected_piece.col)
            elif (row, col) == (10, 4):
                self.promote(Knight, self.selected_piece.row, self.selected_piece.col)

        # Changing Theme
        if 500 < mouse_xy[0] < 560 and 115 < mouse_xy[1] < 175:
            self.game.theme = 0
        elif 570 < mouse_xy[0] < 630 and 115 < mouse_xy[1] < 175:
            self.game.theme = 1
        elif 640 < mouse_xy[0] < 700 and 115 < mouse_xy[1] < 175:
            self.game.theme = 2

        # Clicking on Game Buttons
        if 485 < mouse_xy[0] < 555 and 330 < mouse_xy[1] < 365:
            self.game.resign = True
        elif 565 < mouse_xy[0] < 635 and 330 < mouse_xy[1] < 365:
            self.game.show_AI_calculations = not self.game.show_AI_calculations
        elif 645 < mouse_xy[0] < 715 and 330 < mouse_xy[1] < 365:
            self.game.show_valid_moves = not self.game.show_valid_moves
        return False

    def move(self, row, col):
        piece = self.game.board.get_piece(row, col)
        prev_row = self.selected_piece.row
        prev_col = self.selected_piece.col
        move_str = ""

        if (row, col) not in self.selected_piece.valid_moves:
            return False

        # Player is trying to castle
        if isinstance(self.selected_piece, King) and isinstance(piece, Rook) \
                and self.selected_piece.color == piece.color and (row, col) in self.valid_moves:
            dangerous_squares = self.game.get_dangerous_squares()
            if self.game.castle(self.selected_piece, piece, row, col, dangerous_squares, self.game.board):
                move_str = self.game.board.move_notation
                move_str = self.game.move_creates_check(move_str)
                self.game.move_history.move_log.append(move_str)
                self.game.board.previous_move = [(prev_row, prev_col), (row, col)]
                self.game.update_game()
                self.game.update_screen(self.valid_moves, self.game.board)

        # Capturing an enemy piece
        if isinstance(piece, (Pawn, Knight, Bishop, Rook, Queen)) and self.selected_piece.color != piece.color:
            self.game.board.board[row][col] = 0
            self.game.board.move(self.selected_piece, row, col)

            # If moving the piece puts you in check, undo it
            if self.game.king_checked():
                self.game.board.move(self.selected_piece, prev_row, prev_col)
                self.game.board.board[row][col] = piece
                return False
            else:
                if isinstance(self.selected_piece, (Rook, King)):
                    self.selected_piece.can_castle = False
                if isinstance(self.selected_piece, (Knight, Bishop, Rook, Queen, King)):
                    move_str = self.selected_piece.letter + "x" + \
                               self.game.move_history.get_file(row) + str(abs(8 - col))
                elif isinstance(self.selected_piece, Pawn):
                    if abs(self.selected_piece.col - prev_col) <= 1:
                        self.selected_piece.vulnerable_to_en_passant = False
                    move_str = self.game.move_history.get_file(prev_row) + "x" + \
                        self.game.move_history.get_file(row) + str(abs(8 - col))
                    if self.game.detect_promotion(self.selected_piece):
                        self.promoting = True

                self.game.capture(piece)
                move_str = self.game.move_creates_check(move_str)
                self.game.move_history.move_log.append(move_str)
                self.game.board.previous_move = [(prev_row, prev_col), (row, col)]
                self.game.update_game()

        # Moving to an empty square
        if self.selected_piece and piece == 0 and (row, col) in self.valid_moves:
            self.game.board.move(self.selected_piece, row, col)

            # If moving the piece puts you in check, undo it
            if self.game.king_checked():
                self.game.board.move(self.selected_piece, prev_row, prev_col)
                return False
            else:
                if isinstance(self.selected_piece, (Knight, Bishop, Rook, Queen, King)):
                    move_str = self.selected_piece.letter + self.game.move_history.get_file(row) + str(abs(8 - col))

                    # If a king or a rook moves before castling, it can no longer castle
                    if isinstance(self.selected_piece, (Rook, King)):
                        self.selected_piece.can_castle = False
                elif isinstance(self.selected_piece, Pawn):
                    # If a pawn only moves 1 square, it is not vulnerable to en passant
                    if abs(self.selected_piece.col - prev_col) <= 1:
                        self.selected_piece.vulnerable_to_en_passant = False

                    # Pawn captures by en passant
                    if self.selected_piece.direction == "Up":
                        piece = self.game.board.board[self.selected_piece.row][self.selected_piece.col + 1]
                        if isinstance(piece, Pawn):
                            self.game.board.board[self.selected_piece.row][self.selected_piece.col + 1] = 0
                            self.game.capture(piece)
                            move_str = self.game.move_history.get_file(row) + "x" + str(abs(8 - col))
                        else:
                            move_str = self.game.move_history.get_file(row) + str(abs(8 - col))
                    else:
                        piece = self.game.board.board[self.selected_piece.row][self.selected_piece.col - 1]
                        if isinstance(piece, Pawn):
                            self.game.board.board[self.selected_piece.row][self.selected_piece.col - 1] = 0
                            self.game.capture(piece)
                            move_str = self.game.move_history.get_file(row) + "x" + str(abs(8 - col))
                        else:
                            move_str = self.game.move_history.get_file(row) + str(abs(8 - col))

                    if self.game.detect_promotion(self.selected_piece):
                        self.promoting = True

                move_str = self.game.move_creates_check(move_str)
                self.game.move_history.move_log.append(move_str)
                self.game.board.previous_move = [(prev_row, prev_col), (row, col)]
                self.game.update_game()

        # Check if stalemate or checkmate
        self.game.check_game_status()

        # Reset selected piece
        if not self.game.detect_promotion(self.selected_piece):
            self.selected_piece = None

        self.game.update_screen(self.valid_moves, self.game.board)

        return True

    def promote(self, choice, row, col):
        self.game.board.board[row][col] = choice(row, col, self.color)
        self.promoting = False
        self.game.board.material.update_advantages(self.game.board)
