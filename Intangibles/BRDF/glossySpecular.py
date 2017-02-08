from RayTracer.Utils.Color import Color
import numpy as np
import math


class GlossySpecular:

    def __init__(self, ks, cs, sampler, exp):
        self.ks = ks
        self.cs = cs
        self.sampler = sampler
        self.exp = exp

    def f(self, sr, wo, wi):
        # BRDF function
        L = Color((0, 0, 0))
        normal = sr.getNormal(sr.hitPoint)
        n_dot_wi = np.dot(normal, wi)
        r = -wi + 2.0 * normal * n_dot_wi
        r_dot_wo = np.dot(r, wo)

        if r_dot_wo > 0:
            L = self.ks * self.cs * math.pow(r_dot_wo, self.exp)

        return L

    def sample_f(self, sr, wo):
        # sampling BRDF
        normal = sr.getNormal(sr.hitPoint)
        n_dot_wo = np.dot(normal, wo)
        r = -wo + 2.0 * normal * n_dot_wo

        w = r
        u = np.cross(np.array([0.00424, 1, 0.00764]), w)
        u /= np.linalg.norm(u)
        v = np.cross(u, w)

        sp = self.sampler.sample_hemisphere()
        wi = sp[0] * u + sp[1] * v + sp[2] * w

        # check if the sampling point is above the plane
        cos_theta = np.dot(normal, wi)
        # if not flip them
        if cos_theta < 0.0:
            wi = -sp[0] * u - sp[1] * v + sp[2] * w

        r_dot_wi = np.dot(r, wi)
        phong_lobe = math.pow(r_dot_wi, self.exp)
        pdf = phong_lobe * np.dot(normal, wi)

        c = self.ks * self.cs * phong_lobe

        return wi, pdf, c