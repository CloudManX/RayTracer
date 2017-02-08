import numpy as np
import math
from RayTracer.Intangibles.BRDF.perfectSpecular import PerfectSpecular
from RayTracer.Intangibles.BDTF.perfectTransmitter import PerfectTransmitter
from RayTracer.Intangibles.shadowRec import ShadowRec
from RayTracer.Utils.Color import Color
from RayTracer.Materials.material import Material
from RayTracer.Intangibles.ray import Ray


class Transparent(Material):

    def __init__(self, ka, kd, ks, kr, kt, cd, depth=2):
        super(Transparent, self).__init__(ka, kd, ks, cd)
        self.reflective_brdf = PerfectSpecular(kr, cd)
        self.specular_btdf = PerfectTransmitter(kt, 0.9)
        self.depth_limit = depth

    def shade(self, sr, world):
        # Shading the object using brdf functions
        # Arg: sr - shadow record
        #      world - current world
        # Return: Color to print
        wo = -sr.ray.direction
        L = super(Transparent, self).shade(sr, world)
        wo = -sr.ray.direction
        n = sr.getNormal(sr.hitPoint)
        temp = self.reflective_brdf.sample_f(sr, wo)
        wi = temp[0]
        fr = temp[1]
        reflected_ray = Ray(sr.hitPoint, wi)

        if self.specular_btdf.tir(sr):
            L += self.trace(reflected_ray, sr.depth + 1, world)
        else:
            temp = self.specular_btdf.sample_f(sr, wo)
            wt = temp[0]
            ft = temp[1]
            transmitted_ray = Ray(sr.hitPoint, wt)

            L += fr * self.trace(reflected_ray, sr.depth + 1, world) * math.fabs(np.dot(n, wi))
            L += ft * self.trace(transmitted_ray, sr.depth + 1, world) * math.fabs(np.dot(n, wi))

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