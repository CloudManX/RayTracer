import numpy

from RayTracer.GameObjects.bbox import BBox
from RayTracer.GameObjects.planes import Plane
from RayTracer.Intangibles.shadowRec import ShadowRec

class Triangle(Plane):

    def __init__(self, p0, p1, p2, material, kEpsilon = 0.00001):
        """Initialize a triangle with 3 points
             p0: 3D point for the vertex of a triangle
             p1: 3D point for the vertex of a triangle
             p2: 3D point for the vertex of a triangle
             material: user defined RGB 3D vector value
             kEpsilon: tolerance integer value
        Returns: void
        """
        self.mailbox = -1
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.bbox = BBox(self.getBBox())
        normal = numpy.cross((p1 - p0), (p2 - p0))
        super(Triangle, self).__init__(p0, normal, material, kEpsilon)

    def hit(self, ray):
        """ check where the ray hits the triangle
        Args:
            ray: a vector that shoots out from view plane
        Returns: Shadow Record
        """

        # check if the ray intersects the plane that the triangle is on
        s = super(Triangle, self).hit(ray)
        if (not s.hits()):
            return s
        intersect = ray.getPoint(s.getTValue())
        # check if the intersection is inside the triangle
        temp = numpy.cross((self.p1 - self.p0), (intersect - self.p0))
        first_condition = True if numpy.dot(temp, self.normal) >= 0 else False
        temp = numpy.cross((self.p2 - self.p1), (intersect - self.p1))
        second_condition = True if numpy.dot(temp, self.normal) >= 0 else False
        temp = numpy.cross((self.p0 - self.p2), (intersect - self.p2))
        third_condition = True if numpy.dot(temp, self.normal) >= 0 else False
        if (first_condition and second_condition and third_condition and s.getTValue() > self.kEpsilon):
            return s
        else:
            return ShadowRec()

    def shadow_hit(self, ray):
        """ check if the shadow ray hits the object
        Args:
            ray: a vector that shoots out from view plane
        Returns: tuple of (bool and t)
        """
        sr = self.hit(ray)
        if (sr.hits()):
            return (True, sr.getTValue())
        else:
            return (False, 0)


    def getBBox(self):
        """ check if the shadow ray hits the object
        Args:
            Void
        Returns: tuple of lower and upper bound of the BBox
        """
        x_min = min(self.p0[0], self.p1[0], self.p2[0])
        x_max = max(self.p0[0], self.p1[0], self.p2[0])
        y_min = min(self.p0[1], self.p1[1], self.p2[1])
        y_max = max(self.p0[1], self.p1[1], self.p2[1])
        z_min = min(self.p0[2], self.p1[2], self.p2[2])
        z_max = max(self.p0[2], self.p1[2], self.p2[2])
        lower = numpy.array([x_min, y_min, z_min])
        upper = numpy.array([x_max, y_max, z_max])
        return (lower, upper)

