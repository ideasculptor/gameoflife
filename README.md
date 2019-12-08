# Game of Life
simple interview coding test

Note: There are some very verbose comments in the code.  In real life, most of the multiline comments would be a whole lot more terse amd likely only a single line.  I definitely erred on the side of verbosity, since you'll likely read it when I'm not there, so some of the functions are a little tall, as a result.  The docstrings are legit, though.

Uses setuptools to create an executable script in the current environment.

To install, checkout the repository and change directory into it.

* Create a virtual environment named venv via `python -m venv venv`
* Activate the environment by executing `source ./venv/bin/activate` (windows users, please note that virtual envs require special instructions for you.  RTFM)
* Install the package and `gameoflife` script by running `pip install .`
* run `gameoflife --help`
* run `gameoflife` for a default execution
* To pick up live edits, use `pip install --editable .` or `python setup.py develop` when installing

## The Relevant Iterations

1. Check out the first commit to see the original 90 minute task.
1. From there, I added Board wraparound and code to detect if the board was updated after each tick in order to allow early exit. I also cleaned up the object model some, removing the upward dependency from Cell to Board by moving Cell tick logic to the Board.  
1. As I was doing that, I realized the remaining algorithm was dependent only on the set of live Cells except when rendering, and rendering dead cells doesn't require any real logic, so it was clear the array of Cells could go away entirely. I saved the change for a separate commit, but it proved remarkably simple to do. It really just required update to the set_cell_state and get_cell_state methods of Board, to utilize the live_cells set exclusively.    
1. Final cleanup fixed a minor bug that inverted width and height when using non-default values and added a really minor optimization, just to make code a little more readable (maybe).

## Notes

Performance is limited by the refresh rate of my console as the board gets larger.  High framerates have little impact on large boards.  The implemented algorithm is very space efficient. Framerate doesn't take computation or render time into account, but console updates appear to be asynchronous and happen in parallel with the sleep, so framerate is constant once it sleeps for less time than it takes to render a new frame.  At least, that's what I assume is happening.

I realize I've probably pre-empted a bunch of interview discussion by optimizing the algorithm for space efficiency, but I figure we can still talk about how to break it up into a distributed process in order to compute really large boards. Wwe'll need more graphics know how than I possess in order to render it effectively. I'm sure a browser could render a much larger board with reasonable framerate if I knew my way around SVG.  Or we could talk about algorithms to mask just the updating areas in order to avoid recomputing whole sections of the board.  A distributed process mostly solves that problem for us. It's pretty interesting to reason about what needs to be transmitted to the cluster for each tick computation - the state of all cells that border the piece computed by each node should get the job done, I think, assuming each node has the current state of its piece from the last generation computation. It'll be fun talking about how to design that..
