import numpy


class ViewPlane():

    def __init__(self, hres, vres):
        """ initialize view plane with user defined horizontal and
            vertical int value
        Args:
             hres: int horizontal width for the view plane
             vres: int vertical height for the view plane
        Returns: void
        """
        self.hres = hres
        self.vres = vres
        self.setCorners(numpy.array([-1.0, -1.0, 0.0]), numpy.array([1.0, 1.0, 0.0]))

    # <Comment flag> #419begin #type=<1> #src=<Prof. Eric Shaffer>
    def setCorners(self, minC, maxC):
        """ set the size of pixel on the view plane with top-right corner
            and bottom left corner
        Args:
             maxC: vector representing 3D point on max corner on view space
             minC: vector representing 3D point on minimum corner on view space
        Returns: void
        """
        self.minCorner = minC
        self.maxCorner = maxC
        self.size = (self.maxCorner[0] - self.minCorner[0])/self.hres
    # <Comment flag> #419end

    def getPixelCenter(self, col, row, jitter = False, x_offset = 0, y_offset = 0):
        """ calculate the center coordinates for each pixel on the view plane depending
            on whether multi-jittering sampling is used
        Args:
            col: integer value for column of the view plane
            row: integer value for row of the view plane
            jitter: boolean value to determine if multi-jittering is used
            x_offset: integer value for sampling offset on horizontal direction
            y_offset: integer value for sampling offset on vertical direction
        Returns: 3D point of ray origin on the view play for each pixel
        """
        if jitter :
            x = self.size * (col - self.hres/2.0)
            y = self.size * (row - self.vres/2.0)
            z = self.minCorner[2]
            return numpy.array([x + x_offset * self.size, y + y_offset * self.size, z])
        else:
            x = self.size * (col - self.hres/2.0 + 0.5)
            y = self.size * (row - self.vres/2.0 + 0.5)
            z = self.minCorner[2]
            return numpy.array([x, y, z])

    def getPerspectiveDir(self, col, row, d, lookAt, eyePoint, up, jitter = False, x_offset = 0, y_offset = 0):
        """ calculate the ray direction each pixel on the view plane depending
            on whether multi-jittering sampling is used
        Args:
            col: integer value for column of the view plane
            row: integer value for row of the view plane
            d: integer value for distance from view point to view plane
            lookAt: 3D point for look at point
            eyePoint: 3D point for eye position of camera
            up: 3D vector for local up vector
            jitter: boolean value to determine if multi-jittering is used
            x_offset: integer value for sampling offset on horizontal direction
            y_offset: integer value for sampling offset on vertical direction
        Returns: 3D vector for ray direction
        """
        if jitter:
            x = self.size * (col - 0.5 * (self.hres)) + x_offset * self.size
            y = self.size * (row - 0.5 * (self.vres)) + y_offset * self.size
        else:
            x = self.size * (col - 0.5 * (self.hres - 1.0))
            y = self.size * (row - 0.5 * (self.vres - 1.0))

        # #419begin #type=3 #src=Ray Tracing from the Ground Up
        z = -d
        w = eyePoint - lookAt
        w = w / numpy.linalg.norm(w)
        u = numpy.cross(up, w)
        u = u / numpy.linalg.norm(u)
        v = numpy.cross(w, u)

        return x * u + y * v + z * w
        # #419end
