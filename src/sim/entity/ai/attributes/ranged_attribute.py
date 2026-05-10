from src.sim.entity.ai.attributes.base_attribute import BaseAttribute
from src.sim.util.math_helper import MathHelper

class RangedAttribute(BaseAttribute):
    def __init__(self, p_i45891_1_, unlocalized_name_in, default_value, minimum_value_in, maximum_value_in):
        super().__init__(p_i45891_1_, unlocalized_name_in, default_value)
        self.minimum_value = minimum_value_in
        self.maximum_value = maximum_value_in

    def set_description(self, description_in):
        self.description = description_in
        return self
    
    def clamp_value(self, p_111109_1_):
        p_111109_1_ = MathHelper.clamp_double(p_111109_1_, self.minimum_value, self.maximum_value)
        return p_111109_1_
        