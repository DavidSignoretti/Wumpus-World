import random as rd
import sys


class Coords:
    """
    Creates a datatype Coords that sets up a grid location for the game
    """

    def __init__(self, x: int, y: int):
        """
        :rtype: the objects grid location
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
        self.reward: int = 0


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
        self.grid: list = []
        # self.adjacent: dict = {'breeze': False, 'stench': False, 'glitter': False}

    def adjacent(self, adj: Coords):
        """

        :return:
        """
        if self.agent.location.x == adj.x \
                and self.agent.location.y == adj.y + 1 \
                or self.agent.location.x == adj.x + 1 \
                and self.agent.location.y == adj.y \
                or self.agent.location.x == adj.x \
                and self.agent.location.y == adj.y + 1 \
                or self.agent.location.x == adj.x - 1 \
                and self.agent.location.x == adj.y \
                or self.agent.location.x == adj.x \
                and self.agent.location.y == adj.y - 1:
            return True
        else:
            return False

    def precept(self):
        """
        if the agent is located at the same coords as a alive wumpus or pits the game ends
        :return:
            stench: bool : is wumpas adjacent
            glitter: bool : is the agent on the gold
            breeze: list[bool] : are there pits adjacent
        """

        breeze: list = []
        stench: bool = False

        if self.agent.location == self.board.wumpuscoord and self.board.wumpusalive:
            self.exitgame()
        else:
            stench = self.adjacent(self.board.wumpuscoord)

        if self.agent.location == self.board.goldcoord:
            glitter = True
        else:
            glitter = False

        for _i in range(len(self.board.pitscoord)):

            if self.agent.location == self.board.pitscoord[_i]:
                self.exitgame()
            else:
                breeze.append(self.adjacent(self.board.pitscoord[_i]))

        return stench, glitter, breeze

    def exitgame(self):
        if self.agent.hasgold and self.board.terminate:
            self.agent.reward += 1001
            print("You Win ", self.agent.reward)
            sys.exit()
        else:
            self.agent.reward += -1001
            print("You Lose ", self.agent.reward)
            sys.exit()

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
        if action == 0 and self.agent.facing == 0:
            self.agent.location.set_y(min(self.board.height - 1, self.agent.location.y + 1))
            self.precept()
            self.grid.append(Coords(self.agent.location.x, self.agent.location.y))
        elif action == 1 and self.agent.facing == 1:
            self.agent.location.set_x(min(self.board.width - 1, self.agent.location.x + 1))
            self.precept()
            self.grid.append(Coords(self.agent.location.x, self.agent.location.y))
        elif action == 2 and self.agent.facing == 2:
            self.agent.location.set_y(max(0, self.agent.location.y - 1))
            self.precept()
            self.grid.append(Coords(self.agent.location.x, self.agent.location.y))
        elif action == 3 and self.agent.facing == 3:
            self.agent.location.set_x(max(0, self.agent.location.x - 1))
            self.precept()
            self.grid.append(Coords(self.agent.location.x, self.agent.location.y))
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
            self.agent.reward += -1
        # grab gold
        elif action == 7:
            if self.agent.location == self.board.goldcoord:
                self.agent.hasgold = True
        # climb out with gold
        elif action == 8:
            if self.agent.hasgold and self.agent.location.x == 0 and self.agent.location.y == 0:
                self.exitgame()
            else:
                self.agent.reward += -10

        self.agent.reward += -1
