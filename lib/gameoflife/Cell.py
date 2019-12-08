import sys
from preconditions import preconditions

class Cell:
  """Represents the state of a single cell in a GoL Board"""

  @preconditions(
    lambda board, x: isinstance(x, int) and x >= 0 and x < board.width,
    lambda board, y: isinstance(y, int) and y >= 0 and y < board.height,
    lambda alive: isinstance(alive, bool),
  )
  def __init__(self, board, x, y, alive = False):
    self.__board = board
    self.__x = x
    self.__y = y
    self.__alive = alive

    # Keep a list of neighbor cell addresses, to avoid recomputing, especially
    # cell's at the edge of the board. Better code would provide an iterator
    # instead of maintaining a list..
    self.__neighbours = [
      (x, y)
      for x in range(max(self.x - 1, 0), min(self.x + 2, self.board.width))
      for y in range(max(self.y - 1, 0), min(self.y + 2, self.board.height))
      if (x, y) != (self.x, self.y)
    ]


  @property
  def board(self):
    return self.__board


  @property
  def x(self):
    return self.__x


  @property
  def y(self):
    return self.__y


  @property
  def alive(self):
    return self.__alive


  def die(self):
    self.__alive = False


  def generate(self):
    self.__alive = True


  def tick(self, dead_neighbours):
    """Return the state of this cell in the next generation."""

    live_neighbours = 0

    if self.alive:
      # All live cells with 2 or 3 live neighbours survive, all others die
      for neighbour in self.__neighbours:
        if self.board.get_cell_state(*neighbour):
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
      for neighbour in self.__neighbours:
        if self.board.get_state(*neighbour):
          live_neighbours += 1

      if live_neighbours == 3:
        return True

    return False    


  def render(self):
    """Render the cell as space/inverted-space for alive/dead, respectively"""
    if self.alive:
      print('  ', end = "")
    else:
      # render dead cells with inverse colors and print space
      # cells are 2 spaces to make board wider relative to height
      sys.stdout.write("\033[7m")
      print("  ", end="")
      sys.stdout.write("\033[0m")


