# Visual Chess by Jeffery Xie
A functional chess game implemented in python, with pygame as a supporting module. This program includes local multiplayer and single player vs an AI, which uses the minimax algorithm to determine its moves. A special feature of this program is the "visual" aspect where the user can toggle a setting that allows them to see which moves the computer is currently considering in real time.

# Requirements and Installation
**Required Modules**
* A list of all required modules. To install, simply enter these commands into your terminal. (for macOS users, replace pip with pip3)
* pip install pygame
  * If the command above does not work, visit https://www.pygame.org/wiki/GettingStarted for help.
* pip install tkinter

**Setting up Repository**
* To clone repository, press the green "Code" button, and copy the HTTPS to your clipboard.
* Create a new project in your code editor or IDE of choice.
* Import the HTTPS url into version control on your new project.
* Two Examples:
  * If using pycharm, go to VCS --> get from version control --> paste the url --> clone
  * If using Visual Studio Code, go to explorer (ctrl + shift + e) --> clone repository --> paste the url --> clone

**Running**
* Running the chess.py file will start the program!

# Special Notes to User
* **AI Difficulties Guidelines**
  * Note that the time in between moves depends on search depth, along with the number of valid moves that the AI has.
  * Easy (Depth 2) will think for about 5-10 seconds on its moves.
  * Medium (Depth 3) will think for about 20-40 seconds on its moves.
  * Hard (Depth 4) will think for about 60-120 seconds on its moves.
* If you are playing against the AI, try not to click anything unless it is your turn.
    * Clicking on the screen while the AI is thinking will cause the window to freeze until it is done thinking.

# Features
* Local Multiplayer
* Single Player vs AI
  * AI implements the minimax algorithm to determine its moves.
    * To optimize the minimax algorithm, I also implemented alpha-beta pruning to cut branches off early when they are worse than a move that has already been seen.
  * The evaluation function for the algorithm is based off of pre-determined piece values and piece square tables (How much a piece is worth, plus the relative strength of the piece in respect to its position on the board).
  * A togglable feature that shows the AI thinking in real time, displaying all board outcomes from the possible moves.
* A move history log with standard chess notation.
* Tile indicators that show available moves for the piece that you have selected (toggleable).
  * Also shows the previous move that was made.
* Variety of chess board themes to choose from.
* Material tracker that displays captured pieces and advantages.
  
# Implemented Game Mechanics
* Checkmate Detection.
* Long and Short Side Castling.
    * Detects if enemy has any pieces looking at the castling path!
* En Passant
* Pawn Promotion.
* Invalid move prevention.
* Draw by threefold repetition.
* Draw by stalemate (no valid moves remaining).
* Draw by insufficient material.
* Draw by 50 moves no captures.

# Future Implementations
* Update Chess Notation 
  * If two or more identical pieces can move to the same square, need to write which one is moving
* Update Evaluations
  * Improving the Evaluation function will improve the effectiveness of the alpha-beta pruning, and will give better moves.
    * Ex. Knight outpost, X-ray on king, doubled pawns, rook on empty file, etc.
* Filter the valid moves such that the AI cannot make a move that leaves it in check.
* Flip the board around after each turn so the top player has an easier time reading the position. (Think about how it actually looks when you're playing a real chess game over the board).
* Try implementing Quiescence search to mitigate the *horizon effect* and to make more sensible moves. Quiescence search focuses on searching in greater depths for move trees that are logical and advantageous, while realising very early on if a particular move tree is losing and if so will skip it (similar to how a human would play).
  * The horizon effect is a problem that can occur when every branch (move tree) is searched to a fixed depth. Dangerous threats and positional weaknesses beyond the fixed depth will not be detected and the AI will not realize the mistakes that it made until it is too late. 

# Known Bugs
  * Chess AI can sometimes make a move while in check that does not result in it escaping check (illegal move). (This does not happen in local multiplayer)

# Extra Information
The chess AI can hold its own in most situations, but has no grasp of positional concepts or mid to late game tactics/evaluations. The strength of my AI depends on the strength and complexity of my evaluation function, which is currently a very simple evaluation. It calculates the material still left on the board (pieces), and then calculates the relative strength of each individual piece based on its position on the board using piece square tables.
* To learn more, visit https://www.chessprogramming.org/Simplified_Evaluation_Function

*My Favorite Feature*
* You are able to turn on a visualizer to see the AI calculating its move in real time. This feature will slow the AI down a lot, so it is not recommended to play a full game with this feature on, it should be used to visually learn how the minimax algorithm works.

*Minimax Algorithm*
* In zero-sum games such as chess and checkers where one player winning means that the other player has to lose, the minimax algorithm can be used to create an AI. The minimax algorithm calculates the relative strength of each player on the board and returns a number based on its evaluation function. The min player (black in chess), makes moves that will make the evaluation of the current board as small as possible, and the max player (white in chess) will make moves that make the evaluation of the current board as big as possible. 
  * To learn more, visit https://www.chessprogramming.org/Minimax
* As you increase the depth, the AI will play better, at the cost of taking exponentially more time to calculate its best move.
  * At a depth of 1, the AI will look through all of its available moves for its pieces and calculates the best move that improves its current position without thinking about the future repurcussions of its move. This means that if the AI is given an opportunity to take a piece, it always will. (The AI will prioritize pieces with higher values, ex. Capturing Queen > Capturing Knight) 
  * At a depth of 2, the AI will calculate its current best move, along with calculating your best move if they make that particular move. Calculating the strength of the moves is where the minimax algorithm comes in. It tries to minimize the strength of your best response, while also maximizing the strength of its move.
  * At a depth of 3, the AI is able to calculate its position after its current best move, calculate the position after your best move in response, and then assuming you make the best possible move (up to the standards of the eval function), it can also calculate its next best move and position.

*Alpha Beta Pruning*
* I also implemented Alpha Beta Pruning to optimize the minimax algorithm. The minimax algorithm is particularly slow when it comes to large games such as chess, because there are so many different moves and positions that can occur and the minimax algorithm needs to search through all of the moves. Alpha Beta Pruning keeps track of the best move seen so far, and will cut branches off early when it sees that the move that it is currently evaluating is worse than the current best move.
  * To learn more, visit https://www.chessprogramming.org/Alpha-Beta

Chess Assets were downloaded from this free media repository: https://commons.wikimedia.org/wiki/Category:PNG_chess_pieces/Standard_transparent
