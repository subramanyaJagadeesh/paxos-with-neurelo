import json
from BallotNumber import BallotNumber
from ProcessId import ProcessId
from PValue import PValue
from Command import Command

class PaxosMessage:
    def __init__(self, src, type):
        self.src = src
        self.type = type
    def to_dict(self):
        return {
            "src": str(self.src),  # Assuming `src` is an instance of another class (like `ProcessId`)
            "type" : str(self.type)
        }

class P1aMessage(PaxosMessage):
    def __init__(self, src, ballot_number):
        super().__init__(src, 'P1aMessage')
        self.ballot_number = ballot_number
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "ballot_number": self.ballot_number.to_dict()  # Assuming complex type; define `to_dict` in `BallotNumber` as well
        })
        return data

class P1bMessage(PaxosMessage):
    def __init__(self, src, ballot_number, accepted):
        super().__init__(src, 'P1bMessage')
        self.ballot_number = ballot_number
        self.accepted = accepted
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "ballot_number": self.ballot_number.to_dict(),  # Assuming complex type; define `to_dict` in `BallotNumber` as well
            "accepted": [pvalue.to_dict() for pvalue in self.accepted]
        })
        return data

class P2aMessage(PaxosMessage):
    def __init__(self, src, ballot_number, slot_number, command):
        super().__init__(src, 'P2aMessage')
        self.ballot_number = ballot_number
        self.slot_number = slot_number
        self.command = command
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "ballot_number": self.ballot_number.to_dict(),  # Assuming complex type; define `to_dict` in `BallotNumber` as well
            "slot_number": self.slot_number,
            "command": self.command.to_dict()
        })
        return data

class P2bMessage(PaxosMessage):
    def __init__(self, src, ballot_number, slot_number):
        super().__init__(src, 'P2bMessage')
        self.ballot_number = ballot_number
        self.slot_number = slot_number
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "ballot_number": self.ballot_number.to_dict(),  # Assuming complex type; define `to_dict` in `BallotNumber` as well
            "slot_number": self.slot_number,
        })
        return data

class PreemptedMessage(PaxosMessage):
    def __init__(self, src, ballot_number):
        super().__init__(src, 'PreemptedMessage')
        self.ballot_number = ballot_number
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "ballot_number": self.ballot_number.to_dict(),  # Assuming complex type; define `to_dict` in `BallotNumber` as well
        })
        return data   

class AdoptedMessage(PaxosMessage):
    def __init__(self, src, ballot_number, accepted):
        super().__init__(src, 'AdoptedMessage')
        self.ballot_number = ballot_number
        self.accepted = accepted
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "ballot_number": self.ballot_number.to_dict(),  # Assuming complex type; define `to_dict` in `BallotNumber` as well
            "accepted": [pvalue.to_dict() for pvalue in self.accepted]
        })
        return data

class DecisionMessage(PaxosMessage):
    def __init__(self, src, slot_number, command):
        super().__init__(src, 'DecisionMessage')
        self.slot_number = slot_number
        self.command = command
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "slot_number": self.slot_number,
            "command": self.command.to_dict()
        })
        return data

class RequestMessage(PaxosMessage):
    def __init__(self, src, command):
        super().__init__(src, 'RequestMessage')
        self.command = command
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "command": self.command.to_dict()
        })
        return data

class ProposeMessage(PaxosMessage):
    def __init__(self, src, slot_number, command):
        super().__init__(src, 'ProposeMessage')
        self.slot_number = slot_number
        self.command = command
    def to_dict(self):
        data = super().to_dict()
        data.update({
            "slot_number": self.slot_number,
            "command": self.command.to_dict()
        })
        return data

def construct_message(response):
    if len(response.get("data")) > 0:
        payload = json.loads(response.get("data")[0]['payload'])

        typeofpaylod = payload.get('type')
        del payload['type']

        src = ProcessId(payload.get("src"))
        
        if typeofpaylod == 'P1aMessage':
            return P1aMessage(src=src, ballot_number=BallotNumber.from_dict(payload))
        
        elif typeofpaylod == 'P1bMessage':
            return P1bMessage(
                src=src,
                ballot_number=BallotNumber.from_dict(payload),
                accepted=set([PValue(
                    ballot_number=BallotNumber.from_dict(value), 
                    slot_number=value.get("slot_number"),
                    command=Command.from_dict(value))
                    for value in payload.get('accepted') ]))
        
        elif typeofpaylod == 'P2aMessage':
            return P2aMessage(
                src=src, 
                ballot_number=BallotNumber.from_dict(payload),
                slot_number=payload.get("slot_number"),
                command=Command.from_dict(payload))
        
        elif typeofpaylod == 'P2bMessage':
            return P2bMessage(
                src=src,
                ballot_number=BallotNumber.from_dict(payload),
                slot_number=payload.get("slot_number"))
        
        elif typeofpaylod == 'PreemptedMessage':
            return PreemptedMessage(
                src=src,
                ballot_number=BallotNumber.from_dict(payload))
        
        elif typeofpaylod == 'AdoptedMessage':
            return AdoptedMessage(
                src=src,
                ballot_number=BallotNumber.from_dict(payload),
                accepted=set([PValue(
                    ballot_number=BallotNumber.from_dict(value), 
                    slot_number=value.get("slot_number"),
                    command=Command.from_dict(value))
                    for value in payload.get('accepted')]))
        
        elif typeofpaylod == 'DecisionMessage':
            return DecisionMessage(
                src=src, 
                slot_number=payload.get("slot_number"),
                command=Command.from_dict(payload))
        
        elif typeofpaylod == 'RequestMessage':
            return RequestMessage(
                src=src, 
                command=Command.from_dict(payload))
        
        else:
            return ProposeMessage(
                src=src, 
                slot_number=payload.get("slot_number"),
                command=Command.from_dict(payload))
        
    return None