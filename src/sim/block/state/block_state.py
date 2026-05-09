from src.sim.block.state.block_state_base import BlockStateBase

class BlockState(BlockStateBase):
    def __init__(self, block_in):
        self.block = block_in

    def get_block(self):
        return self.block