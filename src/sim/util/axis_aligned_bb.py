import math
import numpy as np


class AxisAlignedBB:
    def __init__(self, x1, y1, z1, x2, y2, z2):
        self.min_x = math.min(x1, x2)
        self.min_y = math.min(y1, y2)
        self.min_z = math.min(z1, z2)
        self.max_x = math.max(x1, x2)
        self.max_y = math.max(y1, y2)
        self.max_z = math.max(z1, z2)
