from time import time


class Power:
    def __init__(self):
        self._string_1 = 0
        self.string_2 = 0
        self.last_upd_s1 = time()

    @property
    def power(self):
        d69_timeout = 30
        if (time() - self.last_upd_s1) > d69_timeout:
            self.string_1 = 0
        return self.string_1 + self.string_2

    @property
    def string_1(self):
        return self._string_1

    @string_1.setter
    def string_1(self, val):
        self._string_1 = val
        self.last_upd_s1 = time()
