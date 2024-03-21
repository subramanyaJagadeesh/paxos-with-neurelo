from Process import Process
from PaxosMessage import P1aMessage, P1bMessage, P2aMessage, P2bMessage
from PValue import PValue

class Acceptor(Process):
    def __init__(self, env, me):
        super().__init__(env, me)
        self.env = env
        self.me = me
        self.ballot_number = None
        self.accepted = set()
        env.add_proc(me, self)

    def body(self):
        print(f"Here I am: {self.me}")
        while True:
            msg = self.get_next_message()
            if msg == None:
                continue
            if isinstance(msg, P1aMessage):
                if self.ballot_number is None or self.ballot_number < msg.ballot_number:
                    self.ballot_number = msg.ballot_number
                self.send_message(msg.src, P1bMessage(self.me, self.ballot_number, set(self.accepted)))
            elif isinstance(msg, P2aMessage):
                if self.ballot_number is None or self.ballot_number <= msg.ballot_number:
                    self.ballot_number = msg.ballot_number
                    self.accepted.add(PValue(self.ballot_number, msg.slot_number, msg.command))
                self.send_message(msg.src, P2bMessage(self.me, self.ballot_number, msg.slot_number))