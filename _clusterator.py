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
    
    def __kmeans_assign_to_clusters(control: list, rest: list):
        clusters = []

        # Create clusters with only control points in them
        for cpoint in control:
            clusters.append([cpoint])

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
        # Resue the rest list for all points incl. control points
        # for reassignment during updates
        for cpoint in control:
            rest.append(cpoint)
        
        return [clusters, rest]

    def __kmeans_centroid(cluster: list):
        x_all = 0
        y_all = 0
        count = 0

        for point in cluster:
            x_all += point[0]
            y_all += point[1]
            count += 1
                    
        # Only use integer coordinates, because all points so far only have
        # integer coordinates and also this would disappear the floating point
        # imprecision problem, especially problematic for convergence precision
        # however that shouldn't be the case in Python's float implementation,
        # so it is safe to use floats instead, but the convergence will take longer
        centroid = [x_all // count, y_all // count]

        return centroid


    def kmeans_centroid(points: list, k: int, max_iterations: int) -> list:
        rest = points.copy()
        count = len(points)
        control = []
        clusters = []

        # Select k random control points (each creating a cluster)
        # Also add the control points to their clusters
        # No need to check for duplicates because each point
        # is immediately removed and also points are unique
        for j in range(k):
            i = randint(0, count - 1)
            control.append(rest[i])
            rest.pop(i)
            count -= 1

        # Assign the rest of points to the nearest control point's cluster
        # Resue the rest list for all points incl. control points
        clusters, rest = Clusterator.__kmeans_assign_to_clusters(control, rest)
                
        # Update control points using centroid rule unless convergence
        iterations = 0
        success = False
        while (not success and (iterations < max_iterations)):
            converged = 0
            for i, cluster in enumerate(clusters):

                # Calculate centroid coordinates
                centroid = Clusterator.__kmeans_centroid(cluster)
                print(centroid)

                # Add a point to the center of the cluster if it wasn't there
                # and make it a new control point for the cluster
                if (centroid not in rest):
                    control[i] = centroid
                    clusters[i] = [centroid]
                    converged = 0
                else:
                    # If a point was already at the center, successful convergence
                    # for the given cluster only, but not necessarily all.
                    clusters[i] = [centroid]
                    converged += 1

            # If the amount of converged clusters is equivalent to the amount of clusters
            # then successful convergence
            if (converged == (i + 1)):
                success = True

            # Find the closest control point for all points in all clusters
            # if the control point belongs to a different cluster, then move
            # the point. Because this would require buffers due to iteration
            # over the points, we will use rest list instead and assign as if
            # it was the first time. This should not impact the efficiency.

            # Assign the rest of points to the nearest control point's cluster
            # Resue the rest list for all points incl. control points
            clusters, rest = Clusterator.__kmeans_assign_to_clusters(control, rest)

            # Onto the next iteraton if centroid not found
            iterations += 1

        return [success, iterations, clusters, control]

    def kmeans_medoid():
        pass

    def agglome_centroid():
        pass

    def divisive_centroid():
        pass

    pass
