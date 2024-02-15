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
        window = MazeWindow(agent, zombies)
        Maze().register(window)
        window.setup_dollar()
        window.setup_enmies()
        window.setup_walls()
        window.setup()
        window.run()
        agent.save(AGENT_FILE)
        Maze().reset()
        agent.reset()
    plt.plot(agent.history)
    plt.show()
