# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 15:38:47 2024

@author: Matthieu Dupas
"""
from maze2 import Maze
from maze2 import MAP_WALL
from actions import ACTIONS_CLASS


NULL_RADAR = [0] * 9  # Radar-goal Matix 3x3 0
NEIGHBORS = 2
RANGE_NEIGHBORS = range(1, NEIGHBORS)

RANGE_SIGN = [-1, 1]

REWARD_WALL = -128
REWARD_DEFAULT = -1
REWARD_GOAL = 64
REWARD_DOLLAR = 30
REWARD_SUICIDE = -500


def sign(value):
    """Return the sign of a parameter."""
    return 1 if value > 0 else -1 if value < 0 else 0


def build_radar(goal, row, col):
    """Build a radar to goal."""
    radar_goal = NULL_RADAR  # Radar-goal vaut O.
    if goal is not None:
        delta_row = sign(goal[0] - row) + 1
        delta_col = sign(goal[1] - col) + 1
        position = delta_row * 3 + delta_col
        radar_goal[position] = 1
    return radar_goal


class Environment:
    """Defines the Environement."""

    def __init__(self):
        """Intitialize."""
        self.map = Maze().get_all_positions()

    def get_radar(self, state):
        """Compute the radar."""
        row, col = state[0], state[1]

        neighbors = []
        for a_sign in RANGE_SIGN:
            for a_row in RANGE_NEIGHBORS:
                neighbors.append((row + a_sign * a_row, col))
        for a_sign in RANGE_SIGN:
            for a_column in RANGE_NEIGHBORS:
                neighbors.append((row,  col + a_sign * a_column))
        for a_sign in RANGE_SIGN:
            for a_column in RANGE_NEIGHBORS:
                neighbors.append((row-1, col + a_sign * a_column))
        for a_sign in RANGE_SIGN:
            for a_column in RANGE_NEIGHBORS:
                neighbors.append((row+1, col + a_sign * a_column))

        radar = []
        for a_neighbor in neighbors:
            if a_neighbor in self.map:
                # On remplit le radar avec map.
                radar.append(self.map[a_neighbor].my_char)
            else:
                radar.append(MAP_WALL)
        radar_goal = build_radar(Maze().goal, row, col)
        radar_dollars = []
        for dollar in Maze().dollars:
            if Maze().get(dollar).activated:
                radar_dollars.append(build_radar(dollar, row, col))
            else:
                radar_dollars.append([0] * 9)
        # print("----------------- Get Radar ---------------")
        # print(radar + radar_goal + radar_dollars[0])
        # print("-------------------------------------------")
        result = radar + radar_goal
        for dollar in radar_dollars:
            result = result + dollar
        return result

    def do(self, position, action):
        """Do the work."""
        new_position, result_ok = ACTIONS_CLASS[action].execute(position)

        if result_ok:
            position = new_position
            if new_position == Maze().goal:
                reward = REWARD_GOAL
            else:
                for dollar in Maze().dollars:
                    if position == dollar:
                        if Maze().get(position).activated:
                            reward = REWARD_DOLLAR
                            print('---------------:', position)
                            Maze().bring_dollar(position)
                reward = REWARD_DEFAULT
        else:
            reward = REWARD_WALL

        return self.get_radar(position), position, reward
