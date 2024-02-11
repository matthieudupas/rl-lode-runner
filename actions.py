# -*- coding: utf-8 -*-
"""
Created on Tue Jan 16 13:30:15 2024

@author: Matthieu Dupas
"""
from gof import Singleton
from maze2 import Maze
from random import choice

X = 0  # X is up to down.
Y = 1  # Y is left to right.

ACTION_UP = 'U'
ACTION_DOWN = 'D'
ACTION_LEFT = 'L'
ACTION_RIGHT = 'R'
ACTION_IDLE = 'I'
ACTION_DIGG_LEFT = 'H'
ACTION_DIGG_RIGHT = 'K'
ACTIONS_MOVES = [ACTION_UP, ACTION_DOWN, ACTION_LEFT,
                 ACTION_RIGHT, ACTION_IDLE]
ACTIONS_DIGG = [ACTION_DIGG_LEFT, ACTION_DIGG_RIGHT]
ACTIONS = ACTIONS_MOVES #+ ACTIONS_DIGG
#ACTIONS = [ACTION_LEFT, ACTION_RIGHT, ACTION_UP, ACTION_DOWN]


MOVES = {ACTION_UP: (-1, 0),
         ACTION_DOWN: (1, 0),
         ACTION_LEFT: (0, -1),
         ACTION_RIGHT: (0, 1),
         ACTION_IDLE: (0, 0),
         ACTION_DIGG_LEFT: (0, 0),
         ACTION_DIGG_RIGHT: (0, 0)}

DIGG_THRESHOLD = 0.00  # Proba under which we digg.


class AbstractAction(metaclass=Singleton):
    """Represent an abstract action."""

    def __init__(self):
        """Initialize."""
        self.move = MOVES[ACTION_LEFT]

    def execute(self, position):
        """Execute the action."""

    def gravity(self, position):
        """Act the gravity."""
        previous_position = position
        while(Maze().is_enable(position) and not
              Maze().get(position).is_solid()):
            previous_position = position
            position = (position[X] + 1, position[Y])
        if Maze().is_enable(position) and Maze().get(position).hang:
            previous_position = position
        return previous_position

    def compute_new_position(self, position):
        """Compute the new position."""
        return (position[X] + self.move[X], position[Y] + self.move[Y])

    def choice_action(self, proba):
        """Choice of the next actions."""
        result = None
        if proba < DIGG_THRESHOLD:
            result = choice(ACTIONS_DIGG)
        else:
            result = choice(ACTIONS_MOVES)
        return result


class LeftAction(AbstractAction):
    """
    Represent an action going to the left.

    >>> LeftAction().execute((0,0))
    ((0, 0), False)
    >>> LeftAction().execute((0,1))
    ((0, 0), True)
    >>> LeftAction().execute((6,2))
    ((9, 1), True)
    >>> LeftAction().execute((1,11))
    ((6, 10), True)
    >>> LeftAction().execute((6,28))
    ((9, 27), True)
    >>> Maze().get((7, 27)).my_char
    '&'
    """

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.move = MOVES[ACTION_LEFT]

    def execute(self, position):
        """Execute the action."""
        result_ok = False
        new_position = self.compute_new_position(position)
        if Maze().is_access(new_position):
            #  Gravity
            new_position = self.gravity(new_position)
            result_ok = True
        else:
            new_position = position
        return new_position, result_ok


class RightAction(AbstractAction):
    """
    Represent an action going to the right.

    >>> RightAction().execute((0,29))
    ((0, 29), False)
    >>> RightAction().execute((0,6))
    ((6, 7), True)
    >>> RightAction().execute((0,0))
    ((0, 1), True)
    """

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.move = MOVES[ACTION_RIGHT]

    def execute(self, position):
        """Execute the action."""
        result_ok = False
        new_position = self.compute_new_position(position)
        if Maze().is_access(new_position):
            #  Gravity
            new_position = self.gravity(new_position)
            result_ok = True
        else:
            new_position = position
        return new_position, result_ok


class DownAction(AbstractAction):
    """
    Represent an action going Down.

    >>> DownAction().execute((0,0))
    ((1, 0), True)
    >>> DownAction().execute((0,1))
    ((0, 1), False)
    >>> DownAction().execute((6,7))
    ((9, 7), True)
    """

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.move = MOVES[ACTION_DOWN]

    def execute(self, position):
        """Execute the action."""
        result_ok = False
        new_position = position
        if Maze().get(position).is_down_enable():
            new_position = self.compute_new_position(position)
            if Maze().is_access(new_position):
                new_position = self.gravity(new_position)
                result_ok = True
            else:
                new_position = position
        return new_position, result_ok


