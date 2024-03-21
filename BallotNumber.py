from ProcessId import ProcessId

class BallotNumber:
    def __init__(self, round, leader_id):
        self.round = round
        self.leader_id = leader_id

    def __eq__(self, other):
        if not isinstance(other, BallotNumber):
            return NotImplemented
        return self.round == other.round and self.leader_id == other.leader_id

    def __lt__(self, other):
        if not isinstance(other, BallotNumber):
            return NotImplemented
        if self.round != other.round:
            return self.round < other.round
        return self.leader_id < other.leader_id

    def __le__(self, other):
        if not isinstance(other, BallotNumber):
            return NotImplemented
        if self.round != other.round:
            return self.round <= other.round
        return self.leader_id <= other.leader_id
    
    def __repr__(self):
        return f"BN({self.round}, {self.leader_id})"
    
    def to_dict(self):
        return {
            "round": self.round,
            "leader_id": self.leader_id.to_dict()
        }

    def from_dict(payload):
        return BallotNumber(
            round=payload.get("ballot_number").get("round"), 
            leader_id=ProcessId(payload.get("ballot_number").get("leader_id").get("name")))
    
