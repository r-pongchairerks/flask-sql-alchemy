class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node
        

class Stack:
    def __init__(self):
        self.top = None
    
    def peek(self):
        return self.top
    
    def push(self, data):
        if self.top is None:
            self.top = Node(data)
        else:
            next_node = self.top
            self.top = Node(data, next_node)
    
    def pop(self):
        if self.top is None:
            return None
        else:
            popped = self.top
            self.top = self.top.next_node
            return popped
            