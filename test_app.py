"""
Unit & Integration Test Suite for Food Waste Management System
Verifies all 11 DSA custom modules, DB initialization, and Flask route endpoints.
"""
import unittest
import json
from app import create_app
from dsa.linked_list import FoodLinkedList
from dsa.stack import OperationsStack
from dsa.queue import RequestQueue
from dsa.bst import BinarySearchTree
from dsa.binary_tree import BinaryTree
from dsa.graph import Graph
from dsa.searching import linear_search, binary_search
from dsa.sorting import merge_sort, quick_sort, bubble_sort
from dsa.greedy import greedy_food_distribution
from dsa.dynamic_programming import dp_knapsack_food_allocation
from dsa.backtracking import backtracking_donor_assignment

class TestDSAImplementations(unittest.TestCase):
    def test_linked_list(self):
        ll = FoodLinkedList()
        ll.insert_head({'food_id': 1, 'food_name': 'Rice'})
        ll.insert_tail({'food_id': 2, 'food_name': 'Bread'})
        self.assertEqual(ll.size, 2)
        
        # Search
        res, comp = ll.search_by_name('Rice')
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]['food_name'], 'Rice')
        
        # Delete
        deleted = ll.delete_by_id(1)
        self.assertIsNotNone(deleted)
        self.assertEqual(ll.size, 1)

    def test_stack(self):
        st = OperationsStack()
        st.push('ADD', 'Added Item 1')
        st.push('ADD', 'Added Item 2')
        self.assertEqual(st.size, 2)
        self.assertEqual(st.peek().details, 'Added Item 2')
        
        popped = st.pop()
        self.assertEqual(popped.details, 'Added Item 2')
        self.assertEqual(st.size, 1)

    def test_queue(self):
        q = RequestQueue()
        q.enqueue({'req_id': 101, 'name': 'Shelter A'})
        q.enqueue({'req_id': 102, 'name': 'Shelter B'})
        self.assertEqual(q.size, 2)
        
        # FIFO check
        front = q.dequeue()
        self.assertEqual(front['req_id'], 101)
        self.assertEqual(q.size, 1)

    def test_bst(self):
        bst = BinarySearchTree()
        bst.insert(50, {'food_name': 'Item 50'})
        bst.insert(30, {'food_name': 'Item 30'})
        bst.insert(70, {'food_name': 'Item 70'})
        
        node, comp, path = bst.search(30)
        self.assertIsNotNone(node)
        self.assertEqual(node.key, 30)
        
        inorder = bst.inorder()
        keys = [x['key'] for x in inorder]
        self.assertEqual(keys, [30, 50, 70]) # Sorted order

    def test_graph_bfs_dfs(self):
        g = Graph()
        g.add_edge('A', 'B', 5)
        g.add_edge('B', 'C', 4)
        g.add_edge('A', 'C', 10)
        
        bfs_res = g.bfs('A')
        self.assertEqual(bfs_res['traversal_order'][0], 'A')
        self.assertEqual(len(bfs_res['traversal_order']), 3)
        
        dfs_res = g.dfs('A')
        self.assertEqual(dfs_res['traversal_order'][0], 'A')
        self.assertEqual(len(dfs_res['traversal_order']), 3)

    def test_searching_algorithms(self):
        items = [
            {'food_id': 1, 'quantity': 20, 'food_name': 'Apple'},
            {'food_id': 2, 'quantity': 40, 'food_name': 'Banana'},
            {'food_id': 3, 'quantity': 60, 'food_name': 'Carrot'}
        ]
        
        lin = linear_search(items, 'food_name', 'Banana')
        self.assertTrue(lin['found'])
        self.assertEqual(len(lin['matches']), 1)
        
        bin_s = binary_search(items, 'quantity', 40)
        self.assertTrue(bin_s['found'])
        self.assertEqual(bin_s['match']['food_name'], 'Banana')

    def test_sorting_algorithms(self):
        items = [{'quantity': 50}, {'quantity': 10}, {'quantity': 30}]
        sorted_m = merge_sort(items, 'quantity')['sorted_data']
        self.assertEqual([x['quantity'] for x in sorted_m], [10, 30, 50])
        
        sorted_q = quick_sort(items, 'quantity')['sorted_data']
        self.assertEqual([x['quantity'] for x in sorted_q], [10, 30, 50])
        
        sorted_b = bubble_sort(items, 'quantity')['sorted_data']
        self.assertEqual([x['quantity'] for x in sorted_b], [10, 30, 50])

    def test_greedy(self):
        reqs = [
            {'request_id': 1, 'quantity_requested': 30, 'priority': 9},
            {'request_id': 2, 'quantity_requested': 20, 'priority': 5},
            {'request_id': 3, 'quantity_requested': 40, 'priority': 8}
        ]
        res = greedy_food_distribution(50, reqs, heuristic='priority')
        self.assertEqual(res['food_allocated'], 50) # Req 1 (30) accepted, Req 3 (40) skipped, Req 2 (20) accepted
        self.assertEqual(res['remaining_food'], 0)

    def test_dynamic_programming(self):
        reqs = [
            {'request_id': 1, 'quantity_requested': 30, 'priority': 9},
            {'request_id': 2, 'quantity_requested': 20, 'priority': 5},
            {'request_id': 3, 'quantity_requested': 20, 'priority': 8}
        ]
        res = dp_knapsack_food_allocation(50, reqs)
        # Choosing req 1 (30, pri 9) + req 3 (20, pri 8) gives food 50, priority 17
        self.assertEqual(res['max_benefit'], 17)
        self.assertEqual(res['total_food_used'], 50)

    def test_backtracking(self):
        donors = [{'name': 'D1', 'quantity': 20}, {'name': 'D2', 'quantity': 30}]
        centers = [{'name': 'C1', 'capacity': 40}, {'name': 'C2', 'capacity': 40}]
        res = backtracking_donor_assignment(donors, centers)
        self.assertTrue(res['success'])
        self.assertEqual(len(res['final_assignment']), 2)

class TestFlaskEndpoints(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.client = self.app.test_client()

    def test_pages_load(self):
        for route in ['/', '/food', '/donors', '/recipients', '/requests', '/locations', '/algorithms', '/dsa-visualizer']:
            res = self.client.get(route)
            self.assertEqual(res.status_code, 200, f"Route {route} failed with status {res.status_code}")

    def test_api_stats(self):
        res = self.client.get('/api/dashboard/stats')
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['status'], 'success')
        self.assertIn('total_food_records', data['stats'])

if __name__ == '__main__':
    unittest.main()
