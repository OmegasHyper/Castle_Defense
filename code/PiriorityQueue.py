from Queue import *
class PriorityQueue:
    def __init__(self):
        self.high = Queue()
        self.low = Queue()

    def enqueue(self, item, priority='low'):
        if priority == 'high':
            self.high.enqueue(item)
        else:
            self.low.enqueue(item)

    def dequeue(self):
        if not self.high.isempty():
            return self.high.dequeue()
        elif not self.low.isempty():
            return self.low.dequeue()
        else:
            return None
    def get_front(self):
        if not self.high.isempty():
            return self.high.get_front()
        return self.low.get_front()

    def isempty(self):
        return self.high.isempty() and self.low.isempty()

    def get_size(self):
        return self.high.get_size() + self.low.get_size()

    def print_queue(self):
        print("High priority queue:")
        self.high.print_queue()
        print("Low priority queue:")
        self.low.print_queue()
