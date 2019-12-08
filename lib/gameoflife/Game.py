from preconditions import preconditions

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


  def tick(self):
    """Update state of the board with the next generation.

    Each tick replaces the previous board instance with a new one. It would
    be marginally more efficient to switch between 2 boards in order to 
    avoid reallocating, but I have to leave something to talk about in the
    interview.
    """
    next_board = Board(self.__board.width, self.__board.height)
    self.__board = self.__board.tick(next_board)


  def render(self):
    """Render the board's state graphically"""
    self.__board.render()

