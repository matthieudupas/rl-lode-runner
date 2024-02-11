# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 15:07:11 2024

@author: Matthieu Dupas
"""

from maze2 import Maze
from maze2 import MazeObserver

MAX_STEP = 50000000  # Number max of steps.
ZOMBIE_RATE = 2  # Zombies move one step on ZOMBIE_RATE.


class VirtualWindow(MazeObserver):
    """A Window without IHM."""

    def __init__(self, agent, zombies):
        """Initialize."""
        self.agent = agent
        self.games = 1
        self.count_update = 0
        self.zombies = zombies

    def zombies_reset(self):
        """Reset the zombies."""
        for zombie in self.zombies:
            zombie.reset()

    def on_update(self, delta_time):
        """Do on each step."""
        if self.agent.position != Maze().goal:
            Maze().tick(self.agent.position)  # First tick
            # action, reward = self.agent.do(self.zombies)
            # Then try an action
            if not self.agent.do(self.zombies):
                reset_zombies = True
                self.agent.reset()
                self.games += 1
                print("Zombies Suicide score:")
                Maze().reset()
            # Zombies
            if self.count_update == ZOMBIE_RATE:
                self.count_update = 0
                reset_zombies = False
                for zombie in self.zombies:
                    if not zombie.do(self.agent.position):
                        reset_zombies = True
                        self.agent.reset()
                        self.games += 1
                        print("Zombies Suicide score:", self.agent.score,
                              " nb iter:", self.agent.iteration,
                              " game n°:", self.games,
                              "noise:", self.agent.noise,
                              "position:", self.agent.position,
                              "zombie", zombie.position)
                        Maze().reset()

                if reset_zombies:
                    self.zombies_reset()
                    self.reset()

            self.count_update += 1
            self.update_player()
            self.update_enmies()
        else:
            print("score:", self.agent.score, " nb iter:",
                  self.agent.iteration,
                  " game n°:", self.games, "noise:", self.agent.noise)
            self.agent.reset()
            self.zombies_reset()
            self.games += 1
            Maze().reset()

    def run(self):
        """Process."""
        for _ in range(MAX_STEP):
            self.on_update(1.0)

        print("Position:", self.agent.position, "Start:", Maze().start,
              "nb iterations ->", self.agent.iteration)

    def update_wall(self):
        """Process on an update of the walls."""
        if not self.agent.do_wall():  # is agent in the wall closed.
            print("Wall suicide score:", self.agent.score, " nb iter:",
                  self.agent.iteration,
                  " game n°:", self.games, "noise:", self.agent.noise)
            self.agent.reset()
            self.zombies_reset()
            self.games += 1
            Maze().reset()
        # is a zombie in the wall.
        for zombie in self.zombies:
            zombie.do_wall()
        self.reset()

    def update_player(self):
        """Update the position of the player."""
        pass

    def update_dollar(self):
        """Update the position of the dolar."""
        pass

    def update_enmies(self):
        """Update the position of the enmies."""

    def setup_enmies(self):
        """Set up the zombies."""
        pass

    def setup_dollar(self):
        """Set up the dollars."""
        pass

    def setup_walls(self):
        """Set up the dollars."""
        pass

    def setup(self):
        """Set up."""
        pass
