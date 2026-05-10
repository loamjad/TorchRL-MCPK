class BaseAttributeMap:
    def __init__(self):
        self.attributes = {}
        self.attributes_by_name = {}
        self.field_180377_c = {}

    def get_attribute_instance(self, attribute):
        return self.attributes.get(attribute)

    def func_180794_a(self, p_180794_1_):
        pass

    def register_attribute(self, attribute):
        if attribute.get_attribute_unlocalized_name() in self.attributes_by_name:
            raise Exception("Attribute is already registered!")
        else:
            iattributeinstance = self.func_180376_c(attribute)
            self.attributes_by_name[attribute.get_attribute_unlocalized_name()] = iattributeinstance
            self.attributes[attribute] = iattributeinstance

            iattribute = attribute.func_180372_d()
            while iattribute != None:
                self.field_180377_c[iattribute] = attribute
                iattribute = attribute.func_180372_d()

        return iattributeinstance