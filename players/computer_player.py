import pygame
from copy import deepcopy
from pieces import pawn, knight, bishop, rook, queen, king
import time
from functools import wraps
from game.zobrist import ZobristHashing

# Piece Evaluations from https://www.chessprogramming.org/Simplified_Evaluation_Function

profile_data = {}

def profile_function(func):
  @wraps(func)
  def wrapper(*args, **kwargs):
    start_time = time.time()
    result = func(*args, **kwargs)
    elapsed_time = time.time() - start_time

    if func.__name__ not in profile_data:
      profile_data[func.__name__] = {"total_time": 0, "call_count": 0}
    profile_data[func.__name__]["total_time"] += elapsed_time
    profile_data[func.__name__]["call_count"] += 1

    return result

  return wrapper

def print_profile_summary():
  print("\n------------ Chess Engine Profiling Summary ------------")
  for func_name, data in profile_data.items():
    total_time = data["total_time"]
    call_count = data["call_count"]

    if func_name == "simulate_move":
      print(f"{func_name}: Evaluated {call_count} moves in {total_time:.3f} seconds.")
    elif func_name == "get_all_positions":
      print(f"{func_name}: Generated {call_count} positions in {total_time:.3f} seconds.")
    elif func_name == "evaluate_board":
      print(f"{func_name}: Evaluated the board {call_count} times in {total_time:.3f} seconds.")
    elif func_name == "minimax":
      print(f"{func_name}: Completed {call_count} recursive calls in {total_time:.3f} seconds.")
    else:
      print(f"{func_name}: Executed {call_count} times in {total_time:.3f} seconds.")

