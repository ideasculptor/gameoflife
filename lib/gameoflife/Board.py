import sys
from collections import defaultdict
from preconditions import preconditions

from .Cell import Cell

class Board:
  """Represents the current state of the GoL universe."""

  @preconditions(
    lambda width: isinstance(width, int) and width > 0,
    lambda height: isinstance(height, int) and height > 0,
  )
  def __init__(self, width, height, initial_state = None):
    self.__width = width
    self.__height = height

    # Keep a separate list of live_cells, to limit iteration over the full
    # board when the universe is large. Only live cells and their neighbours
    # can change state during a tick
    self.__live_cells = set()


    # Build 2 dimensional array of cells via list comprehension
    self.__cells = [
      [ Cell(self, x, y) for y in range(height) ] for x in range(width)
    ]

    if initial_state != None:
      # populate the board with any initial state provided
      for x in range(self.width):
        for y in range(self.height):
          self.set_cell_state(x, y, initial_state[x][y])


  @property
  def width(self):
    return self.__width


  @property
  def height(self):
    return self.__height


  @preconditions(
    lambda self, x: x >= 0 and x < self.width,
    lambda self, y: y >= 0 and y < self.height,
  )
  def get_cell_state(self, x, y):
    return self.__cells[x][y].alive


  @preconditions(
    lambda self, x: x >= 0 and x < self.width,
    lambda self, y: y >= 0 and y < self.height,
    lambda state: isinstance(state, bool),
  )
  def set_cell_state(self, x, y, state):
    """Update the state of a cell, adding the cell's coords to __live_cells"""
    if state:
      self.__cells[x][y].generate()
      self.__live_cells.add((x, y))
    else:
      self.__cells[x][y].die()
      # We don't actually need this line, since we use a fresh buffer for each
      # generation, so there's no need to clean up.  In truth, the board
      # should be immutable after creation in a particular state, in order
      # to avoid this issue entirely, but I'm time limited.
      self.__live_cells.discard((x, y))

  
  def tick(self, next):
    # Keep a count of dead cells that are adjacent to live cells
    dead_neighbours = defaultdict(int)

    # Only need to tick currently live cells, plus dead ones with 3 neighbours.
    # We compute neighbours while computing the tick of current live cells,
    # So we can create the list of dead cells with live neighbours and their
    # count while processing the current live set
    for (x, y) in self.__live_cells:
      next.set_cell_state(x, y, self.__cells[x][y].tick(dead_neighbours))

    # find all dead cells with exactly 3 neighbours, and bring them to life
    for (neighbour, count) in dead_neighbours.items():
      next.set_cell_state(neighbour[0], neighbour[1], count == 3)

    return next


  def render(self):
    """Render each cell via ASCII"""

    # clears the console and resets cursor to upper left
    sys.stdout.write("\033[2J")
    for y in range(0, self.height):
      for x in range(0, self.width):
        self.__cells[x][y].render()
      print()

