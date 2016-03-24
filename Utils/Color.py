import math

class Color():

    def __init__(self, c = (0, 0, 0)):
        # Args: c - RGB value
        self.setRGB(c)

    def setRGB(self, c):
        # Set the rgb value
        # Args: c - RGB value
        self.r = c[0]
        self.g = c[1]
        self.b = c[2]

    def mul_f(self, factor):
        # Multiply the color with a factor
        r = int(math.floor(factor * self.r))
        g = int(math.floor(factor * self.g))
        b = int(math.floor(factor * self.b))
        return Color((r, g, b))

    def mul(self, color):
        # Multiply color with another color in RGB
        r = int(math.floor((self.r * color.r) / 255))
        g = int(math.floor((self.g * color.g) / 255))
        b = int(math.floor((self.b * color.b) / 255))
        return Color((r, g, b))

    def add(self, color):
        # Add color with another color in RGB
        r = self.r + color.r
        r = r if r <= 255 else 255
        g = self.g + color.g
        g = g if g <= 255 else 255
        b = self.b + color.b
        b = b if b <= 255 else 255
        return Color((r, g, b))

    def value(self):
        # Return a tuple that contains RGB value
        return(self.r, self.g, self.b)

