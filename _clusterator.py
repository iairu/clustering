from random import randint
from math import sqrt

def distance(pointa: list, pointb: list):
    x1, y1 = pointa
    x2, y2 = pointb

    a = abs(x1 - x2) # delta x
    b = abs(y1 - y2) # delta y
    pytag = sqrt(a*a + b*b)

    return pytag

class Clusterator:
    
    def kmeans_centroid(points: list, k: int) -> list: # todo add convergence user limit
        rest = points.copy()
        count = len(points)
        control = []
        clusters = []

        # Select k control points (each creating a cluster)
        # Also add the control points to their clusters
        # No need to check for duplicates because each point
        # is immediately removed and also points are unique
        for j in range(k):
            i = randint(0, count - 1)
            control.append(rest[i])
            clusters.append([rest[i]])
            rest.pop(i)
            count -= 1

        # print("K-Means Centroid, size = " + str(count + k))
        # print("Control points: " + str(control))

        # Assign the rest of points to the nearest control point's cluster
        for rpoint in rest:
            closest_i = None
            closest_dist = None

            # Find the closest control point
            # todo neighbor matrix of distances
            for i, cpoint in enumerate(control):
                dist = distance(cpoint, rpoint)
                if (closest_dist == None or dist < closest_dist):
                    closest_i = i
                    closest_dist = dist

            # Assign the point to the cluster
            clusters[closest_i].append(rpoint)

        # All points have been assigned to a cluster
        rest = []
        count = 0
                
        # todo Update all points using centroid rule until convergence

        return clusters

    def kmeans_medoid():
        pass

    def agglome_centroid():
        pass

    def divisive_centroid():
        pass

    pass
