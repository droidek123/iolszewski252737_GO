"""Module implementing gui"""

from pickle import NONE
import sys
import math
import pygame

sys.path.append(".")
from src.board.board import Board
from src.utils.consts import SIZE, MARGIN, BACKGROUND_COLORS, BLACK_STONE,\
    WHITE_STONE, LEFT, RIGHT, BLACK_TXT, SCORE, MSG
from src.utils.move import Move
from src.utils.stone import Stone


class View(Board):
    """Class implementing gui"""

    def __init__(self) -> None:
        """Constructor"""
        super().__init__(9, 9)
        self.list_of_points = Board.calculate_grid_points(MARGIN, SIZE)
        self.black_points = 0
        self.white_points = 7.5
        self.move = Move.BLACK
        self.pass_counter = 0
        self.last_pass = 0
        self.is_game_ended = 0
        self.color = None
        self.opposit_color = None
        self.font = None

    def init_pygame(self):
        pygame.init()
        self.screen = pygame.display.set_mode((700, 700))
        self.font = pygame.font.SysFont("arial", 30)

    def draw(self):
        self.screen.fill(BACKGROUND_COLORS)
        for i in range(9):
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                self.list_of_points[0][i],
                self.list_of_points[1][i],
                4,
            )
            pygame.draw.line(
                self.screen,
                (0, 0, 0),
                self.list_of_points[2][i],
                self.list_of_points[3][i],
                4,
            )

        for i in range(9):
            for j in range(9):
                if self.array[i][j] == Stone.BLACK:
                    pygame.draw.circle(
                        self.screen,
                        BLACK_STONE,
                        (self.list_of_points[2][i][1],
                         self.list_of_points[0][j][0]),
                        20,
                    )
                elif self.array[i][j] == Stone.WHITE:
                    pygame.draw.circle(
                        self.screen,
                        WHITE_STONE,
                        (self.list_of_points[2][i][1],
                         self.list_of_points[0][j][0]),
                        20,
                    )
        score = (
            f"Black's points: {self.black_points}"
            + f"     White's points: {self.white_points}"
        )
        txt = self.font.render(score, True, BLACK_TXT)
        self.screen.blit(txt, SCORE)
        pygame.display.flip()

    def update(self):
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.MOUSEBUTTONUP and event.button == LEFT:
                self.handle_click()
            elif event.type == pygame.MOUSEBUTTONUP and event.button == RIGHT:
                self.passing()
            elif event.type == pygame.QUIT:
                sys.exit()

    def handle_click(self):
        if self.is_game_ended == 1:
            msg = NONE
            if self.black_points > self.white_points:
                msg = (f"Wygrał Czarny")
            else:
                msg = (f"Wygrał Biały")
                
            txt = self.font.render(msg, True, BLACK_TXT)
            self.screen.blit(txt, MSG)
            pygame.display.flip()
            return

        # get mouse cords
        pos_x, pos_y = pygame.mouse.get_pos()

        # calculate nearest row and column
        delta_x = math.inf
        delta_y = math.inf
        num_x = 0
        num_y = 0
        for i in range(9):
            temp_x = abs(self.list_of_points[2][i][1] - pos_x)
            temp_y = abs(self.list_of_points[0][i][0] - pos_y)
            if temp_x < delta_x:
                delta_x = temp_x
                num_x = i
            if temp_y < delta_y:
                delta_y = temp_y
                num_y = i

        if self.is_place_free(num_x, num_y):
            # check who's turn is now
            if self.move == Move.BLACK:
                self.move = Move.WHITE
                self.color = Stone.BLACK
                self.opposit_color = Stone.WHITE
            else:
                self.move = Move.BLACK
                self.color = Stone.WHITE
                self.opposit_color = Stone.BLACK

            self.set_value_in_board(num_x, num_y, self.color)

            for group in list(self.get_groups(self.opposit_color)):
                if self.has_no_liberties(group):
                    for i, j in group:
                        self.array[i][j] = Stone.EMPTY
                    if self.move == Move.BLACK:
                        self.white_points += len(group)
                    else:
                        self.black_points += len(group)
                        

            # draw stone
            self.draw()
            if self.pass_counter == 1:
                self.pass_counter = 0

    def passing(self):
        self.pass_counter += 1
        if self.pass_counter == 2:
            self.is_game_ended = 1
            print("Gra skonczona")
