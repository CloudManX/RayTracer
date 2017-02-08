import numpy as np
class ShadowRec():

    def __init__(self, hits = False, t = None, material = None, normal_func = None , ray = None):
        # Record for a hit of light and object
        self.h = hits
        self.t = t
        self.mat = material
        self.getNormal = normal_func
        self.ray = ray
        self.depth = 0
        self.hitPoint = None
        self.local_hit_point = np.array([0, 0, 0])


    # Get and set functions
    def hits(self):
        return self.h

    def setHits(self):
        self.h = True

    def getTValue(self):
        return self.t

    def setTValue(self, t):
        self.t = t

    def getMat(self):
        return self.mat

    def setMat(self, mat):
        self.mat = mat

    def getRay(self):
        return self.ray

    def setRay(self, ray):
        self.ray = ray

    def setGetNormal(self, func):
        self.getNormal = func

    def setHitPoint(self):
        self.hitPoint = self.ray.getPoint(self.t)
