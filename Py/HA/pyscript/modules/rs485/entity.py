class Entity:
    def __init__(self, name, unit, device_class):
        self.name = name
        self.unit = unit
        self.device_class = device_class
        self.value = None


class Address:
    def __init__(self, start, end, type_reg):
        self.start = start
        self.end = end
        self.type_reg = type_reg
        self.range = range(start, end+1)