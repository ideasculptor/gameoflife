import sys
from preconditions import preconditions

class Cell:
  """Represents the state of a single cell in a GoL Board"""

  @preconditions(
    lambda alive: isinstance(alive, bool),
  )
  def __init__(self, alive = False):
    self.__alive = alive


  @property
  def alive(self):
    return self.__alive


  def die(self):
    self.__alive = False


  def generate(self):
    self.__alive = True


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

