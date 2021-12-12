import matplotlib
from matplotlib import pyplot

class Visualizator:
    def __init__(self, field: int, lineevery: int, colors: list):
        self.field = field
        self.lineevery = lineevery
        self.colors = colors
        return

    # This always creates and outputs a single complete scatter-plot graph from clusters
    # Each cluster is a set of (x,y) points and gets its own color from self.colors
    # All clusters = [[(x,y), (x,y), ...], [...], [...], ...]
    def plot(self, clusters: list, title: str = "", exportname: str = ""):
        field = self.field
        lineevery = self.lineevery
        colors = self.colors
        export = (exportname != "")

        # Hide toolbar for preview window
        matplotlib.rcParams['toolbar'] = 'None'

        # Create a graph (window) of 5x5 inches
        fig, ax = pyplot.subplots(figsize=(5,5))

        # Adjust the x,y values to be in frame
        pyplot.subplots_adjust(left=0.1, bottom=0.05, top=0.95, right=0.99)

        # Crosshair the center
        ax.set_xticks([0])
        ax.set_yticks([0])

        # Set the amount of minor grid/drop lines (except last value labels, because they don't fit well)
        ax.set_xticks(range(-field, field, lineevery), minor=True) # exclusive range stop -> no last label
        ax.set_yticks(range(-field, field + lineevery, lineevery), minor=True) # incl. last label

        # Show values on minor lines
        ax.xaxis.set_minor_formatter('{x: .0f}')
        ax.yaxis.set_minor_formatter('{x: .0f}')

        # Show minor lines in a slightly transparent color
        ax.grid(which='minor', alpha=0.4)
        ax.grid(which='major', alpha=1)

        # Set maximal graph values to be the max. values of the field
        ax.set(xlim=(-field, field), ylim=(-field, field))

        # Set a graph title
        ax.set_title(title)

        # Set colors for individual .scatter additions
        ax.set_prop_cycle(color=colors)

        # Add point data for a single cluster into the graph
        # Behind the scenes example: clusters = Generator.generatePoints(field, startsize, max(sizes), maxoffset)
        for cluster in clusters:
            ax.scatter(*zip(*cluster)) # zip sets the x,y args of .scatter separately from a (x,y) pair list

        # Output depending on whether to display on screen or export
        if (export):
            # Export the result as a PNG
            pyplot.savefig(exportname)
        else:
            # Show the result on screen
            pyplot.show()
