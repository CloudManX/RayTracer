import numpy as np
import sys
class sample(object):
    def __init__(self, number):
        self.number = number


mySample = sample(2)

r = 215
r = r if r <= 255 else 255
print r