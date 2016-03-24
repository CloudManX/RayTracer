import numpy
import sys

from RayTracer.GameObjects.bbox import BBox
from RayTracer.GameObjects.planes import Plane
from RayTracer.Intangibles.shadowRec import ShadowRec

class MeshTriangle(Plane):

    def __init__(self, p0, p1, p2, i1, i2, i3, material, kEpsilon = 0.00001):
        """Initialize a triangle with 3 points
             p0: 3D point for the vertex of a triangle
             p1: 3D point for the vertex of a triangle
             p2: 3D point for the vertex of a triangle
             i1, i2, i3: indices for vertices of the triangle
             material: user defined RGB 3D vector value
             kEpsilon: tolerance integer value
        Returns: void
        """
        self.mailbox = -1
        self.p0 = p0
        self.p1 = p1
        self.p2 = p2
        self.beta = 0
        self.gamma = 0
        self.index = (i1, i2, i3)
        self.material = material
        self.kEpsilon = kEpsilon
        normal = numpy.cross((p1 - p0), (p2 - p0))
        if numpy.linalg.norm(normal) == 0:
            self.normal = normal
        else:
            self.normal = normal / numpy.linalg.norm(normal)
        self.bbox = BBox(self.getBBox())
        super(MeshTriangle, self).__init__(p0, normal, material, kEpsilon)

    # 419begin #type=3 #src= Ray Tracing from Ground Up by Kevin Suffern
    def hit(self, ray):
        """ check where the ray hits the plane
        Args:
            ray: a vector that shoots out from view plane
        Returns: the parametrization variable where plane and ray intersects
        """
        sr = ShadowRec()
        a = self.p0[0] - self.p1[0]
        b = self.p0[0] - self.p2[0]
        c = ray.direction[0]
        d = self.p0[0] - ray.origin[0]
        e = self.p0[1] - self.p1[1]
        f = self.p0[1] - self.p2[1]
        g = ray.direction[1]
        h = self.p0[1] - ray.origin[1]
        i = self.p0[2] - self.p1[2]
        j = self.p0[2] - self.p2[2]
        k = ray.direction[2]
        l = self.p0[2] - ray.origin[2]
        m = f * k - g * j
        n = h * k - g * l
        p = f * l - h * j
        q = g * i - e * k
        s = e * j - f * i

        if (a * m + b * q + c * s) == 0:
            inv_denom = sys.maxint
        else:
            inv_denom = 1.0 / (a * m + b * q + c * s)
        e1 = d * m - b * n - c * p
        self.beta = e1 * inv_denom
        if (self.beta < 0.0): return sr
        r = e * l - h * i
        e2 = a *n + d * q + c * r
        self.gamma = e2 * inv_denom
        if (self.gamma < 0.0): return sr
        if (self.beta + self.gamma > 1.0): return sr

        e3 = a * p - b * r + d * s
        t = e3 * inv_denom

        if (t < self.kEpsilon): return sr

        sr.setHits()
        sr.setTValue(t)
        sr.setRay(ray)
        sr.setGetNormal(self.getNormal)
        sr.setMat(self.material)
        return sr
    # 419end

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
        """Return the BBox of the triangle
        Input: Void
        Returns: BBox
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

    def getNormal(self, *args):
        """Return the normal of the triangle
        Input: arguments depending on object
        Returns: the normal of the geometric
        """
        return self.interpolateNormal()

    def setNormal(self, n1, n2, n3):
        """store the three normals of each vertex
        Input:
            n1, n2, n3: 3 normals
        Returns: Void
        """
        self.N = (n1, n2, n3)

    def interpolateNormal(self):
        """calculate the interpolated normal
        Input:
            Void
        Returns: Interpolated Normal
        """
        a = 1 - self.beta - self.gamma
        b = self.beta
        c = self.gamma
        n = a * self.N[0] + b * self.N[1] + c * self.N[2]
        if numpy.linalg.norm(n) != 0:
            n /= numpy.linalg.norm(n)
        return n