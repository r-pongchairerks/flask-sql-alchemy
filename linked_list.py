class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node
        
class LinkedList:
    def __init__(self):
        self.head = None
        self.last_node = None
        
    def print_ll(self):
        ll_string = ""
        node = self.head
        if node is None:
            print(None)
        
        while node:
            ll_string += f"{str(node.data)} -> "
            if node.next_node is None:
                ll_string += " None"
            
            node = node.next_node
        
        print(ll_string)
                
    def insert_beginning(self, data):
        new_node = Node(data=data, next_node=self.head)
        if self.head is None:
            self.last_node = new_node 
        
        self.head = new_node
    
    def insert_at_end(self, data):
        if self.head is None:
            self.insert_beginning(data)
            return
         
        self.last_node.next_node = Node(data=data)
        self.last_node = self.last_node.next_node
    
    def to_list(self):
        l = []
        
        if self.head is not None:
            node = self.head
            while node:
                l.append(node.data)
                node = node.next_node
        
        return l
