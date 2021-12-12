import random
import pickle

class Generator:
    # Use pickle to dump a list of points
    def savePoints(points: list, filename: str):
        with open(filename, "wb") as f:
            pickle.dump(points, f)
    
    # Use pickle to load a list of points
    def loadPoints(filename: str):
        points = []
        with open(filename, "rb") as f:
            points = pickle.load(f)
        return points

    def generatePoints(fieldsize, startsize, size, maxoffset):
        # Points that will be generated and returned
        points = []

        # Starter points (startsize amount)
        # These points are randomly generated around the field
        # with unique coordinated
        # todo make generation less random by guaranteeing that the
        # todo newly generated points won't be too close to existing ones
        i = 0
        while (i != startsize):
            x = random.randint(-fieldsize, fieldsize)
            y = random.randint(-fieldsize, fieldsize)
            starter = [x,y]
            if (starter not in points):
                points.append(starter)
                i += 1

        # todo generate the rest of points

        return points