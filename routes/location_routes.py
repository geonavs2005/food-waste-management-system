from flask import Blueprint, render_template, request, jsonify
from database.db import query_db, execute_db
from dsa.graph import Graph

location_bp = Blueprint('location_bp', __name__)

def build_location_graph():
    """Helper to reconstruct Graph from database tables."""
    g = Graph(directed=False)
    locations = query_db("SELECT * FROM locations")
    for loc in locations:
        g.add_vertex(loc['name'], loc.get('type', 'Location'))
        
    connections = query_db("SELECT * FROM location_connections")
    for conn in connections:
        g.add_edge(conn['from_location'], conn['to_location'], int(conn.get('distance', 5)))
        
    return g

@location_bp.route('/locations')
def locations_page():
    locations = query_db("SELECT * FROM locations ORDER BY location_id ASC")
    connections = query_db("SELECT * FROM location_connections ORDER BY connection_id ASC")
    g = build_location_graph()
    
    return render_template('locations.html', 
                           locations=locations, 
                           connections=connections,
                           vertices=g.get_vertices(),
                           edges=g.get_edges(),
                           adj_list=g.adj_list)

@location_bp.route('/api/locations', methods=['GET'])
def get_locations():
    g = build_location_graph()
    return jsonify({
        'status': 'success',
        'vertices': g.get_vertices(),
        'edges': g.get_edges(),
        'adj_list': g.adj_list
    })

@location_bp.route('/api/locations', methods=['POST'])
def add_location():
    data = request.get_json() or request.form
    name = data.get('name', '').strip()
    node_type = data.get('type', 'City Hub').strip()

    if not name:
        return jsonify({'status': 'error', 'message': 'Location name is required!'}), 400

    execute_db("INSERT INTO locations (name, type) VALUES (%s, %s)", (name, node_type))
    return jsonify({'status': 'success', 'message': f"Location '{name}' added!"})

@location_bp.route('/api/locations/connections', methods=['POST'])
def add_connection():
    data = request.get_json() or request.form
    from_loc = data.get('from_location', '').strip()
    to_loc = data.get('to_location', '').strip()
    distance = int(data.get('distance', 5))

    if not from_loc or not to_loc:
        return jsonify({'status': 'error', 'message': 'From and To locations are required!'}), 400

    if from_loc == to_loc:
        return jsonify({'status': 'error', 'message': 'Self loops are not allowed!'}), 400

    execute_db("INSERT INTO location_connections (from_location, to_location, distance) VALUES (%s, %s, %s)", 
               (from_loc, to_loc, distance))
    return jsonify({'status': 'success', 'message': f"Connection added between '{from_loc}' and '{to_loc}' ({distance} km)!"})

@location_bp.route('/api/graph/bfs', methods=['POST'])
def run_bfs():
    data = request.get_json(silent=True) or {}
    start_node = data.get('start_node')
    g = build_location_graph()
    
    if not start_node:
        vertices = g.get_vertices()
        if vertices:
            start_node = vertices[0]['name']
        else:
            return jsonify({'status': 'error', 'message': 'Graph is empty!'}), 400

    result = g.bfs(start_node)
    return jsonify({'status': 'success', 'result': result})

@location_bp.route('/api/graph/dfs', methods=['POST'])
def run_dfs():
    data = request.get_json(silent=True) or {}
    start_node = data.get('start_node')
    g = build_location_graph()
    
    if not start_node:
        vertices = g.get_vertices()
        if vertices:
            start_node = vertices[0]['name']
        else:
            return jsonify({'status': 'error', 'message': 'Graph is empty!'}), 400

    result = g.dfs(start_node)
    return jsonify({'status': 'success', 'result': result})

@location_bp.route('/api/graph/shortest_path', methods=['POST'])
def run_shortest_path():
    data = request.get_json() or {}
    start_node = data.get('start_node')
    end_node = data.get('end_node')
    g = build_location_graph()

    path, total_dist = g.shortest_path(start_node, end_node)
    return jsonify({
        'status': 'success',
        'path': path,
        'distance': total_dist,
        'hops': len(path) - 1 if path else 0
    })
