import random as rd
import sys
import pomegranate as po
from pomegranate import utils
import networkx as nx


utils.enable_gpu()


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
            stench: bool False : is the agent sencing the Wumpus
            breeze: list : is the agent sencing the pits
            glitter: bool False : is the agent sencing the gold
            bump: bool False : diod the agent bump into the wall
            reward: int : the reward for action completed
         """
        self.facing: int = 1
        self.location: Coords = Coords(0, 0)
        self.arrow: bool = True
        self.alive: bool = True
        self.hasgold: bool = False
        self.stench: bool = False
        self.breeze: bool = False
        self.glitter: bool = False
        self.reward: int = 0


# TODO build graph and networkx for shortest path.

class Board:
    """
    Create the board
    """

    rd.seed()

    def __init__(self, width: int, height: int, pits: float):
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
        self.pits: float = pits
        self.pitscoord: list = []
        self.wumpuscoord: Coords = Coords(rd.randrange(1, self.width - 1), rd.randrange(1, self.height - 1))
        self.wumpusalive: bool = True
        self.goldcoord: Coords = Coords(rd.randrange(1, self.width - 1), rd.randrange(1, self.height - 1))
        self.terminate: bool = False

        # set pit locations place the pit in the grid with prod of self.pits.
        while len(self.pitscoord) < 2:
            for _y in range(1, height):
                for _x in range(1, width):
                    if rd.random() < self.pits and len(self.pitscoord) < 2:
                        self.pitscoord.append(Coords(_x, _y))


class Action:
    """
    This class is where the agent is controlled
    """

    def __init__(self, board: Board, agent: Agent):
        """
        :parameter
            board: Board : create and build the wumpus world
            agent: Agent : create the agent
        """
        self.board: Board = board
        self.agent: Agent = agent
        self.route: Graph = nx.Graph()
        self.escape: list = []
        self.ontherun: bool = False

        # init the first node inf the graph
        self.route.add_nodes_from(([('00',
                                     {"_x": self.agent.location.x,
                                      "_y": self.agent.location.y,
                                      "stench": self.agent.stench,
                                      "breeze": self.agent.breeze,
                                      "alive": self.agent.alive})]))
        # init the precet for Coords(0,0)
        self.precept()

    def display(self):
        """
        :prints out the board status at ever move
        """
        sys.stdout.write("------" * self.board.width)
        sys.stdout.write("\n")
        for _h in range(self.board.height - 1, -1, -1):
            for _w in range(0, self.board.width):
                _l = ""
                _n = ""
                sys.stdout.write("|")
                grid: Coords = Coords(_w, _h)
                # display wumpaus
                if self.board.wumpuscoord == grid:
                    _l += "W" if self.board.wumpusalive else "w"
                # display gold
                if self.board.goldcoord == grid:
                    _l += "G"
                # display pits
                for _p in range(len(self.board.pitscoord)):
                    if self.board.pitscoord[_p] == grid:
                        _l += "P"
                # display agent
                if self.agent.location == grid:
                    _l += "A"

                sys.stdout.write("{:<5}".format(_l))
            sys.stdout.write("|")
            sys.stdout.write("\n")
            print("------" * self.board.width)

    def adjacent(self, adj: Coords):
        """
        :return: Ture or False is the agent in an adjacent grid location
        """
        if self.agent.location.x == adj.x and self.agent.location.y + 1 == adj.y \
                or self.agent.location.x + 1 == adj.x and self.agent.location.y == adj.y \
                or self.agent.location.x == adj.x and self.agent.location.y - 1 == adj.y \
                or self.agent.location.x - 1 == adj.x and self.agent.location.y == adj.y:

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
        # TODO assignment 3 calcuate the prob of pits and wumpus on each
        #  move and retain and build model of each location

        # check if agent and wumpus are at the same grid location
        if self.agent.location == self.board.wumpuscoord and self.board.wumpusalive:
            self.exitgame()
        else:
            self.agent.stench = self.adjacent(self.board.wumpuscoord)

        # check if agent and pits are at the same grid location
        _b = []
        for _i in range(len(self.board.pitscoord)):
            if self.agent.location == self.board.pitscoord[_i]:
                self.exitgame()
            elif self.adjacent(self.board.pitscoord[_i]):
                _b.append(True)
            else:
                _b.append(False)

        if (True in _b):
            self.agent.breeze = True

        # check if agent and gold are at the same grid location
        if self.agent.location == self.board.goldcoord:
            self.agent.glitter = True

    def setgraph(self, _x=0, _y=0):
        """
            build a graph of safe locations and precepts
        :param _x: the direction of ht eagnet move in the X direction
        :param _y: the direction of the agent move in Y direction
        :return: None
        """
        _newnode: str = str(self.agent.location.x) + str(self.agent.location.y)

        # add new node to the graph
        self.route.add_nodes_from([(_newnode,
                                    {"_x": self.agent.location.x,
                                     "_y": self.agent.location.y,
                                     "stench": self.agent.stench,
                                     "breeze": self.agent.breeze,
                                     "alive": self.agent.alive})])

        # set the edges
        _oldnode: str = str(_x) + str(_y)
        self.route.add_edge(_oldnode, _newnode, weight=1)
        # build and update the escape plan from current location to Coords(0,0)
        self.escape = nx.dijkstra_path(self.route, _newnode, '00')

    def exitgame(self):
        """
            exit the game
        """
        self.agent.reward += -1001
        print("You LOSE")
        self.board.terminate = True

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
        """
        if action == 0:
            if self.agent.facing != 0:
                self.agent.reward += -2
            else:
                _x, _y = self.agent.location.x, self.agent.location.y
                self.agent.location.set_y(min(self.board.height - 1, self.agent.location.y + 1))
                self.precept()
                if self.agent.location.y != _y and not self.ontherun:
                    self.setgraph(_x=_x, _y=_y)
        elif action == 1:
            if self.agent.facing != 1:
                self.agent.reward += -2
            else:
                _x, _y = self.agent.location.x, self.agent.location.y
                self.agent.location.set_x(min(self.board.width - 1, self.agent.location.x + 1))
                self.precept()
                if self.agent.location.x != _x and not self.ontherun:
                    self.setgraph(_x=_x, _y=_y)
        elif action == 2:
            if self.agent.facing != 2:
                self.agent.reward += -2
            else:
                _x, _y = self.agent.location.x, self.agent.location.y
                self.agent.location.set_y(max(0, self.agent.location.y - 1))
                self.precept()
                if self.agent.location.y != _y and not self.ontherun:
                    self.setgraph(_x=_x, _y=_y)
        elif action == 3:
            if self.agent.facing != 3:
                self.agent.reward += -2
            else:
                _x, _y = self.agent.location.x, self.agent.location.y
                self.agent.location.set_x(max(0, self.agent.location.x - 1))
                self.precept()
                if self.agent.location.x != _x and not self.ontherun:
                    self.setgraph(_x=_x, _y=_y)
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
            # TODO add Wampus -10 and -1 for arrow shots
        # grab gold
        elif action == 7:
            if self.agent.location == self.board.goldcoord:
                self.agent.hasgold = True

        self.agent.reward += -1

    def agenetmove(self, facing, move):
        """
            move the agent to next block based on escape plan,
            first turn the agent in the correct direction
            then move agent to the next square
        :param facing: the negitive turn direction for the agent to turn
        :param move: the direct to move
        :return:
        """
        if self.agent.facing != move:
            if self.agent.facing == facing:
                self.move(5)
                print('Turn left')
                self.display()
            else:
                while self.agent.facing != move:
                    self.move(4)
                print('Turn right')
                self.display()
        self.move(move)
        self.display()

    def agentbeeline(self):
        """
            once the agent has grabbed the gold execute the ecsape plan
        :return: list : of moves to Coords(0,0)
        """
        self.ontherun = True

        # build route to Coords(0,0)
        for _r in range(0, len(self.escape) - 1):

            if self.route.nodes[self.escape[_r]]['_x'] != self.route.nodes[self.escape[_r + 1]]['_x']:
                if self.route.nodes[self.escape[_r]]['_x'] < self.route.nodes[self.escape[_r + 1]]['_x']:
                    self.agenetmove(2, 1)
                else:
                    self.agenetmove(0, 3)
            elif self.route.nodes[self.escape[_r]]['_y'] != self.route.nodes[self.escape[_r + 1]]['_y']:
                if self.route.nodes[self.escape[_r]]['_y'] < self.route.nodes[self.escape[_r + 1]]['_y']:
                    self.agenetmove(1, 0)
                else:
                    self.agenetmove(3, 2)

            if self.agent.location.x == 0 and self.agent.location.y == 0 and self.agent.hasgold == True:
                self.agent.reward += 1001
                print("You WIN your reward = ", self.agent.reward)
                self.board.terminate = True
                sys.exit()
