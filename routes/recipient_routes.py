from flask import Blueprint, render_template, request, jsonify
from models.recipient import Recipient
from dsa.stack import global_operations_stack

recipient_bp = Blueprint('recipient_bp', __name__)

@recipient_bp.route('/recipients')
def recipients_page():
    recipients = Recipient.get_all()
    return render_template('recipients.html', recipients=recipients)

@recipient_bp.route('/api/recipients', methods=['GET'])
def get_recipients():
    recipients = Recipient.get_all()
    return jsonify({'status': 'success', 'data': recipients, 'count': len(recipients)})

@recipient_bp.route('/api/recipients', methods=['POST'])
def add_recipient():
    data = request.get_json(silent=True) or request.form
    name = data.get('name', '').strip()
    organization = data.get('organization', '').strip()
    contact = data.get('contact', '').strip()
    location = data.get('location', '').strip()
    priority = int(data.get('priority', 5))

    if not name or not contact or not location:
        return jsonify({'status': 'error', 'message': 'Recipient name, contact, and location are required!'}), 400

    rec_id = Recipient.create(name, organization, contact, location, priority)
    
    global_operations_stack.push(
        action_type='ADD_RECIPIENT',
        details=f"Registered Recipient '{name}' with Urgency Level {priority}/10"
    )

    return jsonify({
        'status': 'success',
        'message': f"Recipient '{name}' registered successfully!",
        'recipient_id': rec_id
    })

@recipient_bp.route('/api/recipients/<int:recipient_id>', methods=['PUT'])
def update_recipient(recipient_id):
    data = request.get_json(silent=True) or request.form
    name = data.get('name', '').strip()
    organization = data.get('organization', '').strip()
    contact = data.get('contact', '').strip()
    location = data.get('location', '').strip()
    priority = int(data.get('priority', 5))

    Recipient.update(recipient_id, name, organization, contact, location, priority)
    return jsonify({'status': 'success', 'message': f"Recipient #{recipient_id} updated successfully!"})

@recipient_bp.route('/api/recipients/<int:recipient_id>', methods=['DELETE'])
def delete_recipient(recipient_id):
    Recipient.delete(recipient_id)
    return jsonify({'status': 'success', 'message': f"Recipient #{recipient_id} deleted successfully!"})
