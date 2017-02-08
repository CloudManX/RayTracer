import numpy as np

from RayTracer.Intangibles.BRDF.perfectSpecular import PerfectSpecular
from RayTracer.Intangibles.ray import Ray
from RayTracer.Intangibles.shadowRec import ShadowRec
from RayTracer.Materials.material import Material
from RayTracer.Utils.Color import Color

class Reflective(Material):

    def __init__(self, ka, kd, ks, kr, cd, depth = 3):
        # Initialize a reflective material which inherited from material class
        super(Reflective, self).__init__(ka, kd, ks, cd)
        self.kr = kr
        self.reflective_brdf = PerfectSpecular(kr, cd)
        self.depth_limit = depth

    def shade(self, sr, world):
        # Modified shading the object using brdf functions
        # Arg: sr - shadow record
        #      world - current world
        # Return: Color to print
        L = super(Reflective, self).shade(sr, world)
        wo = -sr.ray.direction
        result = self.reflective_brdf.sample_f(sr, wo)
        wi = result[0]
        fr = result[1]
        reflected_ray = Ray(sr.hitPoint, wi, True)
        n_dot_wi = np.dot(sr.getNormal(sr.hitPoint), wi)
        L += fr * self.trace(reflected_ray, sr.depth + 1, world) * n_dot_wi

        return L

    def area_light_shade(self, sr, world):
        # Shading the object using brdf functions regarding to a arealight source
        # Arg: sr - shadow record
        #      world - current world
        # Return: Color to print
        wo = -sr.ray.direction
        L = super(Reflective, self).area_light_shade(sr, world)
        wo = -sr.ray.direction
        result = self.reflective_brdf.sample_f(sr, wo)
        wi = result[0]
        fr = result[1]
        reflected_ray = Ray(sr.hitPoint, wi)
        n_dot_wi = np.dot(sr.getNormal(sr.hitPoint), wi)
        L += fr * self.trace(reflected_ray, sr.depth + 1, world) * n_dot_wi

        return self.max_to_one(L)

    def max_to_one(self, color):
        e = max(color.r, color.g, color.b)
        if (e > 255):
            ratio = e / 255
            c = Color((int(color.r / ratio), int(color.g / ratio), int(color.b / ratio)))
            return c
        return color

    def trace(self, ray, depth, world):
        # trace rays on the hit point to be called recursively
        # Args: ray - incident ray
        #       depth - depth of reflection
        #       world - the world object is in
        # Return; Color of the tracing result
        if depth > self.depth_limit:
            return Color((0, 0, 0))
        else:
            sr_ = ShadowRec()
            for obj in world.objects:
                sr = obj.hit(ray)
                if sr.hits() and (not sr_.hits() or sr_.getTValue() > sr.getTValue()):
                    sr_ = sr

            if sr_.hits():
                sr_.setRay(ray)
                sr_.depth = depth
                return sr_.mat.shade(sr_, world)
            else:
                return Color((0, 0, 0))