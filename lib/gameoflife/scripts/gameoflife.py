import time
import click

from gameoflife.Game import Game

@click.command()
@click.option('--width', default=25, help='width of game board')
@click.option('--height', default=25, help='height of game board')
@click.option('--generations', default=100, help='number of generations to simulate')
@click.option('--framerate', default=15, help='number of frames per second')
def cli(width, height, generations, framerate):
  initial_state = [[False for y in range(0, height)] for x in range (0, width)]
  initial_state[9][9] = True
  initial_state[10][10] = True
  initial_state[8][11] = True
  initial_state[9][11] = True
  initial_state[10][11] = True
    
  game = Game(width, height, initial_state)
  game.run(generations, framerate)
  print("finished")

