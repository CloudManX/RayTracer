import numpy as np

class Ray():

    # #419begin #type=3 #src=Prof. Eric Shaffer https://github.com/shaffer1/UIllinois_Rendering/blob/master/Code/Sphere.py
    def __init__(self, origin, direction, reflected = False):
        self.origin = origin
        self.direction = direction
        self.number = -1
        self.reflected = reflected

    def getPoint(self, t):
        return self.origin + t * self.direction
    # #419end

    def getNumber(self):
        return self.number

    def setNumber(self, number):
        self.number = number

    def setDirection(self, d):
        self.direction = d / np.linalg.norm(d)