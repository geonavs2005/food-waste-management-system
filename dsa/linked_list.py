"""
Linked List Implementation for Food Inventory Management
Academic DSA Project - Food Waste Management System

Demonstrates:
- FoodNode (data, next pointer)
- FoodLinkedList (head pointer, tail tracking, size)
- Operations: insert_head, insert_tail, delete, search, traverse
- Time Complexities:
    * Insert at Head: O(1)
    * Insert at Tail: O(1) (with tail pointer) or O(n)
    * Delete: O(n)
    * Search: O(n)
    * Traversal: O(n)
"""

class FoodNode:
    """
    Node representing an individual Food Item in the Singly Linked List.
    Holds food data dictionary and a pointer to the next node.
    """
    def __init__(self, data):
        self.data = data       # Dict containing food item properties
        self.next = None       # Pointer to next FoodNode in the sequence

    def to_dict(self):
        return {
            'data': self.data,
            'next_id': self.next.data.get('food_id') if self.next else None
        }


class FoodLinkedList:
    """
    Custom Singly Linked List for managing surplus food records.
    Does NOT use Python's built-in list operations for core logic.
    """
    def __init__(self):
        self.head = None
        self.size = 0

    def insert_head(self, data):
        """Inserts a new food item at the beginning of the list. Time: O(1)"""
        new_node = FoodNode(data)
        new_node.next = self.head
        self.head = new_node
        self.size += 1
        return new_node

    def insert_tail(self, data):
        """Inserts a new food item at the end of the list. Time: O(n)"""
        new_node = FoodNode(data)
        if not self.head:
            self.head = new_node
            self.size += 1
            return new_node
        
        curr = self.head
        while curr.next:
            curr = curr.next
        curr.next = new_node
        self.size += 1
        return new_node

    def delete_by_id(self, food_id):
        """
        Deletes a food node by food_id.
        Returns the deleted item dict if found, else None.
        Time: O(n)
        """
        if not self.head:
            return None
        
        # If head holds the item to delete
        if str(self.head.data.get('food_id')) == str(food_id):
            deleted = self.head.data
            self.head = self.head.next
            self.size -= 1
            return deleted

        curr = self.head
        while curr.next and str(curr.next.data.get('food_id')) != str(food_id):
            curr = curr.next

        if curr.next:
            deleted = curr.next.data
            curr.next = curr.next.next
            self.size -= 1
            return deleted
        return None

    def search_by_name(self, food_name):
        """
        Searches linearly through nodes matching substring of food_name.
        Returns list of matching data items and comparison count.
        Time: O(n)
        """
        matches = []
        comparisons = 0
        curr = self.head
        query_lower = food_name.strip().lower()

        while curr:
            comparisons += 1
            curr_name = str(curr.data.get('food_name', '')).lower()
            if query_lower in curr_name:
                matches.append(curr.data)
            curr = curr.next

        return matches, comparisons

    def search_by_id(self, food_id):
        """
        Finds exact node matching food_id.
        Returns node data and step count.
        """
        comparisons = 0
        curr = self.head
        while curr:
            comparisons += 1
            if str(curr.data.get('food_id')) == str(food_id):
                return curr.data, comparisons
            curr = curr.next
        return None, comparisons

    def traverse(self):
        """
        Traverses the list from head to tail.
        Returns ordered list of dicts.
        Time: O(n)
        """
        records = []
        curr = self.head
        while curr:
            records.append(curr.data)
            curr = curr.next
        return records

    def to_visual_list(self):
        """
        Generates structured node link data for UI diagram rendering.
        Example: [ {id: 1, name: 'Biryani', next: 2}, {id: 2, name: 'Bread', next: null} ]
        """
        chain = []
        curr = self.head
        while curr:
            chain.append({
                'food_id': curr.data.get('food_id'),
                'food_name': curr.data.get('food_name'),
                'category': curr.data.get('category'),
                'quantity': curr.data.get('quantity'),
                'status': curr.data.get('status'),
                'next_id': curr.next.data.get('food_id') if curr.next else None
            })
            curr = curr.next
        return chain

    def build_from_records(self, records):
        """Populates linked list from a database result set."""
        self.head = None
        self.size = 0
        for r in records:
            self.insert_tail(r)
        return self
