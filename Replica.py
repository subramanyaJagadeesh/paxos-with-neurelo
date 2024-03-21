from PaxosMessage import DecisionMessage, ProposeMessage, RequestMessage
from Process import Process

class Replica(Process):
    def __init__(self, env, me, leaders):
        super().__init__(env, me)
        self.leaders = leaders
        self.env = env
        self.me = me
        self.slot_num = 1
        self.proposals = {}  # slot number -> Command
        self.decisions = {}  # slot number -> Command
        env.add_proc(me, self)

    def propose(self, c):
        if c not in self.decisions.values():
            s = 0
            while True:  # Infinite range, Python doesn't have Java's `for(;;)` construct
                if s not in self.proposals and s not in self.decisions:
                    self.proposals[s] = c
                    print(f"{self.me}: propose {c}, with slot {s}")
                    for ldr in self.leaders:
                        self.send_message(ldr, ProposeMessage(self.me, s, c))
                    break
                s+=1

    def perform(self, c):
        for s in range(1, self.slot_num):
            if c == self.decisions.get(s):
                self.slot_num += 1
                return
        print(f"{self.me}: perform {c}")
        self.slot_num += 1
        self.env.check_and_stop_processes()

    def body(self):
        print(f"Here I am: {self.me}")
        while True and self.running:
            msg = self.get_next_message()
            if msg == None:
              continue
            if isinstance(msg, RequestMessage):
                self.propose(msg.command)
            elif isinstance(msg, DecisionMessage):
                self.decisions[msg.slot_number] = msg.command
                while True:
                    c = self.decisions.get(self.slot_num)
                    if c is None:
                        break
                    c2 = self.proposals.get(self.slot_num)
                    if c2 and c2 != c:
                        self.propose(c2)
                    self.perform(c)
            else:
                print("Replica: unknown msg type")
