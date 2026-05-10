class AttributeModifier:

    def __init__(self, id_in, name_in, amount_in, operation_in):
        self.is_saved = True
        self.id = id_in
        self.name = name_in
        self.amount = amount_in
        self.operation = operation_in

    def get_id(self):
        return self.id

    def get_name(self):
        return self.name

    def get_amount(self):
        return self.amount

    def get_operation(self):
        return self.operation

    def set_saved(self, saved):
        self.is_saved = saved
        return self

