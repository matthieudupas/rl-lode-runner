import matplotlib.pyplot as plt

from agents import Agent
from agents import AgentZombie
from arcade_window import MazeWindow
from environment import Environment
from maze2 import Maze

MAX_STEP = 1  # Number max of steps.

AGENT_FILE = 'agent.qtable'

if __name__ == '__main__':
    env = Environment()
    agent = Agent(env)
    zombies = []
    for zombie in Maze().zombies:
        zombies.append(AgentZombie(env, zombie))
    for party_count in range(MAX_STEP):
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
    plt.plot(agent.history)
    plt.show()
