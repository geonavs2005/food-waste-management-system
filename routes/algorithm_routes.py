from flask import Blueprint, render_template, request, jsonify
from models.food import Food
from models.donor import Donor
from models.recipient import Recipient
from models.request import FoodRequest
from dsa.searching import linear_search, binary_search
from dsa.sorting import merge_sort, quick_sort, bubble_sort
from dsa.greedy import greedy_food_distribution
from dsa.dynamic_programming import dp_knapsack_food_allocation
from dsa.backtracking import backtracking_donor_assignment
from dsa.bst import BinarySearchTree
from dsa.binary_tree import BinaryTree
from dsa.stack import global_operations_stack

algorithm_bp = Blueprint('algorithm_bp', __name__)

# Global interactive BST instance for live visualization demo
global_demo_bst = BinarySearchTree()
# Global interactive Binary Tree instance
global_demo_btree = BinaryTree()

def _init_demo_trees():
    global global_demo_bst, global_demo_btree
    if global_demo_bst.root is None:
        foods = Food.get_all()
        for f in foods[:7]:
            global_demo_bst.insert(int(f.get('quantity', 50)), f)
    if global_demo_btree.root is None:
        for val in [50, 30, 70, 20, 40, 60, 80]:
            global_demo_btree.insert_level_order(val)

@algorithm_bp.route('/algorithms')
def algorithms_page():
    foods = Food.get_all()
    requests_data = FoodRequest.get_all()
    donors = Donor.get_all()
    return render_template('algorithms.html', foods=foods, requests=requests_data, donors=donors)

@algorithm_bp.route('/dsa-visualizer')
def dsa_visualizer_page():
    _init_demo_trees()
    foods = Food.get_all()
    requests_data = FoodRequest.get_all()
    donors = Donor.get_all()
    
    return render_template('dsa_visualizer.html', 
                           foods=foods, 
                           requests=requests_data, 
                           donors=donors,
                           stack_items=global_operations_stack.to_list())

# ----------------- Searching Endpoints -----------------
@algorithm_bp.route('/api/search/linear', methods=['POST'])
def run_linear_search():
    data = request.get_json(silent=True) or {}
    key_field = data.get('field', 'food_name')
    target = data.get('target', '')
    
    foods = Food.get_all()
    result = linear_search(foods, key_field, target)
    return jsonify({'status': 'success', 'result': result})

@algorithm_bp.route('/api/search/binary', methods=['POST'])
def run_binary_search():
    data = request.get_json(silent=True) or {}
    key_field = data.get('field', 'quantity')
    target = data.get('target', 0)
    
    foods = Food.get_all()
    # Step 1: Pre-sort the array using our custom Merge Sort
    sort_res = merge_sort(foods, key_field=key_field, reverse=False)
    sorted_foods = sort_res['sorted_data']
    
    # Step 2: Conduct Binary Search
    result = binary_search(sorted_foods, key_field, target)
    result['sorted_data_used'] = sorted_foods
    return jsonify({'status': 'success', 'result': result})

# ----------------- Sorting Endpoints -----------------
@algorithm_bp.route('/api/sort', methods=['POST'])
def run_sorting():
    data = request.get_json(silent=True) or {}
    algo = data.get('algorithm', 'merge').lower()
    key_field = data.get('field', 'quantity')
    reverse = bool(data.get('reverse', False))
    
    foods = Food.get_all()
    
    if algo == 'quick':
        result = quick_sort(foods, key_field=key_field, reverse=reverse)
    elif algo == 'bubble':
        result = bubble_sort(foods, key_field=key_field, reverse=reverse)
    else:
        result = merge_sort(foods, key_field=key_field, reverse=reverse)
        
    return jsonify({'status': 'success', 'result': result})

# ----------------- Greedy Distribution -----------------
@algorithm_bp.route('/api/algorithms/greedy', methods=['POST'])
def run_greedy():
    data = request.get_json(silent=True) or {}
    available_food = int(data.get('available_food', 120))
    heuristic = data.get('heuristic', 'priority')
    
    requests_data = FoodRequest.get_all(status_filter='Pending')
    if not requests_data:
        requests_data = FoodRequest.get_all()
        
    result = greedy_food_distribution(available_food, requests_data, heuristic=heuristic)
    return jsonify({'status': 'success', 'result': result})

# ----------------- Dynamic Programming -----------------
@algorithm_bp.route('/api/algorithms/dp', methods=['POST'])
def run_dp():
    data = request.get_json(silent=True) or {}
    capacity = int(data.get('capacity', 100))
    
    requests_data = FoodRequest.get_all(status_filter='Pending')
    if not requests_data:
        requests_data = FoodRequest.get_all()
        
    result = dp_knapsack_food_allocation(capacity, requests_data)
    return jsonify({'status': 'success', 'result': result})

