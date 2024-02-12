from gof import Singleton

MAZE1 = [
    "   $                        *",
    "|##@##|           $         |",
    "|     |    |@@@@@@@@@| $    |",
    "|     |    |         |@@@@@@|",
    "| $§  |    |         |       ",
    "|@@@@@|    |         |       ",
    "|     |----|------   |       ",
    "|     |    |     |@@@######&|",
    "|     |    |  $  |          |",
    "| §   |    |@@@@@|          |",
    "#@@@#@@#@@#|          |@@@|@@",
    "#@@@#      |          |   |  ",
    "#$  #      |   -------|   | $",
    "@@@@@@@@|@@@####      |  @@@@",
    "        |             |      ",
    "    $   |      .      |      ",
    "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"]

MAZE = [
    "                            *",
    "|##@##|                     |",
    "|     |    |@@@@@@@@@|      |",
    "|     |    |         |@@@@@@|",
    "|     |    |         |       ",
    "|@@@@@|    |         |       ",
    "|     |----|------   |       ",
    "|     |    |     |@@@######&|",
    "|     |    |     |          |",
    "|     |    |@@@@@|          |",
    "#@@@#@@#@@#|          |@@@|@@",
    "#@@@#      |          |   |  ",
    "#   #      |   -------|   |  ",
    "@@@@@@@@|@@@####      |  @@@@",
    "        |             |      ",
    "*   $   |      .      |      ",
    "@@@@@@@@@@@@@@@@@@@@@@@@@@@@@"]

# Defines all the characters used in Maze.
MAP_WALL = '#'
MAP_START = '.'
MAP_GOAL = '*'
MAP_DOLLAR = '$'
MAP_LADDER = '|'
MAP_BRIDGE = '-'
MAP_WALL_HOLLOW = '&'
MAP_WALL_DIGGABLE = '@'
MAP_VOID = ' '
MAP_ZOMBIE = '§'
MAP_NULL = "%"


class MazeObserver:
    """Defines an abstract observer."""

    def update_wall(self):
        """Redraw all the wall."""


class MazeElement():
    """Define a generic main Element."""

    def __init__(self):
        """Initialize."""
        self.access = False  # Is it possible to access this position.
        self.solid = True  # gravity don't work.
        self.hang = False
        self.down_enable = False  # It's possible to go down.
        self.up_enable = False  # It's possible to go up.
        self.diggable = False

    def is_access(self) -> bool:
        """Answer if access is possible."""
        return self.access

    def is_solid(self) -> bool:
        """Answer if stop the go."""
        return self.solid

    def is_down_enable(self) -> bool:
        """Answer if it possible to go down."""
        return self.down_enable

    def is_up_enable(self) -> bool:
        """Answer if it possible to go up."""
        return self.up_enable

    def is_diggable(self) -> bool:
        """Answer if it possible to digg."""
        return self.diggable

    def tick(self):
        """Process a tick."""


class WallMaze(MazeElement):
    """Define a Wall."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.my_char = MAP_WALL


class WallDiggable(MazeElement):
    """Define a Wall."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.my_char = MAP_WALL_DIGGABLE
        self.reset()

    def reset(self):
        """Reset the brick."""
        self.access = False
        self.solid = True
        self.diggable = True
        self.number_of_tick = 10

    def digg(self):
        """Digg."""
        self.access = True
        self.solid = False
        self.diggable = False

    def tick(self):
        """Tick is elapsed."""
        self.number_of_tick -= 1
        if self.number_of_tick == 0:
            self.reset()
            Maze().notify_wall()


class WallHollow(MazeElement):
    """Define a Wall."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.my_char = MAP_WALL_HOLLOW
        self.access = True
        self.solid = False


class GenericVoidMaze(MazeElement):
    """Define a generic Void."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.my_char = MAP_VOID
        self.access = True
        self.solid = False
        self.down_enable = True


class VoidMaze(GenericVoidMaze):
    """Define a Wall."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.my_char = MAP_VOID


class DollarMaze(GenericVoidMaze):
    """Define a Dollar."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.my_char = MAP_DOLLAR
        self.activated = True

    def desactivate(self):
        """Desacivate the reward."""
        self.activated = False


