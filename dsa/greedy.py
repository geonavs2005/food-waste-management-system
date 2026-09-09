"""
Greedy Algorithm Implementation for Food Waste Distribution
Academic DSA Project - Food Waste Management System

Demonstrates:
- Greedy Strategy: "Locally optimal choice at each step leading to a global solution"
- Heuristic: Prioritize highest urgency/priority requests first (or highest priority-to-quantity ratio)
- Application: Allocating limited surplus food among competing recipient requests
- Time & Space Complexities:
    * Time: O(n log n) due to sorting requests by greedy heuristic
    * Space: O(n) to store allocation decisions
"""
from dsa.sorting import merge_sort

def greedy_food_distribution(available_food, requests_list, heuristic='priority'):
    """
    Allocates available food to recipient requests using a Greedy approach.
    
    Parameters:
        available_food (int): Total units/packets of surplus food available
        requests_list (list): List of request dictionaries containing 'request_id', 'recipient_name', 'quantity_requested', 'priority'
        heuristic (str): 'priority' (highest priority first) or 'ratio' (highest priority-per-quantity first)
        
    Returns:
        dict containing:
        - initial_food
        - remaining_food
        - total_allocated
        - selected_requests
        - rejected_requests
        - step_by_step_trace
        - time_complexity
        - explanation
    """
    total_available = int(available_food)
    remaining_food = total_available
    
    # Enrich requests with ratio if heuristic is ratio
    prepared_requests = []
    for r in requests_list:
        item = dict(r)
        qty = max(1, int(item.get('quantity_requested', 1)))
        pri = int(item.get('priority', 5))
        item['ratio'] = round(pri / qty, 3)
        prepared_requests.append(item)

    # Sort using custom Merge Sort
    sort_key = 'priority' if heuristic == 'priority' else 'ratio'
    sort_output = merge_sort(prepared_requests, key_field=sort_key, reverse=True)
    sorted_requests = sort_output['sorted_data']

    selected_requests = []
    rejected_requests = []
    step_trace = []
    total_allocated = 0
    total_benefit = 0

    for step_num, req in enumerate(sorted_requests, 1):
        req_id = req.get('request_id')
        req_name = req.get('recipient_name', f"Recipient #{req.get('recipient_id', req_id)}")
        qty = int(req.get('quantity_requested', 0))
        pri = int(req.get('priority', 5))

        if qty <= remaining_food:
            remaining_food -= qty
            total_allocated += qty
            total_benefit += pri
            selected_requests.append(req)
            status_text = "ACCEPTED (Greedily Allocated)"
            reason = f"Sufficient food available ({remaining_food + qty} >= {qty}). Deducted {qty} units."
        else:
            rejected_requests.append(req)
            status_text = "REJECTED (Insufficient Food)"
            reason = f"Requested {qty} units exceeds remaining food ({remaining_food} units)."

        step_trace.append({
            'step': step_num,
            'request_id': req_id,
            'recipient': req_name,
            'priority': pri,
            'quantity': qty,
            'ratio': req.get('ratio'),
            'status': status_text,
            'remaining_after_step': remaining_food,
            'reason': reason
        })

    return {
        'algorithm': 'Greedy Algorithm for Food Distribution',
        'heuristic_used': f"Highest {sort_key.upper()} First",
        'initial_food': total_available,
        'food_allocated': total_allocated,
        'remaining_food': remaining_food,
        'total_priority_satisfied': total_benefit,
        'total_requests': len(requests_list),
        'accepted_count': len(selected_requests),
        'rejected_count': len(rejected_requests),
        'selected_requests': selected_requests,
        'rejected_requests': rejected_requests,
        'step_by_step_trace': step_trace,
        'time_complexity': 'O(n log n)',
        'space_complexity': 'O(n)',
        'explanation': 'The Greedy Algorithm makes the best immediate choice at each step by selecting the highest urgency request available. It produces a fast, practical allocation without exhaustive search.'
    }
