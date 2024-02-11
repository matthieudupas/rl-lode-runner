# -*- coding: utf-8 -*-
"""
Created on Sun Jan 14 15:07:11 2024

@author: Matthieu Dupas
"""
#import arcade

import matplotlib.pyplot as plt

from maze2 import Maze
from environment import Environment
from agents import Agent
from agents import AgentZombie
from arcade_window import MazeWindow

MAX_STEP = 10  # Number max of steps.

AGENT_FILE = 'agent.qtable'


if __name__ == '__main__':
    env = Environment()
    agent = Agent(env)
    zombies = []
    for zombie in Maze().zombies:
        zombies.append(AgentZombie(env, zombie))
    for _ in range(MAX_STEP):
        agent.load(AGENT_FILE)
        # for key, value in agent.qtable.qtable.items():
        #     print("key->", key)
        #     print("value:", value)
        window = MazeWindow(agent, zombies)
        Maze().register(window)
        print("-------------------setup dollar----------------------------")
        window.setup_dollar()
        print("-------------------setup enmies----------------------------")
        window.setup_enmies()
        print("-------------------setup wallss----------------------------")
        window.setup_walls()
        print("-------------------setup ----------------------------")
        window.setup()
        print("-------------------run ----------------------------")

        window.run()

        agent.save(AGENT_FILE)
        Maze().reset()
        agent.reset()
#    plt.plot(agent.history)
#    plt.show()

