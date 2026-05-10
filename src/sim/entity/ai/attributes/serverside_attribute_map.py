from src.sim.entity.ai.attributes.base_attribute_map import BaseAttributeMap
from src.sim.entity.ai.attributes.modifiable_attributes_instance import ModifiableAttributeInstance

class ServersideAttributeMap(BaseAttributeMap):
    def __init__(self):
        super().__init__()

    def p_180794_a(self, p_180794_1_):
        if p_180794_1_.get_attribute().get_should_watch():
            self.attribute_instance_set.add(p_180794_1_)

        for iattribute in self.field_180377_c.get(p_180794_1_.getAttribute()):
            modifiableattributeinstance = self.get_attribute_instance(iattribute)
            if modifiableattributeinstance != None:
                modifiableattributeinstance.flag_for_update()

    def func_180376_c(self, p_180376_1_):
        return ModifiableAttributeInstance(self, p_180376_1_)
            