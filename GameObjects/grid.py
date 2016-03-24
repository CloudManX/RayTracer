import sys

import numpy as np

from RayTracer.GameObjects.bbox import BBox
from RayTracer.Intangibles.shadowRec import ShadowRec

class Grid(object):

    def __init__(self, objects):
        """ initialize the grid for objects
        Args:
            void
        Returns: tuple of (bool and t)
        """
        self.cells = []
        self.counts = []
        self.bbox = BBox()
        self.nx = 0
        self.ny = 0
        self.nz = 0
        self.objects = objects
        self.test = []

    def minCoordinates(self):
        # return the minimum coord of grid
        counter = 0
        for object in self.objects:
            x = object.bbox.x0
            y = object.bbox.y0
            z = object.bbox.z0
            if (counter == 0 ):
                x_min = x
                y_min = y
                z_min = z
            else:
                if (x < x_min):
                    x_min = x
                if (y < y_min):
                    y_min = y
                if (z < z_min):
                    z_min = z
            counter += 1
        self.p0 = np.array([x_min, y_min, z_min])
        return self.p0


    def maxCoordinates(self):
        # return the maximum grid of the grid
        counter = 0
        for object in self.objects:
            x = object.bbox.x1
            y = object.bbox.y1
            z = object.bbox.z1
            if (counter == 0):
                x_max = x
                y_max = y
                z_max = z
            else:
                if (x > x_max):
                    x_max = x
                if (y > y_max):
                    y_max = y
                if (z > z_max):
                    z_max = z
            counter += 1
        self.p1 = np.array([x_max, y_max, z_max])
        return self.p1

    def setup(self):
        # Setup the grid by pushing index to each cell
        obj_index = 0
        bound = (self.minCoordinates(), self.maxCoordinates())
        print bound
        self.bbox.setBox(bound)
        num_objects = len(self.objects)
        print(num_objects)
        wx = self.p1[0] - self.p0[0]
        wy = self.p1[1] - self.p0[1]
        wz = self.p1[2] - self.p0[2]
        multiplier = 2.0
        s = pow(wx * wy * wz / num_objects, 0.33333333)

        self.nx = int(multiplier * wx / s + 1)
        self.ny = int(multiplier * wy / s + 1)
        self.nz = int(multiplier * wz / s + 1)
        num_cells = self.nx * self.ny * self.nz
        print num_cells

        for object in self.objects:
            obj_bbox = object.bbox
            lower = obj_bbox.getLowerBound()
            upper = obj_bbox.getUpperBound()

            for i in range(0, num_cells):
                self.cells.append([])

            ixmin = self.clamp((lower[0] - self.p0[0]) * self.nx / (self.p1[0] - self.p0[0]), 0, self.nx - 1)
            iymin = self.clamp((lower[1] - self.p0[1]) * self.ny / (self.p1[1] - self.p0[1]), 0, self.ny - 1)
            izmin = self.clamp((lower[2] - self.p0[2]) * self.nz / (self.p1[2] - self.p0[2]), 0, self.nz - 1)
            ixmax = self.clamp((upper[0] - self.p0[0]) * self.nx / (self.p1[0] - self.p0[0]), 0, self.nx - 1)
            iymax = self.clamp((upper[1] - self.p0[1]) * self.ny / (self.p1[1] - self.p0[1]), 0, self.ny - 1)
            izmax = self.clamp((upper[2] - self.p0[2]) * self.nz / (self.p1[2] - self.p0[2]), 0, self.nz - 1)

            for iz in range(izmin, izmax + 1):
                for iy in range (iymin, iymax + 1):
                    for ix in range (ixmin, ixmax + 1):
                        index = ix + self.nx * iy + self.nx * self.ny * iz
                        self.cells[index].append(obj_index)
            obj_index += 1
            if (obj_index % 1000 == 0):
                print(obj_index)

    def hit(self, ray):
        """ check where the ray hits the objects in grid
            check each cell and the objects inside them
        Args:
            ray: a vector that shoots out from view plane
        Returns: Shadow Record
        """
        # the ray does not hit the bounding box
        if (not self.bbox.isHit(ray)):
            return ShadowRec()
        o = ray.origin
        # the ray origin is inside the bounding box of the grid
        if self.bbox.isInside(o):
            ix = self.clamp((o[0] - self.bbox.x0) * self.nx / (self.bbox.x1 - self.bbox.x0), 0, self.nx - 1)
            iy = self.clamp((o[1] - self.bbox.y0) * self.ny / (self.bbox.y1 - self.bbox.y0), 0, self.ny - 1)
            iz = self.clamp((o[2] - self.bbox.z0) * self.nz / (self.bbox.z1 - self.bbox.z0), 0, self.nz - 1)
        # the ray hits the grid
        else:
            p = ray.origin + self.bbox.t0 * ray.direction
            l = ray.origin + self.bbox.t1 * ray.direction
            ix = self.clamp((p[0] - self.bbox.x0) * self.nx / (self.bbox.x1 - self.bbox.x0), 0, self.nx - 1)
            iy = self.clamp((p[1] - self.bbox.y0) * self.ny / (self.bbox.y1 - self.bbox.y0), 0, self.ny - 1)
            iz = self.clamp((p[2] - self.bbox.z0) * self.nz / (self.bbox.z1 - self.bbox.z0), 0, self.nz - 1)
            # print('index: ')
            # print(ix, iy, iz)

        dtx = (self.bbox.tx_max - self.bbox.tx_min) / self.nx
        dty = (self.bbox.ty_max - self.bbox.ty_min) / self.ny
        dtz = (self.bbox.tz_max - self.bbox.tz_min) / self.nz

        # Set up the initial conditions for the hit in the first box
        if (ray.direction[0] > 0):
            tx_next = self.bbox.tx_min + (ix + 1) * dtx
            ix_step = +1
            ix_stop = self.nx
        elif(ray.direction[0] < 0):
            tx_next = self.bbox.tx_min + (self.nx - ix) * dtx
            ix_step = -1
            ix_stop = -1
        else:
            tx_next = sys.maxint
            ix_step = -1
            ix_stop = -1

        if (ray.direction[1] > 0):
            ty_next = self.bbox.ty_min + (iy + 1) * dty
            iy_step = +1
            iy_stop = self.ny
        elif (ray.direction[1] < 0):
            ty_next = self.bbox.ty_min + (self.ny - iy) * dty
            iy_step = -1
            iy_stop = -1
        else:
            ty_next = sys.maxint
            iy_step = -1
            iy_stop = -1
        if (ray.direction[2] > 0):
            tz_next = self.bbox.tz_min + (iz + 1) * dtz
            iz_step = +1
            iz_stop = self.nz
        elif (ray.direction[2] < 0):
            tz_next = self.bbox.tz_min + (self.nz - iz) * dtz
            iz_step = -1
            iz_stop = -1
        else:
            tz_next = sys.maxint
            iz_step = -1
            iz_stop = -1

        # print("nx = " + str(self.nx) + " ny = " + str(self.ny) + " nz = " + str(self.nz))
        # print("dtx = " + str(dtx) + " dty = " + str(dty) + " dtz = " + str(dtz))
        # print("tx_min = " + str(self.bbox.tx_min) + " ty_min = " + str(self.bbox.ty_min) + " tz_min = " + str(self.bbox.tz_min))
        # print("tx_max = " + str(self.bbox.tx_max) + " ty_max = " + str(self.bbox.ty_max) + " tz_max = " + str(self.bbox.tz_max))
        # print("tx_next = " + str(tx_next) + " ty_next = " + str(ty_next) + " tz_next = " + str(tz_next))
        # print(ray.direction, ray.origin)
        # print(p, l)
        while (1):
            s_ = ShadowRec()
            index = ix + self.nx * iy + self.nx * self.ny * iz
            self.test.append((ix, iy, iz))
            grid_objects = self.cells[index]
            # gird move in x direction
            if (tx_next < ty_next and tx_next < tz_next):
                if (len(grid_objects) > 0):
                    for index in grid_objects:
                        s = self.objects[index].hit(ray)
                        if(s.hits()):
                            if(not s_.hits() or s_.getTValue() > s.getTValue()):
                                s_ = s
                    if (s_.hits() and s_.getTValue() < tx_next):
                        return s_

                tx_next += dtx
                ix += ix_step
                # The ray does not hit anything
                if (ix == ix_stop):
                    return ShadowRec()

            else:
                # grid move in y direction
                if (ty_next < tz_next):
                    if (len(grid_objects) > 0):
                        for index in grid_objects:
                            s = self.objects[index].hit(ray)
                            if(s.hits()):
                                if(not s_.hits() or s_.getTValue() > s.getTValue()):
                                    s_ = s
                    if (s_.hits() and s_.getTValue() < ty_next):
                        return s_

                    ty_next += dty
                    iy += iy_step
                    if (iy == iy_stop):
                        return ShadowRec()
                # grid move in z direction
                else:
                    if (len(grid_objects) > 0):
                        for index in grid_objects:
                            s = self.objects[index].hit(ray)
                            if(s.hits()):
                                if(not s_.hits() or s_.getTValue() > s.getTValue()):
                                    s_ = s
                    if (s_.hits() and s_.getTValue() < tz_next):
                        return s_

                    tz_next += dtz
                    iz += iz_step
                    if (iz == iz_stop):
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

    def clamp(self, x, min, max):
        # clamp value x regarding to value of min and max
        # Args: max, min
        # Return: The clamped value
        result = int(min if x < min else (max if x > max else x))
        return result