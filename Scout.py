from Process import Process
from PaxosMessage import P1aMessage, P1bMessage, PreemptedMessage, AdoptedMessage

class Scout(Process):
    def __init__(self, env, me, leader, acceptors, ballot_number):
        super().__init__(env, me)
        self.env = env
        self.me = me
        self.leader = leader
        self.acceptors = acceptors
        self.ballot_number = ballot_number
        env.add_proc(me, self)

    def body(self):
        m1 = P1aMessage(self.me, self.ballot_number)
        waitfor = set(self.acceptors)
        pvalues = set()
        
        for a in self.acceptors:
            self.send_message(a, m1)
        
        while 2 * len(waitfor) >= len(self.acceptors):
            msg = self.get_next_message()
            if msg == None:
              continue
            if isinstance(msg, P1bMessage):
                if self.ballot_number != msg.ballot_number:
                    self.send_message(self.leader, PreemptedMessage(self.me, msg.ballot_number))
                    return
                if msg.src in waitfor:
                    waitfor.remove(msg.src)
                    pvalues.update(msg.accepted)
            else:
                print("Scout: unexpected msg")
        
        self.send_message(self.leader, AdoptedMessage(self.me, self.ballot_number, pvalues))
