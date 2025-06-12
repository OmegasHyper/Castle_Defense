#For most use cases in Python: Use collections.deque — it's fast, safe, and designed for queues
# Queue using linked list logic 
class Queue :
    def __init__ (self):
        self.front = None
        self.back = None
        self.size = 0

    def enqueue(self, item):
        newnode = Node(item)
        if self.isempty() :
            self.front = self.back= newnode
        
        else:
            self.back.next = newnode
            self.back = self.back.next
        self.size+=1

    def dequeue(self):
        if self.isempty():
            return None
        elif self.front==self.back:
            temp = self.front
            self.back=self.front=None
            self.size-=1
            return temp.data
        else :
            temp = self.front
            self.front = self.front.next
            self.size-=1
            return temp.data

    def get_front(self):
        if self.isempty():
            return "empty Queue" 
        else : return self.front.data
    def get_back(self) :
        if self.isempty():
            return "empty Queue" 
        else : return self.back.data
    def print_queue(self):
        if self.isempty():
            return "empty Queue" 
        else:
            temp = self.front
            while temp:
                print(temp.data)
                temp = temp.next
    def get_size(self):
        return self.size
    def get_type(self):
        if self.isempty():
            return None 
        return type(self.front.data)
    def isempty(self):
        return self.front == None
class Node :
    def __init__ (self, data):
        self.data = data
        self.next = None

