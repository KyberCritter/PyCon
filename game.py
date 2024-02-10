# Scott Ratchford
# See README.md for usage instructions and license information.

import numpy as np
from enum import IntEnum, Enum
import math
import random
import matplotlib.pyplot as plt
import sys

class Direction(Enum):
    UP = (0, 1)
    RIGHT = (1, 0)
    DOWN = (0, -1)
    LEFT = (-1, 0)
    UP_LEFT = (-1, 1)
    UP_RIGHT = (1, 1)
    DOWN_RIGHT = (1, -1)
    DOWN_LEFT = (-1, -1)

class Tile(IntEnum):
    DEAD = 1
    LIVE = 0

class Game:
    def __init__(self, x: int, y: int, seed: None | int = None):
        self.seed = seed if seed is not None else random.randint(0, int(math.pow(2, x * y) - 1))
        self.grid = np.full((x, y), fill_value=Tile.DEAD, dtype=int)
        self.populate()

    def populate(self):
        # Convert self.seed to a binary number and use that value to populate the grid
        # The resulting binary number must at least be left-padded with 0s to be 2^(x*y) bits long
        # This is done to ensure that the grid is always populated with the same number of tiles
        # for a given seed

        # Convert the seed to a binary number
        binary_seed = bin(self.seed)[2:int(math.pow(2, self.grid.shape[0] * self.grid.shape[1]))].ljust(self.grid.shape[0] * self.grid.shape[1], "0")
        # print(binary_seed)
        for i in range(0, self.grid.shape[0]):
            for j in range(0, self.grid.shape[1]):
                self.grid[i][j] = int(binary_seed[0])
                binary_seed = binary_seed[1:]
    
    def tick(self):
        # Find all the tiles that will be removed
        # Simulate a single turn of the board
        for i in range(0, self.grid.shape[0]):
            for j in range(0, self.grid.shape[1]):
                # 1. Count the number of live neighbors
                live_neighbors = 0
                for direction in Direction:
                    x, y = direction.value
                    if i + x >= 0 and i + x < self.grid.shape[0] and j + y >= 0 and j + y < self.grid.shape[1]:
                        if self.grid[i + x][j + y] == Tile.LIVE:
                            live_neighbors += 1
                
                if self.grid[i][j] == Tile.LIVE:
                    # 2. If the tile is live and has 0 or 1 live neighbors, it dies
                    if live_neighbors < 2:
                        self.grid[i][j] = Tile.DEAD

                    # 3. If the tile is live and has 2 or 3 live neighbors, it lives
                    
                    # 4. If the tile is live and has more than 3 live neighbors, it dies
                    if live_neighbors > 3:
                        self.grid[i][j] = Tile.DEAD
                elif live_neighbors == 3:
                    # 5. If the tile is dead and has exactly 3 live neighbors, it becomes live
                    self.grid[i][j] = Tile.LIVE

    def is_completed(self):
        # Game is completed if all tiles are dead
        return np.all(self.grid == Tile.DEAD)

    def display(self):
        for i in range(0, self.grid.shape[1]):
            print("-", end="")
        print()
        for i in range(0, self.grid.shape[0]):
            for j in range(0, self.grid.shape[1]):
                print(self.grid[i][j], end="")
            print()

if __name__ == "__main__":
    if len(sys.argv) > 2:
        x = int(sys.argv[1])
        y = int(sys.argv[2])
    else:
        print("Usage: python game.py <x> <y> [seed] [tick_interval]")
        sys.exit(-1)
    
    if len(sys.argv) > 3:
        try:
            seed = int(sys.argv[3])
        except ValueError:
            print("Seed must be an integer")
            sys.exit(-1)
    else:
        seed = None
    
    if len(sys.argv) > 4:
        try:
            tick_interval = float(sys.argv[4])
        except ValueError:
            print("Tick interval must be an integer or float")
            sys.exit(-1)
    else:
        tick_interval = 1
    
    game = Game(x, y, seed)
    tick_interval = 1

    prev_grid = np.invert(game.grid)
    while not game.is_completed() and not np.array_equal(prev_grid, game.grid):
        prev_grid = game.grid.copy()
        game.tick()
        # draw the grid with no axes or labels
        plt.axis('off')
        plt.imshow(game.grid, cmap="binary")
        plt.draw()
        plt.pause(tick_interval)
        plt.clf()   # Clear the plot
    if np.array_equal(prev_grid, game.grid):
        print("Game is in a stable state. Exiting.")
