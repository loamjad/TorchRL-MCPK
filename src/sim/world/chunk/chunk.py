from src.sim.init.blocks import Blocks

class Chunk:
    def __init__(self):
        # TODO: Implement
        self.storage_arrays = None

    def get_block_state(self, pos):
        try:
            if pos.get_y() >= 0 and pos.get_y() >> 4 < len(self.storage_arrays):
                extendedblockstorage = self.storage_arrays[pos.get_y() >> 4]

                if extendedblockstorage != None:
                    j = pos.get_x() & 15
                    k = pos.get_y() & 15
                    i = pos.get_z() & 15
                    return extendedblockstorage.get(j, k, i)
                
            return Blocks.air.get_default_state()
        except:
            pass