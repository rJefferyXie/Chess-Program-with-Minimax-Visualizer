import pygame
from pieces import pawn, knight, bishop, rook, queen, king
from game.zobrist import ZobristHashing
from game.profiler import Profiler

class Computer(object):
  WHITE = "White"
  BLACK = "Black"

  # Piece Evaluations from https://www.chessprogramming.org/Simplified_Evaluation_Function
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
    self.profiler = Profiler()
    self.color = color
    self.transposition_table = {}
    
    # These values provide the user valuable information about the current state of the minimax search
    self.moves_evaluated = 0
    self.total_moves_found = 0
    self.current_best_evaluation = 0
    
    self.zobrist = ZobristHashing(8, 8, [ptype.__name__ for ptype in self.PIECE_TYPES], [self.WHITE, self.BLACK])

  def minimax(self, board, game, depth, alpha, beta, max_player):
    """
    Implements the Minimax algorithm to calculate the move that would maximize the AI's positional evaluation.
    Includes alpha-beta pruning to reduce the size of the search tree and reduce redundant computations.
    """
    if depth == 0 or game.game_over():
      return self.evaluate_board(board), board

    best_move = None
    best_score = float("-inf") if max_player == self.WHITE else float("inf")
    other_player = self.BLACK if max_player == self.WHITE else self.WHITE

    all_moves = self.get_all_moves(board, game, max_player)
    self.total_moves_found += len(all_moves)
    for piece, move in all_moves:
      position = self.simulate_move(piece, board, game, move, max_player)
      self.draw_AI_calculations(game, piece, position)
      current_score, _ = self.minimax(position, game, depth - 1, alpha, beta, other_player)
      self.undo_move(board, game)

      if max_player == self.WHITE:
        if current_score > best_score:
          best_score = current_score
          best_move = (piece, move)
          alpha = max(alpha, best_score)

      if max_player == self.BLACK:
        if current_score < best_score:
          best_score = current_score
          best_move = (piece, move)
          beta = min(beta, best_score)
          
      self.current_best_evaluation = best_score

      # if beta <= alpha, it means that the maximizing player already has a move with a better outcome than the current branch's best possible outcome
      # this means that we can can prune this branch to reduce unneccessary computations since we know that the maximizing player will never choose this branch
      # ASIDE: alpha-beta pruning assumes that both players are making optimal moves to maximize or minimize their respective scores
      if beta <= alpha:
        break

    return best_score, best_move

  @Profiler.profile_function
  def get_piece_value(self, piece):
    """
    Calculate the value of a piece using material and positional evaluation.
    """
    piece_key = (piece.color, type(piece).__name__)
    piece_material, piece_eval_table = self.PIECE_EVALUATION_TABLES[piece_key]
    return piece_material + piece_eval_table[piece.row][piece.col]

  @Profiler.profile_function
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
        if not piece:
          continue
        
        if piece.color == self.BLACK:
          position_eval -= self.get_piece_value(piece)
        else:
          position_eval += self.get_piece_value(piece)

    self.transposition_table[board_hash] = position_eval
    return position_eval

  @Profiler.profile_function
  def get_all_moves(self, board, game, color):
    """
    Generates all possible moves for each piece that the player owns.
    """
    all_moves = []
    passive_moves = []
    moves_with_capture = []

    # for each piece that the current player controls, get all valid moves and add them to result
    for piece in board.get_all_pieces(color):
      if isinstance(piece, pawn.Pawn):
        piece.update_valid_moves(board.board, game.move_history.move_log)
      else:
        piece.update_valid_moves(board.board)

      for row, col in piece.valid_moves:
        if board.board[row][col] != 0 and board.get_piece(row, col).color != color:
          moves_with_capture.append((piece, (row, col)))
        else:
          passive_moves.append((piece, (row, col)))

    moves_with_capture = self.order_moves(moves_with_capture, board.board)

    # by using move ordering and putting moves where the AI captured a piece first, we evaluate the moves
    # that are likely to be the strongest earlier in the search tree, making alpha-beta pruning more efficient.
    all_moves.extend(moves_with_capture)
    all_moves.extend(passive_moves)
    return all_moves

  @Profiler.profile_function
  def order_moves(self, moves, board):
    def mvv_lva(move):  # https://www.chessprogramming.org/MVV-LVA
      piece, (targetRow, targetCol) = move
      return self.get_piece_value(board[targetRow][targetCol]) - self.get_piece_value(piece)

    return sorted(moves, key=mvv_lva, reverse=True)

  def draw_AI_calculations(self, game, piece, board):
    """
    If the user has enabled the visualize AI feature, show the current position that the AI is considering after every move.
    """    
    self.moves_evaluated += 1

    if not game.board.show_AI_calculations:
      return
    
    if game.board.AI_speed == "Medium":
      pygame.time.delay(20)
    elif game.board.AI_speed == "Slow":
      pygame.time.delay(50)

    self.draw_moves(piece, game, board)

  @Profiler.profile_function
  def simulate_move(self, piece, board, game, move, color):
    """
    Simulates a move on the board.
    """
    target = board.get_piece(move[0], move[1])

    board.prev_square = (piece.row, piece.col)
    board.piece = piece
    board.target = (move[0], move[1])

    # Save state for undoing the move
    board.stored_moves.append({
      'piece': piece,
      'from': board.prev_square,
      'to': move,
      'captured': target,
      'can_castle': getattr(piece, 'can_castle', None),
    })

    # simulating a castling move
    if isinstance(piece, king.King) and isinstance(target, rook.Rook) and piece.color == target.color:
      game.castle(piece, target, game.get_dangerous_squares(), board)
      board.stored_moves[-1]['rook'] = target
      board.stored_moves[-1]['rook_from'] = (move[0], move[1])

    else:
      # simulating capturing opponents piece
      if target != 0 and target.color != color:  
        board.board[move[0]][move[1]] = 0
        board.captured_piece = target

      board.move(piece, move[0], move[1])

      if game.detect_promotion(piece):
        # for simplicity, the computer will always promote to a queen
        board.board[piece.row][piece.col] = queen.Queen(piece.row, piece.col, piece.color)

    # after a rook or king moves, it can no longer castle
    if isinstance(piece, (rook.Rook, king.King)):
      piece.can_castle = False

    # Initialize the hash if not already set
    if not board.hash:
      board.hash = self.zobrist.calculate_hash(board)

    # Update the Zobrist hash
    board.hash = self.zobrist.update_hash(board.hash, piece, board.prev_square, board.target)

    return board

  @Profiler.profile_function
  def undo_move(self, board, game):
    # Restore previous move data
    move_data = board.stored_moves.pop()
    piece = move_data['piece']
    from_square = move_data['from']
    to_square = move_data['to']
    captured_piece = move_data['captured']
    can_castle = move_data['can_castle']

    # Undo castling moves
    if isinstance(piece, king.King) and move_data.get('rook'):
      rook_piece = move_data.get('rook')  # Retrieve stored rook
      if rook_piece:
        rook_from = move_data['rook_from']

        # Ensure the rook moves back to its original position
        board.move(rook_piece, rook_from[0], rook_from[1])

    # Revert the piece's position
    board.move(piece, from_square[0], from_square[1])

    # Restore the captured piece, if any
    if captured_piece and captured_piece.color != piece.color:
      board.board[to_square[0]][to_square[1]] = captured_piece
      board.captured_piece = 0

    # Undo any pawn promotion
    if isinstance(piece, queen.Queen) and game.detect_promotion(piece):
      board.board[from_square[0]][from_square[1]] = pawn.Pawn(from_square[0], from_square[1], piece.color)

    # Restore the castling ability for rook or king if it was altered
    if isinstance(piece, (king.King, rook.Rook)) and can_castle is not None:
      piece.can_castle = can_castle

    # Revert Zobrist hash
    board.hash = self.zobrist.update_hash(board.hash, piece, to_square, from_square)

  def draw_moves(self, piece, game, board):
    valid_moves = piece.valid_moves
    game.update_screen(valid_moves, board)
  
  def reset_visualizer_stats(self):
    self.moves_evaluated = 0
    self.total_moves_found = 0
    self.current_best_evaluation = 0

  def computer_move(self, game, move):
    board = self.simulate_move(move[0], game.board, game, move[1], self.color)
    game.board.board = board.board

    if isinstance(board.piece, pawn.Pawn):
      if isinstance(board.captured_piece, self.PIECE_TYPES):
        board.move_notation = game.move_history.get_file(board.piece.col) + "x" + \
            game.move_history.get_file(
            board.target[1]) + str(abs(8 - board.target[0]))
      else:
        board.move_notation = game.move_history.get_file(
          board.target[1]) + str(abs(8 - board.target[0]))
    else:
      if isinstance(board.captured_piece, self.PIECE_TYPES):
        if board.captured_piece.color != board.piece.color:
          board.move_notation = board.piece.letter + "x" + \
              game.move_history.get_file(
                board.target[1]) + str(abs(8 - board.target[0]))
      else:
        board.move_notation = board.piece.letter + \
            game.move_history.get_file(
              board.target[1]) + str(abs(8 - board.target[0]))
    if board.captured_piece != 0 and board.captured_piece.color != board.piece.color:
      game.capture(board.captured_piece)
    game.move_history.move_log.append(board.move_notation)
    game.board.previous_move = [
      (board.prev_square[0], board.prev_square[1]), (board.target[0], board.target[1])]
    game.update_game()
    game.check_game_status()

    self.profiler.print_profile_summary()
    self.profiler.reset_profiler()