import numpy as np
from RayTracer.Utils.Color import Color

class AmbientLight:

    def __init__(self, ls = 1.0):
        # setup ambient light with light intensity
        self.ls = ls
        self.color = Color((0, 0, 0))

    def getDir(self, sr):
        return np.array([0.0, 0.0, 0.0])

    def L(self, sr):
        return self.color * self.ls

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
        return self.color * self.ls


class PointLight:

    def __init__(self, location, ls = 2.0, shadow_on = False):
        # setup point light
        # Args: shadow_on - bool for whether using the shadow
        self.ls = ls
        self.color = Color((255, 255, 255))
        self.loc = location
        self.shadow_on = shadow_on

    def getDir(self, sr):
        # get the direction of the light
        direction = (self.loc - sr.hitPoint)
        direction /= np.linalg.norm(direction)
        return direction

    def L(self, sr):
        return self.color * self.ls

    def in_shadow(self, ray, sr, w):
        # check the shadow relations among objects
        # Args: ray - shadow ray
        #       sr - shadow record
        #       w - the current world
        # return: bool for the situation
        direction = self.loc - ray.origin
        d = np.linalg.norm(direction)
        for obj in w.objects:
            # print(obj.shadow_hit(ray)[0])
            if obj.shadow_hit(ray)[0] and obj.shadow_hit(ray)[1] < d:
                return True

        return False


class AreaLight:

    def __init__(self, geometry, emissiveMat, shadow_on = False):
        self.lightSourceShape = geometry
        self.emi = emissiveMat
        self.normal = None
        self.wi = None
        self.sample_point = None
        self.shadow_on = shadow_on
        self.kEpsilon = 0.00001

    def in_shadow(self, ray, sr, w):
        # check the shadow relations among objects
        # Args: ray - shadow ray
        #       sr - shadow record
        #       w - the current world
        # return: bool for the situation
        direction = self.sample_point - ray.origin
        ts = np.dot(direction, ray.direction)
        for obj in w.objects:
            # print(obj.shadow_hit(ray)[0])
            if obj.shadow_hit(ray)[0] and obj.shadow_hit(ray)[1] + self.kEpsilon < ts:
                return True
        return False

    def getDir(self, sr):
        # Get the direction of the area light
        # Args: sr - shadow record of a ray hit
        # Return: the direciton of the incident ray
        self.sample_point = self.lightSourceShape.sample()
        self.normal = self.lightSourceShape.getNormal(self.sample_point)
        self.wi = self.sample_point - sr.hitPoint
        self.wi /= np.linalg.norm(self.wi)

        return self.wi

    def L(self, sr):
        # L term of the BRDF for area light calculation
        # Args: sr - shadow record of a ray hit
        # Return: Base color
        n_dot_d = np.dot(-self.normal, self.wi)
        if n_dot_d > 0.0:
            return self.emi.get_Le(sr)
        else:
            return Color((0, 0, 0))

    def G(self, sr):
        # Calculate the g term
        n_dot_d = np.dot(-self.normal, self.wi)
        denom_temp = self.sample_point - sr.hitPoint
        denom_temp = np.linalg.norm(denom_temp)
        denom = denom_temp * denom_temp
        return n_dot_d / denom

    def pdf(self, sr):
        # Calculate the specific PDF for different objects
        return self.lightSourceShape.pdf(sr)
