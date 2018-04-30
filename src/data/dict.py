class Dict(dict):
    def __init__(self, keys=[]):
        super().__init__()
        self.create(keys)
    def set(self, key, value):
        self[key] = value
    def get(self, key):
        return self[key]
    def create(self, keys, value=None, type=None):
        for i in range(len(keys)):
            k = keys[i]
            x = value
            if value == None and type != None:
                x = type()
            self[k] = x
        return self
    def has(self, key):
        return key in self.keys()
    def keys(self):
         return list(super().keys())