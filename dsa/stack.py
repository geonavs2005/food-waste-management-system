"""
Stack Implementation using Linked List (LIFO - Last In First Out)
Academic DSA Project - Food Waste Management System

Demonstrates:
- StackNode (data, next pointer)
- OperationsStack (top pointer, size tracking)
- Operations: push, pop, peek, is_empty, to_list
- Application: Action History & Undo Demonstration for Food Management
- Time Complexities:
    * Push: O(1)
    * Pop: O(1)
    * Peek: O(1)
    * Is Empty: O(1)
"""
import datetime

class StackNode:
    """Node representing an action record in the Stack."""
    def __init__(self, action_type, details, undo_data=None):
        self.action_type = action_type  # e.g., 'ADD_FOOD', 'DELETE_FOOD', 'PROCESS_REQUEST'
        self.details = details          # Description string
        self.undo_data = undo_data      # Dict required to reverse/undo the operation
        self.timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        self.next = None                # Pointer to node underneath

    def to_dict(self):
        return {
            'action_type': self.action_type,
            'details': self.details,
            'undo_data': self.undo_data,
            'timestamp': self.timestamp
        }


class OperationsStack:
    """
    Custom Stack using Singly Linked List nodes.
    Maintains LIFO order for all operational activities.
    """
    def __init__(self, max_capacity=50):
        self.top = None
        self.size = 0
        self.max_capacity = max_capacity

    def push(self, action_type, details, undo_data=None):
        """
        Pushes a new operation onto the top of the stack.
        Time: O(1)
        """
        new_node = StackNode(action_type, details, undo_data)
        new_node.next = self.top
        self.top = new_node
        self.size += 1
        return new_node

    def pop(self):
        """
        Removes and returns the top operation from the stack.
        Returns None if stack is empty underflow.
        Time: O(1)
        """
        if self.is_empty():
            return None
        popped_node = self.top
        self.top = self.top.next
        self.size -= 1
        return popped_node

    def peek(self):
        """
        Returns the top operation without removing it.
        Time: O(1)
        """
        if self.is_empty():
            return None
        return self.top

    def is_empty(self):
        """Checks if the stack contains zero elements. Time: O(1)"""
        return self.top is None

    def to_list(self):
        """
        Traverses the stack from TOP to BOTTOM.
        Time: O(n)
        """
        items = []
        curr = self.top
        while curr:
            items.append(curr.to_dict())
            curr = curr.next
        return items

# Global in-memory stack instance for active session history
global_operations_stack = OperationsStack()
