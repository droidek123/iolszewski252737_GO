""" Module implementing logic """

import sys
import numpy as np
import itertools
import networkx as nx

sys.path.append(".")
from src.utils.stone import Stone
from xmlrpc.client import boolean


class Board:
    """Class implementing logic"""

    def __init__(self, width, height):
        """Constructor"""
        self.__width = width
        self.__height = height
        self.array = np.zeros((width, height))

    @property
    def width(self):
        """Getter"""
        return self.__width

    @width.setter
    def width(self, width):
        """Setter"""
        self.__width = width

    @property
    def height(self):
        """Getter"""
        return self.__height

    @height.setter
    def height(self, __height):
        """Setter"""
        self.__height = __height

    def set_value_in_board(self, pos_x: int, pos_y: int, value: Stone) -> None:
        self.array[pos_x][pos_y] = value

    def is_place_free(self, pos_x: int, pos_y: int) -> boolean:
        return True if self.array[pos_x][pos_y] == 0 else False

    @staticmethod
    def calculate_grid_points(margin, size, number_of_lines=9):

        # vertical points
        xp = np.linspace(margin, size - margin, number_of_lines)
        yp = np.full((number_of_lines), margin)
        svp = list(zip(xp, yp))

        yp = np.full((number_of_lines), size - margin)
        evp = list(zip(xp, yp))

        # horizontal points
        yp = np.linspace(margin, size - margin, number_of_lines)
        xp = np.full((number_of_lines), margin)
        shp = list(zip(xp, yp))

        xp = np.full((number_of_lines), size - margin)
        ehp = list(zip(xp, yp))

        return (svp, evp, shp, ehp)

    def find_groups(self, color: Stone):
        c = 0
        if color == Stone.BLACK:
            c = Stone.BLACK
        else:
            c = Stone.WHITE
        x, y = np.where(self.array == c)
        graph = nx.grid_graph(dim=[9, 9])
        stones = set(zip(x, y))
        all = set(itertools.product(range(9), range(9)))
        to_remove = all - stones
        graph.remove_nodes_from(to_remove)
        return nx.connected_components(graph)

    def find_liberties(self, group):
        for x, y in group:
            if x > 0 and self.array[x - 1, y] == 0:
                return False
            if y > 0 and self.array[x, y - 1] == 0:
                return False
            if x < self.array.shape[0] - 1 and self.array[x + 1, y] == 0:
                return False
            if y < self.array.shape[0] - 1 and self.array[x, y + 1] == 0:
                return False
        return True
