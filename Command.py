from ProcessId import ProcessId
class Command:
    def __init__(self, client, req_id, op):
        self.client = client
        self.req_id = req_id
        self.op = op

    def __eq__(self, other):
        if not isinstance(other, Command):
            # Ensures that the comparison is only performed with instances of Command
            return NotImplemented
        return self.client == other.client and self.req_id == other.req_id and self.op == other.op

    def __repr__(self):
        # Provides a string representation of the instance, useful for debugging
        return f"Command({self.client}, {self.req_id}, {self.op})"
    
    def to_dict(self):
        return {
            "client": self.client.to_dict(),
            "req_id": self.req_id,
            "op": self.op
        }
    
    def from_dict(value):
        return Command(
            client=ProcessId(value.get("command").get("client").get("name")), 
            req_id=value.get("command").get("req_id"), 
            op=value.get("command").get("op")
        )
