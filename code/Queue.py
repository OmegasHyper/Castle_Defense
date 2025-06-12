#For most use cases in Python: Use collections.deque — it's fast, safe, and designed for queues
# Queue using linked list logic 
class Queue :
    def __init__ (self):
        self.front = None
        self.back = None

    def enqueue(self, item):
        newnode = Node(item)
        if self.isempty() :
            self.front = self.back= newnode
            return
        else:
            self.back.next = newnode
            self.back = self.back.next

    def dequeue(self):
        pass
    def get_front(self):
        pass
    def get_back(self) :
        pass
    def print_queue(self):
        pass
    def get_size(self):
        pass
    def get_type(self):
        pass
    def isempty(self):
        return self.front == None
class Node :
    def __init__ (self, data):
        self.data = data
        self.next = None

