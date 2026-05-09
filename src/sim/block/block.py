import numpy as np

class Block:
    def __init__(self):
        # TODO: Implement
        self.get_default_state = None
        self.slipperiness = np.float32(0.0)

    def get_default_state(self):
        return self.default_block_state