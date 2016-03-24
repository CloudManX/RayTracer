import numpy as np
import random
from RayTracer.Intangibles.viewPlane import ViewPlane
from RayTracer.GameObjects.mesh import Mesh
from RayTracer.GameObjects.grid import Grid
from RayTracer.GameObjects.planes import Plane
from RayTracer.GameObjects.sphere import Sphere
from RayTracer.Intangibles.light import AmbientLight
from RayTracer.Intangibles.light import DirectionalLight
from RayTracer.Intangibles.light import PointLight
from RayTracer.Intangibles.material import Material
from RayTracer.Utils.Color import Color


class World:

    def __init__(self, viewPlane = None, background_color = np.array([]), lights = [], objects = []):
        # Set up the world of current view
        # Args: viewPlane - vierplane that shoots the ray
        #       background_color - color of the default image
        #       lights - list of customized light sources
        #       objects - list of objects
        self.vp = viewPlane
        self.bColor = background_color
        self.lights = lights
        self.objects = objects
        self.ambient = AmbientLight()

    def mp2_setup(self):
        # hard code default values

        self.up = [0, 1, 0]  # up direction of local frame
        # setup
        self.vp = ViewPlane(1000, 1000)
        floor = Plane(np.array([0, -0.5, 0]), np.array([0, 1, 0]),Material(0.25, 0.6, 0.2, Color((200, 200, 200))))

        #self.lights.append(DirectionalLight())
        self.objects.append(floor)

        # # balls
        # self.eyePoint = np.array([-2, 0, 2]) # eye point position of the camera
        # self.lookAt = np.array([0, 0, 0.5]) # look at direction vector
        # self.lights.append(PointLight(np.array([-1, 1, 2]), shadow_on = True))
        # obj_list = []
        # radius = 0.3
        # for j in range(0, 10):
        #     o = np.array([-2, 0, 1])
        #     for i in range(0, 200):
        #         r = random.random() * 255
        #         g = random.random() * 255
        #         b = random.random() * 255
        #         old_radius = radius
        #         radius = random.random() * 0.01
        #         distance = random.random() * 0.001
        #         y_distance = random.random() - 0.5
        #         if (y_distance + o[1] < -0.5 or y_distance > 2):
        #             y_distance = -y_distance
        #         if (i % 2  == 0):
        #             o = np.array([old_radius + radius + distance + o[0], y_distance + o[1], o[2]])
        #         else:
        #             o = np.array([o[0], o[1] + y_distance, old_radius + radius + distance + o[2]])
        #         sphere = Sphere(radius, o, Material(0.25, 0.6, 0.4, Color((r, g, b))))
        #         obj_list.append(sphere)
        #
        #
        # sphereGrid = Grid(obj_list)
        # sphereGrid.setup()
        # self.objects.append(sphereGrid)


        # draw complex mesh
        self.eyePoint = np.array([0, 180, 200]) # eye point position of the camera
        self.lookAt = np.array([0, 90, 0]) # look at direction vector
        self.lights.append(PointLight(np.array([-2, 200, 180]), shadow_on = True))
        mesh = Mesh('OBJ/gundam.obj', Material(0.25, 0.6, 0.4, Color((220, 220, 220))))
        grid = Grid(mesh.triangles)
        grid.setup()
        self.objects.append(grid)

