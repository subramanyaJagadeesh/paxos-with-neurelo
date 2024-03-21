class ProcessId:
    def __init__(self, name):
        self.name = name

    def __eq__(self, other):
        if isinstance(other, ProcessId):
            return self.name == other.name
        return NotImplemented

    def __lt__(self, other):
        if isinstance(other, ProcessId):
            return self.name < other.name
        return NotImplemented
    
    def __le__(self, other):
        if isinstance(other, ProcessId):
            return self.name <= other.name
        return NotImplemented
    
    def __hash__(self):
        return hash(self.name)

    def __str__(self):
        return self.name
    
    def to_dict(self):
        return {
            "name": self.name,
        }
