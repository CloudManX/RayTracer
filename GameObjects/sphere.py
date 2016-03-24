
import numpy
from RayTracer.Intangibles.shadowRec import ShadowRec
from RayTracer.GameObjects.bbox import BBox

class Sphere:

    def __init__(self, radius, center, material, kEpsilon = 0.00001):
        """Initialize the sphere object with user defined center and radius
             radius: int value for radius of sphere
             center: 3D point for center of sphere
             material: user defined RGB 3D vector value
             kEpsilon: tolerance integer value
        Returns: void
        """
        self.radius = radius
        self.center = center
        self.material = material
        self.kEpsilon = kEpsilon
        upper_bound = (center[0] + radius, center[1] + radius, center[2] + radius)
        lower_bound = (center[0] - radius, center[1] - radius, center[2] - radius)
        self.bbox = BBox((lower_bound, upper_bound))

    def hit(self, ray):
        """ check where the ray hits the Sphere
        Args:
            ray: a vector that shoots out from view plane
        Returns: the parametrization variable where plane and ray intersects
        """
        a = numpy.dot(ray.direction, ray.direction)
        b = 2 * numpy.dot((ray.origin - self.center), ray.direction)
        c = numpy.dot((ray.origin - self.center), (ray.origin - self.center)) - self.radius * self.radius
        d = b * b - 4 * a * c

        if d < 0:
            return ShadowRec()
        else:
            sr = ShadowRec()
            e = numpy.sqrt(d)
            denom = 2 * a
            t = (- b - e) / denom

            if (t > self.kEpsilon):
                sr.setHits()
                sr.setTValue(t)
                sr.setRay(ray)
                sr.setMat(self.material)
                sr.setGetNormal(self.getNormal)
                return sr

            t = (-1.0 * b + e) / denom
            if(t > self.kEpsilon):
                sr.setHits()
                sr.setTValue(t)
                sr.setRay(ray)
                sr.setMat(self.material)
                sr.setGetNormal(self.getNormal)
                return sr
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


    # #419begin #type=1 #src=https://github.com/shaffer1/UIllinois_Rendering/blob/master/Code/Sphere.py
    def getNormal(self,pt):
        """ Returns unit normal of sphere at the point pt """
        n = pt - self.center
        return n/numpy.linalg.norm(n)
    # #419end