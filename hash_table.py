class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node
        
class Data:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        
class HashTable:
    def __init__(self, table_size):
        self.table_size = table_size
        self.hash_table = [None] * self.table_size
    
    def custom_hash(self, key):
        hash_value = 0
        for i in key:
            hash_value += ord(i)
            hash_value = (hash_value * ord(i)) % self.table_size
        
        return hash_value
    
    def add_key_value(self, key, value):
        hash_value = self.custom_hash(key)
        
        # first item with this hash key
        if self.hash_table[hash_value] is None:
            self.hash_table[hash_value] = Node(Data(key, value), None)
        else:
            node = self.hash_table[hash_value]
            
            while node.next_node:
                node = node.next_node
            
            node.next_node = Node(Data(key, value), None)
        
    def get_value(self, key):
        val = None
        
        hash_value = self.custom_hash(key)
        
        if self.hash_table[hash_value] is not None:
            if self.hash_table[hash_value].next_node is None:
                val = self.hash_table[hash_value].data.value
            else:
                node = self.hash_table[hash_value]
                while node:
                    if node.data.key is key:
                        val = node.data.value
                        break
                    
                    node = node.next_node
        
        return val
    
    def print_hash(self):
        print("{")
        
        for i, val in enumerate(self.hash_table):
            if val is not None:
                llist_string = ""
                node = val
                if node.next_node:
                    while node.next_node:
                        llist_string += (
                            str(node.data.key) + " : " + str(node.data.value) + " --> "
                        )
                        node = node.next_node
                    llist_string += (
                        str(node.data.key) + " : " + str(node.data.value) + " --> None"
                    )
                    print(f"    [{i}] {llist_string}")
                else:
                    print(f"    [{i}] {val.data.key} : {val.data.value}")
            else:
                print(f"    [{i}] {val}")
        print("}")