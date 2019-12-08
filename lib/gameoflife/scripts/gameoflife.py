import click
import random
import time

from gameoflife.Game import Game

@click.command()
@click.option('--width', default=25, help='width of game board')
@click.option('--height', default=25, help='height of game board')
@click.option('--initialpop', default=20, help='percentage of the board which should be alive initially')
@click.option('--generations', default=100, help='number of generations to simulate')
@click.option('--framerate', default=10, help='number of frames per second')
def cli(width, height, initialpop, generations, framerate):
  initial_state = [
    [ True if random.random() > (1 - initialpop/100) else False
      for y in range(0, height) ]
    for x in range (0, width)
  ]

  # This defines a glider
#  initial_state[9][9] = True
#  initial_state[10][10] = True
#  initial_state[8][11] = True
#  initial_state[9][11] = True
#  initial_state[10][11] = True

  # This defines a static population (4x4 square)
#  initial_state[9][10] = True
#  initial_state[10][10] = True
#  initial_state[9][11] = True
#  initial_state[10][11] = True
    
  game = Game(width, height, initial_state)
  game.run(generations, framerate)
  print("finished")

