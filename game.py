from typing import List
from dataclasses import dataclass


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
        picked = self.current_level.grid[y][x]
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
