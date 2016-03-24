import numpy as np
from RayTracer.Utils.Color import Color

class AmbientLight:

    def __init__(self, ls = 1.0):
        # setup ambient light with light intensity
        self.ls = ls
        self.color = Color((255, 255, 255))

    def getDir(self, sr):
        return np.array([0.0, 0.0, 0.0])

    def L(self, sr):
        return self.color.mul_f(self.ls)

class DirectionalLight:

    def __init__(self, ls = 1.0, shadow_on = False):
        # setup directional light
        # Args: shadow_on - bool for whether using the shadow
        self.ls = ls
        self.color = Color((255, 255, 255))
        self.shadow_on = shadow_on

    def getDir(self, sr):
        # get the direction of the light
        return np.array([0.0, 0.0, 1.0])

    def L(self, sr):
        # return the color of the light
        return self.color.mul_f(self.ls)


class PointLight:

    def __init__(self, location, ls = 2.0, shadow_on = False):
        # setup point light
        # Args: shadow_on - bool for whether using the shadow
        self.ls = ls
        self.color = Color((255,255,255))
        self.loc = location
        self.shadow_on = shadow_on

    def getDir(self, sr):
        # get the direction of the light
        dir = (self.loc - sr.getHitPoint())
        dir /= np.linalg.norm(dir)
        return dir

    def L(self, sr):
        return self.color.mul_f(self.ls)

    def in_shadow(self, ray, sr, w):
        # check the shadow relations among objects
        # Args: ray - shadow ray
        #       sr - shadow record
        #       w - the current world
        # return: bool for the situation
        dir = self.loc - ray.origin
        d = np.linalg.norm(dir)
        for obj in w.objects:
            # print(obj.shadow_hit(ray)[0])
            if (obj.shadow_hit(ray)[0] and obj.shadow_hit(ray)[1] < d):
                return True

        return False
