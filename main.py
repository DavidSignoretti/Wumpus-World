from WumpusWorld import WumpusWorld
import random as rd
import sys

if __name__ == '__main__':
    rd.seed()

    name = ["Move the agent one block north",
            "Move the agent one block east",
            "Move the agent one block south",
            "Move the agent one block west",
            "Agent turn right",
            "Agent turn left",
            "Shoot arrow",
            "Grab gold",
            "Climb out"]

    agent = WumpusWorld.Agent()
    board = WumpusWorld.Board(4, 4, 2)
    action = WumpusWorld.Action(board, agent)

    for _i in range(0, rd.randrange(10, 500)):
        _m = rd.randrange(0, 8)
        action.move(_m)
        print("Agent moved ", name[_m])
        for _h in range(board.height, 0, -1):


            # sys.stdout.write("\n")
            for _w in range(board.width):
                _l = ""
                sys.stdout.write("----" * board.width)
                sys.stdout.write("\n")
                sys.stdout.write("|")
                grid: WumpusWorld.Coords = WumpusWorld.Coords(_w, _h)
                if board.wumpuscoord == grid:
                    _l += "W" if board.wumpusalive else "w"
                if board.goldcoord == grid:
                    _l += "G"
                for _p in range(len(board.pitscoord)):
                    if board.pitscoord[_p] == grid:
                        _l += "P"
                if agent.location == grid:
                    _l += "A"
                sys.stdout.write(_l)
            sys.stdout.write("|")
            sys.stdout.write("\n")
            print("----" * board.width)