from flask import Blueprint, render_template, request, jsonify
from models.food import Food
from models.donor import Donor
from dsa.linked_list import FoodLinkedList
from dsa.stack import global_operations_stack
from dsa.searching import linear_search, binary_search
from dsa.sorting import merge_sort

food_bp = Blueprint('food_bp', __name__)

@food_bp.route('/food')
def food_page():
    foods = Food.get_all()
    donors = Donor.get_all()
    
    # Load into custom FoodLinkedList for viva demonstration
    ll = FoodLinkedList()
    ll.build_from_records(foods)
    visual_chain = ll.to_visual_list()
    
    return render_template('food.html', foods=foods, donors=donors, visual_chain=visual_chain, list_size=ll.size)

@food_bp.route('/api/food', methods=['GET'])
def get_all_food():
    foods = Food.get_all()
    ll = FoodLinkedList().build_from_records(foods)
    return jsonify({
        'status': 'success',
        'count': len(foods),
        'data': foods,
        'linked_list_visual': ll.to_visual_list()
    })

@food_bp.route('/api/food', methods=['POST'])
def add_food():
    data = request.get_json(silent=True) or request.form
    donor_id = data.get('donor_id')
    food_name = data.get('food_name', '').strip()
    category = data.get('category', '').strip()
    quantity = data.get('quantity')
    expiry_date = data.get('expiry_date')
    location = data.get('location', '').strip()
    status = data.get('status', 'Available')

    if not food_name or not quantity or not expiry_date:
        return jsonify({'status': 'error', 'message': 'Food name, quantity, and expiry date are required!'}), 400

    try:
        quantity = int(quantity)
        if quantity <= 0:
            return jsonify({'status': 'error', 'message': 'Quantity must be greater than 0!'}), 400
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Quantity must be a valid integer!'}), 400

    new_id = Food.create(donor_id, food_name, category, quantity, expiry_date, location, status)
    
    # Record in Stack
    global_operations_stack.push(
        action_type='ADD_FOOD',
        details=f"Added '{food_name}' ({quantity} packets) under category '{category}'",
        undo_data={'action': 'DELETE_FOOD', 'food_id': new_id}
    )

    return jsonify({
        'status': 'success',
        'message': f"Food '{food_name}' added successfully!",
        'food_id': new_id
    })

@food_bp.route('/api/food/<int:food_id>', methods=['PUT'])
def update_food(food_id):
    data = request.get_json(silent=True) or request.form
    existing = Food.get_by_id(food_id)
    if not existing:
        return jsonify({'status': 'error', 'message': 'Food item not found!'}), 404

    donor_id = data.get('donor_id', existing.get('donor_id'))
    food_name = data.get('food_name', existing.get('food_name')).strip()
    category = data.get('category', existing.get('category')).strip()
    quantity = int(data.get('quantity', existing.get('quantity')))
    expiry_date = data.get('expiry_date', existing.get('expiry_date'))
    location = data.get('location', existing.get('location')).strip()
    status = data.get('status', existing.get('status'))

    Food.update(food_id, donor_id, food_name, category, quantity, expiry_date, location, status)
    
    # Record in Stack
    global_operations_stack.push(
        action_type='UPDATE_FOOD',
        details=f"Updated Food #{food_id} '{food_name}'",
        undo_data={'action': 'RESTORE_FOOD', 'previous_state': existing}
    )

    return jsonify({'status': 'success', 'message': f"Food #{food_id} updated successfully!"})

@food_bp.route('/api/food/<int:food_id>', methods=['DELETE'])
def delete_food(food_id):
    existing = Food.get_by_id(food_id)
    if not existing:
        return jsonify({'status': 'error', 'message': 'Food item not found!'}), 404

    Food.delete(food_id)
    
    # Record in Stack for Undo
    global_operations_stack.push(
        action_type='DELETE_FOOD',
        details=f"Deleted Food #{food_id} '{existing.get('food_name')}'",
        undo_data={'action': 'RECREATE_FOOD', 'record': existing}
    )

    return jsonify({'status': 'success', 'message': f"Food #{food_id} deleted successfully!"})

@food_bp.route('/api/food/linked_list/traverse', methods=['GET'])
def traverse_linked_list():
    foods = Food.get_all()
    ll = FoodLinkedList().build_from_records(foods)
    return jsonify({
        'status': 'success',
        'algorithm': 'Custom Singly Linked List Traversal',
        'time_complexity': 'O(n)',
        'size': ll.size,
        'chain': ll.to_visual_list(),
        'elements': ll.traverse()
    })
