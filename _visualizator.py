import matplotlib
from matplotlib import pyplot
from matplotlib import ticker

def frange(start, step, stop):
    # float range without numpy
    fr = []
    while (start < stop):
        fr.append(start)
        start += step
    return fr

class Visualizator:
    def __init__(self, field: int, lineevery: int, timeMaxY: float, colors: list):
        self.field = field
        self.lineevery = lineevery
        self.colors = colors
        self.timeMaxY = timeMaxY
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
        ax.xaxis.set_minor_formatter(ticker.FuncFormatter(lambda x, y: x))
        ax.yaxis.set_minor_formatter(ticker.FuncFormatter(lambda x, y: x))

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
        # Set the point size (by area) to minimal allowed (1)
        for cluster in clusters:
            ax.scatter(*zip(*cluster), s=1) # zip sets the x,y args of .scatter separately from a (x,y) pair list

        # Output depending on whether to display on screen or export
        if (export):
            # Export the result as a PNG
            pyplot.savefig(exportname)
        else:
            # Show the result on screen
            pyplot.show()

    def time(self, times_per_size: list, alg_titles: list, title: str = "", exportname: str = ""):
        colors = self.colors
        maxy = self.timeMaxY
        export = (exportname != "")
        
        # Calculate average times
        runs = len(times_per_size[0])
        alg_range = range(len(times_per_size))
        avgs = [0.0 for alg in alg_range]
        # Time per size, then algorithm
        for a, times_per_alg in enumerate(times_per_size):
            # Add all runs at once and arithmetic average
            avgs[a] += sum(times_per_alg)
            avgs[a] /= runs
        
        # Hide toolbar for preview window
        matplotlib.rcParams['toolbar'] = 'None'

        # Create a graph (window) of 5x5 inches
        fig, ax = pyplot.subplots(figsize=(5,5))

        # Adjust the x,y values to be in frame
        pyplot.subplots_adjust(left=0.1, bottom=0.05, top=0.95, right=0.99)
        if (maxy > 0):
            ax.set(ylim=(0, maxy))

        # Set a graph title
        ax.set_title(title)
        ax.set_ylabel("Time per run (sec)")
        ax.set_xlabel("Runs")

        # Set colors for individual .plot additions
        ax.set_prop_cycle(color=colors)

        # Add plot data for times per algorithm into the graph
        for i, times_per_alg in enumerate(times_per_size):
            ax.plot(range(runs), times_per_alg, linewidth=2.0, label=(alg_titles[i] + " (avg " + "{:.3f}".format(avgs[i]) + ")"))

        # Add a legend showing the labels
        ax.legend(loc='upper right')

        # Output depending on whether to display on screen or export
        if (export):
            # Export the result as a PNG
            pyplot.savefig(exportname)
        else:
            # Show the result on screen
            pyplot.show()

        return
