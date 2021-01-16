from typing import List
from dataclasses import dataclass
import numpy as np
from math import sqrt


@dataclass
class Level:
    grid: List[List[int]]
    max_picks: int
    num_of_good_tiles: int


class Game:
    def __init__(self, levels: List[Level]):
        self.levels = levels
        self.current_level = levels[0]
        self.current_level_index = 0
        self.correct_picks = 0
        self.all_picks = 0

    def pick_tile(self, x: int, y: int):
        # 0 -> zła
        # 1 -> dobra
        # -1 -> dobra i go to next level
        # -2 -> zła i restart level
        self.all_picks += 1
        picked = self.current_level.grid[x][y]
        if picked:
            self.correct_picks += 1
        if self.correct_picks == self.current_level.num_of_good_tiles:
            self.next_level()
            return -1
        if self.should_restart_level():
            self.restart_level()
            return -2
        return picked

    def check_score(self):
        return self.correct_picks

    def next_level(self):
        self.current_level_index += 1
        self.current_level = self.levels[self.current_level_index]
        self.correct_picks = 0
        self.all_picks = 0

    def restart_level(self):
        self.correct_picks = 0
        self.all_picks = 0

    def should_restart_level(self):
        return self.all_picks > self.current_level.max_picks


def generate_levels(board_size):
    levels = list()

    #LEVEL 1
    grid = np.array([i%2 for i in range(board_size**2)])
    levels.append(Level(grid.reshape(board_size, board_size), np.sum(grid)+2, np.sum(grid)))

    # LEVEL 2
    grid = np.array([0 for i in range(board_size ** 2)])
    for i in range(board_size):
        grid[i**2] = 1
    levels.append(Level(grid.reshape(board_size, board_size), np.sum(grid)+2, np.sum(grid)))

    # LEVEL 3
    grid = np.array([0 for i in range(board_size ** 2)])
    primes = [x for x in range(2, board_size**2) if not [i for i in range(2, int(sqrt(x)) + 1) if x % i == 0]]
    for prime in primes:
        grid[prime] = 1
    levels.append(Level(grid.reshape(board_size, board_size), np.sum(grid)+2, np.sum(grid)))

    # LEVEL 4
    grid = np.array([0 for i in range(board_size ** 2)])
    fibs = [0, 1]
    n = 1
    while fibs[n-1] + fibs[n] < board_size ** 2:
        fibs.append(fibs[n-1] + fibs[n])
        n += 1
    for fib in fibs:
        grid[fib] = 1
    levels.append(Level(grid.reshape(board_size, board_size), 2, np.sum(grid)))

    # LEVEL 5
    grid = np.array([0 for i in range(board_size ** 2)])
    catalans = [1]
    n = 0
    while True:
        next_catalan = 0
        for i in range(n+1):
            next_catalan += catalans[i] * catalans[n-i]
        if next_catalan >= board_size ** 2:
            break
        catalans.append(next_catalan)
        n += 1
    for catalan in catalans:
        grid[catalan] = 1
    levels.append(Level(grid.reshape(board_size, board_size), 2, np.sum(grid)))

    return levels

