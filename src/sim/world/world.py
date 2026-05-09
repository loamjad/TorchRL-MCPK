from src.sim.init.blocks import Blocks

class World:
    @classmethod
    def is_valid(cls, pos):
        pass

    @classmethod
    def get_block_state(cls, pos):
        if not World.is_valid(pos):
            return Blocks.air
        else:
            chunk = Blocks.get_chunk_from_block_coords(pos)
            return chunk.get_block_state(pos)
        
    @classmethod
    def get_chunk_from_block_coords(cls, pos):
        return Blocks.get_chunk_from_chunk_coords(pos.get_x() >> 4, pos.get_z() >> 4)
    
    @classmethod
    def get_chunk_from_chunk_coords(cls, chunk_x, chunk_z):
        return Blocks.chunk_provider.provideChunk(chunk_x, chunk_z)
    
Blocks.chunk_provider = None
        
