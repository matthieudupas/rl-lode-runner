import arcade
from arcade import Sprite
from arcade import SpriteList
from arcade import Window
from arcade import start_render

from actions import X
from actions import Y
from maze2 import INVALID_POSITION
from maze2 import MAP_BRIDGE
from maze2 import MAP_LADDER
from maze2 import MAP_WALL
from maze2 import MAP_WALL_DIGGABLE
from maze2 import MAP_WALL_HOLLOW
from maze2 import Maze
from virtual_window import VirtualWindow

# from arcade_test import Window
# from arcade_test import Sprite
# from arcade_test import SpriteList
# from arcade_test import start_render

SPRITE_SCALING = 0.25
SPRITE_SIZE = 32
OFFSET = 0.5

ROOT = ":resources:images/"
ROOT_TILE = ROOT + "tiles/"
IMAGE_ZOMBIE = ROOT + "animated_characters/zombie/zombie_idle.png"
IMAGE_WALL = ROOT_TILE + "stoneMid.png"
IMAGE_WALL_HOLLOW = ROOT_TILE + "dirtCenter_rounded.png"
IMAGE_BRIDGE = ROOT_TILE + "bridgeA.png"
IMAGE_EXIT = ROOT_TILE + "signExit.png"
IMAGE_START = ROOT_TILE + "doorClosed_mid.png"
IMAGE_WALL_DIGG = ROOT_TILE + "boxCrate_single.png"
IMAGE_DOLLAR = ROOT + "items/coinGold.png"
IMAGE_LADDER = ROOT + "items/ladderMid.png"
IMAGE_AGENT = ROOT + "animated_characters/female_adventurer/femaleAdventurer_idle.png"


def build_a_sprite(image, position):
    """Build a sprite with the address image center on position."""
    sprite = Sprite(image, SPRITE_SCALING)
    sprite.center_x, sprite.center_y = state_to_xy(position)
    return sprite


def state_to_xy(position):
    """Scale to x, y."""
    x_coordinate = (position[Y] + OFFSET) * SPRITE_SIZE
    y_coordinate = (Maze().rows - position[X] - OFFSET) * SPRITE_SIZE
    return x_coordinate, y_coordinate


