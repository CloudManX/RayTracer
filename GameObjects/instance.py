import sys

import numpy as np

from RayTracer.Intangibles.ray import Ray
from bbox import BBox


class Instance:

    def __init__(self, obj, mat):
        self.object = obj
        self.tMatrix = np.identity(4)
        self.invMatrix = np.linalg.inv(self.tMatrix)
        self.bbox = self.calcBBox()
        self.mat = mat

    def calcBBox(self):
        # Calculate the new bounding box after transformation
        # Args: Void
        # Return: Void
        points = []
        # p0
        p = np.array([self.object.bbox.x0, self.object.bbox.y0, self.object.bbox.z0])

        points.append(np.dot(self.tMatrix, np.append(p, [1])))
        p = np.array([self.object.bbox.x0, self.object.bbox.y0, self.object.bbox.z1])
        points.append(np.dot(self.tMatrix, np.append(p, [1])))
        p = np.array([self.object.bbox.x0, self.object.bbox.y1, self.object.bbox.z0])
        points.append(np.dot(self.tMatrix, np.append(p, [1])))
        p = np.array([self.object.bbox.x0, self.object.bbox.y1, self.object.bbox.z1])
        points.append(np.dot(self.tMatrix, np.append(p, [1])))
        p = np.array([self.object.bbox.x1, self.object.bbox.y0, self.object.bbox.z0])
        points.append(np.dot(self.tMatrix, np.append(p, [1])))
        p = np.array([self.object.bbox.x1, self.object.bbox.y0, self.object.bbox.z1])
        points.append(np.dot(self.tMatrix, np.append(p, [1])))
        p = np.array([self.object.bbox.x1, self.object.bbox.y1, self.object.bbox.z0])
        points.append(np.dot(self.tMatrix, np.append(p, [1])))
        p = np.array([self.object.bbox.x1, self.object.bbox.y1, self.object.bbox.z1])
        points.append(np.dot(self.tMatrix, np.append(p, [1])))

        x_min = sys.maxint
        y_min = sys.maxint
        z_min = sys.maxint

        x_max = -sys.maxint
        y_max = -sys.maxint
        z_max = -sys.maxint

        for point in points:
            if point[0] < x_min:
                x_min = point[0]
            if point[1] < y_min:
                y_min = point[1]
            if point[2] < z_min:
                z_min = point[2]

        for point in points:
            if point[0] > x_max:
                x_max = point[0]
            if point[1] > y_max:
                y_max = point[1]
            if point[2] > z_max:
                z_max = point[2]

        return BBox(((x_min, y_min, z_min), (x_max, y_max, z_max)))

    def hit(self, ray):
        # Check if the inversely transformed rays hit an object
        # Args: ray - input trace ray
        # Return: Void
        o = np.dot(self.invMatrix, np.append(ray.origin, [1]))
        d = np.dot(self.invMatrix, np.append(ray.direction, [0]))
        inv_origin = np.array([o[0], o[1], o[2]])
        inv_direction = np.array([d[0], d[1], d[2]])
        inv_ray = Ray(inv_origin, inv_direction)

        sr = self.object.hit(inv_ray)
        if sr.hits():
            sr.setGetNormal(self.getNormal)
            sr.setMat(self.mat)
            sr.setRay(ray)
        return sr

    def shadow_hit(self, ray):
        """ check if the shadow ray hits the object
        Args:
            ray: a vector that shoots out from view plane
        Returns: tuple of (bool and t)
        """
        sr = self.hit(ray)
        if sr.hits():
            return True, sr.getTValue()
        else:
            return False, 0

    def getNormal(self, pt):
        # Transform the normal with the original
        # Args: pt - hit point
        # Return: the corresponding normal
        temp = np.dot(self.invMatrix, np.append(self.object.getNormal(pt), [0]))
        normal = np.array([temp[0], temp[1], temp[2]])
        normal /= np.linalg.norm(normal)
        return normal

    def translate(self, x, y, z):
        # translate the instance object in three directions
        # Args: x - translation along x-axis
        #       y - translation along y-axis
        #       z - translation along z-axis
        # Return: Void
        self.tMatrix[0][3] = x
        self.tMatrix[1][3] = y
        self.tMatrix[2][3] = z
        self.updateInv()
        self.bbox = self.calcBBox()

    def scale(self, a, b, c):
        # scale the instance object in three dimensions
        # Args: a - scaling along x-axis
        #       b - scaling along y-axis
        #       c - scaling along z-axis
        # Return: Void
        self.tMatrix[0][0] = a
        self.tMatrix[1][1] = b
        self.tMatrix[2][2] = c
        self.updateInv()
        self.bbox = self.calcBBox()

    def updateInv(self):
        # Update the corresponding inverse matrix data in the class
        self.invMatrix = np.linalg.inv(self.tMatrix)

