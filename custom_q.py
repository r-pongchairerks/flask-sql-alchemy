class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node
        
class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        
    def enqueue(self, data):
        if self.tail is None and self.head is None:
            self.tail = self.head = Node(data, None)
        else:
            self.tail.next_node = Node(data, None)
            self.tail = self.tail.next_node
            
    def dequeue(self):
        item = None
        if self.head:
            item = self.head
            self.head = self.head.next_node
        
        if self.head is None:
            self.tail = None
        
        return item
