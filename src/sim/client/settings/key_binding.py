class KeyBinding:
    def __init__(self, description, key_code, category):
        self.description = description
        self.key_code = key_code
        self.category = category
        self.pressed = False

    def is_key_down(self):
        return self.pressed