class MazeWindow(Window, VirtualWindow):
    """Define a window with arcade."""

    def __init__(self, agent, zombies):
        """Initialize."""
        VirtualWindow.__init__(self, agent, zombies)
        Window.__init__(self,
                        Maze().cols * SPRITE_SIZE,
                        Maze().rows * SPRITE_SIZE,
                        "ESGI Lode Runner")
        self.enmies = SpriteList()
        self.dollars = SpriteList()
        self.walls_non_diggable = SpriteList()
        self.walls = SpriteList()
        self.wait = 0.01
        self.stop = False
        self.zombies_on = False

    def reset(self):
        """Reset the drawing."""
        self.setup()
        self.setup_enmies()
        self.setup_walls()
        self.setup_dollar()

    def on_update(self, delta_time):
        """Give the control to the mother class."""
        VirtualWindow.on_update(self, delta_time)
        self.setup_dollar()

    def setup_enmies(self):
        """Set up the enemies i.e. the zombies."""
        self.enmies = SpriteList()
        for zombie in self.zombies:
            zombie_sprite = Sprite(IMAGE_ZOMBIE, SPRITE_SCALING)
            zombie_sprite.center_x, \
                zombie_sprite.center_y = state_to_xy(zombie.position)
            self.enmies.append(zombie_sprite)
        self.update_enmies()

    def update_player(self):
        """Update the position of the player."""
        self.player.center_x, \
            self.player.center_y = state_to_xy(self.agent.position)

    def update_enmies(self):
        """Update the position of the enemies."""
        for count, zombie in enumerate(self.enmies):
            zombie.center_x, \
                zombie.center_y = state_to_xy(self.zombies[count].position)

    def setup(self):
        """Set up."""
        print('SETUP')
        self.walls_non_diggable = SpriteList()
        for position, block in Maze().get_all_positions().items():
            if block.my_char == MAP_WALL:
                wall_sprite = Sprite(IMAGE_WALL, SPRITE_SCALING)
                wall_sprite.center_x, \
                    wall_sprite.center_y = state_to_xy(position)
                self.walls_non_diggable.append(wall_sprite)
            elif block.my_char == MAP_LADDER:
                ladder_sprite = Sprite(IMAGE_LADDER, SPRITE_SCALING)
                ladder_sprite.center_x, \
                    ladder_sprite.center_y = state_to_xy(position)
                self.walls_non_diggable.append(ladder_sprite)
            elif block.my_char == MAP_BRIDGE:
                bridge_sprite = Sprite(IMAGE_BRIDGE, SPRITE_SCALING)
                bridge_sprite.center_x, \
                    bridge_sprite.center_y = state_to_xy(position)
                self.walls_non_diggable.append(bridge_sprite)
            elif block.my_char == MAP_WALL_HOLLOW:
                wall_hallow_sprite = Sprite(IMAGE_WALL_HOLLOW, SPRITE_SCALING)
                wall_hallow_sprite.center_x, \
                    wall_hallow_sprite.center_y = state_to_xy(position)
                self.walls_non_diggable.append(wall_hallow_sprite)
            print(Maze().goal)

        self.start = Sprite(IMAGE_START, SPRITE_SCALING)
        self.start.center_x, \
            self.start.center_y = state_to_xy(Maze().start)

        self.player = Sprite(IMAGE_AGENT, SPRITE_SCALING)
        self.update_player()

    def setup_dollar(self):
        """Set up the dollars."""
        self.dollars = SpriteList()
        for dollar in Maze().dollars:
            if Maze().get(dollar).activated:
                dollar_sprite = Sprite(IMAGE_DOLLAR, SPRITE_SCALING)
                dollar_sprite.center_x, \
                    dollar_sprite.center_y = state_to_xy(dollar)
                self.dollars.append(dollar_sprite)

    def setup_walls(self):
        """Set up the diggable wall."""
        self.walls = SpriteList()
        for position in Maze().get_all_positions():
            my_element = Maze().get(position)
            if my_element.my_char == MAP_WALL_DIGGABLE and \
                    not my_element.is_access():
                wall_diggable_sprite = Sprite(IMAGE_WALL_DIGG, SPRITE_SCALING)
                wall_diggable_sprite.center_x, \
                    wall_diggable_sprite.center_y = state_to_xy(position)
                self.walls.append(wall_diggable_sprite)

    def on_draw(self):
        """Redraw all."""
        start_render()
        if Maze().goal != INVALID_POSITION:
            self.goal = Sprite(IMAGE_EXIT, SPRITE_SCALING)
            self.goal.center_x, \
                self.goal.center_y = state_to_xy(Maze().goal)
            self.goal.draw()
        self.start.draw()
        self.walls.draw()
        self.walls_non_diggable.draw()
        self.player.draw()
        self.dollars.draw()
        self.enmies.draw()

        arcade.draw_text(
            f'#{self.agent.iteration} Score : {self.agent.score} Parties : {self.games} Noise : {self.agent.noise}',
            10, 10, arcade.color.WHITE, 16)
    # def on_key_press(self, key, modifiers):
    #     # print("key:",key)
    #     if key == arcade.key.R:
    #         self.agent.reset()
    #         self.update_player()
    #         self.update_enemies()
    #         self.stop = False
    #     elif key == arcade.key.S:
    #         self.stop = True
    #         print(len(Maze().zombies))
    #     elif key == arcade.key.MOTION_RIGHT:
    #         self.wait += 0.01
    #     elif key == arcade.key.MOTION_LEFT:
    #         self.wait -= 0.01
    #     elif key == arcade.key.KEY_0:
    #         self.wait = 1.0
    #     elif key == arcade.key.KEY_1:
    #         self.wait = 0.01
    #     elif key == arcade.key.Q:
    #         self.wait = 0.01
    #     else:
    #         pass
