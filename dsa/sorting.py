"""
Sorting Algorithms Implementation
Academic DSA Project - Food Waste Management System

Demonstrates:
- Merge Sort (Divide and Conquer, Stable, O(n log n))
- Quick Sort (Partitioning, In-place, O(n log n) average)
- Bubble Sort (Iterative comparison, O(n^2))
- Detailed step tracking and comparison metrics
- Strictly custom implementations without Python's built-in sort()
- Time Complexities:
    * Merge Sort: Best O(n log n), Average O(n log n), Worst O(n log n), Space O(n)
    * Quick Sort: Best O(n log n), Average O(n log n), Worst O(n^2), Space O(log n)
    * Bubble Sort: Best O(n), Average O(n^2), Worst O(n^2), Space O(1)
"""
import copy

def _extract_val(item, key_field):
    """Helper to extract sortable value from record dict."""
    val = item.get(key_field)
    if val is None:
        return ""
    try:
        return float(val)
    except (ValueError, TypeError):
        return str(val).lower()

def merge_sort(arr, key_field='quantity', reverse=False):
    """
    Custom Merge Sort implementation on a list of dictionary records.
    Divide and Conquer: Recursively divides array into two halves, sorts them, and merges.
    """
    stats = {'comparisons': 0, 'steps': []}
    
    def _merge(left, right):
        result = []
        i = 0
        j = 0
        
        while i < len(left) and j < len(right):
            stats['comparisons'] += 1
            val_l = _extract_val(left[i], key_field)
            val_r = _extract_val(right[j], key_field)
            
            condition = (val_l >= val_r) if reverse else (val_l <= val_r)
            if condition:
                result.append(left[i])
                i += 1
            else:
                result.append(right[j])
                j += 1
                
        while i < len(left):
            result.append(left[i])
            i += 1
            
        while j < len(right):
            result.append(right[j])
            j += 1
            
        return result

    def _sort_recursive(data):
        if len(data) <= 1:
            return data
        
        mid = len(data) // 2
        left_half = _sort_recursive(data[:mid])
        right_half = _sort_recursive(data[mid:])
        merged = _merge(left_half, right_half)
        
        stats['steps'].append({
            'left_size': len(left_half),
            'right_size': len(right_half),
            'merged_sample': [_extract_val(x, key_field) for x in merged[:5]]
        })
        return merged

    # Create shallow copy of data list to avoid mutating original in-place unexpectedly
    data_copy = [dict(item) for item in arr]
    sorted_result = _sort_recursive(data_copy)

    return {
        'algorithm': 'Merge Sort',
        'key_field': key_field,
        'order': 'Descending' if reverse else 'Ascending',
        'comparisons_count': stats['comparisons'],
        'total_elements': len(arr),
        'sorted_data': sorted_result,
        'time_complexity': 'O(n log n)',
        'space_complexity': 'O(n)',
        'description': 'Divide and Conquer: Splits array recursively into halves, sorts sub-arrays, and merges them.'
    }


def quick_sort(arr, key_field='quantity', reverse=False):
    """
    Custom Quick Sort implementation with Lomuto partition scheme.
    """
    stats = {'comparisons': 0}
    data_copy = [dict(item) for item in arr]

    def _partition(low, high):
        pivot_val = _extract_val(data_copy[high], key_field)
        i = low - 1
        
        for j in range(low, high):
            stats['comparisons'] += 1
            curr_val = _extract_val(data_copy[j], key_field)
            condition = (curr_val >= pivot_val) if reverse else (curr_val <= pivot_val)
            if condition:
                i += 1
                data_copy[i], data_copy[j] = data_copy[j], data_copy[i]
                
        data_copy[i + 1], data_copy[high] = data_copy[high], data_copy[i + 1]
        return i + 1

    def _qsort(low, high):
        if low < high:
            pi = _partition(low, high)
            _qsort(low, pi - 1)
            _qsort(pi + 1, high)

    if len(data_copy) > 1:
        _qsort(0, len(data_copy) - 1)

    return {
        'algorithm': 'Quick Sort',
        'key_field': key_field,
        'order': 'Descending' if reverse else 'Ascending',
        'comparisons_count': stats['comparisons'],
        'total_elements': len(arr),
        'sorted_data': data_copy,
        'time_complexity': 'O(n log n) Average, O(n^2) Worst',
        'space_complexity': 'O(log n)',
        'description': 'Picks a pivot element and partitions array into elements smaller and greater than the pivot.'
    }


def bubble_sort(arr, key_field='quantity', reverse=False):
    """
    Custom Bubble Sort implementation for academic comparison.
    """
    stats = {'comparisons': 0, 'swaps': 0}
    data_copy = [dict(item) for item in arr]
    n = len(data_copy)

    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            stats['comparisons'] += 1
            val_a = _extract_val(data_copy[j], key_field)
            val_b = _extract_val(data_copy[j + 1], key_field)
            
            condition = (val_a < val_b) if reverse else (val_a > val_b)
            if condition:
                data_copy[j], data_copy[j + 1] = data_copy[j + 1], data_copy[j]
                stats['swaps'] += 1
                swapped = True
        if not swapped:
            break

    return {
        'algorithm': 'Bubble Sort',
        'key_field': key_field,
        'order': 'Descending' if reverse else 'Ascending',
        'comparisons_count': stats['comparisons'],
        'swaps_count': stats['swaps'],
        'total_elements': len(arr),
        'sorted_data': data_copy,
        'time_complexity': 'O(n^2) Worst/Average, O(n) Best',
        'space_complexity': 'O(1)',
        'description': 'Repeatedly steps through the list, compares adjacent elements and swaps them if out of order.'
    }
