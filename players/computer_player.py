from copy import deepcopy
from pieces.pawn import Pawn, black_pawn_eval_table, white_pawn_eval_table
from pieces.knight import Knight, black_knight_eval_table, white_knight_eval_table
from pieces.bishop import Bishop, black_bishop_eval_table, white_bishop_eval_table
from pieces.rook import Rook, black_rook_eval_table, white_rook_eval_table
from pieces.queen import Queen, black_queen_eval_table, white_queen_eval_table
from pieces.king import King, black_king_eval_table, white_king_eval_table
import pygame

# Piece Evaluations from https://www.chessprogramming.org/Simplified_Evaluation_Function

class Computer(object):
    def __init__(self, color):
        self.color = color

        self.white_piece_eval_tables = {
            "Pawn": (100, white_pawn_eval_table),
            "Knight": (320, white_knight_eval_table),
            "Bishop": (330, white_bishop_eval_table),
            "Rook": (500, white_rook_eval_table),
            "Queen": (900, white_queen_eval_table),
            "King": (20000, white_king_eval_table)
        }

        self.black_piece_eval_tables = {
            "Pawn": (100, black_pawn_eval_table),
            "Knight": (320, black_knight_eval_table),
            "Bishop": (330, black_bishop_eval_table),
            "Rook": (500, black_rook_eval_table),
            "Queen": (900, black_queen_eval_table),
            "King": (20000, black_king_eval_table)
        }

    def minimax(self, board, game, depth, alpha, beta, max_player):
        if depth == 0 or game.game_over():
            return self.evaluate(board), board

        if max_player == "White":
            max_evaluation = float("-inf")
            best_position = None
            for position in self.get_all_positions(board, game, "White"):
                current_evaluation = self.minimax(position, game, depth - 1, alpha, beta, "Black")[0]

                # If the current move was the best one so far, update best_position
                if current_evaluation > max_evaluation:
                    best_position = position
                    max_evaluation = current_evaluation

                # Update alpha
                alpha = max(alpha, max_evaluation)
                if beta <= alpha:
                    return max_evaluation, best_position

            return max_evaluation, best_position

        else:
            min_evaluation = float("inf")
            best_position = None
            for position in self.get_all_positions(board, game, "Black"):
                current_evaluation = self.minimax(position, game, depth - 1, alpha, beta, "White")[0]

                # If the current move was the best one so far, update best_position
                if current_evaluation < min_evaluation:
                    best_position = position
                    min_evaluation = current_evaluation
                
                # Update beta
                beta = min(beta, current_evaluation)
                if beta <= alpha:
                    return min_evaluation, best_position

            return min_evaluation, best_position

    def get_piece_eval(self, piece):
        piece_material = 0
        piece_eval_table = []

        if piece.color == "White":
            piece_material, piece_eval_table = self.white_piece_eval_tables[piece.__class__.__name__]
            
        if piece.color == "Black":
            piece_material, piece_eval_table = self.black_piece_eval_tables[piece.__class__.__name__]
        
        return piece_material + piece_eval_table[piece.row][piece.col]

    def evaluate(self, board):
        position_eval = 0
        for row in board.board:
            for piece in row:
                if isinstance(piece, (Pawn, Knight, Bishop, Rook, Queen, King)):
                    if piece.color == "Black":
                        position_eval -= self.get_piece_eval(piece)
                    else:
                        position_eval += self.get_piece_eval(piece)

        return position_eval

    def get_all_positions(self, board, game, color):
        boards = []

        # Get every piece on the board that is the same color as the current player's team, and update valid moves
        for piece in board.get_all_pieces(color):
            if isinstance(piece, Pawn):
                valid_moves = piece.update_valid_moves(board.board, game.move_history.move_log)
            else:
                valid_moves = piece.update_valid_moves(board.board)
            
            # Simulate each move and add the new board to boards
            for move in valid_moves:
                temp_board = deepcopy(board)
                temp_piece = temp_board.get_piece(piece.row, piece.col)
                new_temp_board = self.simulate_move(temp_piece, temp_board, game, move, color)
                
                if game.board.show_AI_calculations:
                    if game.board.AI_speed == "Medium":
                        pygame.time.delay(20)
                    elif game.board.AI_speed == "Slow":
                        pygame.time.delay(50)

                    self.draw_moves(piece, game, new_temp_board)
                boards.append(new_temp_board)

        return boards

    def simulate_move(self, piece, board, game, move, color):
        target = board.get_piece(move[0], move[1])

        board.prev_square = (piece.row, piece.col)
        board.piece = piece
        board.target = (move[0], move[1])
        board.captured_piece = target

        # Castling
        if isinstance(piece, King) and isinstance(target, Rook) and piece.color == target.color:
            dangerous_squares = game.get_dangerous_squares()
            game.castle(piece, target, move[0], move[1], dangerous_squares, board)
        else:
            if target != 0 and target.color != color:
                board.board[move[0]][move[1]] = 0

            board.move(piece, move[0], move[1])

            # Promote the pawn
            if game.detect_promotion(piece):
                board.board[piece.row][piece.col] = Queen(piece.row, piece.col, piece.color)

            # If a rook or king moves, it loses castling privileges
            if isinstance(piece, (Rook, King)):
                piece.can_castle = False

        return board

    def draw_moves(self, piece, game, board):
        valid_moves = piece.valid_moves
        game.update_screen(valid_moves, board)

    def computer_move(self, game, board):
        game.board.board = board.board

        if isinstance(board.piece, Pawn):
            if isinstance(board.captured_piece, (Pawn, Knight, Bishop, Rook, Queen, King)):
                board.move_notation = game.move_history.get_file(board.piece.row) + "x" + \
                       game.move_history.get_file(board.target[0]) + str(abs(8 - board.target[1]))
            else:
                board.move_notation = game.move_history.get_file(board.target[0]) + str(abs(8 - board.target[1]))
        else:
            if isinstance(board.captured_piece, (Pawn, Knight, Bishop, Rook, Queen, King)):
                if board.captured_piece.color != board.piece.color:
                    board.move_notation = board.piece.letter + "x" + \
                                          game.move_history.get_file(board.target[0]) + str(abs(8 - board.target[1]))
            else:
                board.move_notation = board.piece.letter + \
                                      game.move_history.get_file(board.target[0]) + str(abs(8 - board.target[1]))
        if board.captured_piece != 0 and board.captured_piece.color != board.piece.color:
            game.capture(board.captured_piece)
        game.move_history.move_log.append(board.move_notation)
        game.board.previous_move = [(board.prev_square[0], board.prev_square[1]), (board.target[0], board.target[1])]
        game.update_game()
        game.check_game_status()
