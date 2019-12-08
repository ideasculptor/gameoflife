from preconditions import preconditions
import time

from .Board import Board

class Game:
  """Simulate the Game of Life via console animation"""

  @preconditions(
    lambda width: isinstance(width, int),
    lambda width: width > 0,
    lambda height: isinstance(height, int),
    lambda height: height > 0,
  )
  def __init__(self, width, height, initial_state):
    self.__board = Board(width, height, initial_state)
    self.render()


  def tick(self):
    """Update state of the board with the next generation.

    Each tick replaces the previous board instance with a new one."""
    if self.__board:
      self.__board = self.__board.tick()


  def render(self):
    """Render the board's state graphically"""
    if self.__board:
      self.__board.render()


  def run(self, generations, framerate):
    """Run the game through specified generations at specified framerate
    
    Simulation stops if the population stabilizes. Framerate doesn't take
    computation time of each tick or render time into account. Console 
    doesn't refresh very quickly, anyway."""
    for i in range(0, generations):
      time.sleep(1/framerate)
      self.tick()
      if not self.__board:
        break
      self.render()

