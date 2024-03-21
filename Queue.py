from collections import deque
from threading import Condition

class Queue:
    def __init__(self):
        self.queue = deque()
        self.condition = Condition()

    def enqueue(self, obj):
        with self.condition:
            self.queue.append(obj)
            self.condition.notify()

    def bdequeue(self):
        with self.condition:
            while len(self.queue) == 0:
                self.condition.wait()
            return self.queue.popleft()