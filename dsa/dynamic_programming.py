"""
Dynamic Programming (0/1 Knapsack) Implementation for Food Allocation
Academic DSA Project - Food Waste Management System

Demonstrates:
- 0/1 Knapsack Dynamic Programming formulation
- State definition: DP[i][w] = max total priority benefit using subset of first i requests with total food capacity w
- Recurrence Relation:
    DP[i][w] = DP[i-1][w]                                    (if req[i].quantity > w)
    DP[i][w] = max(DP[i-1][w], DP[i-1][w - req[i].quantity] + req[i].priority)  (otherwise)
- Optimal Substructure & Overlapping Subproblems
- Backtracking through DP matrix to reconstruct selected optimal recipient requests
- Time & Space Complexities:
    * Time: O(n * W), where n is number of requests, W is food capacity
    * Space: O(n * W) for matrix visualization and path reconstruction
"""

def dp_knapsack_food_allocation(capacity, requests_list):
    """
    Finds the optimal combination of recipient requests to maximize total priority benefit
    within the surplus food capacity constraint W.
    
    Parameters:
        capacity (int): Total available food units (W)
        requests_list (list): List of request dicts
        
    Returns:
        dict containing:
        - max_benefit
        - total_food_used
        - capacity
        - selected_requests
        - unselected_requests
        - dp_table_summary (sampled 2D grid for UI visualizer)
        - time_complexity
        - explanation
    """
    W = max(0, int(capacity))
    n = len(requests_list)
    
    if n == 0 or W == 0:
        return {
            'algorithm': '0/1 Knapsack Dynamic Programming',
            'max_benefit': 0,
            'total_food_used': 0,
            'capacity': W,
            'selected_requests': [],
            'unselected_requests': requests_list,
            'dp_matrix_rows': 0,
            'dp_matrix_cols': 0,
            'time_complexity': 'O(n * W)',
            'space_complexity': 'O(n * W)',
            'explanation': 'No requests or zero capacity provided.'
        }

    # Extract quantities (weights) and priorities (values)
    # 1-indexed for clear DP matrix alignment
    quantities = [0] + [int(r.get('quantity_requested', 0)) for r in requests_list]
    priorities = [0] + [int(r.get('priority', 5)) for r in requests_list]

    # Initialize 2D DP Table of dimensions (n + 1) x (W + 1) with 0
    dp = [[0 for _ in range(W + 1)] for _ in range(n + 1)]

    # Populate DP Table bottom-up
    for i in range(1, n + 1):
        wi = quantities[i]
        vi = priorities[i]
        for w in range(W + 1):
            if wi > w:
                dp[i][w] = dp[i - 1][w]
            else:
                exclude_val = dp[i - 1][w]
                include_val = dp[i - 1][w - wi] + vi
                dp[i][w] = max(exclude_val, include_val)

    max_benefit = dp[n][W]

    # Backtracking to reconstruct optimal subset of selected requests
    selected_requests = []
    unselected_requests = []
    current_w = W
    total_food_used = 0

    for i in range(n, 0, -1):
        # If value comes from including request i
        if dp[i][current_w] != dp[i - 1][current_w]:
            req = requests_list[i - 1]
            selected_requests.append(req)
            total_food_used += quantities[i]
            current_w -= quantities[i]
        else:
            unselected_requests.append(requests_list[i - 1])

    # Reverse to keep original order
    selected_requests.reverse()

    # Generate sampled DP matrix for visual representation in UI (max 15 columns if W is large)
    step_col = max(1, W // 10)
    sample_cols = sorted(list(set([0] + list(range(step_col, W + 1, step_col)) + [W])))
    
    matrix_visualization = {
        'headers': ['Request \\ Capacity'] + [f"Cap {c}" for c in sample_cols],
        'rows': []
    }

    for i in range(n + 1):
        row_label = "Base (0)" if i == 0 else f"Req #{requests_list[i-1].get('request_id')} (Qty:{quantities[i]}, Pri:{priorities[i]})"
        row_cells = [dp[i][c] for c in sample_cols]
        matrix_visualization['rows'].append({
            'label': row_label,
            'values': row_cells,
            'is_selected': (i > 0 and requests_list[i-1] in selected_requests)
        })

    return {
        'algorithm': '0/1 Knapsack Dynamic Programming for Food Allocation',
        'capacity': W,
        'max_benefit': max_benefit,
        'total_food_used': total_food_used,
        'remaining_capacity': W - total_food_used,
        'selected_requests': selected_requests,
        'unselected_requests': unselected_requests,
        'selected_count': len(selected_requests),
        'total_requests': n,
        'dp_matrix_visualization': matrix_visualization,
        'time_complexity': f"O(n * W) = O({n} * {W}) = {n * W} operations",
        'space_complexity': f"O(n * W) = { (n + 1) * (W + 1) } table cells",
        'explanation': 'Dynamic Programming solves the food allocation problem by breaking it into subproblems, memoizing optimal values for smaller capacities, and combining them without recomputation to guarantee mathematically optimal total benefit.'
    }
