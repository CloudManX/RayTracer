import numpy as np

from RayTracer.GameObjects.bbox import BBox
from RayTracer.GameObjects.meshTriangle import MeshTriangle
from RayTracer.Intangibles.shadowRec import ShadowRec

class Mesh(object):

    def __init__(self, filename, material, kEpsilon = 0.00001):
        # Setup a mesh of triangles with a .obj file
        # Args: filename - the name of .obj file
        #       material - the material for the mesh
        self.vertices = []
        self.faces = []
        self.triangles = []
        self.normals = []
        self.material = material
        self.loadObj(filename)
        self.num_vertices = len(self.vertices)
        self.num_triangles = len(self.faces)
        self.calcNormals()
        self.normal = np.array([0.0, 0.0, 0.0])

        self.kEpsilon = kEpsilon

    def calcNormals(self):
        # Calculate the per vertex normals
        for x in range(0, self.num_vertices):
            self.normals.append(np.array([0.0, 0.0, 0.0]))
        for face in self.faces:
            v1 = self.vertices[face[0]-1]
            v2 = self.vertices[face[1]-1]
            v3 = self.vertices[face[2]-1]
            e1 = v2 - v1
            e2 = v3 - v2
            n = np.cross(e1, e2)
            self.normals[face[0]-1] += n
            self.normals[face[1]-1] += n
            self.normals[face[2]-1] += n
        for i in range(0, len(self.normals)):
            if np.linalg.norm(self.normals) != 0:
                self.normals[i] /= np.linalg.norm(self.normals[i])

        for j in range(0, len(self.triangles)):
            n1 = self.normals[self.triangles[j].index[0]]
            n2 = self.normals[self.triangles[j].index[1]]
            n3 = self.normals[self.triangles[j].index[2]]
            self.triangles[j].setNormal(n1, n2, n3)

    def hit(self, ray):
        """ check where the ray hits the objects in grid
            check each cell and the objects inside them
        Args:
            ray: a vector that shoots out from view plane
        Returns: Shadow Record
        """
        s_ = ShadowRec()
        if (not self.bbox.isHit(ray)):
            return s_
        for triangle in self.triangles:
            s = triangle.hit(ray)
            if (s.hits()):
                if(not s_.hits() or s_.getTValue() > s.getTValue()):
                    s_ = s
        return s_

    def getNormal(self, *args):
        return self.normal

    def loadObj(self, filename):
        # load the obj file with the filename
        x_min = 0.0
        x_max = 0.0
        y_min = 0.0
        y_max = 0.0
        z_min = 0.0
        z_max = 0.0
        counter = 0
        file = open(filename, 'r')
        while (1):
            line = file.readline()
            if not line:
                break

            element = line.split()
            if len(element) > 0:
                spec = element[0]
                if (spec == 'v'):

                    x = float(element[1])
                    y = float(element[2])
                    z = float(element[3])
                    if (counter == 0):
                        x_min = x
                        x_max = x
                        y_min = y
                        y_max = y
                        z_min = z
                        z_max = z
                    else:
                        if (x < x_min):
                            x_min = x
                        if (x > x_max):
                            x_max = x
                        if (y < y_min):
                            y_min = y
                        if (y > y_max):
                            y_max = y
                        if (z < z_min):
                            z_min = z
                        if (z > z_max):
                            z_max = z
                    counter += 1
                    self.vertices.append(np.array([x, y, z]))
                elif (spec == 'f'):
                    v1 = int(element[1].split('/')[0])
                    v2 = int(element[2].split('/')[0])
                    v3 = int(element[3].split('/')[0])
                    self.faces.append(np.array([v1, v2, v3]))


        for face in self.faces:
            index1 = face[0] - 1
            index2 = face[1] - 1
            index3 = face[2] - 1
            v1 = self.vertices[index1]
            v2 = self.vertices[index2]
            v3 = self.vertices[index3]
            self.triangles.append(MeshTriangle(v1, v2, v3, index1, index2, index3, self.material))
        lower = np.array([x_min, y_min, z_min])
        upper = np.array([x_max, y_max, z_max])
        self.bbox = BBox((lower,upper))