import numpy as np

class ModifiableAttributeInstance:
    def __init__(self, attribute_map_in, generic_attribute_in):
        self.map_by_operation = {}
        self.map_by_name = {}
        self.map_by_UUID = {}

        self.attribute_map = attribute_map_in
        self.generic_attribute = generic_attribute_in
        self.base_value = generic_attribute_in.get_default_value()

        for i in range(3):
            self.map_by_operation[i] = set()

        self.needs_update = True
        self.cached_value = self.base_value

    def get_modifier(self, id):
        return self.map_by_UUID.get(id)

    def get_base_value(self):
        return self.base_value
    
    def set_base_value(self, base_value):
        if base_value != self.get_base_value():
            self.base_value = base_value
            self.flag_for_update()

    def get_modifiers_by_operation(self, operation):
        return self.map_by_operation[operation]

    def func_180375_b(self, p_180375_1_):
        s = set(self.get_modifiers_by_operation(p_180375_1_))

        iattribute = self.generic_attribute.func_180372_d()
        while iattribute is not None:
            iattributeinstance = self.attribute_map.get_attribute_instance(iattribute)
            if iattributeinstance is not None:
                s.update(iattributeinstance.get_modifiers_by_operation(p_180375_1_))
            iattribute = iattribute.func_180372_d()

        return s

    def apply_modifier(self, modifier):
        if self.get_modifier(modifier.get_id()) is not None:
            raise Exception("Modifier is already applied on this attribute!")
        else:
            s = self.map_by_name.get(modifier.get_name())

            if s is None:
                s = set()
                self.map_by_name[modifier.get_name()] = s

            self.map_by_operation.get(modifier.get_operation()).add(modifier)
            s.add(modifier)
            self.map_by_UUID[modifier.get_id()] = modifier
            self.flag_for_update()

    def get_attribute_value(self):
        if self.needs_update:
            self.cached_value = self.compute_value()
            self.needs_update = False

        return self.cached_value

    def compute_value(self):
        d0 = self.get_base_value()

        for attributemodifier in self.func_180375_b(0):
            d0 += attributemodifier.get_amount()

        d1 = d0

        for attributemodifier1 in self.func_180375_b(1):
            d1 += d0 * attributemodifier1.get_amount()

        for attributemodifier2 in self.func_180375_b(2):
            d1 *= np.float64(1.0) + attributemodifier2.get_amount()

        return self.generic_attribute.clamp_value(d1)

    def flag_for_update(self):
        self.needs_update = True
        self.attribute_map.func_180794_a(self)
