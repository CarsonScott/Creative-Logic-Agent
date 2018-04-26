class Domain:
    def __init__(self, low, high):
        self.low = low
        self.high = high
        self.bounds = (low, high)

    def length(self):
        return self.high - self.low

    def center(self):
        return self.length() / 2

    def contains(self, value):
        return self.low <= value and self.high > value

class Variable:
    def __init__(self, domain=None, rate=0, value=0):
        self.domain = domain
        self.value = value
        self.rate = rate

    def is_bounded(self):
        return self.domain == None

    def is_valid(self):
        if self.domain == None:
            return True
        return self.domain.contains(self.value)

    def get(self):
        return self.value

    def set(self, value):
        self.value = value
        if not self.is_valid():
            if value < self.domain.low:
                self.value = self.domain.low
            elif value >= self.domain.high:
                self.value = self.domain.high

    def error(self, value):
        return pow(value - self.domain.center(), 2)

    def iterate(self, delta=0):
        rate = self.rate
        value = self.value + delta * rate
        error = self.error(value)-self.error(self.value)
        delta -= error
        target = value + delta * rate
        self.value = target

    def decay(self, delta=0):
        offset = self.value - self.domain.center()
        delta = abs(delta)

        if offset > 0:
            delta = -delta
        self.iterate(delta)
