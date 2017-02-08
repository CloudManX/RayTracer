import numpy as np
from RayTracer.GameObjects.bbox import BBox
from RayTracer.Intangibles.shadowRec import ShadowRec

class Rectangle():

    def __init__(self, center, width, height, normal, material, kEpsilon = 0.00001):
        self.c = center
        self.width = width
        self.height = height
        self.n = normal / np.linalg.norm(normal)
        self.mat = material
        self.kEpsilon = kEpsilon
        self.calcPoints()
        self.bbox = BBox(self.getBBox())

    def calcPoints(self):
        u = np.array([0, 1, 0])
        w = np.cross(self.n, u)
        self.p0 = self.c + (self.height/2.0) * u + (self.width/2.0) * w
        self.p1 = self.c + (self.height/2.0) * u - (self.width/2.0) * w
        self.p2 = self.c - (self.height/2.0) * u + (self.width/2.0) * w
        self.p3 = self.c - (self.height/2.0) * u - (self.width/2.0) * w
        self.sideA = self.p1 - self.p0
        self.sideB = self.p2 - self.p0
        self.a_len_squared = np.linalg.norm(self.sideA) * np.linalg.norm(self.sideA)
        self.b_len_squared = np.linalg.norm(self.sideB) * np.linalg.norm(self.sideB)
        print (self.a_len_squared , self.b_len_squared)

    def getBBox(self):
        delta = 0.0001
        # Find the max x, y, z value of corner points respectively
        x_max = max(self.p0[0], self.p1[0], self.p2[0], self.p3[0]) + delta
        x_min = min(self.p0[0], self.p1[0], self.p2[0], self.p3[0]) - delta
        y_max = max(self.p0[1], self.p1[1], self.p2[1], self.p3[1]) + delta
        y_min = min(self.p0[1], self.p1[1], self.p2[1], self.p3[1]) - delta
        z_max = max(self.p0[2], self.p1[2], self.p2[2], self.p3[2]) + delta
        z_min = min(self.p0[2], self.p1[2], self.p2[2], self.p3[2]) - delta
        lower = (x_min, y_min, z_min)
        upper = (x_max, y_max, z_max)
        return lower, upper

    def hit(self, ray):
        sr = ShadowRec()
        if not self.bbox.isHit(ray):
            return sr
        denom = np.dot(ray.direction, self.n)
        if denom == 0:
            return sr
        t = np.dot((self.p0 - ray.origin), self.n) / denom
        if t <= self.kEpsilon:
            return sr

        d = ray.getPoint(t) - self.p0

        d_dot_a = np.dot(d, self.sideA)
        if d_dot_a < 0.0 or d_dot_a > self.a_len_squared:
            return sr

        d_dot_b = np.dot(d, self.sideB)
        if d_dot_b < 0.0 or d_dot_b > self.b_len_squared:
            return sr

        sr.setHits()
        sr.setTValue(t)
        sr.setMat(self.mat)
        sr.setRay(ray)
        sr.setGetNormal(self.getNormal)
        sr.setHitPoint()
        return sr

    def shadow_hit(self, ray):
        sr = self.hit(ray)
        if sr.hits():
            return True, sr.getTValue()
        else:
            return False, 0

    def getNormal(self, *args):
        return self.n

    def setSampler(self, sampler):
        self.sampler = sampler
        self.sampler.generate_samples()

    def sample(self):

        sp = self.sampler.sample_unit_square()
        return self.p0 + sp[0] * self.sideA + sp[1] * self.sideB

    def pdf(self, *args): return 1.0 / (self.width * self.height)