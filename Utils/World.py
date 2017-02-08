import numpy as np

from RayTracer.GameObjects.Primitives.rectangle import Rectangle
from RayTracer.GameObjects.grid import Grid
from RayTracer.GameObjects.instance import Instance
from RayTracer.GameObjects.planes import Plane
from RayTracer.GameObjects.sphere import Sphere
from RayTracer.Intangibles.light import AmbientLight
from RayTracer.Intangibles.light import AreaLight
from RayTracer.Intangibles.light import PointLight
from RayTracer.Intangibles.viewPlane import ViewPlane
from RayTracer.Materials.Reflective import Reflective
from RayTracer.Materials.transparent import Transparent
from RayTracer.Materials.emissive import Emissive
from RayTracer.Materials.material import Material
from RayTracer.Materials.textureMatt import TextureMatt
from RayTracer.Materials.glossyReflective import GlossyReflective
from RayTracer.Samplers.sampler import Sampler
from RayTracer.Utils.Color import Color
from RayTracer.Texture.texture import Texture
from RayTracer.Texture.checkerTexture import CheckerTexture

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
        self.vp = ViewPlane(200, 200)
        floor = Plane(np.array([0, -0.5, 0]), np.array([0, 1, 0]), Material(0.25, 0.6, 0.2, Color((200, 200, 200))))
        # self.lights.append(DirectionalLight())
        rect = Rectangle(np.array([0, 100, 0]), 50, 100, np.array([0, 0, 1]), Material(0.25, 0.6, 0.2, Color((255, 0, 0))))
        self.objects.append(floor)
        self.objects.append(rect)
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
        # mesh = Mesh('OBJ/gundam.obj', Material(0.25, 0.6, 0.4, Color((220, 220, 220))))
        # grid = Grid(mesh.triangles)
        # grid.setup()
        # self.objects.append(grid)

    def mp3_setup(self, samplingSize):
        # hard code default values

        self.up = [0, 1, 0]  # up direction of local frame
        # setup
        self.vp = ViewPlane(1024, 1024)

        emissive = Emissive(10.0, Color((255, 255, 255)))
        sampler = Sampler(samplingSize)
        obj = []
        rectangleLightSource = Rectangle(np.array([-1, 0, -3]), 1.4, 2, np.array([0, 0, 1]), emissive)
        rectangleLightSource.setSampler(sampler)

        area_light = AreaLight(rectangleLightSource, emissive, True)
        self.lights.append(area_light)

        sphere = Sphere(0.5, np.array([-1, -0.5, 0]), Reflective(0.25, 0.6, 0.6, 2.0, Color((200, 0, 200))))
        sphere2 = Instance(sphere, Material(0.25, 0.6, 0.0, Color((255, 255, 0))))
        sphere3 = Instance(sphere, Material(0.25, 0.6, 0.6, Color((0, 255, 255))))
        sphere2.translate(-1.5, 0, 1)
        sphere3.translate( 0.5, 1, -1)
        sphere3.scale(0.5, 2, 0.5)
        floor = Plane(np.array([0, -1, 0]), np.array([0, 1, 0]), Reflective(0.25, 0.6, 0.2, 1.0, Color((200, 200, 200))))
        obj.append(rectangleLightSource)

        obj.append(sphere)
        obj.append(sphere2)
        obj.append(sphere3)
        grid = Grid(obj)
        grid.setup()
        self.objects.append(floor)
        self.objects.append(grid)
        self.eyePoint = np.array([-2, 2, -2.9]) # eye point position of the camera
        # self.eyePoint = np.array([-5, 2, -1]) # eye point position of the camera
        self.lookAt = np.array([0, 1, 0]) # look at direction vector

    def test_setup(self):
        # hard code default values

        self.up = [0, 1, 0]  # up direction of local frame
        # setup
        self.vp = ViewPlane(1600, 1200)
        checkerT = CheckerTexture(1.0)
        floor = Plane(np.array([0, -0.5, 0]), np.array([0, 1, 0]), TextureMatt(0.25, 0.6, 0.15, checkerT))
        # self.lights.append(DirectionalLight())
        sphere1 = Sphere(0.5, np.array([0, 0, 0]), Transparent(0.25, 0.0, 0.15, 0.1, 0.9, Color((0, 255, 255))))
        sphere2 = Sphere(0.5, np.array([0, 0, -2]), Material(0.25, 0.6, 0.15, Color((0, 255, 255))))
        texture = Texture('Texture/pokeball.jpg')
        sphere3 = Sphere(0.5, np.array([-1.5, 0, -1.5]), TextureMatt(0.25, 0.6, 0.15, texture))
        exp = 100.0
        sampler = Sampler(400)
        sampler.generate_samples()
        sampler.setup_shuffled_indices()
        sampler.map_samples_to_hemisphere(exp)
        sphere4 = Sphere(0.5, np.array([1.5, 0, -1.5]),
                          GlossyReflective(0.25, 0.4, 0.15, 0.9, Color((255, 255, 0)), sampler, exp))
        self.objects.append(floor)
        self.objects.append(sphere1)
        self.objects.append(sphere2)
        self.objects.append(sphere3)
        self.objects.append(sphere4)

        self.eyePoint = np.array([-2, 2, -1]) # eye point position of the camera

        self.eyePoint = np.array([3, 1, 2]) # eye point position of the camera
        self.lookAt = np.array([0, 0, 0]) # look at direction vector
        self.lights.append(PointLight(np.array([-1, 3, 1]), ls=3.0, shadow_on=True))
        self.lights.append(PointLight(np.array([4, 3, 4]), ls=5.0, shadow_on=True))
        self.lights.append(PointLight(np.array([3, 3, -3]), ls=5.0, shadow_on=True))



