
import numpy

class JitterSampler:

    def __init__(self, numSamples, table):
        """Initialize JitterSampler with sampling size and empty table. Call jittering()
            to put pixel coordinates(offsets) in the table
        Args:
             numSamples: customized sampling integer size
             table: array for empty table for holding offets
        Returns: void
        """
        self.samplingSize = numSamples
        self.offsetTable = table
        self.jittering()

    def jittering(self):
        """ Using Muti-jittering algorithm to computer per pixel coordinates for each
            ray and save them in the table
        Args:
            None
        Returns: void
        """
        for j in range(0, self.samplingSize):
            for i in range(0, self.samplingSize):
                x_offset = (i + (j + numpy.random.random()) / self.samplingSize) / self.samplingSize
                y_offset = 1 - (j + (i + numpy.random.random()) / self.samplingSize) / self.samplingSize
                offset = (x_offset, y_offset)
                self.offsetTable[j * self.samplingSize + i] = offset
                # canonical random sampling

        for j in range(0, self.samplingSize):
            for i in range(0, self.samplingSize):
                k = int(j + numpy.random.random() * (self.samplingSize - j))
                first = j * self.samplingSize + i
                second = k * self.samplingSize + i

                temp = self.offsetTable[first]
                self.offsetTable[first] = (self.offsetTable[second][0], self.offsetTable[first][1])
                self.offsetTable[second] = (temp[0], self.offsetTable[second][1])
                # second term does not change

        for i in range(0, self.samplingSize):
            for j in range(0, self.samplingSize):
                k = int(i + numpy.random.random() * (self.samplingSize - i))
                first = j * self.samplingSize + i
                second = j * self.samplingSize + k

                temp = self.offsetTable[first]
                self.offsetTable[first] = (self.offsetTable[first][0], self.offsetTable[second][1])
                self.offsetTable[second] = (self.offsetTable[second][0], temp[1])
                # first term does not change

    def getOffset(self, i, j):
        """Access the per pixel coordinates to serve as offsets for
        Args:
             i: horizontal int counter for table
             j: vertical int counter for table
        Returns: a tuple holds x and y offsets
        """
        return self.offsetTable[j * self.samplingSize + 1]
