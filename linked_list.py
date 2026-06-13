class Node:
    def __init__(self, task):
        self.task = task
        self.next = None

# Using a list would work fine for something of this scale. 
# Just demonstrating Linked List usage here. 
# Using linked list would make sense and be beneficial if the list of tasks was really large. 
# In that case, an insert at the head would take O(1) time instead of O(n) that a Python list would take. 

class LinkedList:
    def __init__(self):
        self.head = None
    
    # insert a node into the linked list
    def insert(self, task):
        new_node = Node(task)
        # if the list is empty
        if self.head is None:
            self.head = new_node
        # if the list is not empty, traverse the list to the end, add the node to end of the list
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        
    # convert the linked list to a list
    def to_list(self):
        task_list = []
        current = self.head
        while current is not None:
            task_list.append(current.task)
            current = current.next
        return task_list
    
    # reorder the linked list using a list of tasks
    def reorder(self, tasks):
        self.head = None
        for task in tasks:
            self.insert(task)
            