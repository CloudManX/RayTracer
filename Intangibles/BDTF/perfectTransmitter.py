import numpy as np
import math
from RayTracer.Utils.Color import Color

class PerfectTransmitter:

    def __init__(self, kt=0.0, ior=1.0):
        self.kt = kt
        self.ior = ior

    def f(self):
        # F function - return black
        return Color((0, 0, 0))

    def sample_f(self, sr, wo):
        # Sampling function on the refracted ray
        # Return: wt, Color
        n = sr.getNormal(sr.hitPoint)
        cos_thetai = np.dot(n, wo)
        eta = self.ior

        if cos_thetai < 0.0:
            cos_thetai = - cos_thetai
            # reverse the direction of normal
            n = -n
            eta = 1.0 / eta

        cos_thetat_square = 1.0 - (1.0 - cos_thetai * cos_thetai) / (eta * eta)
        cos_thetat = math.sqrt(cos_thetat_square)

        wt = -wo / eta - (cos_thetat - cos_thetai / eta) * n

        temp = self.kt / (eta * eta)
        normal = sr.getNormal(sr.hitPoint)
        ft = temp * Color((255, 255, 255)) / math.fabs(np.dot(normal, wt))
        return wt, ft

    def rho(self):
        # rho function - return black
        return Color((0, 0, 0))

    def tir(self, sr):
        # Check if thetai exceeds the critical angle
        # Args: sr - shadow record from ray
        # Returns: bool value for the condition
        wo = -sr.ray.direction
        normal = sr.getNormal(sr.hitPoint)
        cos_thetai = np.dot(normal, wo)
        eta = self.ior

        if cos_thetai < 0.0:
            eta = 1.0 / eta

        return 1.0 - (1.0 - cos_thetai * cos_thetai) / (eta * eta) < 0.0