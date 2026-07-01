from collections import deque
from linked_list import LinkedList

class TaskManager:
    # A class that showcases a usage of different data structures to manage tasks.
    def __init__(self):
        self.tasks = {}                     # dict
        self.completed_tasks = set()        # set
        self.backlog = deque()              # queue
        self.undo_stack = []                # list stack
        self.priority_list = LinkedList()   # linked list
        self.next_id = 1                    # int
        self.current_task = None            # int

    def add_task(self, description):
        # Usage: Add a task to the TaskManager.
        # How it does its job: Add the task id and description to the tasks dictionary and the task id to the backlog queue.
        #   then increment the next_id variable to prepare for the next task when added.
        #
        if not description or description.strip() == "":
            return (False, None)
        
        current_task_id = self.next_id
        self.tasks[current_task_id] = description
        self.backlog.append(current_task_id)
        # Increment the task id variable for the next task that will be added.
        self.next_id += 1
        return (True, current_task_id)

    def complete_task(self, task_id):
        # Usage: Mark a task as complete.
        # How it does its job: Complete a task by adding a task id to the completed task set 
        #   and then pushing the task id onto self.undo_stack stack. It also removes the task id from 
        #   the backlog queue if the task was in the backlog.
        # 
        if task_id in self.tasks:
            self.completed_tasks.add(task_id)
            self.undo_stack.append(task_id)
            # Clears the current task variable if the task id being passed in matches the task id that is currently being worked on
            if self.current_task == task_id:
                self.current_task = None
            # Removes the task id from the backlog, if the task id was in the backlog to reflect that the task is now completed
            if task_id in self.backlog:
                self.backlog.remove(task_id)
            return (True, task_id)
        else:
            return (False, None)
        
    
    def undo(self):
        # Usage: Undo the last completed task.
        # How it does its job: Performs an undo on the last completed task by popping the last item on the undo stack.
        #   Also removes the task id from the completed tasks set and adds the task to the back of the backlog.
        # 
        # Checks to see if the undo stack is not empty
        if len(self.undo_stack) > 0:
            # Undos the last completed task by popping the task id from the undo stack
            # and also removing the task id from completed_tasks. completed_tasks is a set.
            undo_task_id = self.undo_stack.pop()
            self.completed_tasks.remove(undo_task_id)
            # Add the task id to the back of the backlog so it can be completed again. 
            self.backlog.append(undo_task_id) 
            return (True, undo_task_id)
        else:
            return (False, None)

    
    def process_next(self):
        # Usage: Process the next task from the backlog queue.
        # How it does its job: It pops the oldest task id in the backlog queue and assigns the task id to the current_task variable.
        # 
        # Check to see if there is already a current task being worked on, if there is, return busy
        if self.current_task is not None:
            return ("busy", self.current_task)
        if len(self.backlog) > 0:
            # Remove the oldest task id from the backlog
            current_task_id = self.backlog.popleft()
            # Assign the task id that was popped off to the current_task variable
            self.current_task = current_task_id
            return ("success", current_task_id)
        else:
            return ("empty", None)

    def show(self):
        # Usage: Show all tasks. Grouped by Status: Backlog, In Progress, Completed.
        # How it does its job: Three loops to check, iterate and print the task ids and their descriptions for 
        #   the backlog queue, current_task and completed_task data structures.
        #
        # Show all tasks by looping through each of the main three groups.

        # Backlog - All tasks that are added but not in progress and not completed yet.
        print("\nBacklog:")
        if len(self.backlog) == 0:
            print("(None)")
        else:
            for task_id in self.backlog:
                print(f"  {task_id}: {self.tasks[task_id]}")

        # In Progress/Current task - The task that is in progress/currently being worked on.
        print("\nIn Progress:")
        if self.current_task is not None:
            print(f"  {self.current_task}: {self.tasks[self.current_task]}")
        else:
            print("(None)")
        
        # Completed tasks - All the tasks that have been completed.
        print("\nCompleted tasks")
        completed_tasks_found = False
        for task_id in self.completed_tasks:
            # Completed Tasks
            print(f"  {task_id}: {self.tasks[task_id]}")
            completed_tasks_found = True
        if not completed_tasks_found:
            print("(None)")

    def follow(self, suggested_tasks):
        # Usage: Reorders and creates a new backlog by following a lists of task ids as the new priority order. 
        # How it does its job: The suggested tasks will be in the format example: [3, 1, 2]
        #   reorder() will then take in the task ids and recreate the new reordered linked list 
        #   which will then be converted it to a list and then casted to a deque object and set as the new backlog.
        #
        if not suggested_tasks:
            return ("error", None)
        # Rebuild the linked list order
        self.priority_list.reorder(suggested_tasks)
        # Convert the linked list into a regular list
        reordered_task_list = self.priority_list.to_list()
        # Set the new priority list as the backlog. Since backlog is a queue, we will need to cast it to a deque object
        self.backlog = deque(reordered_task_list)