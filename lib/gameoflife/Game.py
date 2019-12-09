from preconditions import preconditions
import sys
import time

from .Board import Board

class Game:
  """Simulate the Game of Life via console animation"""

  @preconditions(
    lambda width: isinstance(width, int) and width > 0,
    lambda height: isinstance(height, int) and height > 0,
  )
  def __init__(self, width, height, initial_state):
    self.__board = Board(width, height, initial_state)


  def tick(self):
    """Update state of the board with the next generation.

    Each tick replaces the previous board instance with a new one."""
    if self.__board:
      self.__board = self.__board.tick()


  def render(self):
    """Render the board's state graphically"""
    if self.__board:
      self.__board.render()


  @preconditions(
    lambda generations: isinstance(generations, int),
    lambda generations: generations > 0 and generations <= 2000,
    lambda framerate: isinstance(framerate, int),
    lambda framerate: framerate > 0 and framerate <= 200,
  )
  def run(self, generations, framerate):
    """Run the game through specified generations at specified framerate
    
    Simulation stops if the population stabilizes. Framerate doesn't take
    computation time of each tick or render time into account. Console 
    doesn't refresh very quickly, anyway."""

    t0 = time.perf_counter()
    sys.stdout.write("\033[2J")
    self.render()

    for i in range(0, generations):
      t1 = time.perf_counter()
      time.sleep(max(1/framerate - (t1 - t0), 0))
      t0 = time.perf_counter()

      self.tick()
      if not self.__board:
        break
      self.render()

