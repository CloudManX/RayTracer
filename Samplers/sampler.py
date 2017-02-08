import random
from random import randint
import math
import numpy as np
import sys


class Sampler:

    def __init__(self, num_samples):
        # Set up a sampler with coustomized sampling size
        # Args: num_samples - sampling size
        self.count = 0
        self.num_samples = num_samples
        self.samples = []
        self.jump = 0 # random index jump
        self.hemiSamples = []
        self.shuffledIndices = []
        self.num_sets = 83
        self.generate_samples()

    def generate_samples(self):
        # Generate samples on a rectangular plane
        n = int(math.sqrt(self.num_samples))
        for i in range(0, self.num_sets):
            for j in range(0, n):
                for k in range(0, n):
                    sample_point = np.array([(k + random.random())/n, (j + random.random())/n])

                    self.samples.append(sample_point)

    def setup_shuffled_indices(self):
        # Shuffle indices
        indices = []
        for j in range(0, self.num_samples):
            indices.append(j)

        for p in range(0, self.num_sets):
            random.shuffle(indices)
            for i in range(0, self.num_samples):
                self.shuffledIndices.append(indices[i])

    def sample_unit_square(self):
        # if self.count % self.num_samples == 0:
            # self.jump =(random.randint() % self.num_sets) * self.num_samples
        # Sampling with jump
        self.count += 1
        sample_point = self.samples[self.count % (self.num_samples * self.num_sets)]
        return sample_point

    def map_samples_to_hemisphere(self, exp):
        for sample in self.samples:
            cos_phi = math.cos(2.0 * math.pi * sample[0])
            sin_phi = math.sin(2.0 * math.pi * sample[0])
            cos_theta = math.pow(1.0 - sample[1], 1.0 / (exp + 1.0))
            sin_theta = math.sqrt(1.0 - cos_theta * cos_theta)
            pu = sin_theta * cos_phi
            pv = sin_theta * sin_phi
            pw = cos_theta
            self.hemiSamples.append(np.array([pu, pv, pw]))

    def sample_hemisphere(self):
        if self.count % self.num_samples == 0:
            self.jump = (randint(0, sys.maxint) % self.num_sets) * self.num_samples
        self.count += 1
        idx = self.jump + self.count % self.num_samples
        sample_point = self.hemiSamples[self.jump + self.shuffledIndices[idx]]
        return sample_point

    def clear(self):
        # reset the count
        self.count = 0
