from preconditions import preconditions
import time

from .Board import Board

class Game:
  """Simulate the Game of Life via console animation

  For testing, Boards and Cells really ought to be dependency injected.
  That would allow mocks to be injected and each layer of the hierarchy to
  be tested independently
  """

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

    Each tick replaces the previous board instance with a new one. It would
    be marginally more efficient to switch between 2 boards in order to 
    avoid reallocating, but I have to leave something to talk about in the
    interview.
    """
    if not self.complete:
      next_board = Board(self.__board.width, self.__board.height)
      self.__board = self.__board.tick(next_board)


  @property
  def complete(self):
    return self.__board == None


  def render(self):
    """Render the board's state graphically"""
    if not self.complete:
      self.__board.render()


  def run(self, generations, framerate):
    for i in range(0, generations):
      time.sleep(1/framerate)
      self.tick()
      self.render()
      if self.complete:
        break

