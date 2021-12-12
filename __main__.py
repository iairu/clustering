from _generator import Generator
from _visualizator import Visualizator
from _clusterator import Clusterator

from datetime import datetime

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
    # every ... points on <-field;field> x and y axes draw a line
    lineevery = 1000 
    # (t) will be replaced with a timestamp and (s) with a size 
    # if empty then display on screen instead
    exportname = "export/(t)_graph_(s).png"
    # colors for individual clusters, if k > len(colors) then they will loop
    # valid options: https://matplotlib.org/stable/tutorials/colors/colors.html
    colors = ["r", "g", "b", "m"] 

    # --------------------------------------------------------------------------------------------

    # Generate and select points to be used
    _all = Generator.generatePoints(field, startsize, max(sizes), maxoffset)
    _all2 = Generator.generatePoints(field, startsize, max(sizes), maxoffset) # tmp demo
    _all3 = Generator.generatePoints(field, startsize, max(sizes), maxoffset) # tmp demo
    _all4 = Generator.generatePoints(field, startsize, max(sizes), maxoffset) # tmp demo
    _all5 = Generator.generatePoints(field, startsize, max(sizes), maxoffset) # tmp demo

    # Run and time clustering algorithms for every point count

    # Visualize clusters of points per algorithm incl. times
    # Globally initiate the visualizator with common values for field size, line count and plot colors
    vis = Visualizator(field, lineevery, colors)

    # Specify the exportname for the given instance with an up-to-date timestamp and a correct size
    currname = exportname.replace("(s)", "sizetodo")
    timestamp = datetime.now().strftime("%Y-%m-%dT%H-%M-%S")
    currname = currname.replace("(t)", timestamp)
    # Then plot all of the clusters for the given instance (algorithm), include a title and export
    vis.plot([_all, _all2, _all3, _all4, _all5], "Hello world!", currname)


    return

if __name__ == "__main__":
    main()