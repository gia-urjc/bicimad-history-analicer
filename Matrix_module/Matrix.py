from Commons.constants import *

class Matrix:

    def __init__(self):
        self.matrices = []
        for i in range(0, NUM_STATIONS+1):
            self.matrices.append([])
            for h in range(0, HOURS):
                self.matrices[i].append([])
                self.matrices[i][h] = 0
