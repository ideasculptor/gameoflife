# Game of Life
simple interview coding test

Note: There are some very verbose comments in the code.  In real life, most of the multiline comments would be a whole lot more terse amd likely only a single line.  I definitely erred on the side of verbosity, since you'll likely read it when I'm not there, so some of the functions are a little tall, as a result. 

Uses setuptools to create an executable script in the current environment.

To install, 
* Checkout the repository and change directory into it.
* Create a virtual environment named venv via `python -m venv venv`
* Activate the environment by executing `source ./venv/bin/activate` (windows users, please note that virtual envs require special instructions for you.  See Python docs for details)
* Install the package and `gameoflife` script by running `pip install .`
* run `gameoflife --help`
* run `gameoflife` for a default execution, add `--startpattern glider` or `--startpattern beacon` for non-random initializations
* To pick up live edits, use `pip install --editable .` or `python setup.py develop` when installing
* deactivate the virtual env by running `deactivate`

## The Relevant Iterations

1. Check out the first commit to see the original 90 minute task.
1. From there, I added Board wraparound and code to detect if the board was updated after each tick in order to allow early exit with static boards. I also cleaned up the object model some, removing the upward dependency from Cell to Board by moving Cell tick logic to the Board.  
1. As I was doing that, I realized the remaining algorithm was dependent only on the set of live Cells except when rendering, and rendering dead cells doesn't require any real logic, so it was clear the array of Cells could go away entirely. I saved the change for a separate commit, but it proved remarkably simple to do. It really just required update to the set_cell_state and get_cell_state methods of Board, to utilize the live_cells set exclusively.    
1. Final cleanup fixed a minor bug that inverted width and height when using non-default values and added a really minor optimization, just to make code a little more readable (maybe).
1. Somehwre in there I made rendering faster by not clearing the board before each pass and adjusting sleep time to account for computation and render time.
1. Added various initialization patterns - random, beacon, glider.  random is the default and you can specify the population size as a percentage. Use `--help`

## Notes

Performance was severely hampered by the preconditions library I used initially. Once the profiler turned that up, I removed the library but didn't replace all the precondition checks. 

Framerate currently takes computation and render time into account, but the first version didn't. It is now capable of running at very rapid framerates (a function of board size, however, so I won't give absolute numbers), but the tty can't refresh that quickly on my macbook. 

The current algorithm implementation is very space efficient relative to board size. Storage size is O(live cells) and Computation complexity is O(live cells + dead cells adjacent to live cells). Rendering is O(W x H). All 3 were O(W x H) originally.  Storage could be made smaller by using a more space efficient data format for storing the data, but I don't think it can get algorithmically smaller.

I realize I've probably pre-empted a bunch of interview discussion by optimizing my original algorithm, but I left the commit history intact and I figure we can still talk about how to break it up into a parallel process in order to compute really large boards.  It's pretty interesting to reason about what needs to be transmitted between nodes for each tick computation in a parallel system.

To be honest, I go through my regular code and optimize it to much the same extent that I've cleaned this up. I'm not just showing off here - things tend to percolate in my head, involuntarily, until I get the code clarity and performance I'm looking for - but it's not something that lends itself to a 90 minute time interval. Plus, I was re-learning python, which gave me further impetus to think about it after it was ostensibly complete.
