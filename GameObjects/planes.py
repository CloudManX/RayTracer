
import numpy
from RayTracer.Intangibles.shadowRec import ShadowRec


class Plane(object):

    def __init__(self, point, normal, material, kEpsilon = 0.00001):
        """Initialize the plane object with a point and a vector as normal and its material
        Args:
             point: customized 3D point on the plane
             normal: vector perpendicular to plane
             material: user defined RGB vector value
             kEpsilon: tolerance integer value
        Returns: void
        """
        self.point = point
        if numpy.linalg.norm(normal) == 0:
            self.normal = normal
        else:
            self.normal = normal / numpy.linalg.norm(normal)
        self.material = material
        self.kEpsilon = kEpsilon

    def hit(self, ray):
        """ check where the ray hits the plane
        Args:
            ray: a vector that shoots out from view plane
        Returns: Shadow Record
        """
        shadowRec = ShadowRec()
        denom = numpy.dot(ray.direction, self.normal)
        if denom == 0:
            return ShadowRec
        t = numpy.dot((self.point - ray.origin), self.normal)/ denom

        if t > self.kEpsilon:
            shadowRec.setHits()
            shadowRec.setTValue(t)
            shadowRec.setMat(self.material)
            shadowRec.setRay(ray)
            shadowRec.setGetNormal(self.getNormal)
            shadowRec.setHitPoint()
        return shadowRec

    def shadow_hit(self, ray):
        """ check if the shadow ray hits the object
        Args:
            ray: a vector that shoots out from view plane
        Returns: tuple of (bool and t)
        """
        sr = self.hit(ray)
        if sr.hits():
            return (True, sr.getTValue())
        else:
            return (False, 0)

    def getNormal(self, *args):
        """Return the normal of the triangle
        Input: arguments depending on object
        Returns: the normal of the geometric
        """
        return self.normal