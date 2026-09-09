"""
Binary Tree Implementation
Academic DSA Project - Food Waste Management System

Demonstrates:
- TreeNode (val, left, right)
- BinaryTree (root, level-order insertion)
- Recursive Traversals: Inorder (L-Root-R), Preorder (Root-L-R), Postorder (L-R-Root)
- Depth / Height computation
- Time Complexities:
    * Traversal: O(n)
    * Insertion (Level Order): O(n)
"""

class TreeNode:
    """Node in a Binary Tree."""
    def __init__(self, val, label=""):
        self.val = val
        self.label = label or str(val)
        self.left = None
        self.right = None

    def to_dict(self):
        """Converts subtree to a hierarchical dictionary for visualization."""
        return {
            'val': self.val,
            'label': self.label,
            'left': self.left.to_dict() if self.left else None,
            'right': self.right.to_dict() if self.right else None
        }


class BinaryTree:
    """General Binary Tree with level order insertion and standard traversals."""
    def __init__(self):
        self.root = None

    def insert_level_order(self, val, label=""):
        """
        Inserts value at the first available position in level order.
        Uses a custom FIFO Queue approach for level traversal.
        """
        new_node = TreeNode(val, label)
        if not self.root:
            self.root = new_node
            return new_node

        # Custom queue representation using list iteration
        queue = [self.root]
        while queue:
            curr = queue.pop(0)
            if not curr.left:
                curr.left = new_node
                break
            else:
                queue.append(curr.left)

            if not curr.right:
                curr.right = new_node
                break
            else:
                queue.append(curr.right)
        return new_node

    def inorder(self, node=None, is_root=True):
        """Inorder Traversal: Left -> Root -> Right"""
        if is_root:
            node = self.root
        if not node:
            return []
        res = []
        if node.left:
            res.extend(self.inorder(node.left, False))
        res.append(node.label)
        if node.right:
            res.extend(self.inorder(node.right, False))
        return res

    def preorder(self, node=None, is_root=True):
        """Preorder Traversal: Root -> Left -> Right"""
        if is_root:
            node = self.root
        if not node:
            return []
        res = [node.label]
        if node.left:
            res.extend(self.preorder(node.left, False))
        if node.right:
            res.extend(self.preorder(node.right, False))
        return res

    def postorder(self, node=None, is_root=True):
        """Postorder Traversal: Left -> Right -> Root"""
        if is_root:
            node = self.root
        if not node:
            return []
        res = []
        if node.left:
            res.extend(self.postorder(node.left, False))
        if node.right:
            res.extend(self.postorder(node.right, False))
        res.append(node.label)
        return res

    def height(self, node=None, is_root=True):
        """Computes the maximum depth/height of the tree."""
        if is_root:
            node = self.root
        if not node:
            return 0
        left_h = self.height(node.left, False)
        right_h = self.height(node.right, False)
        return 1 + max(left_h, right_h)
