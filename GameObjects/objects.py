from sphere import Sphere
from planes import Plane
from triangle import Triangle
from mesh import Mesh
from grid import Grid
import numpy
import time

class Objects:

    def __init__(self, list = []):
        """ Create a object that holds a list for objects to be displayed
        Args:
            list: empty object list
        :Return: void
        """
        self.list = list


    def addObject(self, obj):
        """ Add a new object to list
        Args:
            obj: custom defined object
        :Return: void
        """
        self.list.append(obj)


