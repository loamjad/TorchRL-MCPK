class BaseAttribute:
    def __init__(self, p_i45892_1_, unlocalized_name_in, default_value_in):
        self.field_180373_a = p_i45892_1_
        self.unlocalized_name = unlocalized_name_in
        self.default_value = default_value_in

    def get_attribute_unlocalized_name(self):
        return self.unlocalized_name

    def get_default_value(self):
        return self.default_value

    def set_should_watch(self, should_watch_in):
        self.should_watch = should_watch_in
        return self
    
    def func_180372_d(self):
        return self.field_180373_a