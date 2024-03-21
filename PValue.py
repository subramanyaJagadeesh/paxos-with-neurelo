class PValue:
    def __init__(self, ballot_number, slot_number, command):
        self.ballot_number = ballot_number
        self.slot_number = slot_number
        self.command = command

    def __str__(self):
        return f"PV({self.ballot_number}, {self.slot_number}, {self.command})"
    
    def to_dict(self):
        return {
            "ballot_number": self.ballot_number.to_dict(),
            "slot_number": self.slot_number,
            "command": self.command.to_dict(),
        }

