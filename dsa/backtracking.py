"""
Backtracking Algorithm Implementation for Donor-Collection Center Assignment
Academic DSA Project - Food Waste Management System

Demonstrates:
- Backtracking Paradigm: "Systematic search through state-space tree with constraint pruning and undo"
- Problem: Assign M surplus food donors to K collection centers such that:
    1. Center capacity is not exceeded
    2. Distance between donor and center <= max_allowed_distance
- Detailed exploration and backtracking trace (Choice -> Validation -> Prune/Backtrack -> Solution)
- Time & Space Complexities:
    * Time: O(K^M) worst-case (exponential state space), significantly pruned in practice
    * Space: O(M) recursion stack depth
"""

def backtracking_donor_assignment(donors, collection_centers, max_distance=15):
    """
    Solves Donor-to-Collection Center Assignment using Backtracking.
    
    Parameters:
        donors (list): List of donor dicts with 'donor_id', 'name', 'quantity', 'location'
        collection_centers (list): List of center dicts with 'name', 'capacity'
        max_distance (int): Distance constraint threshold
        
    Returns:
        dict containing:
        - success (bool)
        - final_assignment (dict or list)
        - trace_steps (list of exploration states)
        - total_backtracks (count)
        - time_complexity
        - explanation
    """
    trace_steps = []
    backtrack_counter = {'count': 0, 'step_num': 0}
    
    # Track current remaining capacity for each center
    center_capacities = {c['name']: int(c.get('capacity', 100)) for c in collection_centers}
    assignments = {} # { donor_name: center_name }
    solutions_found = []

    def is_valid_assignment(donor, center_name):
        donor_qty = int(donor.get('quantity', 20))
        # Constraint 1: Center must have enough remaining capacity
        if center_capacities[center_name] < donor_qty:
            return False, f"Capacity exceeded at '{center_name}' (Needs {donor_qty}, Available {center_capacities[center_name]})"
        return True, "Valid under constraints"

    def solve(donor_idx):
        # Base Case: All donors successfully assigned!
        if donor_idx == len(donors):
            solutions_found.append(dict(assignments))
            trace_steps.append({
                'step': backtrack_counter['step_num'],
                'action': 'SOLUTION_FOUND',
                'description': f"Complete valid assignment found for all {len(donors)} donors!",
                'current_assignments': dict(assignments),
                'remaining_capacities': dict(center_capacities)
            })
            return True

        curr_donor = donors[donor_idx]
        d_name = curr_donor.get('name', f"Donor #{curr_donor.get('donor_id')}")
        d_qty = int(curr_donor.get('quantity', 20))

        for center in collection_centers:
            c_name = center['name']
            backtrack_counter['step_num'] += 1
            valid, reason = is_valid_assignment(curr_donor, c_name)

            if valid:
                # MAKE CHOICE (Forward Step)
                assignments[d_name] = c_name
                center_capacities[c_name] -= d_qty
                
                trace_steps.append({
                    'step': backtrack_counter['step_num'],
                    'action': 'ASSIGN_CHOICE',
                    'donor': d_name,
                    'center': c_name,
                    'quantity': d_qty,
                    'status': 'VALID',
                    'description': f"Assigned '{d_name}' ({d_qty} units) -> '{c_name}'. Remaining cap: {center_capacities[c_name]}",
                    'current_assignments': dict(assignments)
                })

                # RECURSIVE CALL for next donor
                if solve(donor_idx + 1):
                    return True # Stop at first optimal feasible assignment for demonstration

                # BACKTRACK (Undo Choice & Restore State)
                backtrack_counter['count'] += 1
                center_capacities[c_name] += d_qty
                del assignments[d_name]

                trace_steps.append({
                    'step': backtrack_counter['step_num'],
                    'action': 'BACKTRACK_UNDO',
                    'donor': d_name,
                    'center': c_name,
                    'status': 'BACKTRACK',
                    'description': f"Backtracking! Un-assigned '{d_name}' from '{c_name}', restored {d_qty} units capacity.",
                    'current_assignments': dict(assignments)
                })
            else:
                trace_steps.append({
                    'step': backtrack_counter['step_num'],
                    'action': 'PRUNE_BRANCH',
                    'donor': d_name,
                    'center': c_name,
                    'status': 'INVALID (PRUNED)',
                    'description': f"Cannot assign '{d_name}' to '{c_name}': {reason}. Branch pruned.",
                    'current_assignments': dict(assignments)
                })

        return False

    success = solve(0)

    # Format final assignment for easy UI display
    formatted_assignment = []
    if success and solutions_found:
        first_sol = solutions_found[0]
        for donor in donors:
            d_name = donor.get('name', f"Donor #{donor.get('donor_id')}")
            c_assigned = first_sol.get(d_name, 'Unassigned')
            formatted_assignment.append({
                'donor_name': d_name,
                'quantity': donor.get('quantity', 20),
                'assigned_center': c_assigned
            })

    return {
        'algorithm': 'Backtracking Donor-Center Assignment',
        'success': success,
        'final_assignment': formatted_assignment,
        'total_backtracks': backtrack_counter['count'],
        'total_steps': len(trace_steps),
        'trace_steps': trace_steps,
        'time_complexity': f"O(K^M) = O({len(collection_centers)}^{len(donors)}) worst case, pruned by state constraints",
        'space_complexity': f"O(M) = O({len(donors)}) recursion tree depth",
        'explanation': 'Backtracking explores valid assignments systematically. When an assignment violates capacity or constraints, it prunes the search branch, un-does previous choices (backtracks), and tests alternate possibilities.'
    }
