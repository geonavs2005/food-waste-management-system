"""
Binary Search Tree (BST) Implementation
Academic DSA Project - Food Waste Management System

Demonstrates:
- BSTNode (key, data, left, right)
- BinarySearchTree (insert, search, delete, min/max, in/pre/postorder traversals)
- Application: Fast Food Item Indexing & Searching by ID / Quantity
- Time Complexities:
    * Search (Average): O(log n)
    * Search (Worst case): O(n)
    * Insert (Average): O(log n)
    * Inorder Traversal (Produces sorted order): O(n)
"""

class BSTNode:
    """Node in a Binary Search Tree."""
    def __init__(self, key, data=None):
        self.key = key          # Numeric or sortable key (e.g. food_id or quantity)
        self.data = data or {}  # Associated record
        self.left = None        # Left child (keys < self.key)
        self.right = None       # Right child (keys > self.key)

    def to_dict(self):
        """Hierarchical dictionary format for frontend tree canvas rendering."""
        return {
            'key': self.key,
            'label': f"{self.key}: {self.data.get('food_name', '')}" if self.data else str(self.key),
            'data': self.data,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None
        }


class BinarySearchTree:
    """
    Custom Binary Search Tree adhering to the BST property:
    Left subtree keys < Node key < Right subtree keys
    """
    def __init__(self):
        self.root = None
        self.count = 0

    def insert(self, key, data=None):
        """
        Inserts a key-data pair into the BST following standard BST rules.
        Time: O(log n) average, O(n) worst case.
        """
        if self.root is None:
            self.root = BSTNode(key, data)
            self.count += 1
            return self.root

        curr = self.root
        while True:
            if key < curr.key:
                if curr.left is None:
                    curr.left = BSTNode(key, data)
                    self.count += 1
                    return curr.left
                curr = curr.left
            elif key > curr.key:
                if curr.right is None:
                    curr.right = BSTNode(key, data)
                    self.count += 1
                    return curr.right
                curr = curr.right
            else:
                # Key already exists, update data
                curr.data = data or curr.data
                return curr

    def search(self, key):
        """
        Searches for a key in the BST.
        Returns: (found_node, comparisons_count, path_visited)
        Time: O(log n) average, O(n) worst case.
        """
        comparisons = 0
        path = []
        curr = self.root

        while curr:
            comparisons += 1
            path.append(curr.key)
            if key == curr.key:
                return curr, comparisons, path
            elif key < curr.key:
                curr = curr.left
            else:
                curr = curr.right

        return None, comparisons, path

    def inorder(self, node=None, is_root=True):
        """
        Inorder traversal (Left, Root, Right) yielding naturally SORTED order.
        Time: O(n)
        """
        if is_root:
            node = self.root
        if not node:
            return []
        res = []
        if node.left:
            res.extend(self.inorder(node.left, False))
        res.append({
            'key': node.key,
            'label': node.data.get('food_name', str(node.key)),
            'data': node.data
        })
        if node.right:
            res.extend(self.inorder(node.right, False))
        return res

    def preorder(self, node=None, is_root=True):
        """
        Preorder traversal (Root, Left, Right). Useful for tree cloning / serialization.
        Time: O(n)
        """
        if is_root:
            node = self.root
        if not node:
            return []
        res = [{
            'key': node.key,
            'label': node.data.get('food_name', str(node.key)),
            'data': node.data
        }]
        if node.left:
            res.extend(self.preorder(node.left, False))
        if node.right:
            res.extend(self.preorder(node.right, False))
        return res

    def postorder(self, node=None, is_root=True):
        """
        Postorder traversal (Left, Right, Root). Useful for deletion / bottom-up processing.
        Time: O(n)
        """
        if is_root:
            node = self.root
        if not node:
            return []
        res = []
        if node.left:
            res.extend(self.postorder(node.left, False))
        if node.right:
            res.extend(self.postorder(node.right, False))
        res.append({
            'key': node.key,
            'label': node.data.get('food_name', str(node.key)),
            'data': node.data
        })
        return res

    def min_node(self, node=None):
        """Finds minimum key node in BST."""
        curr = node if node else self.root
        if not curr:
            return None
        while curr.left:
            curr = curr.left
        return curr

    def max_node(self, node=None):
        """Finds maximum key node in BST."""
        curr = node if node else self.root
        if not curr:
            return None
        while curr.right:
            curr = curr.right
        return curr

    def to_tree_dict(self):
        """Returns JSON-serializable tree for rendering."""
        return self.root.to_dict() if self.root else None
