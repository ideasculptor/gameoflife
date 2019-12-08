import sys
from collections import defaultdict
# from preconditions import preconditions

class Board:
  """Represents the current state of the GoL universe."""

   # preconditions package profiles as SUPER-slow, and has no built-in
   # mechanism for easy disable. I left them here so you know I didn't
   # neglect safety checks entirely.
#  @preconditions(
#    lambda width: isinstance(width, int) and width > 0,
#    lambda height: isinstance(height, int) and height > 0,
#  )
  def __init__(self, width, height, initial_state = None):
    """Initialize the board. 

    initial_state should be a 2 dimensional array of bool."""

    self.__width = width
    self.__height = height

    # Keep a list of live_cells, to prevent iteration over a full board
    # Only live cells and their immediate neighbours can change state
    # during a tick so we don't need the full board in memory
    self.__live_cells = set()

    # populate the board with any initial state provided
    if initial_state != None:
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


#  @preconditions(
#    lambda self, x: x >= 0 and x < self.width,
#    lambda self, y: y >= 0 and y < self.height,
#  )
  def get_cell_state(self, x, y):
    if (x, y) in self.__live_cells:
      return True


#  @preconditions(
#    lambda self, x: x >= 0 and x < self.width,
#    lambda self, y: y >= 0 and y < self.height,
#    lambda state: isinstance(state, bool),
#  )
  def set_cell_state(self, x, y, state):
    """Update the state of a cell.

    Adds the cell's coords to __live_cells"""
    if state:
      if (x, y) not in self.__live_cells:
        self.__live_cells.add((x, y))
    else:
      if (x, y) in self.__live_cells:
        # We don't actually need this line. We use a fresh buffer for each
        # generation so there's no need to clean up.  In truth, the board
        # should be immutable after creation in a particular state, in order
        # to avoid this issue entirely, but I'm time limited.
        self.__live_cells.remove((x, y))

  
  def tick(self):
    """Compute the state of the next board, which is passed in as a buffer"""

    next = Board(self.width, self.height)

    # If nothing changes, indicate that, since the game can stop
    is_mod = False

    # Keep a count of dead cells that are adjacent to live cells
    dead_neighbours = defaultdict(int)

    # Only need to tick currently live cells, plus dead ones with 3 neighbours.
    # We iterate neighbours while computing the tick of current live cells,
    # so we can create the list of dead cells with live neighbours and their
    # count while processing the current live set
    for (x, y) in self.__live_cells:
      (next_state, state_changed) = self.tick_cell(x, y, dead_neighbours)
      if next_state:
        next.set_cell_state(x, y, next_state)

      if state_changed:
        is_mod = True

    # We now have a map of all dead cells with at least one adjacent live cell,
    # since we have checked the neighbours of all live cells. find all dead
    # cells with exactly 3 neighbours, and bring them to life
    for (neighbour, count) in dead_neighbours.items():
      if count == 3:
        next.set_cell_state(*neighbour, True)
        is_mod = True

    if not is_mod:
      return None

    return next


  def tick_cell(self, x, y, dead_neighbours):
    """Compute the next state of a single cell.

    Receives a map of neighbour_coords -> count of live neighbours, which 
    is incremented for each neighbour, if this cell is alive.
    Returns a tuple of the next value and whether the value changed."""

    live_neighbours = 0
    next_state = False
    state_changed = False

    # Could calculate inline with update, but it is still a constant time
    # operation, just a slightly faster one
    neighbours = self.compute_neighbours(x, y)

    if self.get_cell_state(x, y):
      for neighbour in neighbours:
        if self.get_cell_state(*neighbour):
          live_neighbours += 1
        else:
          dead_neighbours[neighbour] += 1

      # All live cells with 2 or 3 live neighbours survive, all others die
      if live_neighbours == 2 or live_neighbours == 3:
        next_state = True
      else:
        state_changed = True
    else:
      # Caller can perform tick on the current live set, and then just directly
      # update the cells in dead_neighbours that have count = 3.  This branch
      # ensures unit tests would pass correctly, but is otherwise unnecessary.
      for neighbour in neighbours:
        if self.get_cell_state(*neighbour):
          live_neighbours += 1

      if live_neighbours == 3:
        next_state = True
        state_changed = True

    return (next_state, state_changed)


  def compute_neighbours(self, x, y):
    """compute a set of neighbor cell addresses. 

    Handle board edge semantics here. This version wraps"""

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

        neighbours.add((i, j))
    return neighbours


  def render(self):
    """Render each cell as ASCII character"""

    # clears the console and resets cursor to upper left
    sys.stdout.write("\033[2J")

    for y in range(0, self.height):
      for x in range(0, self.width):
        if (x, y) not in self.__live_cells:
          # render dead cells with inverse colors and print a space.
          sys.stdout.write("\033[7m  \033[0m")
        else:
          sys.stdout.write("  ")
      sys.stdout.write("\n")
    sys.stdout.flush()

