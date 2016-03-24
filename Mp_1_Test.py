import numpy
from GameObjects.objects import Objects
from Intangibles.ray import Ray
from Intangibles.shadowRec import ShadowRec
from PIL import Image

from RayTracer.Intangibles.viewPlane import ViewPlane

# hard code default values
hres = 100  # screen horizontal resolution
vres = 100  # screen vertical resolution
eyePoint = numpy.array([0, 0, 2]) # eye point position of the camera
lookAt = numpy.array([0, 0, 0]) # look at direction vector
up = [0, 1, 0]  # up direction of local frame
samplingSize = 4 # sampling size for multi-jittering


# setup
ray = Ray(numpy.array([0, 0, 0]), numpy.array([0, 0, -1])) # set default central ray
viewPlane = ViewPlane(hres, vres)   # setup view plane with dimension
myObjects = Objects() # initialize objects wanted to be displayed on the screen

# <Comment flag> #419begin #type=<1> #src=<Prof. Eric Shaffer>
image = Image.new("RGB",((viewPlane.hres, viewPlane.vres)))
pix = image.load()  # Setup up image for pixel manipulation
# <Comment flag> #419end

# define a light direction
ldir = numpy.array([0,0,1]) #light direction
kd = 0.75  #reflectivity
illum = 1.0  #light luminosity

# <Comment flag> #419begin #type=1 #src = https://github.com/shaffer1/UIllinois_Rendering/blob/master/Code/RayTracer.py
def phongDiffuse(x, n, mat):
    """Implements a Phong-style diffuse shading function
    Args:
         x: is a point on a surface
         n: is the unit normal at that point
         mat: is an RGB tuple of the surface color
    Returns: A tuple representing an RGB color with values in [0,255]

    """
    factor = kd * illum * max(0, n.dot(ldir))
    color = numpy.rint(factor * mat).astype(int)
    return numpy.array([color[0], color[1], color[2]])
# <Comment flag> #419end


def draw(persp):
    """ Draw the scene orthographically or in perspective regarding to
    boolean input persp without multi-jittering
    Args:
        persp: boolean value determines whether perspective projection
               is used
    Return: void
    """
    miss_count = 0
    hit_count = 1
    for row in range(viewPlane.vres):
        # print(row)
        for col in range(viewPlane.hres):
            ray.origin = viewPlane.getPixelCenter(col, row)
            ray.setNumber(col + viewPlane.hres * row)
            if persp:
                ray.origin = eyePoint
                rayDir = viewPlane.getPerspectiveDir(col, row, 1, lookAt, eyePoint, up)
                ray.direction = rayDir / numpy.linalg.norm(rayDir)
            if (1):
                # shadowRec ordering
                s_ = ShadowRec()
                for obj in myObjects.list:
                    s = obj.hit(ray)
                    # print(obj.test)
                    if(not s_.hits()):
                        if(s.hits()):
                            s_ = s
                    else:
                        if(s.hits and s_.getTValue() > s.getTValue()):
                            s_ = s

                if (s_.hits()):
                    hit_count += 1
                    xp = ray.getPoint(s_.getTValue())
                    color = phongDiffuse(xp, s_.getNormal(xp), s_.getMat())
                    pix[col, (viewPlane.vres - 1 - row)] = (color[0], color[1], color[2])
                    print(ray.getNumber())
                else:
                    miss_count += 1

    print(hit_count, miss_count)

# def drawJittered(persp):
#     """ Draw the scene orthographically or in perspective regarding to
#     boolean input persp with multi-jittering
#     Args:
#         persp: boolean value determines whether perspective projection
#                is used
#     Return: void
#     """
#     for row in range(viewPlane.vres):
#         print(row)
#         for col in range(viewPlane.hres):
#             color = numpy.array([0, 0, 0])
#             table = initTable(samplingSize)
#             sampler = JitterSampler(samplingSize, table)
#             for j in range(0, samplingSize):
#                 for i in range(0, samplingSize):
#                     offset = sampler.getOffset(i, j)
#                     ray.origin = viewPlane.getPixelCenter(col, row, True, offset[0], offset[1])
#                     if persp:
#                         ray.origin = eyePoint
#                         rayDir = viewPlane.getPerspectiveDir(col, row, 1, lookAt, eyePoint, up,
#                                                              True, offset[0], offset[1])
#                         ray.direction = rayDir / numpy.linalg.norm(rayDir)
#
#                     # shadowRec ordering
#                     shadowRec_ = None
#                     for obj in myObjects.list:
#                         shadowRec = obj.hit(ray)
#                         if(shadowRec_ == None):
#                             if(shadowRec != None):
#                                 shadowRec_ = shadowRec
#                         else:
#                             if(shadowRec != None and shadowRec_[0] > shadowRec[0]):
#                                 shadowRec_ = shadowRec
#
#                     if (shadowRec_ != None):
#                         xp = ray.getPoint(shadowRec_[0])
#                         color += phongDiffuse(xp, shadowRec_[1](xp), shadowRec_[2])
#             denom = samplingSize * samplingSize
#             pix[col, (viewPlane.vres - 1 - row)] = (color[0]/denom, color[1]/denom, color[2]/denom)


def initTable(samplingSize):
    """ Draw the scene orthographically or in perspective regarding to
    boolean input persp without multi-jittering
    Args:
        samplingSize: integer value for rays per pixel
    :Return: a 1-D empty table of size samplinSize * samplingSize
    """
    table = []
    for j in range(0, samplingSize):
        for i in range(0, samplingSize):
            table.append((0, 0))
    return table

if __name__ == "__main__":

    """One orthographic rendering of a scene with spheres and triangles"""
    # draw(False)
    # image.save('orthographic_rendering.png')
    # image.show()

    """One perspective rendering of the same scene"""
    draw(True)
    image.save("perspective_rendering.png")
    image.show()

    """An additional perspective rendering of the same scene from a different viewpoint"""
    # eyePoint = numpy.array([-1.5, 0, -2.5]) # change eye point position of the camera
    # lookAt = numpy.array([0, 0, -2.5]) # change look at direction vector
    # draw(True)
    # image.save('different_view.png')
    # image.show()

    "Two images illustrating the effects of using jittering"
    # eyePoint = numpy.array([0, 0, 0.5])
    # lookAt = numpy.array([0, -0.5, -1])
    # draw(True)
    # image.save("jittering_one_ray_per_pixel.png")
    # image.show()
    # drawJittered(True)
    # image.save("multi_jittering.png")
    # image.show()