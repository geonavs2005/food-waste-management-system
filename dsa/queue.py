"""
Queue Implementation using Linked List (FIFO - First In First Out)
Academic DSA Project - Food Waste Management System

Demonstrates:
- QueueNode (data, next pointer)
- RequestQueue (front pointer, rear pointer, size tracking)
- Operations: enqueue, dequeue, peek, is_empty, to_list
- Application: Recipient Food Request Processing in Strict Arrival Order
- Time Complexities:
    * Enqueue: O(1)
    * Dequeue: O(1)
    * Peek: O(1)
    * Is Empty: O(1)
"""

class QueueNode:
    """Node representing an item waiting in the Queue."""
    def __init__(self, data):
        self.data = data   # Request record dictionary
        self.next = None   # Pointer to the next node in queue

    def to_dict(self):
        return {
            'data': self.data,
            'next_id': self.next.data.get('request_id') if self.next else None
        }


class RequestQueue:
    """
    Custom FIFO Queue using Linked List with front and rear pointers.
    Guarantees O(1) Enqueue at rear and O(1) Dequeue at front.
    """
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def enqueue(self, data):
        """
        Inserts a request at the rear (tail) of the queue.
        Time: O(1)
        """
        new_node = QueueNode(data)
        if self.is_empty():
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node
        self.size += 1
        return new_node

    def dequeue(self):
        """
        Removes and returns the request at the front (head) of the queue.
        Returns None if queue is empty.
        Time: O(1)
        """
        if self.is_empty():
            return None
        
        dequeued_node = self.front
        self.front = self.front.next
        self.size -= 1
        
        # If queue became empty after removal
        if self.front is None:
            self.rear = None
            
        return dequeued_node.data

    def peek(self):
        """
        Returns the front item without removing it.
        Time: O(1)
        """
        if self.is_empty():
            return None
        return self.front.data

    def is_empty(self):
        """Checks if the queue is empty. Time: O(1)"""
        return self.front is None

    def to_list(self):
        """
        Returns all queued items in arrival order from Front to Rear.
        Time: O(n)
        """
        items = []
        curr = self.front
        pos = 1
        while curr:
            item = dict(curr.data)
            item['queue_position'] = pos
            items.append(item)
            curr = curr.next
            pos += 1
        return items

    def build_from_records(self, records):
        """Builds the queue state from database records."""
        self.front = None
        self.rear = None
        self.size = 0
        for r in records:
            self.enqueue(r)
        return self
