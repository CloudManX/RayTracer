from RayTracer.Utils.Color import Color
import numpy as np


class PerfectSpecular:

    def __init__(self, k, cr):
        self.k = k
        self.cr = cr

    def f(self):
        # F function - return black
        return Color((0, 0, 0))

    def sample_f(self, sr, wo):
        # Perfect specular sampling function
        normal = sr.getNormal(sr.hitPoint)
        n_dot_wo = np.dot(normal, wo)
        wi = -wo + 2.0 * normal * n_dot_wo
        n_dot_wi = np.dot(normal, wi)
        return wi, self.k * self.cr / n_dot_wi

    def rho(self):
        # rho function - return black
        return Color((0, 0, 0))