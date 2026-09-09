"""
Comprehensive End-to-End Workflow Verification Script
Simulates full user journey through Flask test client.
"""
import json
from app import create_app

def run_e2e_verification():
    app = create_app()
    client = app.test_client()
    print("\n--- [1] Testing Page Renders ---")
    pages = [
        ('/', 'System Dashboard'),
        ('/food', 'Food Inventory'),
        ('/donors', 'Donors Management'),
        ('/recipients', 'Recipients & Shelters Management'),
        ('/requests', 'Request Management & FIFO Queue'),
        ('/locations', 'Location Network & Graph Algorithms'),
        ('/algorithms', 'Algorithm Optimizer'),
        ('/dsa-visualizer', '11-in-1 DSA Visualizer')
    ]
    for url, title in pages:
        res = client.get(url)
        assert res.status_code == 200, f"Failed loading {url}"
        assert title in res.text, f"Title {title} not found in {url}"
        print(f"  [OK] {url} loaded successfully (Status 200)")

    print("\n--- [2] Testing CRUD & Linked List ---")
    # Add Donor
    donor_res = client.post('/api/donors', json={
        'name': 'Master Chef Ananya',
        'organization': 'Royal Palms Hotel',
        'contact': '+91 99999 11111',
        'location': 'Anna Nagar Food Bank'
    })
    assert donor_res.status_code == 200
    donor_id = json.loads(donor_res.data)['donor_id']
    print(f"  [OK] Registered Donor #{donor_id}")

    # Add Food (Linked list insertion)
    food_res = client.post('/api/food', json={
        'food_name': 'Paneer Pulao & Raita',
        'category': 'Meals',
        'quantity': 55,
        'expiry_date': '2026-09-10',
        'donor_id': donor_id,
        'location': 'Anna Nagar Food Bank'
    })
    assert food_res.status_code == 200
    food_id = json.loads(food_res.data)['food_id']
    print(f"  [OK] Inserted Food item #{food_id} into Linked List & DB")

    # Traverse Linked List
    ll_res = client.get('/api/food/linked_list/traverse')
    assert ll_res.status_code == 200
    ll_data = json.loads(ll_res.data)
    print(f"  [OK] Linked List Traversal verified: {ll_data['size']} nodes in chain")

    print("\n--- [3] Testing FIFO Queue Processing ---")
    # Enqueue request
    req_res = client.post('/api/requests', json={
        'recipient_id': 1,
        'food_category': 'Meals',
        'quantity_requested': 30,
        'priority': 9
    })
    assert req_res.status_code == 200
    req_id = json.loads(req_res.data)['request_id']
    print(f"  [OK] Enqueued Request #{req_id} at Queue Rear")

    # Dequeue front request (FIFO)
    dequeue_res = client.post('/api/requests/process')
    assert dequeue_res.status_code == 200
    dq_data = json.loads(dequeue_res.data)
    print(f"  [OK] FIFO Dequeue processed: Request #{dq_data['processed_item']['request_id']}")

    print("\n--- [4] Testing LIFO Stack Undo ---")
    undo_res = client.post('/api/stack/undo')
    assert undo_res.status_code == 200
    undo_data = json.loads(undo_res.data)
    print(f"  [OK] Stack Undo executed: {undo_data['message']}")

    print("\n--- [5] Testing Searching Algorithms ---")
    # Linear Search
    lin_res = client.post('/api/search/linear', json={'field': 'food_name', 'target': 'Biryani'})
    assert lin_res.status_code == 200
    lin_data = json.loads(lin_res.data)['result']
    print(f"  [OK] Linear Search for 'Biryani': {lin_data['comparisons_count']} comparison(s) -> Found: {lin_data['found']}")

    # Binary Search
    bin_res = client.post('/api/search/binary', json={'field': 'quantity', 'target': 45})
    assert bin_res.status_code == 200
    bin_data = json.loads(bin_res.data)['result']
    print(f"  [OK] Binary Search for Quantity 45: {bin_data['comparisons_count']} comparison(s) -> Found: {bin_data['found']}")

    print("\n--- [6] Testing Sorting Algorithms ---")
    sort_res = client.post('/api/sort', json={'algorithm': 'merge', 'field': 'quantity', 'reverse': False})
    assert sort_res.status_code == 200
    sort_data = json.loads(sort_res.data)['result']
    print(f"  [OK] Merge Sort on Quantity: {sort_data['comparisons_count']} comparisons (Time: {sort_data['time_complexity']})")

    print("\n--- [7] Testing Graph Traversals (BFS & DFS) ---")
    bfs_res = client.post('/api/graph/bfs', json={'start_node': 'Central Kitchen Hub'})
    assert bfs_res.status_code == 200
    bfs_data = json.loads(bfs_res.data)['result']
    print(f"  [OK] BFS Traversal Order: {' -> '.join(bfs_data['traversal_order'])}")

    dfs_res = client.post('/api/graph/dfs', json={'start_node': 'Central Kitchen Hub'})
    assert dfs_res.status_code == 200
    dfs_data = json.loads(dfs_res.data)['result']
    print(f"  [OK] DFS Traversal Order: {' -> '.join(dfs_data['traversal_order'])}")

    print("\n--- [8] Testing Greedy Food Distribution ---")
    greedy_res = client.post('/api/algorithms/greedy', json={'available_food': 100, 'heuristic': 'priority'})
    assert greedy_res.status_code == 200
    g_data = json.loads(greedy_res.data)['result']
    print(f"  [OK] Greedy Allocated: {g_data['food_allocated']} pkts, Priority Score: {g_data['total_priority_satisfied']}")

    print("\n--- [9] Testing Dynamic Programming (0/1 Knapsack) ---")
    dp_res = client.post('/api/algorithms/dp', json={'capacity': 100})
    assert dp_res.status_code == 200
    dp_data = json.loads(dp_res.data)['result']
    print(f"  [OK] DP 0/1 Knapsack Max Benefit: {dp_data['max_benefit']}, Utilized: {dp_data['total_food_used']} / {dp_data['capacity']}")

    print("\n--- [10] Testing Backtracking Assignment ---")
    bt_res = client.post('/api/algorithms/backtracking', json={})
    assert bt_res.status_code == 200
    bt_data = json.loads(bt_res.data)['result']
    print(f"  [OK] Backtracking Solver: Success = {bt_data['success']}, Total Backtracks = {bt_data['total_backtracks']}")

    print("\n=======================================================")
    print(" ALL 10 DSA WORKFLOW INTEGRATION TESTS PASSED 100%!")
    print("=======================================================\n")

if __name__ == '__main__':
    run_e2e_verification()
