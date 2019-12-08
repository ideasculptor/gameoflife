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
    self.__cells = [ [ Cell() for y in range(height) ] for x in range(width) ]

    if initial_state != None:
      # populate the board with any initial state provided
      for x in range(self.width):
        for y in range(self.height):
          if initial_state[x][y]:
            self.set_cell_state(x, y, True)


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
    """Update the state of a cell.

    Adds the cell's coords to __live_cells, and returns bool indicator
    of whether state changed or not.
    """
    if state:
      self.__live_cells.add((x, y))
      return self.__cells[x][y].generate()
    else:
      # We don't actually need this line, since we use a fresh buffer for each
      # generation, so there's no need to clean up.  In truth, the board
      # should be immutable after creation in a particular state, in order
      # to avoid this issue entirely, but I'm time limited.
      self.__live_cells.discard((x, y))
      return self.__cells[x][y].die()

  
  def tick(self, next):
    """Compute the state of the next board, which is passed in as a buffer"""

    # If nothing changes, indicate that, since the game can stop
    is_mod = False

    # Keep a count of dead cells that are adjacent to live cells
    dead_neighbours = defaultdict(int)

    # Only need to tick currently live cells, plus dead ones with 3 neighbours.
    # We compute neighbours while computing the tick of current live cells,
    # So we can create the list of dead cells with live neighbours and their
    # count while processing the current live set
    for (x, y) in self.__live_cells:
      next_state = self.tick_cell(x, y, dead_neighbours)
      next.set_cell_state(x, y, next_state)

      if next_state != self.get_cell_state(x, y):
        is_mod = True

    # find all dead cells with exactly 3 neighbours, and bring them to life
    for (neighbour, count) in dead_neighbours.items():
      if count == 3:
        next.set_cell_state(neighbour[0], neighbour[1], True)
        is_mod = True

    if not is_mod:
      return None

    return next


  def tick_cell(self, x, y, dead_neighbours):
    """Compute the next state of a single cell.

    Receives a map of neighbour_coords -> count of live neighbours, which 
    is incremented for each neighbour, if this cell is alive."""

    live_neighbours = 0

    # Could use a global lookup to prevent recomputing on every pass, but
    # that is complicated by board wrap semantics
    neighbours = self.compute_neighbours(x,y)

    if self.get_cell_state(x, y):
      # All live cells with 2 or 3 live neighbours survive, all others die
      for neighbour in neighbours:
        if self.get_cell_state(*neighbour):
          live_neighbours += 1
        else:
          dead_neighbours[neighbour] += 1

      if live_neighbours == 2 or live_neighbours == 3:
        return True

    else:
      # Ideally, this branch is never called.  Caller can perform tick on the
      # current live set, and then just directly update the cells in 
      # dead_neighbours that have count = 3.  This branch is here just for
      # correctness, in case someone brute forces a board through a tick on 
      # every cell. It ensures unit tests would pass correctly.
      for neighbour in neighbours:
        if self.get_cell_state(*neighbour):
          live_neighbours += 1

      if live_neighbours == 3:
        return True

    return False    


  def compute_neighbours(self, x, y):
    # compute a set of neighbor cell addresses. Handle board edge semantics

    neighbours = set()
    for i in range(x - 1, x + 2):
      if i == self.width:
        i = 0
      elif i < 0:
        i = self.width - 1

      for j in range(y - 1, y + 2):
        if j == self.height:
          j = 0
        elif j < 0:
          j = self.height - 1

        if (i, j) == (x, y):
          continue

        neighbours.add((i,j))

    return neighbours


  def render(self):
    """Render each cell via ASCII"""

    # clears the console and resets cursor to upper left
    sys.stdout.write("\033[2J")
    for y in range(0, self.height):
      for x in range(0, self.width):
        self.__cells[x][y].render()
      print()

