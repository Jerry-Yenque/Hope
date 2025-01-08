class DropdownConstant:
    def __init__(self, identifier, value):
        self.identifier = identifier
        self.value = value

    def __repr__(self):
        return f"{self.identifier}({self.value})"