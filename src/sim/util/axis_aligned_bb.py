class AxisAlignedBB:
    def __init__(self, x1, y1, z1, x2, y2, z2):
        self.min_x = min(x1, x2)
        self.min_y = min(y1, y2)
        self.min_z = min(z1, z2)
        self.max_x = max(x1, x2)
        self.max_y = max(y1, y2)
        self.max_z = max(z1, z2)

    def offset(self, x, y, z):
        return AxisAlignedBB(
            self.min_x + x,
            self.min_y + y,
            self.min_z + z,
            self.max_x + x,
            self.max_y + y,
            self.max_z + z,
        )
