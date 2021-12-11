import random

class Generator:
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

        return points
