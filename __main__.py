from _generator import Generator
from _visualizator import Visualizator
from _clusterator import Clusterator
from matplotlib import pyplot

def main():
    # OPTIONS
    
    # - GENERATOR
    # value for both x,y from center in both positive and negative directions (inclusive)
    field = 5000 
    # number of points with unique coordinates to generate at the beginning randomly
    startsize = 20
    # number of points that will be generated on top of the startsize afterwards
    # maximal value of these will be used for point generation, others will be derived from the
    # previously generated points
    sizes = (1000, 2500, 10000, 20000)
    # a randomly selected point will be used after the generation of startsize points
    # for a subsequent generation of sizes[i] points, which shall be generated around such point
    # with an offset, whose maximum can be the value below (inclusive)
    # offset will be reduced for points nearing border to guarantee a more ideal placement of new 
    # points away from the borders of the field
    maxoffset = 100

    # - CLUSTERING
    # k-means count of control points, also its count of clusters
    k = 3
    # value for both x,y for maximal allowed average distance from the center for clustering
    # if the average is this value or lower it means clustering success, else failure (inclusive)
    success = 500

    # - VISUALIZATION

    # --------------------------------------------------------------------------------------------

    # Generate and select points to be used
    _all = Generator.generatePoints(field, startsize, max(sizes), maxoffset)
    print(_all)

    # Run and time clustering algorithms for every point count

    # Visualize clusters of points per algorithm incl. times
    pyplot.style.use("_mpl-gallery")
    fig, ax = pyplot.subplots()

    ax.scatter(*zip(*_all), vmin=-field, vmax=field)

    ax.set(xlim=(-field, field),
           ylim=(-field, field))

    pyplot.show()

    return

if __name__ == "__main__":
    main()