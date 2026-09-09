"""
Graph Data Structure Implementation using Adjacency List
Academic DSA Project - Food Waste Management System

Demonstrates:
- Adjacency List representation
- Graph Operations: add_vertex, add_edge, get_vertices, get_edges
- Breadth-First Search (BFS) - Level by Level exploration using Queue
- Depth-First Search (DFS) - Deep path exploration using Stack/Recursion
- Shortest Path calculation
- Application: Food Supply Chain Network (Donors -> Collection Centers -> NGO Shelters)
- Time Complexities:
    * BFS: O(V + E)
    * DFS: O(V + E)
    * Add Vertex: O(1)
    * Add Edge: O(1)
"""
from dsa.queue import RequestQueue

class Graph:
    """
    Graph representation using an Adjacency List.
    Nodes represent Locations (Donors, Centers, Shelters).
    Edges represent logistics routes with distance weights.
    """
    def __init__(self, directed=False):
        self.adj_list = {}        # { vertex_name: [ {'node': neighbor, 'weight': distance}, ... ] }
        self.vertex_meta = {}     # { vertex_name: { 'type': 'Donor Hub' | 'Collection Center' | 'NGO' } }
        self.directed = directed

    def add_vertex(self, vertex, node_type="Location"):
        """Adds a new location vertex to the graph. Time: O(1)"""
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []
            self.vertex_meta[vertex] = {'type': node_type}
            return True
        return False

    def add_edge(self, u, v, weight=1):
        """
        Adds an edge between vertex u and vertex v.
        Time: O(1)
        """
        if u not in self.adj_list:
            self.add_vertex(u)
        if v not in self.adj_list:
            self.add_vertex(v)

        # Check if edge already exists
        for neighbor in self.adj_list[u]:
            if neighbor['node'] == v:
                neighbor['weight'] = weight
                break
        else:
            self.adj_list[u].append({'node': v, 'weight': weight})

        if not self.directed:
            for neighbor in self.adj_list[v]:
                if neighbor['node'] == u:
                    neighbor['weight'] = weight
                    break
            else:
                self.adj_list[v].append({'node': u, 'weight': weight})

    def get_vertices(self):
        """Returns all vertices with metadata."""
        return [{'name': k, 'type': self.vertex_meta.get(k, {}).get('type', 'Location')} for k in self.adj_list]

    def get_edges(self):
        """Returns all unique edges formatted for UI/Canvas."""
        edges = []
        seen = set()
        for u in self.adj_list:
            for neighbor in self.adj_list[u]:
                v = neighbor['node']
                w = neighbor['weight']
                edge_id = tuple(sorted([u, v])) if not self.directed else (u, v)
                if edge_id not in seen:
                    seen.add(edge_id)
                    edges.append({'from': u, 'to': v, 'distance': w})
        return edges

    def bfs(self, start_vertex):
        """
        Breadth-First Search (BFS) starting from start_vertex.
        Explores all neighbors at current depth level before moving to the next level.
        Uses a custom FIFO Queue for traversal order.
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        """
        if start_vertex not in self.adj_list:
            return {'error': f"Start vertex '{start_vertex}' not found in graph."}

        visited = {start_vertex}
        traversal_order = []
        steps = []
        
        # Using custom RequestQueue to demonstrate DSA queue usage in BFS
        queue = RequestQueue()
        queue.enqueue({'vertex': start_vertex, 'level': 0})

        while not queue.is_empty():
            curr_item = queue.dequeue()
            curr_v = curr_item['vertex']
            level = curr_item['level']
            traversal_order.append(curr_v)

            step_neighbors = []
            for neighbor_info in self.adj_list.get(curr_v, []):
                neighbor = neighbor_info['node']
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.enqueue({'vertex': neighbor, 'level': level + 1})
                    step_neighbors.append(neighbor)

            steps.append({
                'current_node': curr_v,
                'level': level,
                'visited_so_far': list(traversal_order),
                'newly_discovered': step_neighbors
            })

        return {
            'algorithm': 'Breadth-First Search (BFS)',
            'start_vertex': start_vertex,
            'traversal_order': traversal_order,
            'steps': steps,
            'total_visited': len(traversal_order),
            'time_complexity': 'O(V + E)',
            'space_complexity': 'O(V)'
        }

    def dfs(self, start_vertex):
        """
        Depth-First Search (DFS) starting from start_vertex.
        Explores as deep as possible along each branch before backtracking.
        Uses recursive DFS helper.
        Time Complexity: O(V + E)
        Space Complexity: O(V)
        """
        if start_vertex not in self.adj_list:
            return {'error': f"Start vertex '{start_vertex}' not found in graph."}

        visited = set()
        traversal_order = []
        steps = []

        def _dfs_helper(vertex, depth):
            visited.add(vertex)
            traversal_order.append(vertex)
            steps.append({
                'current_node': vertex,
                'depth': depth,
                'visited_so_far': list(traversal_order)
            })

            for neighbor_info in self.adj_list.get(vertex, []):
                neighbor = neighbor_info['node']
                if neighbor not in visited:
                    _dfs_helper(neighbor, depth + 1)

        _dfs_helper(start_vertex, 0)

        return {
            'algorithm': 'Depth-First Search (DFS)',
            'start_vertex': start_vertex,
            'traversal_order': traversal_order,
            'steps': steps,
            'total_visited': len(traversal_order),
            'time_complexity': 'O(V + E)',
            'space_complexity': 'O(V)'
        }

    def shortest_path(self, start_vertex, end_vertex):
        """
        Finds the shortest route using BFS (unweighted) or Dijkstra's logic.
        Returns path sequence and total distance.
        """
        if start_vertex not in self.adj_list or end_vertex not in self.adj_list:
            return None, 0

        distances = {v: float('inf') for v in self.adj_list}
        previous = {v: None for v in self.adj_list}
        distances[start_vertex] = 0
        unvisited = set(self.adj_list.keys())

        while unvisited:
            # Pick node with min distance
            curr = min(unvisited, key=lambda node: distances[node])
            if distances[curr] == float('inf'):
                break
            if curr == end_vertex:
                break
            unvisited.remove(curr)

            for neighbor_info in self.adj_list[curr]:
                neighbor = neighbor_info['node']
                weight = neighbor_info['weight']
                alt = distances[curr] + weight
                if alt < distances[neighbor]:
                    distances[neighbor] = alt
                    previous[neighbor] = curr

        # Reconstruct path
        path = []
        curr = end_vertex
        while curr:
            path.insert(0, curr)
            curr = previous[curr]

        if path and path[0] == start_vertex:
            return path, distances[end_vertex]
        return [], 0