class Computer(object):
    WHITE = "White"
    BLACK = "Black"

    PIECE_TYPES = (pawn.Pawn, knight.Knight, bishop.Bishop, rook.Rook, queen.Queen, king.King)
    PIECE_EVALUATION_TABLES = {
        (WHITE, "Pawn"): (100, pawn.white_pawn_eval_table),
        (WHITE, "Knight"): (320, knight.white_knight_eval_table),
        (WHITE, "Bishop"): (330, bishop.white_bishop_eval_table),
        (WHITE, "Rook"): (500, rook.white_rook_eval_table),
        (WHITE, "Queen"): (900, queen.white_queen_eval_table),
        (WHITE, "King"): (20000, king.white_king_eval_table),

        (BLACK, "Pawn"): (100, pawn.black_pawn_eval_table),
        (BLACK, "Knight"): (320, knight.black_knight_eval_table),
        (BLACK, "Bishop"): (330, bishop.black_bishop_eval_table),
        (BLACK, "Rook"): (500, rook.black_rook_eval_table),
        (BLACK, "Queen"): (900, queen.black_queen_eval_table),
        (BLACK, "King"): (20000, king.black_king_eval_table),
    }

    def __init__(self, color):
        self.color = color
        self.transposition_table = {}
        self.zobrist = ZobristHashing(8, 8, [ptype.__name__ for ptype in self.PIECE_TYPES], [self.WHITE, self.BLACK])

    @profile_function
    def minimax(self, board, game, depth, alpha, beta, max_player):
        """
        Implements the Minimax algorithm to calculate the move that would maximize the AI's positional evaluation. 
        Includes alpha-beta pruning to reduce the size of the search tree and reduce redundant computations.
        """
        if depth == 0 or game.game_over():
            return self.evaluate_board(board), board

        best_position = None
        best_score = float("-inf") if max_player == self.WHITE else float("inf")
        other_player = self.BLACK if max_player == self.WHITE else self.WHITE

        for position in self.get_all_positions(board, game, max_player):
            current_score, _ = self.minimax(position, game, depth - 1, alpha, beta, other_player)

            if max_player == self.WHITE:
                if current_score > best_score:
                    best_score = current_score
                    best_position = position
                    alpha = max(alpha, best_score)
            
            if max_player == self.BLACK:
                if current_score < best_score:
                    best_score = current_score
                    best_position = position
                    beta = min(beta, best_score)
                    
            # if beta <= alpha, it means that the maximizing player already has a move with a better outcome than the current branch's best possible outcome
            # this means that we can can prune this branch to reduce unneccessary computations since we know that the maximizing player will never choose this branch
            # ASIDE: alpha-beta pruning assumes that both players are making optimal moves to maximize or minimize their respective scores
            if beta <= alpha:
                break
          
        return best_score, best_position
            
    def get_piece_value(self, piece):
        """
        Calculate the value of a piece using material and positional evaluation.        
        """
        piece_key = (piece.color, type(piece).__name__)
        piece_material, piece_eval_table = self.PIECE_EVALUATION_TABLES[piece_key]

        return piece_material + piece_eval_table[piece.row][piece.col]        

    @profile_function
    def evaluate_board(self, board):
        """
        Evaluate the board state, considering material and positional advantages.        
        """
        # use the cached result if this board state has already been evaluated before
        board_hash = self.zobrist.calculate_hash(board)
        if board_hash in self.transposition_table:
            return self.transposition_table[board_hash]
                
        position_eval = 0
        for row in board.board:
            for piece in row:
                if isinstance(piece, self.PIECE_TYPES):
                    if piece.color == self.BLACK:
                        position_eval -= self.get_piece_value(piece)
                    else:
                        position_eval += self.get_piece_value(piece)

        self.transposition_table[board_hash] = position_eval
        return position_eval

    @profile_function
    def get_all_positions(self, board, game, color):
        """
        Generates all possible positions after simulating the valid moves for each piece that the player owns.
        """
        all_positions = []
        passive_positions = []
        positions_with_capture = []
        
        # for each piece that the current player controls, simulate every possible move and save the new position in positions
        for piece in board.get_all_pieces(color):
            if isinstance(piece, pawn.Pawn):
                valid_moves = piece.update_valid_moves(board.board, game.move_history.move_log)
            else:
                valid_moves = piece.update_valid_moves(board.board)
            
            for move in valid_moves:
                board_copy = deepcopy(board) # need to create a deep copy so we don't modify the original board when simulating the move
                temp_piece = board_copy.get_piece(piece.row, piece.col)
                new_temp_position, did_capture_piece = self.simulate_move(temp_piece, board_copy, game, move, color)
                
                if did_capture_piece:
                    positions_with_capture.append(new_temp_position)
                else:
                    passive_positions.append(new_temp_position)
                
                if game.board.show_AI_calculations:
                    self.draw_AI_calculations(game, piece, new_temp_position)

        # by using move ordering and putting positions where the AI captured a piece first, we evaluate the moves
        # that are likely to be the strongest earlier in the search tree, making alpha-beta pruning more efficient.
        all_positions.extend(positions_with_capture)
        all_positions.extend(passive_positions)
        return all_positions

    def draw_AI_calculations(self, game, piece, board):
        """
        If the user has enabled the visualize AI feature, show the current position that the AI is considering after every move.
        """
        if game.board.AI_speed == "Medium":
            pygame.time.delay(20)
        elif game.board.AI_speed == "Slow":
            pygame.time.delay(50)
            
        self.draw_moves(piece, game, board)

    @profile_function
    def simulate_move(self, piece, board, game, move, color):
        """
        Simulates a move on a copy of the board.
        """
        did_capture_piece = False
        target = board.get_piece(move[0], move[1])

        board.prev_square = (piece.row, piece.col)
        board.piece = piece
        board.target = (move[0], move[1])
        board.did_capture_piece = target

        if isinstance(piece, king.King) and isinstance(target, rook.Rook) and piece.color == target.color: # simulating a castling move
            dangerous_squares = game.get_dangerous_squares()
            game.castle(piece, target, move[0], move[1], dangerous_squares, board)
        else:
            if target != 0 and target.color != color: # simulating capturing opponents piece
                board.board[move[0]][move[1]] = 0
                did_capture_piece = True

            board.move(piece, move[0], move[1])

            if game.detect_promotion(piece):
                board.board[piece.row][piece.col] = queen.Queen(piece.row, piece.col, piece.color) # for simplicity, the computer will always promote to a queen

            if isinstance(piece, (rook.Rook, king.King)): # after a rook or king moves, it can no longer castle
                piece.can_castle = False
        
        # Initialize the hash if not already set
        if not board.hash:
            board.hash = self.zobrist.calculate_hash(board)

        # Update the Zobrist hash
        board.hash = self.zobrist.update_hash(board.hash, piece, board.prev_square, board.target)

        return board, did_capture_piece

    def draw_moves(self, piece, game, board):
        valid_moves = piece.valid_moves
        game.update_screen(valid_moves, board)

    def computer_move(self, game, board):
        game.board.board = board.board

        if isinstance(board.piece, pawn.Pawn):
            if isinstance(board.captured_piece, self.PIECE_TYPES):
                board.move_notation = game.move_history.get_file(board.piece.row) + "x" + \
                       game.move_history.get_file(board.target[0]) + str(abs(8 - board.target[1]))
            else:
                board.move_notation = game.move_history.get_file(board.target[0]) + str(abs(8 - board.target[1]))
        else:
            if isinstance(board.captured_piece, self.PIECE_TYPES):
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

        print_profile_summary()
        profile_data.clear()