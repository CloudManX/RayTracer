import numpy as np

from RayTracer.Intangibles.BRDF.lambertian import Lambertian
from RayTracer.Intangibles.BRDF.specular import Specular
from RayTracer.Utils.Color import Color
from RayTracer.Intangibles.ray import Ray


class Material(object):

    def __init__(self, ka, kd, ks, cd):
        # setup the material with intensity factors
        # Args: ka - ambient intensity factor
        #       kd - diffuse intensity factor
        #       ks - specular intensity factor
        #       cd - the color of the material
        self.ambient_brdf = Lambertian(ka, cd)
        self.diffuse_brdf = Lambertian(kd, cd)
        self.specular_brdf = Specular(ks)

    def setCd(self, cd):
        # set color of the material
        self.ambient_brdf.setCD(cd)
        self.diffuse_brdf.setCD(cd)
        self.specular_brdf.setCD(cd)

    # 419begin #type=3 #src= Ray Tracing from Ground Up by Kevin Suffern
    def shade(self, sr, world):
        # Shading the object using brdf functions
        # Arg: sr - shadow record
        #      world - current world
        # Return: Color to print
        wo = -sr.ray.direction
        L = self.ambient_brdf.rho(sr, wo) * world.ambient.L(sr)
        for light in world.lights:
            wi = light.getDir(sr)
            n_dot_wi = np.dot(sr.getNormal(sr.hitPoint), wi)
            if n_dot_wi > 0.0:
                shadow_hit = False
                if light.shadow_on:
                    shadow_ray = Ray(sr.hitPoint, wi)
                    shadow_hit = light.in_shadow(shadow_ray, sr, world)
                if not shadow_hit:
                    c = self.diffuse_brdf.f(sr, wo, wi) + self.specular_brdf.f(sr, wo, wi)
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

    def area_light_shade(self, sr, world):
        # Shading the object using brdf functions regarding to a arealight source
        # Arg: sr - shadow record
        #      world - current world
        # Return: Color to print
        wo = -sr.ray.direction
        L = self.ambient_brdf.rho(sr, wo) * world.ambient.L(sr)
        for area_light in world.lights:
            wi = area_light.getDir(sr)
            n_dot_wi = np.dot(sr.getNormal(sr.hitPoint), wi)

            if n_dot_wi > 0.0:
                shadow_hit = False
                if area_light.shadow_on:
                    shadow_ray = Ray(sr.hitPoint, wi)
                    shadow_hit = area_light.in_shadow(shadow_ray, sr, world)
                if not shadow_hit:
                    c = self.diffuse_brdf.f(sr, wo, wi) + self.specular_brdf.f(sr, wo, wi)
                    L += c * area_light.L(sr) * n_dot_wi * area_light.G(sr) * (1.0 / area_light.pdf(sr))
        return self.max_to_one(L)