# ----------------- Backtracking -----------------
@algorithm_bp.route('/api/algorithms/backtracking', methods=['POST'])
def run_backtracking():
    data = request.get_json(silent=True) or {}
    donors_input = data.get('donors')
    centers_input = data.get('centers')
    
    if not donors_input:
        donors_input = [
            {'donor_id': 1, 'name': 'Annapoorna Kitchen', 'quantity': 45},
            {'donor_id': 2, 'name': 'Green Bakery', 'quantity': 30},
            {'donor_id': 3, 'name': 'Taj Banquet', 'quantity': 60},
            {'donor_id': 4, 'name': 'SRM Cafeteria', 'quantity': 35}
        ]
        
    if not centers_input:
        centers_input = [
            {'name': 'Anna Nagar Food Bank', 'capacity': 90},
            {'name': 'T Nagar Community Hub', 'capacity': 80}
        ]
        
    result = backtracking_donor_assignment(donors_input, centers_input)
    return jsonify({'status': 'success', 'result': result})

# ----------------- BST Visualizer Endpoints -----------------
@algorithm_bp.route('/api/bst/insert', methods=['POST'])
def bst_insert():
    data = request.get_json(silent=True) or {}
    try:
        val = int(data.get('value'))
        label = data.get('label', '')
        global_demo_bst.insert(val, {'food_name': label or f"Item (Key: {val})", 'quantity': val})
        return jsonify({
            'status': 'success',
            'tree': global_demo_bst.to_tree_dict(),
            'count': global_demo_bst.count
        })
    except (ValueError, TypeError):
        return jsonify({'status': 'error', 'message': 'Value must be an integer!'}), 400

@algorithm_bp.route('/api/bst/search', methods=['POST'])
def bst_search():
    data = request.get_json() or {}
    try:
        val = int(data.get('value'))
        node, comparisons, path = global_demo_bst.search(val)
        return jsonify({
            'status': 'success',
            'found': node is not None,
            'comparisons': comparisons,
            'path': path,
            'node_data': node.data if node else None
        })
    except (ValueError, TypeError):
        return jsonify({'status': 'error', 'message': 'Value must be an integer!'}), 400

@algorithm_bp.route('/api/bst/traverse', methods=['GET'])
def bst_traverse():
    return jsonify({
        'status': 'success',
        'inorder': global_demo_bst.inorder(),
        'preorder': global_demo_bst.preorder(),
        'postorder': global_demo_bst.postorder(),
        'tree': global_demo_bst.to_tree_dict()
    })

@algorithm_bp.route('/api/bst/reset', methods=['POST'])
def bst_reset():
    global global_demo_bst
    global_demo_bst = BinarySearchTree()
    for val in [50, 20, 80, 10, 30, 60, 100]:
        global_demo_bst.insert(val, {'food_name': f"Food Packet #{val}", 'quantity': val})
    return jsonify({'status': 'success', 'tree': global_demo_bst.to_tree_dict()})

# ----------------- Stack Endpoints -----------------
@algorithm_bp.route('/api/stack', methods=['GET'])
def get_stack():
    return jsonify({
        'status': 'success',
        'size': global_operations_stack.size,
        'is_empty': global_operations_stack.is_empty(),
        'top': global_operations_stack.peek().to_dict() if global_operations_stack.peek() else None,
        'items': global_operations_stack.to_list()
    })

@algorithm_bp.route('/api/stack/undo', methods=['POST'])
def stack_undo():
    """
    Pops top operation and performs Undo logic.
    Demonstrates LIFO Stack property in real web actions.
    """
    if global_operations_stack.is_empty():
        return jsonify({'status': 'error', 'message': 'Stack Underflow: No operations to undo!'}), 400

    popped = global_operations_stack.pop()
    undo_data = popped.undo_data
    
    # Handle undo logic if applicable
    if undo_data:
        action = undo_data.get('action')
        if action == 'DELETE_FOOD' and 'food_id' in undo_data:
            Food.delete(undo_data['food_id'])
        elif action == 'REVERT_REQUEST_STATUS' and 'request_id' in undo_data:
            FoodRequest.update_status(undo_data['request_id'], 'Pending')
        elif action == 'RECREATE_FOOD' and 'record' in undo_data:
            r = undo_data['record']
            Food.create(r.get('donor_id'), r.get('food_name'), r.get('category'), 
                        r.get('quantity'), r.get('expiry_date'), r.get('location'), r.get('status', 'Available'))

    return jsonify({
        'status': 'success',
        'message': f"Undid operation: {popped.details} (LIFO Pop)",
        'undone_operation': popped.to_dict(),
        'remaining_stack_size': global_operations_stack.size
    })
