import numpy as np
import time
from Intangibles.ray import Ray
from Intangibles.shadowRec import ShadowRec
from Utils.World import World
from Samplers.jitterSampler import JitterSampler
from PIL import Image


world = World()
sampleSize = 1
sampleSize_square = sampleSize * sampleSize
world.mp3_setup(16)

# <Comment flag> #419begin #type=<1> #src=<Prof. Eric Shaffer>
image = Image.new("RGB",((world.vp.hres, world.vp.vres)))
pix = image.load()  # Setup up image for pixel manipulation
# <Comment flag> #419end


def draw(persp):
    """ Draw the scene orthographically or in perspective regarding to
    boolean input persp without multi-jittering
    Args:
        persp: boolean value determines whether perspective projection
               is used
    Return: void
    """
    for row in range(world.vp.vres):
        if row % 10 == 0:
            print(row / 10)
        for col in range(world.vp.hres):
            color = (0, 0, 0)
            # table = initTable(sampleSize)
            # sampler = JitterSampler(sampleSize, table)
            for j in range(0, sampleSize):
                for i in range(0, sampleSize):
                    # offset = sampler.getOffset(i, j)
                    ray = Ray(np.array([0, 0, 0]), np.array([0, 0, -1])) # set default central ray
                    ray.origin = world.vp.getPixelCenter(col, row)
                    if persp:
                        ray.origin = world.eyePoint
                        rayDir = world.vp.getPerspectiveDir(col, row, 1, world.lookAt, world.eyePoint, world.up)
                        ray.setDirection(rayDir)
                    # shadowRec ordering
                    sr_ = ShadowRec()
                    for obj in world.objects:
                        sr = obj.hit(ray)
                        if sr.hits() and (not sr_.hits() or sr_.getTValue() > sr.getTValue()):
                            sr_ = sr

                    if sr_.hits():
                        # print sr_.getMat().shade(sr_, world).value()
                        temp = (0, 0, 0)
                        for i in range(0, 16):
                            c = sr_.getMat().area_light_shade(sr_, world).value()
                            temp = (temp[0] + c[0], temp[1] + c[1], temp[2] + c[2])
                        temp = (temp[0] / 16, temp[1] / 16, temp[2] / 16)
                    else:
                        temp = (0, 0, 0)
                    color = (color[0] + temp[0], color[1] + temp[1], color[2] + temp[2])

            pix[col, (world.vp.vres - 1 - row)] = (color[0] / sampleSize_square, color[1] / sampleSize_square, color[2] / sampleSize_square)

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

    start = time.time()
    draw(True)
    image.save("Graph/mp3_result.png")
    image.show()
    end = time.time()
    print str(end - start) + " s of running time"