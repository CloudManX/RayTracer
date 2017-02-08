from PIL import Image
from RayTracer.Utils.Color import Color
import math


class CheckerTexture:

    def __init__(self, size, color1= Color((0, 0, 0)), color2=Color((255, 255, 255))):
        self.size = size
        self.color1 = color1
        self.color2 = color2

    def get_color(self, sr):
        # get specifc color from current texture
        # Args: sr - shadow record
        # Returns: the color from texture
        eps = -0.000187453738
        x = sr.hitPoint[0] + eps
        y = sr.hitPoint[1] + eps
        z = sr.hitPoint[2] + eps
        temp = int(x / self.size) + int(y / self.size) + int(z / self.size)
        if temp % 2 == 0:
            return self.color1
        else:
            return self.color2