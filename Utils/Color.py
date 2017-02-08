import math

class Color():

    def __init__(self, c = (0, 0, 0)):
        # Args: c - RGB value
        self.setRGB(c)
        self.__rmul__ = self.__mul__

    def setRGB(self, c):
        # Set the rgb value
        # Args: c - RGB value
        self.r = c[0]
        self.g = c[1]
        self.b = c[2]

    def __mul__(self, other):
        # Multiply the color with a factor
        if isinstance(other, float) or isinstance(other, int):
            r = int(math.floor(other * self.r))
            g = int(math.floor(other * self.g))
            b = int(math.floor(other * self.b))
            return Color((r, g, b))
        if isinstance(other, Color):
            # Multiply color with another color in RGB
            r = int(math.floor((self.r * other.r) / 255))
            g = int(math.floor((self.g * other.g) / 255))
            b = int(math.floor((self.b * other.b) / 255))
            return Color((r, g, b))

    def __div__(self, other):
        r = int(math.floor(self.r / other))
        g = int(math.floor(self.g / other))
        b = int(math.floor(self.b / other))
        return Color((r, g, b))

    def __add__(self, other):
        # Add color with another color in RGB
        r = self.r + other.r
        r = r if r <= 255 else 255
        g = self.g + other.g
        g = g if g <= 255 else 255
        b = self.b + other.b
        b = b if b <= 255 else 255
        return Color((r, g, b))

    def value(self):
        # Return a tuple that contains RGB value
        return(self.r, self.g, self.b)

