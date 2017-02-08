import math


class SV_Lambertian:
    def __init__(self, kd, tex):
        self.kd = kd
        self.tex = tex

    def rho(self, sr):
        # Get texture color dynamically
        return self.kd * self.tex.get_color(sr)

    def f(self, sr):
        # BRDF
        return self.kd * self.tex.get_color(sr) / math.pi
