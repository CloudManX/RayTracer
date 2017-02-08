import numpy as np

from RayTracer.Intangibles.BRDF.perfectSpecular import PerfectSpecular
from RayTracer.Intangibles.BRDF.glossySpecular import GlossySpecular
from RayTracer.Intangibles.ray import Ray
from RayTracer.Intangibles.shadowRec import ShadowRec
from RayTracer.Materials.material import Material
from RayTracer.Utils.Color import Color


class GlossyReflective(Material):

    def __init__(self, ka, kd, ks, kr, cd, sampler, exp, depth=3):
        # Initialize a reflective material which inherited from material class
        super(GlossyReflective, self).__init__(ka, kd, ks, cd)
        self.kr = kr
        self.reflective_brdf = GlossySpecular(ks, cd, sampler, exp)
        self.depth_limit = depth

    def shade(self, sr, world):
        # Modified shading the object using brdf functions
        # Arg: sr - shadow record
        #      world - current world
        # Return: Color to print
        L = super(GlossyReflective, self).shade(sr, world)
        wo = -sr.ray.direction
        c = self.sample_shade(sr, wo, world)
        for i in range(0, 24):
            c += self.sample_shade(sr, wo, world)
        L += c/25
        return L

    def sample_shade(self, sr, wo, world):
        # helper function for shading multiple times
        # Args: sr - shadow record
        #       wo - input directoin
        #       world - current world we are in
        # return: color of one sample calculation
        result = self.reflective_brdf.sample_f(sr, wo)
        wi = result[0]
        pdf = result[1]
        fr = result[2]
        reflected_ray = Ray(sr.hitPoint, wi, True)
        n_dot_wi = np.dot(sr.getNormal(sr.hitPoint), wi)
        return fr * self.trace(reflected_ray, sr.depth + 1, world) * n_dot_wi / pdf

    def max_to_one(self, color):
        # normalize the color
        e = max(color.r, color.g, color.b)
        if e > 255:
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