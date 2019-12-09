import click
import random
import time

from gameoflife.Game import Game

def random_pop(width, height, initialpop):
  """Populate the board randomly, with specified population percentage."""

  initial_state = [
    [ True if random.random() > (1 - initialpop/100) else False
      for y in range(0, height) ]
    for x in range (0, width)
  ]
  return initial_state

def glider(width, height):
  """Populate the board with a glider at upper left."""

  initial_state = [
    [ False
      for y in range(0, height) ]
    for x in range (0, width)
  ]
  initial_state[1][0] = True
  initial_state[2][1] = True
  initial_state[0][2] = True
  initial_state[1][2] = True
  initial_state[2][2] = True

  return initial_state

def beacon(width, height):
  """Populate the board with a beacon."""

  initial_state = [
    [ False
      for y in range(0, height) ]
    for x in range (0, width)
  ]

  x = width//2 - 6
  y = height//2 - 6

  def row_one(x, y):
    x = x + 2
    initial_state[x][y] = True
    x += 1
    initial_state[x][y] = True
    x += 1
    initial_state[x][y] = True
    x += 4
    initial_state[x][y] = True
    x += 1
    initial_state[x][y] = True
    x += 1
    initial_state[x][y] = True

  def row_two(x, y):
    x = x
    initial_state[x][y] = True
    x += 5
    initial_state[x][y] = True
    x += 2
    initial_state[x][y] = True
    x += 5
    initial_state[x][y] = True

  row_one(x, y)
  y += 2
  row_two(x, y)
  y += 1
  row_two(x, y)
  y += 1
  row_two(x, y)
  y += 1
  row_one(x, y)
  y += 2
  row_one(x, y)
  y += 1
  row_two(x, y)
  y += 1
  row_two(x, y)
  y += 1
  row_two(x, y)
  y += 2
  row_one(x, y)
  return initial_state


@click.command()
@click.option('--width', type=click.IntRange(20,100), default=25, help='width of game board')
@click.option('--height', type=click.IntRange(20,50), default=25, help='height of game board')
@click.option('--startpattern', type=click.Choice(['random', 'glider', 'beacon'], case_sensitive=False), default='random')
@click.option('--initialpop', type=click.IntRange(5,50), default=20, help='percentage of the board which should be alive initially')
@click.option('--generations', type=click.IntRange(10,2000, clamp=True), default=100, help='number of generations to simulate')
@click.option('--framerate', type=click.IntRange(1,100, clamp=True), default=5, help='number of frames per second')
def cli(width, height, startpattern, initialpop, generations, framerate):
  initial_state = None
  if startpattern == 'random':
    initial_state = random_pop(width, height, initialpop)
  elif startpattern == 'glider':
    initial_state = glider(width, height)
  else:
    initial_state = beacon(width, height)

  game = Game(width, height, initial_state)
  game.run(generations, framerate)

  print("complete")

