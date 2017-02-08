

import numpy as np
import math
from RayTracer.Intangibles.BRDF.lambertian import Lambertian
from RayTracer.Intangibles.BRDF.specular import Specular
from RayTracer.Intangibles.BRDF.SV_Lambertian import SV_Lambertian
from RayTracer.Utils.Color import Color
from RayTracer.Intangibles.ray import Ray


class TextureMatt(object):

    def __init__(self, ka, kd, ks, texture):
        # setup the material with intensity factors
        # Args: ka - ambient intensity factor
        #       kd - diffuse intensity factor
        #       ks - specular intensity factor
        #       cd - the color of the material
        self.ambient_brdf = SV_Lambertian(ka, texture)
        self.diffuse_brdf = SV_Lambertian(kd, texture)
        self.specular_brdf = Specular(ks)

    # 419begin #type=3 #src= Ray Tracing from Ground Up by Kevin Suffern
    def shade(self, sr, world):
        # Shading the object using brdf functions
        # Arg: sr - shadow record
        #      world - current world
        # Return: Color to print
        wo = -sr.ray.direction
        L = self.ambient_brdf.rho(sr) * world.ambient.L(sr)
        for light in world.lights:
            wi = light.getDir(sr)
            n_dot_wi = np.dot(sr.getNormal(sr.hitPoint), wi)
            if n_dot_wi > 0.0:
                shadow_hit = False
                if light.shadow_on:
                    shadow_ray = Ray(sr.hitPoint, wi)
                    shadow_hit = light.in_shadow(shadow_ray, sr, world)
                if not shadow_hit:
                    c = self.diffuse_brdf.f(sr) + self.specular_brdf.f(sr, wo, wi)
                    L += c * (light.L(sr) * n_dot_wi)
        return self.max_to_one(L)

    # 419end

    def max_to_one(self, color):
        # Preventing overflow
        e = max(color.r, color.g, color.b)
        if (e > 255):
            ratio = e / 255
            c = Color((int(color.r / ratio), int(color.g / ratio), int(color.b / ratio)))
            return c
        return color




