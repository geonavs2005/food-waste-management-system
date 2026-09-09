"""
Searching Algorithms Implementation
Academic DSA Project - Food Waste Management System

Demonstrates:
- Linear Search: Sequential element inspection on unsorted data
- Binary Search: Divide-and-conquer on sorted data
- Detailed comparison step logging and metrics for viva demonstration
- Time & Space Complexities:
    * Linear Search: Time O(n), Space O(1)
    * Binary Search: Time O(log n), Space O(1)
"""

def linear_search(data_list, key_field, target_value):
    """
    Performs Linear Search sequentially across data_list.
    Checks items one-by-one from index 0 to n-1.
    
    Parameters:
        data_list (list): Array of dictionaries (food/request records)
        key_field (str): Dictionary key to compare (e.g. 'food_name', 'food_id', 'category')
        target_value: Value to look for
        
    Returns:
        dict with found status, matching item(s), comparison steps, and comparison count.
    """
    comparisons = 0
    steps = []
    matches = []
    
    target_str = str(target_value).strip().lower()

    for idx, item in enumerate(data_list):
        comparisons += 1
        current_val = str(item.get(key_field, '')).strip()
        current_val_lower = current_val.lower()
        
        is_match = (target_str in current_val_lower) if isinstance(target_value, str) else (current_val == str(target_value))

        steps.append({
            'step': comparisons,
            'index': idx,
            'examined_value': current_val,
            'target_value': str(target_value),
            'matched': is_match,
            'item': item
        })

        if is_match:
            matches.append(item)

    return {
        'algorithm': 'Linear Search',
        'key_field': key_field,
        'target_value': target_value,
        'found': len(matches) > 0,
        'matches': matches,
        'comparisons_count': comparisons,
        'total_elements': len(data_list),
        'steps': steps,
        'time_complexity': 'O(n)',
        'space_complexity': 'O(1)',
        'explanation': f"Linear search examined {comparisons} element(s) sequentially from index 0 to {len(data_list)-1}."
    }


def binary_search(sorted_list, key_field, target_value):
    """
    Performs Binary Search using Divide and Conquer.
    Requires data_list to already be sorted by key_field.
    
    Parameters:
        sorted_list (list): Pre-sorted array of dictionaries
        key_field (str): Field on which binary search is conducted (e.g. 'quantity', 'food_id')
        target_value: Value to search
        
    Returns:
        dict with found status, result item, steps (low, mid, high, mid_val), and comparison count.
    """
    comparisons = 0
    steps = []
    low = 0
    high = len(sorted_list) - 1
    found_item = None
    found_index = -1

    # Attempt numeric conversion if possible
    try:
        target_num = float(target_value)
        is_numeric = True
    except (ValueError, TypeError):
        target_str = str(target_value).strip().lower()
        is_numeric = False

    while low <= high:
        comparisons += 1
        mid = (low + high) // 2
        mid_item = sorted_list[mid]
        raw_val = mid_item.get(key_field)

        if is_numeric:
            try:
                mid_val = float(raw_val)
                val_to_compare = target_num
            except (ValueError, TypeError):
                mid_val = str(raw_val)
                val_to_compare = str(target_value)
        else:
            mid_val = str(raw_val).strip().lower()
            val_to_compare = target_str

        step_record = {
            'step': comparisons,
            'low_index': low,
            'mid_index': mid,
            'high_index': high,
            'mid_value': raw_val,
            'target_value': target_value
        }

        if mid_val == val_to_compare:
            step_record['action'] = 'Match found at mid index!'
            steps.append(step_record)
            found_item = mid_item
            found_index = mid
            break
        elif mid_val < val_to_compare:
            step_record['action'] = f"Mid value ({raw_val}) < Target ({target_value}) -> Searching Right Half [mid + 1, high]"
            steps.append(step_record)
            low = mid + 1
        else:
            step_record['action'] = f"Mid value ({raw_val}) > Target ({target_value}) -> Searching Left Half [low, mid - 1]"
            steps.append(step_record)
            high = mid - 1

    return {
        'algorithm': 'Binary Search',
        'key_field': key_field,
        'target_value': target_value,
        'found': found_item is not None,
        'match': found_item,
        'match_index': found_index,
        'comparisons_count': comparisons,
        'total_elements': len(sorted_list),
        'steps': steps,
        'time_complexity': 'O(log n)',
        'space_complexity': 'O(1)',
        'explanation': f"Binary search found the target in {comparisons} comparison(s) by halving the search interval at each step."
    }
