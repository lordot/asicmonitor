class Asic:
    def __init__(self, ip: str, workername: str):
        self.ip: str = ip
        self.workername: str = workername

    def __repr__(self):
        return self.ip
