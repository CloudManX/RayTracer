import math
import numpy as np
from RayTracer.Utils.Color import Color

class Specular(object):

    def __init__(self, k, cd):
        # Set up specular light
        # Args: k - intensity
        #       cd - color
        self.k = k
        self.cd = cd
        self.exp = 1

    # 419begin #type=3 #src= Ray Tracing from Ground Up by Kevin Suffern
    def f(self, sr, wo, wi):
        # brdf
        hit_point = sr.getHitPoint()
        r = -wi + 2.0 * sr.getNormal(hit_point) * np.dot(sr.getNormal(hit_point), wi)
        r_dot_wo = np.dot(r, wo)
        if (r_dot_wo > 0.0):
            f = self.k * math.pow(r_dot_wo, self.exp)
            return self.cd.mul_f(f)
        return Color()
    # 419 end

    def rho(self, sr, wo):
        return self.cd.mul_f(self.k)

    def setK(self, k):
        self.k = k

    def setCD(self, cd):
        self.cd = cd

