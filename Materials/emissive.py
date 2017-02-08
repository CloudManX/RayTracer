import numpy as np

from RayTracer.Utils.Color import Color


class Emissive:

    def __init__(self, ls, ce):
        self.ls = ls # radiance scaling facot
        self.ce = ce # color

    def area_light_shade(self, sr, world):
        # Shade the Emissive light source
        # Args: sr - shadow record of a ray hit
        #       world - the world light source is in
        if np.dot(-sr.getNormal(), sr.ray.direction) > 0.0:
            return self.ce * self.ls
        else:
            return Color((0, 0, 0))

    def get_Le(self, sr):
        # calculate the default light intensity of the light source
        return self.ce * self.ls