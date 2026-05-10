import numpy as np

from src.sim.entity.ai.attributes.ranged_attribute import RangedAttribute

class SharedMonsterAttributes:
    pass

SharedMonsterAttributes.movement_speed = RangedAttribute(None, "generic.movementSpeed", np.float64(0.699999988079071), np.float64(0.0), np.float64(1024.0)).set_description("Movement Speed").set_should_watch(True)