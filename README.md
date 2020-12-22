How to Run:
* Running the chess.py file will start the game!

* Local Multiplayer
* Player vs Computer
   * AI implements the minimax algorithm to determine its moves.


* Implemented:
    * Game Graphics
    * Tile indicators that show available moves for the piece that you have selected.
        * Also shows the previous move that was made.
    * Draw by threefold repetition.
    * Draw by stalemate (no valid moves remaining).
    * Draw by insufficient material.
    * Draw by 50 moves no captures.
    * Checkmate Detection.
    * Material tracker (displays captured pieces and advantage).
    * A move history log with chess notation.
    * Long and Short Side Castling.
        * Detects if enemy has any pieces looking at the castling path!
    * En Passant Rule
    * Pawn Promotion.
    * Invalid move prevention.
    * Switch colors after every game.
   
* To Implement:
    * Update Chess Notation 
        * If two or more identical pieces can move to the same square, need to write which one is moving


* If you are playing against the AI, try not to click anything unless it is your turn.
    * Clicking on the screen while the AI is thinking will cause the window to freeze until it is done thinking.


How the Minimax Algorithm Works:
As you increase the depth, the AI will play better, at the cost of taking exponentially more time to calculate its best move.
* To learn more, visit https://www.chessprogramming.org/Minimax or https://en.wikipedia.org/wiki/Minimax

* At a depth of 1, the AI will only calculate the move that immediately betters its current position without thinking about the future repurcussions of its move. This means that if the AI is given an opportunity to take a piece, it always will. (The AI will prioritize pieces with higher values, ex. Capturing Queen > Capturing Knight) 
* At a depth of 2, the AI will calculate its current best move, along with calculating your best move if they make that particular move. Calculating the strength of the moves is where the minimax algorithm comes in. It tries to minimize the strength of your best move, while also maximizing the strength of the computer's position.
* At a depth of 3, the AI is able to calculate its current best move, calculate your best move in response, and then calculate

I also implemented Alpha Beta Pruning to optimize the minimax algorithm. The minimax algorithm is particularly slow when it comes to large games such as chess, because there are so many different moves and positions that can occur and the minimax algorithm needs to search through all of the moves. Alpha Beta Pruning
* To learn more, visit https://www.chessprogramming.org/Alpha-Beta or https://en.wikipedia.org/wiki/Alpha%E2%80%93beta_pruning

Cool Feature:
You are able to turn on a visualizer to see the AI calculating its move in real time. This feature will slow the AI down a lot, so it is not recommended to play a full game with this feature on, but rather to learn how the minimax algorithm works.

The chess AI can hold its own in most situations, but has no grasp of positional concepts or mid to late game tactics/evaluations. The strength of my AI depends on the strength and complexity of my evaluation function, which is currently a very simple evaluation. It calculates the material still left on the board (pieces), and then calculates the relative strength of each individual piece based on its position on the board using piece square tables.
* To learn more, visit https://www.chessprogramming.org/Simplified_Evaluation_Function

Chess Assets were taken from this free media repository: https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent