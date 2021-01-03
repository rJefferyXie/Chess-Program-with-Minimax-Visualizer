import pygame

pygame.font.init()
my_font = pygame.font.SysFont("cambria", 15)
letters = ["a", "b", "c", "d", "e", "f", "g", "h"]


class MoveHistory(object):
    def __init__(self):
        self.move_log = []

    def get_file(self, row):
        if row == 0:
            return "a"

        elif row == 1:
            return "b"

        elif row == 2:
            return "c"

        elif row == 3:
            return "d"

        elif row == 4:
            return "e"

        elif row == 5:
            return "f"

        elif row == 6:
            return "g"

        elif row == 7:
            return "h"
        else:
            pass

    def draw_move_log(self, window):
        # Draw First 50 Moves
        if 0 < len(self.move_log) <= 50:
            self.show_move_log(0, window)

        # Draw next 50
        elif 50 <= len(self.move_log) < 100:
            self.show_move_log(50, window)
        
        # Draw next 50
        elif 100 <= len(self.move_log) < 150:
            self.show_move_log(100, window)

    def show_move_log(self, start, window):
        move_list = []
        move_string = ""

        for i in range(start, len(self.move_log)):
            move = str(i + 1) + "." + self.move_log[i] + ", "
            move_string += move
            text = my_font.render(move_string, True, (0, 0, 0))

            if len(move_list) == 0:
                window.blit(text, (10, 490))

            elif len(move_list) > 0:
                for move_ind in range(len(move_list)):
                    list_text = my_font.render(move_list[move_ind], True, (0, 0, 0))
                    window.blit(list_text, (10, 490 + 20 * move_ind))

                window.blit(text, (10, 490 + 20 * len(move_list)))

            # Every 11th move added to move string, append it to move list
            if i != 0 and i % 11 == 0:
                move_list.append(move_string)
                move_string = ""
