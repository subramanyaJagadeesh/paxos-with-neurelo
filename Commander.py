from PaxosMessage import P2aMessage, P2bMessage, PreemptedMessage, DecisionMessage
from Process import Process

class Commander(Process):
    def __init__(self, env, me, leader, acceptors, replicas, ballot_number, slot_number, command):
        super().__init__(env, me)
        self.env = env
        self.me = me
        self.leader = leader
        self.acceptors = acceptors
        self.replicas = replicas
        self.ballot_number = ballot_number
        self.slot_number = slot_number
        self.command = command
        env.add_proc(me, self)

    def body(self):
        m2 = P2aMessage(self.me, self.ballot_number, self.slot_number, self.command)
        waitfor = set(self.acceptors)
        
        for a in self.acceptors:
            self.send_message(a, m2)
        
        while len(waitfor) * 2 >= len(self.acceptors):
            msg = self.get_next_message()
            if msg == None:
              continue
            if isinstance(msg, P2bMessage):
                if self.ballot_number == msg.ballot_number:
                    if msg.src in waitfor:
                        waitfor.remove(msg.src)
                else:
                    self.send_message(self.leader, PreemptedMessage(self.me, msg.ballot_number))
                    return
        
        for r in self.replicas:
            self.send_message(r, DecisionMessage(self.me, self.slot_number, self.command))
