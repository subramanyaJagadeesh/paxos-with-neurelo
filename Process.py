from threading import Thread, Event
from PaxosMessage import *
from Neurelo import Neurelo
import sys

class Process(Thread):
    def __init__(self, env, me):
        super().__init__()
        self.me = me
        self.env = env
        self.neurelo = Neurelo.get_instance()
        self.running = True

    def run(self):
        while self.running:
            self.body()
            self.env.remove_proc(self.me)
            # Your thread's main loop or task
            pass
        
    def stop(self):
       sys.exit()
    
    def body(self):
        raise NotImplementedError("Subclass must implement abstract method")
    
    def get_next_message(self):
        response = self.neurelo.pop_item_from_queue(self)
        return construct_message(response)

    def send_message(self, dst, msg):
        self.env.send_message(dst, msg)

    def deliver(self, msg):
        self.neurelo.push_item_to_queue(self, msg)