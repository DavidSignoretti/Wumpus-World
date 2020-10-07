import random as rd


class Coords:
    """
    Creates a datatype Coords that sets up a grid location for the game
    """

    def __init__(self, x: int, y: int):
        """
        :parameter
            _x int:
            _y int:
        """
        self._x: int = x
        self._y: int = y

    @property
    def y(self):
        """
        :return:
            _y: int
        """
        return self._y

    @property
    def x(self):
        """
        :return:
            _x: int
        """
        return self._x

    def __eq__(self, other):
        """
        :return:
            Ture if comparison of coords is equal
        """
        return self._x == other.x and self._y == other.y

    def set_y(self, y: int):
        self._y = y

    def set_x(self, x: int):
        self._x = x

    def values(self):
        return self._x, self._y


class Agent:
    """
    The agent creates a datatype
    """

    def __init__(self):
        """
        :parameter
            facing: int : values 0=north, 1=east, 2=south, 3=west
            location: Coords(0,0) : starting grid
            arrow: bool True : agent start with one arrow
            alive: bool True : start agent alive
            hasgold: bool False : determine if the agent has grabbed the gold
         """
        self.facing: int = 1
        self.location: Coords = Coords(0, 0)
        self.arrow: bool = True
        self.alive: bool = True
        self.hasgold: bool = False


class Board:
    """
    Create the board
    """

    rd.seed()

    def __init__(self, width: int, height: int, pits: int):
        """
        :parameter
            width: int : the width of the board
            height: int : the height of the board
            pits: int : the number of the pits for the board
            pitscoord: List : create list of coords with the location of the pits
            wumpuscoord: Coords : the location of the wumpus
            wumpusalive: bool : status of the wumpase alive True and dead False
            hasgold: bool : does the agent have the gold (true, default=False)
            goldcoord: Coords : the location of the gold
            terminate: bool : end the game (ture, default=False)
         """
        self.width: int = width
        self.height: int = height
        self.pits: int = pits
        self.pitscoord: list = []
        self.wumpuscoord: Coords = Coords(rd.randrange(1, self.width - 1), rd.randrange(1, self.height - 1))
        self.wumpusalive: bool = True
        self.hasgold: bool = False
        self.goldcoord: Coords = Coords(rd.randrange(1, self.width - 1), rd.randrange(1, self.height - 1))
        self.terminate: bool = False

        # set pit location to an list 0 to the value of pits
        for _i in range(0, pits):
            self.pitscoord.append(Coords(rd.randrange(1, self.width - 1), rd.randrange(1, self.height - 1)))


class Action:
    """
    Pending
    """

    def __init__(self, board: Board, agent: Agent):
        """
        :parameter
            board: Board : create and build the wumpus world
            agent: Agent : create the agent
        """
        self.board: Board = board
        self.agent: Agent = agent

    def move(self, action: int):
        """
        :parameter action:
            0: Move the agent one block north
            1: Move the agent one block east
            2: Move the agent one block south
            3: Move the agent one block west
            4: Agent turn right
            5: Agent turn left
            6: Shoot arrow
            7: Grab gold
            8: Climb out
        """
        if action == 0:
            self.agent.location.set_y(min(self.board.height - 1, self.agent.location.y + 1))
            self.precept()
        elif action == 1:
            self.agent.location.set_x(min(self.board.width - 1, self.agent.location.x + 1))
            self.precept()
        elif action == 2:
            self.agent.location.set_y(max(0, self.agent.location.y - 1))
            self.precept()
        elif action == 3:
            self.agent.location.set_x(max(0, self.agent.location.x - 1))
            self.precept()
        elif action == 4:
            self.agent.facing += 1
            if self.agent.facing > 3:
                self.agent.facing = 0
        elif action == 5:
            self.agent.facing -= 1
            if self.agent.facing < 0:
                self.agent.facing = 3
        elif action == 6:
            if self.agent.arrow:

                # shoot arrow north
                if self.agent.facing == 0 and self.agent.location.y < self.board.wumpuscoord.y \
                        and self.agent.location.x == self.board.wumpuscoord.x:
                    self.board.wumpusalive = False

                # shoot arrow east
                elif self.agent.facing == 1 and self.agent.location.x < self.board.wumpuscoord.x \
                        and self.agent.location.y == self.board.wumpuscoord.y:
                    self.board.wumpusalive = False

                # shoot arrow south
                elif self.agent.facing == 2 and self.agent.location.y > self.board.wumpuscoord.y \
                        and self.agent.location.x == self.board.wumpuscoord.x:
                    self.board.wumpusalive = False

                # shoot arrow west
                elif self.agent.facing == 3 and self.agent.location.x > self.board.wumpuscoord.x \
                        and self.agent.location.y == self.board.wumpuscoord.y:
                    self.board.wumpusalive = False
            else:
                pass
        elif action == 7:
            if self.agent.location == self.board.goldcoord:
                self.agent.hasgold = True
        elif action == 8:
            if self.agent.hasgold and self.agent.location.x == 0 and self.agent.location.y == 0:
                self.board.terminate = True
            else:
                pass

    def precept(self):
        print("Precet", self.board.wumpuscoord == self.agent.location)

    def display(self):
        pass
