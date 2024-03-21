
from BallotNumber import BallotNumber
from Commander import Commander
from PaxosMessage import AdoptedMessage, PreemptedMessage, ProposeMessage
from Process import Process
from ProcessId import ProcessId
from Scout import Scout

class Leader(Process):
    def __init__(self, env, me, acceptors, replicas):
        super().__init__(env, me)
        self.env = env
        self.me = me
        self.ballot_number = BallotNumber(0, me)
        self.acceptors = acceptors
        self.replicas = replicas
        self.proposals = {}
        self.active = False
        env.add_proc(me, self)

    def body(self):
        print(f"Here I am: {self.me}")
        Scout(self.env, ProcessId(f"scout:{self.me}:{self.ballot_number}"), self.me, self.acceptors, self.ballot_number)
        
        while True:
            msg = self.get_next_message()
            if msg == None:
                continue
            if isinstance(msg, ProposeMessage):
                if msg.slot_number not in self.proposals:
                    self.proposals[msg.slot_number] = msg.command
                    if self.active:
                        Commander(self.env, ProcessId(f"commander:{self.me}:{self.ballot_number}:{msg.slot_number}"), self.me, self.acceptors, self.replicas, self.ballot_number, msg.slot_number, msg.command)
            elif isinstance(msg, AdoptedMessage):
                if self.ballot_number == msg.ballot_number:
                    max = {}
                    for pv in msg.accepted:
                        bn = max.get(pv.slot_number)
                        if bn is None or bn < pv.ballot_number:
                            max[pv.slot_number] = pv.ballot_number
                            self.proposals[pv.slot_number] = pv.command
                    for sn in self.proposals:
                        Commander(self.env, ProcessId(f"commander:{self.me}:{self.ballot_number}:{sn}"), self.me, self.acceptors, self.replicas, self.ballot_number, sn, self.proposals[sn])
                    self.active = True
            elif isinstance(msg, PreemptedMessage):
                if self.ballot_number < msg.ballot_number:
                    self.ballot_number = BallotNumber(msg.ballot_number.round + 1, self.me)
                    Scout(self.env, ProcessId(f"scout:{self.me}:{self.ballot_number}"), self.me, self.acceptors, self.ballot_number)
                    self.active = False
            else:
                print("Leader: unknown msg type")
