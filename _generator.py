from random import randint
import pickle

class Generator:
    # Use pickle to dump a list of points
    def savePoints(points: list, filename: str):
        with open(filename, "wb") as f:
            pickle.dump(points, f)
    
    # Use pickle to load a list of points
    def loadPoints(filename: str) -> list:
        points = []
        with open(filename, "rb") as f:
            points = pickle.load(f)
        return points

    # Select a precise amount of points from a point pool
    # This function will always select the same nth point (non-random)
    def modSelectPoints(pool: list, size: int) -> list:
        points = []

        n = len(pool) // size # integer division => floor => there will be some outliers
        i = 0
        j = 0
        for point in pool:
            # Only add every nth point to match the size
            if (i % n == 0):
                points.append(point)
                j += 1
                # Don't add outliers above size limit
                # (there will be at least startsize of them, considering the way generatePoints works)
                if (j >= size):
                    break
            i += 1

        return points

    def generatePoints(fieldsize: int, startsize: int, size: int, maxoffset: int) -> list:
        # Points that will be generated and returned
        # Total amount will be startsize + size
        points = []
        pcount = 0

        # Starter points (startsize amount)
        # These points are randomly generated around the field
        # with unique coordinated
        i = 0
        while (i != startsize):
            x = randint(-fieldsize, fieldsize)
            y = randint(-fieldsize, fieldsize)
            starter = [x,y]
            if (starter not in points):
                points.append(starter)
                i += 1
        pcount = startsize

        # Generate the rest of points
        i = 0
        while (i != size):
            # Select any existing point
            n = randint(0, pcount - 1)
            parent_x, parent_y = points[n]
            # Calculate existing point's offset
            edgeoffset_x = fieldsize - abs(parent_x)
            edgeoffset_y = fieldsize - abs(parent_y)
            # If the existing point is too close (under existing offset) to either edge, reduce offset for the new point
            # Only reduce offset for the given edge that the point is close to
            edge_rightx = True if (parent_x > 0) else False
            edge_topy = True if (parent_y > 0) else False
            # Calculate the new maximal offset for each side for the new point
            max_leftx = (maxoffset - edgeoffset_x) if (not edge_rightx and edgeoffset_x < maxoffset) else maxoffset
            max_rightx = (maxoffset - edgeoffset_x) if (edge_rightx and edgeoffset_x < maxoffset) else maxoffset
            max_boty = (maxoffset - edgeoffset_y) if (not edge_topy and edgeoffset_y < maxoffset) else maxoffset
            max_topy = (maxoffset - edgeoffset_y) if (edge_topy and edgeoffset_y < maxoffset) else maxoffset
            # Generate a random offset from calculated maxes as the position of the new point
            offset_x = randint(-max_leftx, max_rightx)
            offset_y = randint(-max_boty, max_topy)
            # Create a possibly non-unique point
            adder = [parent_x + offset_x, parent_y + offset_y]
            # Make sure the point is unique, if so append, else try again in next iteration
            if (adder not in points):
                points.append(adder)
                i += 1
                # print(f"{str(startsize + i)}")
                # print(f"generator p  ({str(parent_x)},{str(parent_y)})")
                # print(f"max offset X <-{str(max_leftx)}; {str(max_rightx)}>")
                # print(f"max offset Y <-{str(max_boty)}; {str(max_topy)}>")
                # print(f"new p        ({str(adder[0])},{str(adder[1])})")
        # pcount = startsize + size

        return points