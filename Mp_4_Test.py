import numpy as np
import time
from Intangibles.ray import Ray
from Intangibles.shadowRec import ShadowRec
from Utils.World import World
from PIL import Image



world = World()
world.test_setup()

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
        if (row % 10 == 0):
            print(row / 10)
        for col in range(world.vp.hres):
            ray = Ray(np.array([0, 0, 0]), np.array([0, 0, -1])) # set default central ray
            ray.origin = world.vp.getPixelCenter(col, row)
            ray.setNumber(col + world.vp.hres * row)
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
                pix[col, (world.vp.vres - 1 - row)] = sr_.getMat().shade(sr_, world).value()
            else:
                pix[col, (world.vp.vres - 1 - row)] = (0, 0, 0)


if __name__ == "__main__":
    start = time.time()
    draw(True)
    image.save("Graph/mp2_result.png")
    image.show()
    end = time.time()
    print str(end - start) + " s of running time"