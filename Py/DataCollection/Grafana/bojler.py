

class Bojler:
    def __init__(self):
        self.EAsun_voltage = 0
        self.string_power = 0

    @property
    def power(self):
        if not self.EAsun_voltage:
            return self.string_power
        else:
            return 0