class UpAction(AbstractAction):
    """
    Represent an action going up.

    >>> UpAction().execute((0,0))
    ((0, 0), False)
    >>> UpAction().execute((1,0))
    ((0, 0), True)
    >>> UpAction().execute((2,0))
    ((1, 0), True)
    >>> UpAction().execute((7,17))
    ((6, 17), True)
    """

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.move = MOVES[ACTION_UP]

    def execute(self, position):
        """Execute the action."""
        result_ok = False
        new_position = position
        if Maze().get(position).is_up_enable():
            new_position = self.compute_new_position(position)
            result_ok = Maze().is_access(new_position)
        else:
            new_position = position

        return new_position, result_ok


class IdleAction(AbstractAction):
    """
    Represent an action going up.

    IdleAction().execute((0,0))
    ((0, 0), True)
    """

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.move = MOVES[ACTION_IDLE]

    def execute(self, position):
        """Execute the action."""
        return position, True


class DiggRightAction(AbstractAction):
    """
    Represent an action digging on the left.

    >>> Maze().build_maze()
    >>> DiggRightAction().execute((0, 0))
    ((0, 0), False)
    >>> DiggRightAction().execute((0, 2))
    ((0, 2), True)
    >>> RightAction().execute((0, 2))
    ((4, 3), True)
    >>> Maze().tick((1, 3))
    >>> Maze().get((1, 3)).is_diggable()
    False
    >>> Maze().tick((1, 3))
    >>> Maze().get((1, 3)).is_diggable()
    False
    >>> Maze().tick((1, 3))
    >>> Maze().get((1, 3)).is_diggable()
    False
    >>> Maze().tick((1, 3))
    >>> Maze().get((1, 3)).is_diggable()
    False
    >>> Maze().tick((1, 3))
    >>> Maze().tick((1, 3))
    >>> Maze().tick((1, 3))
    >>> Maze().tick((1, 3))
    >>> Maze().tick((1, 3))
    >>> Maze().tick((1, 3))
    >>> Maze().tick((1, 3))
    >>> Maze().get((1, 3)).is_diggable()
    True
    """

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.move = MOVES[ACTION_DIGG_RIGHT]

    def execute(self, position):
        """Execute the action."""
        result_ok = False
        try:
            right_position, possible = RightAction().execute(position)
            if possible:  # It's possible to go on the right.
                position_digg = (right_position[X]+1, right_position[Y])
                if Maze().is_exist(position_digg) and\
                   Maze().get(position_digg).is_diggable():
                    Maze().digg(position_digg)
                    result_ok = True
            return position, result_ok
        except KeyError:
            return position, result_ok


class DiggLeftAction(AbstractAction):
    """
    Represent an action digging on the right.

    >>> Maze().build_maze()
    >>> Maze().get((1, 3)).is_diggable()
    True
    >>> Maze().get((5, 3)).is_solid()
    True
    >>> DiggLeftAction().execute((0, 0))
    ((0, 0), False)
    >>> DiggLeftAction().execute((0, 4))
    ((0, 4), True)
    >>> LeftAction().execute((0, 4))
    ((4, 3), True)
    >>> Maze().get((5, 3)).is_solid()
    True
    """

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.move = MOVES[ACTION_DIGG_LEFT]

    def execute(self, position):
        """Execute the action."""
        result_ok = False
        try:
            left_position, possible = LeftAction().execute(position)
            if possible:  # It's possible to go on the right.
                position_digg = (left_position[X] + 1, left_position[Y])
                if Maze().is_exist(position_digg) and\
                   Maze().get(position_digg).is_diggable():
                    Maze().digg(position_digg)
                    result_ok = True
            return position, result_ok
        except KeyError:
            return position, result_ok


ACTIONS_CLASS = {ACTION_UP: UpAction(),
                 ACTION_DOWN: DownAction(),
                 ACTION_LEFT: LeftAction(),
                 ACTION_RIGHT: RightAction(),
                 ACTION_IDLE: IdleAction(),
                 ACTION_DIGG_LEFT: DiggLeftAction(),
                 ACTION_DIGG_RIGHT: DiggRightAction()}


if __name__ == "__main__":
    import doctest

    doctest.testmod()
