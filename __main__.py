from _generator import Generator
from _visualizator import Visualizator
from _clusterator import Clusterator

from datetime import datetime
from os.path import exists

from time import perf_counter

def main():
    # OPTIONS
    


    # - GENERATOR
    # generate fresh points and save them into the cachename file or reuse existing pointcache
    # file for a cached point pool (it will be created if it doesn't exist, reused as long as it exists)
    cachename = "cachedpoints/cache.bin"
    # value for both x,y from center in both positive and negative directions (inclusive)
    field = 5000 
    # number of points with unique coordinates to generate at the beginning randomly
    startsize = 20
    # number of points that will be generated on top of the startsize afterwards
    # maximal value of these will be used for point generation, others will be derived from the
    # previously generated points
    # sizes = [1000, 2500, 10000, 20000]
    sizes = [1000]
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
    success = 500 # todo implement



    # - TIMING
    # time testing rerun count
    # all will use the same settings mentioned above
    # difference between runs will occur for random selection of control points and thus time to convergence
    timing_reruns = 50



    # - VISUALIZATION
    # every ... points on <-field;field> x and y axes draw a line
    lineevery = 1000 
    # (t) will be replaced with a timestamp and (s) with a size 
    # if empty then display on screen instead
    exportname = "export/(t)_graph_(s).png"
    # colors for individual clusters, if k > len(colors) then they will loop
    # valid options: https://matplotlib.org/stable/tutorials/colors/colors.html
    colors = ["r", "g", "b", "m"]
    # (t) will be replaced with a timestamp and (s) with a size 
    # if empty then display on screen instead
    timing_exportname = "export/(t)_time_(s).png"
    # maximal amount of seconds to plot on graph
    # this will normalize graph ranges between all sizes
    # set to 0 for range relative to given single graph's values
    timing_maxy = 0.01



    # --------------------------------------------------------------------------------------------



    # - GENERATOR
    # Generate or load all points (point pool) for all algorithms and sizes
    if (exists(cachename)):
        pool = Generator.loadPoints(cachename)
    else:
        # Pool will have (max(sizes) + startsize) points
        pool = Generator.generatePoints(field, startsize, max(sizes), maxoffset)
        Generator.savePoints(pool, cachename)
    # Non-randomly select points to be used depending on sizes
    # Points will exactly match the given size
    selected = []
    for size in sizes:
        selected.append(Generator.modSelectPoints(pool, size))



    # - CLUSTERING + TIMING
    # Run and time clustering algorithms for every point count

    # Clusters graph data
    titles = []
    clusters = []

    # Times graph data
    alg_range = range(1) # number of active algorithms
    times = [[[] for alg in alg_range] for size in sizes]
    times_titles = ["K-Means Centroid wip"]

    for rerun in range(timing_reruns):
        # For each size (in other words selected size's points)
        # Run all algorithms, get their output "localclusters" and append them to clusters (all)
        # Also save titles that include count data and other user constants
        for i, points in enumerate(selected):
            alg_pos = 0

            # Run a benchmark for an algorithm
            time = perf_counter()
            localclusters = Clusterator.kmeans_centroid(points, k)
            time = perf_counter() - time

            # Save for timing (all runs considered)
            times[i][alg_pos].append(time) # times[size][algorithm] = [times for each rerun]
            alg_pos += 1

            # Save for scatter plot
            # Only last rerun considered otherwise there would be hundreds of plots
            if (rerun == timing_reruns - 1):
                # Create a graph title
                # Considering modSelectPoints, the sizes should be equivalent 
                # to user defined sizes, for demonstration use a recounted size
                recount = sum(len(cluster) for cluster in localclusters)
                title = "K-Means Centroid wip (k = " + str(k) + ", " + str(recount) + " points)"
                
                # Save for graph (only final run considered)
                clusters.append(localclusters)
                titles.append(title)



    # - VISUALIZATION
    # Visualize clusters of points per algorithm incl. times
    # Globally initiate the visualizator with common values for field size, line count and plot colors
    vis = Visualizator(field, lineevery, timing_maxy, colors)

    # Clusters graph
    for i, localclusters in enumerate(clusters):
        # Specify the exportname for the given instance with an up-to-date timestamp and a correct size
        _exportname = exportname.replace("(s)", str(sizes[i]))
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        _exportname = _exportname.replace("(t)", timestamp)
        # Then plot all of the clusters for the given instance (algorithm), include a title and export
        vis.plot(localclusters, titles[i], _exportname)

    # Times graph
    for i, times_per_size in enumerate(times):
        # Specify the exportname for the given instance with an up-to-date timestamp and a correct size
        _exportname = timing_exportname.replace("(s)", str(sizes[i]))
        timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
        _exportname = _exportname.replace("(t)", timestamp)
        # Plot timing
        vis.time(times_per_size, times_titles, "Algorithm times (k = " + str(k) + ", size = " + str(size) + ")", _exportname)



    return

if __name__ == "__main__":
    main()