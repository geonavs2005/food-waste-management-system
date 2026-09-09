from flask import Blueprint, render_template, request, jsonify
from models.donor import Donor
from dsa.stack import global_operations_stack

donor_bp = Blueprint('donor_bp', __name__)

@donor_bp.route('/donors')
def donors_page():
    donors = Donor.get_all()
    return render_template('donors.html', donors=donors)

@donor_bp.route('/api/donors', methods=['GET'])
def get_donors():
    donors = Donor.get_all()
    return jsonify({'status': 'success', 'data': donors, 'count': len(donors)})

@donor_bp.route('/api/donors', methods=['POST'])
def add_donor():
    data = request.get_json(silent=True) or request.form
    name = data.get('name', '').strip()
    contact = data.get('contact', '').strip()
    organization = data.get('organization', '').strip()
    location = data.get('location', '').strip()

    if not name or not contact or not location:
        return jsonify({'status': 'error', 'message': 'Donor name, contact, and location are required!'}), 400

    donor_id = Donor.create(name, contact, organization, location)
    
    global_operations_stack.push(
        action_type='ADD_DONOR',
        details=f"Registered Donor '{name}' ({organization or 'Individual'})"
    )

    return jsonify({
        'status': 'success',
        'message': f"Donor '{name}' registered successfully!",
        'donor_id': donor_id
    })

@donor_bp.route('/api/donors/<int:donor_id>', methods=['PUT'])
def update_donor(donor_id):
    data = request.get_json(silent=True) or request.form
    name = data.get('name', '').strip()
    contact = data.get('contact', '').strip()
    organization = data.get('organization', '').strip()
    location = data.get('location', '').strip()

    Donor.update(donor_id, name, contact, organization, location)
    return jsonify({'status': 'success', 'message': f"Donor #{donor_id} updated successfully!"})

@donor_bp.route('/api/donors/<int:donor_id>', methods=['DELETE'])
def delete_donor(donor_id):
    Donor.delete(donor_id)
    return jsonify({'status': 'success', 'message': f"Donor #{donor_id} deleted successfully!"})
