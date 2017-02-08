import math
from RayTracer.Utils.Color import Color

class Lambertian(object):

    def __init__(self, k, cd):
        # set up a Lambertian light
        # Args: k - intensity factor
        #       cd - color
        self.k = k
        self.cd = cd

    def f(self, sr, wo, wi):
        #brdf
        factor = self.k / math.pi
        return self.cd * factor

    # perfect diffuse
    def rho(self, sr, wo):
        return self.cd * self.k

    def setKD(self, k):
        self.kd = k

    def setCD(self, cd):
        self.cd = cd

