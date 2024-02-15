import pickle
from os.path import exists
from random import random

from actions import ACTIONS
from actions import ACTIONS_CLASS
from actions import ACTIONS_MOVES
from actions import ACTION_DOWN
from actions import ACTION_LEFT
from actions import ACTION_RIGHT
from actions import ACTION_UP
from actions import AbstractAction
from actions import X
from actions import Y
from environment import REWARD_SUICIDE
from environment import build_radar
from maze2 import MAP_WALL_DIGGABLE
from maze2 import Maze

ALEA_FACTOR = 0.95
START_NOISE = 0.40
LEARNING_RATE = 0.9
DISCOUNT_FACTOR = 0.6

AGENT_FILE = 'agent.qtable'


def arg_max(table):
    """Return the max of the table."""
    return max(table, key=table.get)


class AgentZombie():
    """Manages a zombie."""

    def __init__(self, env, position_start):
        """Initialize."""
        self.position_start = position_start
        self.env = env
        self.reset()

    def reset(self):
        """Reset the zombie."""
        self.position = self.position_start

    def do(self, position_hero):
        """Activate, Action done by the zombie."""
        # Compute the next position.
        result = True  # the zombie can move.
        actions = []
        if self.position[X] - position_hero[X] > 0:
            actions.append(ACTION_UP)
        else:
            actions.append(ACTION_DOWN)
        if self.position[Y] - position_hero[Y] > 0:
            actions.append(ACTION_LEFT)
        else:
            actions.append(ACTION_RIGHT)
        # Try the first move.
        new_position, result_ok = \
            ACTIONS_CLASS[actions[X]].execute(self.position)
        # If nothing has been done try the second move.
        if not result_ok:
            new_position, result_2 = \
                ACTIONS_CLASS[actions[Y]].execute(self.position)
            if result_2:
                self.position = new_position
        else:
            self.position = new_position
        if self.position == position_hero:
            # The end
            result = False  # end of the game.
        return result

    def do_wall(self):
        """Treat the close of the wall."""
        # print(Maze().get(self.position).my_char)
        result = True
        if Maze().get(self.position).my_char == MAP_WALL_DIGGABLE:
            # print(Maze().get(self.position).is_access())
            if not Maze().get(self.position).is_access():
                # The wall is close on the agent
                self.reset()
                print("Je reset le zombie--------------")
                result = False
        return result


class Qtable():
    """Modelizes a Q_table."""

    def __init__(self, actions,
                 learning_rate=LEARNING_RATE,
                 discount_factor=DISCOUNT_FACTOR):
        """Initialize."""
        self.qtable = {}
        self.actions = actions
        self.learning_rate = learning_rate
        self.discount_factor = discount_factor

    def add_state(self, state):
        """Add a state in the q_table."""
        if state not in self.qtable:
            self.qtable[state] = {}
            for action in self.actions:
                self.qtable[state][action] = 0.0

    def update(self, state, new_state, reward, action):
        """Update the Qtable."""
        try:
            self.add_state(new_state)
            maxQ = max(self.qtable[new_state].values())
            delta = self.learning_rate * \
                    (reward + self.discount_factor * maxQ - self.qtable[state][action])
            self.qtable[state][action] += delta
        except KeyError:
            print('---------------------------------------------------')
            print(state)
            print(new_state)
            print(action)
            print('---------------------------------------------------')

    def get_max(self, state):
        """Get the max."""
        try:
            return arg_max(self.qtable[state])
        except KeyError:
            print('-------get max error-------------------------------------------')
            return ACTION_LEFT


class Agent:
    """Represents an Agent."""

    def __init__(self, env,
                 learning_rate=LEARNING_RATE,
                 discount_factor=DISCOUNT_FACTOR):
        """Initialize."""
        self.env = env
        self.reset()
        self.qtable = Qtable(ACTIONS, learning_rate, discount_factor)
        self.qtable.add_state(self.state)
        self.history = []
        self.noise = START_NOISE
        self.previous_state = self.state
        self.previous_new_state = self.state

    def reset(self):
        """Reset the instance."""
        self.position = Maze().start
        self.score = 0
        self.iteration = 0
        a_state = self.env.get_radar(self.position)
        for zombie in Maze().zombies:
            a_state += build_radar(zombie,
                                   self.position[0], self.position[1])
        self.state = tuple(a_state)
        self.my_min = 15

    def zombie_radar(self, zombies, state_in, position):
        """Build de radar of the zombies."""
        my_state = state_in
        for zombie in zombies:
            my_state += build_radar(zombie.position, position[0], position[1])
        return tuple(my_state)

    def best_action(self):
        """Return the best action alea or calaculate."""
        proba = random()
        if proba < self.noise:
            my_action = AbstractAction().choice_action(proba)
        #            my_action = choice(ACTIONS)
        else:
            my_action = self.qtable.get_max(self.state)
        return my_action

    def do(self, zombies):
        """Do the job."""
        result = True
        action = self.best_action()
        a_state, position, reward = self.env.do(self.position, action)
        new_state = self.zombie_radar(zombies, a_state, position)
        for zombie in zombies:
            if position == zombie.position:
                reward = REWARD_SUICIDE
                result = False
        self.score += reward
        self.iteration += 1
        self.position = position
        # Q-learning
        self.qtable.update(self.state, new_state, reward, action)
        self.state = new_state
        if position[0] < self.my_min or position[0] < 8:
            # print(position, "goal:", Maze().goal, "score:", self.score)
            self.my_min = position[0]
        if self.position == Maze().goal:
            # Each time the goal is reached alea decrease.
            self.history.append(self.score)
            self.noise *= ALEA_FACTOR
        else:
            # A normal step store the last move
            if action in ACTIONS_MOVES:
                self.previous_action = action
                self.previous_state = self.state
                self.previous_new_state = self.state
        return result
        # return action, reward

    def do_wall(self):
        """Treat the close of the wall."""
        # print(Maze().get(self.position).my_char)
        result = True
        if Maze().get(self.position).my_char == MAP_WALL_DIGGABLE:
            # print(Maze().get(self.position).is_access())
            if not Maze().get(self.position).is_access():
                # The wall is closed on the agent.
                self.qtable.update(self.previous_state,
                                   self.previous_new_state,
                                   REWARD_SUICIDE,
                                   self.previous_action)
                # print("Je reset --------------")
                result = False
        return result

    def load(self, filename):
        """Load Qtable from a file."""
        if exists(filename):
            with open(filename, 'rb') as file:
                self.qtable = pickle.load(file)
            self.reset()

    def save(self, filename):
        """Save qtable from a file."""
        with open(filename, 'wb') as file:
            pickle.dump(self.qtable, file)
