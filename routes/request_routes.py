from flask import Blueprint, render_template, request, jsonify
from models.request import FoodRequest
from models.recipient import Recipient
from models.food import Food
from dsa.queue import RequestQueue
from dsa.stack import global_operations_stack

request_bp = Blueprint('request_bp', __name__)

@request_bp.route('/requests')
def requests_page():
    all_requests = FoodRequest.get_all()
    pending_requests = FoodRequest.get_all(status_filter='Pending')
    recipients = Recipient.get_all()
    
    # Custom RequestQueue instance
    rq = RequestQueue().build_from_records(pending_requests)
    queue_list = rq.to_list()
    
    return render_template('requests.html', 
                           all_requests=all_requests, 
                           pending_requests=pending_requests,
                           recipients=recipients,
                           queue_list=queue_list,
                           queue_size=rq.size)

@request_bp.route('/api/requests', methods=['GET'])
def get_requests():
    status_filter = request.args.get('status')
    requests_data = FoodRequest.get_all(status_filter=status_filter)
    rq = RequestQueue().build_from_records(requests_data)
    
    return jsonify({
        'status': 'success',
        'data': requests_data,
        'queue_visual': rq.to_list(),
        'front_item': rq.peek(),
        'queue_size': rq.size
    })

@request_bp.route('/api/requests', methods=['POST'])
def create_request():
    data = request.get_json(silent=True) or request.form
    recipient_id = data.get('recipient_id')
    food_category = data.get('food_category', '').strip()
    quantity_requested = data.get('quantity_requested')
    priority = int(data.get('priority', 5))

    if not recipient_id or not food_category or not quantity_requested:
        return jsonify({'status': 'error', 'message': 'Recipient, category, and quantity are required!'}), 400

    try:
        quantity_requested = int(quantity_requested)
        if quantity_requested <= 0:
            return jsonify({'status': 'error', 'message': 'Requested quantity must be greater than 0!'}), 400
    except ValueError:
        return jsonify({'status': 'error', 'message': 'Quantity must be an integer!'}), 400

    req_id = FoodRequest.create(recipient_id, food_category, quantity_requested, priority)
    
    # Stack log
    global_operations_stack.push(
        action_type='ENQUEUE_REQUEST',
        details=f"Enqueued Request #{req_id} ({quantity_requested} units of '{food_category}')"
    )

    return jsonify({
        'status': 'success',
        'message': f"Request #{req_id} added to processing queue!",
        'request_id': req_id
    })

@request_bp.route('/api/requests/process', methods=['POST'])
def process_next_request():
    """
    Dequeues the Front item from the custom RequestQueue (FIFO order),
    marks it as 'Processed' in the database, and pushes the event to the Stack.
    """
    pending_requests = FoodRequest.get_all(status_filter='Pending')
    if not pending_requests:
        return jsonify({'status': 'error', 'message': 'Queue Underflow: No pending requests in queue to process!'}), 400

    rq = RequestQueue().build_from_records(pending_requests)
    
    # Custom FIFO Dequeue operation
    dequeued_item = rq.dequeue()
    req_id = dequeued_item.get('request_id')
    
    # Update DB status
    FoodRequest.update_status(req_id, 'Processed')
    
    # Push to Stack
    global_operations_stack.push(
        action_type='PROCESS_REQUEST',
        details=f"Dequeued & Processed Request #{req_id} for '{dequeued_item.get('recipient_name')}'",
        undo_data={'action': 'REVERT_REQUEST_STATUS', 'request_id': req_id}
    )

    return jsonify({
        'status': 'success',
        'message': f"Request #{req_id} successfully dequeued and processed in FIFO order!",
        'processed_item': dequeued_item,
        'remaining_in_queue': rq.size
    })

@request_bp.route('/api/requests/<int:request_id>', methods=['DELETE'])
def delete_request(request_id):
    FoodRequest.delete(request_id)
    return jsonify({'status': 'success', 'message': f"Request #{request_id} deleted successfully!"})
