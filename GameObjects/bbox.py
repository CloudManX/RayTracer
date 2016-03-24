import numpy as np
import sys

class BBox(object):
    def __init__(self, bound = None, kEpsilon = 0.00001):
        # Set up the bounding box with a given bound
        # Args: bound - a tuple of two tuples representing upper and lower bound
        if(bound):
            self.setBox(bound)
        self.kEpsilon = kEpsilon

    def setBox(self, bound):
        # set the bounding box with a new bound
        lower = bound[0]
        upper = bound[1]
        self.x0 = lower[0]
        self.y0 = lower[1]
        self.z0 = lower[2]
        self.x1 = upper[0]
        self.y1 = upper[1]
        self.z1 = upper[2]
        self.t0 = 0
        self.t1 = 0

    def isInside(self, v):
        # Check a specific point is inside the box
        # Args: v - coordinates of the point
        # Return: bool of the situation
        first_condition = (v[0] >= self.x0 and v[1] >= self.y0 and v[2] >= self.z0)
        second_condition = (v[0] <= self.x1 and v[1] <= self.y1 and v[2] <= self.z1)
        return first_condition and second_condition

    def isHit(self, ray):
        # Check if a ray hits the box
        # Args: ray - a ray object shooting in
        # Return: bool of the situation
        ox = ray.origin[0]
        oy = ray.origin[1]
        oz = ray.origin[2]
        dx = ray.direction[0]
        dy = ray.direction[1]
        dz = ray.direction[2]

        if dx == 0:
            a = sys.maxint
        else:
            a = 1.0 / dx
        if (a >= 0):
            self.tx_min = (self.x0 - ox) * a
            self.tx_max = (self.x1 - ox) * a
        else:
            self.tx_min = (self.x1 - ox) * a
            self.tx_max = (self.x0 - ox) * a
        if dy == 0:
            b = sys.maxint
        else:
            b = 1.0 / dy
        if (b >= 0):
            self.ty_min = (self.y0 - oy) * b
            self.ty_max = (self.y1 - oy) * b
        else:
            self.ty_min = (self.y1 - oy) * b
            self.ty_max = (self.y0 - oy) * b
        if dz == 0:
            c = sys.maxint
        else:
            c = 1.0 / dz
        if (c >= 0):
            self.tz_min = (self.z0 - oz) * c
            self.tz_max = (self.z1 - oz) * c
        else:
            self.tz_min = (self.z1 - oz) * c
            self.tz_max = (self.z0 - oz) * c

        self.t0 = max(self.tx_min, self.ty_min, self.tz_min)
        self.t1 = min(self.tx_max, self.ty_max, self.tz_max)

        return (self.t0 < self.t1 and self.t1 > self.kEpsilon)

    def getLowerBound(self):
        return np.array([self.x0, self.y0, self.z0])

    def getUpperBound(self):
        return np.array([self.x1, self.y1, self.z1])