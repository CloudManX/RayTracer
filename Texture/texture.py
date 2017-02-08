from PIL import Image
from RayTracer.Utils.Color import Color
import math


class Texture:

    def __init__(self, picname):
        self.im = Image.open(picname)
        self.xres = self.im.size[0]
        self.yres = self.im.size[1]
        print (self.xres, self.yres)

    def get_color(self, sr):
        # get specifc color from current texture
        # Args: sr - shadow record
        # Returns: the color from texture
        x = sr.local_hit_point[0]
        y = sr.local_hit_point[1]
        z = sr.local_hit_point[2]

        theta = math.acos(y)

        phi = math.atan2(x, z)

        if phi < 0:
            phi += 2 * math.pi

        u = phi / (2 * math.pi)
        v = theta / math.pi

        col = int((self.xres - 1) * u)
        row = int((self.yres - 1) * v)

        r = self.im.getpixel((col, row))
        # print col, row
        return Color((r[0], r[1], r[2]))