# -*- coding: utf-8 -*-
"""
Created on Sun Jan 21 09:00:33 2024

@author: Matthieu Dupas
"""


class Window:
    """Provide a mack of the Window."""

    def __init__(self, x_size, y_size, title):
        print("x:", x_size, "y:", y_size, "Title:", title)


class Sprite:
    """Provide a mock of sprite."""

    def __init__(self, file_name, scale):
        """Initialize."""
        # print("file:", file_name, "scale:", scale)


class SpriteList(list):
    """Provide a mock of spriteList."""

    def __init__(self):
        """Initialize."""
        pass



def start_render():
    """Provide a mock of start_render."""
    pass
