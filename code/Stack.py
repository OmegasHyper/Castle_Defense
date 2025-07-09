from Queue import Node
import game
import Obstacles
class Stack :
    def __init__(self):
        self.top = None  # Points to the top of
        self.size = 0
    
    def push (self,data):
        newnode = Node(data)
        newnode.next = self.top
        self.top = newnode
        self.size += 1
    ## modified pop to kill the 
    def pop (self):
        if self.isempty():return None
        temp=self.top
        self.top = self.top.next
        self.size -= 1
        return temp.data
    def peek (self):
        if self.isempty():return None
        return self.top.data
    def display(self):
        current = self.top
        while current:
            # print(current.data)
            current = current.next
    def isempty(self):
        return self.top is None
    def get_size(self):
        return self.size

class Stack_obstacles (Stack):
    def __init__(self):
        super().__init__()
    def pop(self):
        if self.isempty():return None
        
        temp=self.top
        self.top = self.top.next
        self.size -= 1
        if temp.data.health == 40:
            game.gold_quantity += Obstacles.pricee
        temp.data.kill()