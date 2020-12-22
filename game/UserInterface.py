import tkinter as tk
import pygame
from game.constants import width, height, square_size, themes
from game.game import Game


def position_window(root):
    root.minsize(400, 240)
    w = 400  # width of the window
    h = 240  # height of the window

    ws = root.winfo_screenwidth()  # width of the screen
    hs = root.winfo_screenheight()  # height of the screen

    # calculate x and y coordinates for the window
    x = (ws / 2) - (w / 2)
    y = (hs / 2) - (h / 2)

    # set the dimensions of the screen and where it is placed
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))


class MainMenu(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Chess")
        position_window(self.root)
        self.create_window()
        self.root.mainloop()

    def create_window(self):
        single_frame = tk.Frame(self.root, bg="lightskyblue")
        multi_frame = tk.Frame(self.root, bg="salmon1")
        single_frame.grid(row=0, column=0, sticky="nsew")
        multi_frame.grid(row=0, column=1, sticky="nsew")
        self.root.rowconfigure(0, weight=1)
        self.root.columnconfigure(0, weight=1)
        self.root.columnconfigure(1, weight=1)

        single_player = tk.Button(self.root, text="Single Player", command=self.single_player)
        single_player.place(x=50, y=100, height=40, width=100)

        local_multiplayer = tk.Button(self.root, text="Local Multiplayer", command=self.multiplayer)
        local_multiplayer.place(x=250, y=100, height=40, width=100)

    def single_player(self):
        self.root.destroy()
        SinglePlayer()

    def multiplayer(self):
        self.root.destroy()
        Multiplayer()


class SinglePlayer(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(background="lightskyblue")
        self.root.title = "Single Player Chess"
        position_window(self.root)
        self.white_king_image = tk.PhotoImage(file="pieces/assets/White_King.png")
        self.black_king_image = tk.PhotoImage(file="pieces/assets/Black_King.png")
        self.difficulty = tk.StringVar(self.root)
        self.color = ""
        self.create_window()
        self.root.mainloop()

    def create_window(self):
        main_menu = tk.Button(self.root, text="Main Menu", command=self.main_menu)
        main_menu.place(x=150, y=20, height=40, width=100)

        difficulties = [("Easy", "Depth: 2"), ("Medium", "Depth: 3"), ("Hard", "Depth: 4")]
        difficulty_selection = tk.OptionMenu(self.root, self.difficulty, *difficulties)

        difficulty_selection.place(x=130, y=140, height=32, width=140)
        if self.color == "":
            white_king = tk.Button(self.root, bg="lightskyblue", image=self.white_king_image,
                                   command=lambda color="White": self.select_color(color))
            black_king = tk.Button(self.root, bg="lightskyblue", image=self.black_king_image,
                                   command=lambda color="Black": self.select_color(color))
        elif self.color == "White":
            white_king = tk.Button(self.root, bg="salmon", image=self.white_king_image,
                                   command=lambda color="White": self.select_color(color))
            black_king = tk.Button(self.root, bg="lightskyblue", image=self.black_king_image,
                                   command=lambda color="Black": self.select_color(color))
        else:
            white_king = tk.Button(self.root, bg="lightskyblue", image=self.white_king_image,
                                   command=lambda color="White": self.select_color(color))
            black_king = tk.Button(self.root, bg="salmon", image=self.black_king_image,
                                   command=lambda color="Black": self.select_color(color))
        white_king.place(x=60, y=140, height=64, width=64)
        black_king.place(x=275, y=140, height=64, width=64)

        play = tk.Button(self.root, text="Play", command=self.play)
        play.place(x=150, y=80, height=40, width=100)

    def select_color(self, color):
        self.color = color
        self.create_window()
        self.root.update()

    def main_menu(self):
        self.root.destroy()
        MainMenu()

    def play(self):
        if self.color != "" and self.difficulty != "PY_VAR0":
            difficulty = self.difficulty.get()
            self.root.destroy()
            if "Easy" in difficulty:
                single_player_game(self.color, 0, 2)
            elif "Medium" in difficulty:
                single_player_game(self.color, 0, 3)
            else:
                single_player_game(self.color, 0, 4)


class Multiplayer(object):
    def __init__(self):
        self.root = tk.Tk()
        self.root.configure(background="salmon1")
        self.root.title = "Multi Player Chess"
        position_window(self.root)
        self.create_window()
        self.root.mainloop()

    def create_window(self):
        main_menu = tk.Button(self.root, text="Main Menu", command=self.main_menu)
        main_menu.place(x=150, y=70, height=40, width=100)

        play = tk.Button(self.root, text="Play", command=self.play)
        play.place(x=150, y=130, height=40, width=100)

    def main_menu(self):
        self.root.destroy()
        MainMenu()

    def play(self):
        multiplayer_game("White", 0)
        self.root.destroy()


pygame.font.init()
my_font = pygame.font.SysFont("cambria", 15)
letters = ["a", "b", "c", "d", "e", "f", "g", "h"]


def calc_mouse_pos(pos):
    col = pos[0] // square_size
    row = pos[1] // square_size
    return col, row


def multiplayer_game(color, theme):
    pygame.init()
    game_window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Chess")
    chess_game = Game(game_window, color, theme)
    chess_game.board.initiate_pieces()
    fps = 60
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_xy = pygame.mouse.get_pos()
                row, col = calc_mouse_pos(mouse_xy)
                if chess_game.game_over():
                    if 1 <= row <= 3 and 3 <= col <= 4:
                        if color == "White":
                            multiplayer_game("Black", chess_game.theme)
                        else:
                            multiplayer_game("White", chess_game.theme)
                    elif 4 <= row <= 5 and 3 <= col <= 4:
                        running = False
                else:
                    chess_game.human.select(row, col, mouse_xy)

        if chess_game.game_over():
            draw_end_screen(chess_game, game_window)
        else:
            chess_game.update_screen(chess_game.human.valid_moves, chess_game.board)

    pygame.quit()


def single_player_game(color, theme, depth):
    pygame.init()
    game_window = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Chess")
    chess_game = Game(game_window, color, theme)
    chess_game.board.initiate_pieces()
    fps = 60
    clock = pygame.time.Clock()
    running = True
    while running:
        clock.tick(fps)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_xy = pygame.mouse.get_pos()
                row, col = calc_mouse_pos(mouse_xy)
                if chess_game.game_over():
                    if 1 <= row <= 3 and 3 <= col <= 4:
                        if color == "White":
                            single_player_game("Black", chess_game.theme, depth)
                        else:
                            single_player_game("White", chess_game.theme, depth)
                    elif 4 <= row <= 5 and 3 <= col <= 4:
                        running = False
                else:
                    # if chess_game.turn == chess_game.human.color or chess_game.human.promoting:
                    chess_game.human.select(row, col, mouse_xy)

        if chess_game.turn == chess_game.computer.color \
                and not chess_game.human.promoting and not chess_game.game_over():
            if chess_game.computer.color == "White":
                value, board = chess_game.computer.minimax(chess_game.board, chess_game,
                                                           depth, float("-inf"), float("inf"), "White")
            else:
                value, board = chess_game.computer.minimax(chess_game.board, chess_game,
                                                           depth, float("-inf"), float("inf"), "Black")
            chess_game.computer.computer_move(chess_game, board)

        if chess_game.game_over():
            draw_end_screen(chess_game, game_window)
        else:
            chess_game.update_screen(chess_game.human.valid_moves, chess_game.board)

    pygame.quit()


def draw_end_screen(chess_game, game_window):
    if chess_game.checkmate_win:
        if chess_game.turn == "White":
            main_text = my_font.render("Black won by checkmate.", False, themes[chess_game.theme][0])
        else:
            main_text = my_font.render("White won by checkmate.", False, themes[chess_game.theme][0])
    elif chess_game.stalemate_draw:
        if chess_game.turn == "Black":
            main_text = my_font.render("Stalemate. Black has no moves.", False, themes[chess_game.theme][0])
        else:
            main_text = my_font.render("Stalemate. White has no moves.", False, themes[chess_game.theme][0])
    elif chess_game.threefold_draw:
        main_text = my_font.render("Draw by threefold repetition.", False, themes[chess_game.theme][0])
    elif chess_game.resign:
        main_text = my_font.render(chess_game.turn + " has resigned the game.", False, themes[chess_game.theme][0])
    else:
        main_text = my_font.render("Draw by insufficient material.", False, themes[chess_game.theme][0])

    # The main box, border, and text
    pygame.draw.rect(game_window, [0, 0, 0], (85, 160, 310, 160))
    pygame.draw.rect(game_window, [100, 100, 100], (90, 165, 300, 150))
    game_window.blit(main_text, (150, 180))

    # Play again button
    pygame.draw.rect(game_window, [255, 255, 255], (115, 215, 110, 60))
    pygame.draw.rect(game_window, themes[chess_game.theme][1], (120, 220, 100, 50))
    play_again_text = my_font.render("Play Again", False, [0, 0, 0])
    game_window.blit(play_again_text, (135, 235))

    # Quit button
    pygame.draw.rect(game_window, [255, 255, 255], (245, 215, 110, 60))
    pygame.draw.rect(game_window, themes[chess_game.theme][1], (250, 220, 100, 50))
    quit_text = my_font.render("Quit", False, [0, 0, 0])
    game_window.blit(quit_text, (285, 235))

    pygame.display.update()


if __name__ == "__main__":
    MainMenu()