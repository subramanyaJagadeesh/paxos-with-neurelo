from ProcessId import ProcessId
from Acceptor import Acceptor
from Replica import Replica
from Leader import Leader
from Command import Command
from PaxosMessage import RequestMessage
from Neurelo import Neurelo
import os
import sys
import time

class Env:
    def __init__(self, n_acceptors, n_replicas, n_leaders, n_ops):
        self.procs = {}
        self.n_acceptors = n_acceptors
        self.n_replicas = n_replicas
        self.n_leaders = n_leaders
        self.n_requests = n_ops
        self.complete_requests = 0
        self.neurelo = Neurelo.get_instance()
        self.start_time = time.time_ns()

    def send_message(self, dst, msg):
        # In a multithreaded context, consider using locks for thread safety
        p = self.procs.get(dst)
        if p is not None:
            p.deliver(msg)

    def add_proc(self, pid, proc):
        # In a multithreaded context, consider using locks for thread safety
        self.procs[pid] = proc
        proc.start()  # Ensure the Process class implements a start method, perhaps initiating a thread

    def remove_proc(self, pid):
        # In a multithreaded context, consider using locks for thread safety
        if pid in self.procs:
            del self.procs[pid]
    
    def check_and_stop_processes(self):
        self.complete_requests+=1
        if self.complete_requests >= self.n_replicas * (self.n_requests - 2) :
            response = self.neurelo.delete_items_in_queue()
            if response.status_code == 200:
                execution_time = time.time_ns() - self.start_time
                print(f"Performed {self.n_requests} requests in {execution_time/1_000_000_000.0}s, shutting down!")
                os._exit(0)
            else:
                raise 'Unable to delete all queue items'
            
    def run(self):
        acceptors = [ProcessId(f"acceptor-{i}") for i in range(self.n_acceptors)]
        replicas = [ProcessId(f"replica-{i}") for i in range(self.n_replicas)]
        leaders = [ProcessId(f"leader-{i}") for i in range(self.n_leaders)]

        for i, pid in enumerate(acceptors):
            Acceptor(self, pid)  # Assumes Acceptor's constructor registers itself

        for i, pid in enumerate(replicas):
            Replica(self, pid, leaders)  # Assumes Replica's constructor registers itself

        for i, pid in enumerate(leaders):
            Leader(self, pid, acceptors, replicas)  # Assumes Leader's constructor registers itself

        for i in range(1, self.n_requests):
            pid = ProcessId(f"client-{i}")
            for r in replicas:
                self.send_message(r, RequestMessage(pid, Command(pid, 0, f"operation {i}")))
        return
def validate_input(num):
    if not num.isdigit() or (int(num) < 1 or int(num) >10):
        return False
    return True

if __name__ == "__main__":
    print('Paxos Consensus Algorithm with the power of Neurelo\'s Data Access API!')

    n_acceptors = input('Enter the number of Acceptors between 1 to 10: \n')

    if not validate_input(n_acceptors): 
        print('Acceptors must be within 1 to 10')
        sys.exit(1)        

    n_replicas = input('Enter the number of Replicas between 1 to 10: \n')
    if not validate_input(n_replicas): 
        print('Replicas must be within 1 to 10')
        sys.exit(1)

    n_leaders = input('Enter the number of Leaders between 1 to 10: \n')
    if not validate_input(n_leaders): 
        print('Leaders must be within 1 to 10')
        sys.exit(1)
    
    n_ops = input('Enter the number of operations to perform between 1 to 10: \n')
    if not validate_input(n_ops): 
        print('Operations must be within 1 to 10')
        sys.exit(1)
    Env(int(n_acceptors), int(n_replicas), int(n_leaders), int(n_ops)).run()