class LadderMaze(MazeElement):
    """Define a Ladder."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.my_char = MAP_LADDER
        self.access = True
        self.down_enable = True
        self.up_enable = True


class BridgeMaze(MazeElement):
    """Define a Bridge."""

    def __init__(self):
        """Initialize."""
        super().__init__()
        self.my_char = MAP_BRIDGE
        self.access = True
        self.down_enable = True
        self.hang = True
        self.solid = True


class Subject:
    """Defines a subject for the maze."""

    def __init__(self):
        """Initialize."""
        self.observers = []

    def notify_wall(self):
        """Propagates the modifications."""
        for obs in self.observers:
            obs.update_wall()

    def register(self, observer):
        """Register observer as an observer."""
        self.observers.append(observer)


INVALID_POSITION = (None, None)


class Maze(Subject, metaclass=Singleton):
    """
    Define the maze.

    >>> Maze().is_access((0, 0)) # Empty position.
    True
    >>> Maze().is_access((-1, 0)) # outside position.
    False
    >>> Maze().is_access((1, 1))  # Wall position.
    False
    >>> Maze().is_access((1, 0))   # Ladder position.
    True
    """

    def __init__(self):
        """Initialise of the Maze."""
        super().__init__()
        self.cols = 0  # Number of columns.
        self.rows = 0  # Number of rows

        self.goal = INVALID_POSITION
        self.start = INVALID_POSITION
        self._map = {}  # The map of the maze.
        self.reset()

    def reset(self):
        """Reset the maze."""
        self._map = {}  # The map of the maze.
        self.zombies = []  # The initial position of zombies.
        self.dollars = []
        self.build_maze()

    def build_maze(self):
        """Build the maze."""
        self.goal = INVALID_POSITION
        self.number_of_dollars = 0
        row = 0
        for line in MAZE:
            col = 0
            for char in line:
                pos = (row, col)
                if char == MAP_VOID:
                    self._map[pos] = VoidMaze()
                elif char == MAP_DOLLAR:
                    self._map[pos] = DollarMaze()
                    self.dollars.append(pos)
                    self.number_of_dollars += 1
                elif char == MAP_GOAL:
                    self.final_goal = pos
                    self._map[pos] = VoidMaze()
                elif char == MAP_START:
                    self.start = pos
                    self._map[pos] = VoidMaze()
                elif char == MAP_WALL:
                    self._map[pos] = WallMaze()
                elif char == MAP_LADDER:
                    self._map[pos] = LadderMaze()
                elif char == MAP_WALL_DIGGABLE:
                    self._map[pos] = WallDiggable()
                elif char == MAP_WALL_HOLLOW:
                    self._map[pos] = WallHollow()
                elif char == MAP_BRIDGE:
                    self._map[pos] = BridgeMaze()
                elif char == MAP_ZOMBIE:
                    self.zombies.append(pos)
                    self._map[pos] = VoidMaze()
                else:
                    print("ERREUR")
                col += 1
            self.cols = len(line)
            row += 1

        self.rows = row

    def bring_dollar(self, position):
        """Reward is taken."""
        self._map[position].desactivate()
        self.number_of_dollars -= 1
        if self.number_of_dollars == 0:
            print("Ouverture Porte _________________________________")
            self.goal = self.final_goal

    def is_enable(self, position) -> bool:
        """It's a position of the maze."""
        return position in self._map

    def is_access(self, position) -> bool:
        """Is it possible to access this position."""
        if position not in self._map:
            return False
        return self._map[position].is_access()

    def is_exist(self, position):
        """Is this position exist."""
        return position in self._map

    def get(self, position):
        """
        Get the position.

        Get the object at the position of the parameter position
        in the Maze.
        """
        return self._map[position]

    def get_all_positions(self):
        """Get all the objects in the Maze."""
        return self._map

    def tick(self, position):
        """Tick of time."""
        if position in self._map:
            self._map[position].tick()

    def digg(self, position):
        """Digg."""
        if position in self._map:
            self._map[position].digg()
            self.notify_wall()


if __name__ == "__main__":
    import doctest

    doctest.testmod()
