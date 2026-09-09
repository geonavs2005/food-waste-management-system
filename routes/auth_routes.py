from functools import wraps
from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from models.user import User
from models.food import Food
from models.donor import Donor
from models.recipient import Recipient
from models.request import FoodRequest
from dsa.stack import global_operations_stack

auth_bp = Blueprint('auth_bp', __name__)

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('auth_bp.login_page'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in first.', 'warning')
            return redirect(url_for('auth_bp.login_page'))
        if session.get('role') != 'admin':
            flash('Access denied. Administrator privileges required.', 'danger')
            return redirect(url_for('dashboard'))
        return f(*args, **kwargs)
    return decorated_function

@auth_bp.route('/login', methods=['GET', 'POST'])
def login_page():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        requested_role = data.get('role', 'admin') # 'admin', 'donor', or 'receiver'

        if not username or not password:
            msg = 'Username and password are required.'
            if request.is_json:
                return jsonify({'status': 'error', 'message': msg}), 400
            flash(msg, 'danger')
            return render_template('login.html')

        user = User.get_by_username(username)
        if not user or user.get('password') != password:
            msg = 'Invalid username or password.'
            if request.is_json:
                return jsonify({'status': 'error', 'message': msg}), 401
            flash(msg, 'danger')
            return render_template('login.html')

        # Role verification
        if requested_role and user.get('role') != requested_role:
            msg = f"Account exists, but it is registered as '{user.get('role').upper()}', not '{requested_role.upper()}'."
            if request.is_json:
                return jsonify({'status': 'error', 'message': msg}), 403
            flash(msg, 'warning')
            return render_template('login.html')

        # Setup session
        session['user_id'] = user['user_id']
        session['username'] = user['username']
        session['name'] = user['name']
        session['role'] = user['role']
        session['donor_id'] = user.get('donor_id')
        session['recipient_id'] = user.get('recipient_id')

        # Push to stack
        global_operations_stack.push('USER_LOGIN', f"{user['role'].upper()} '{user['name']}' logged in")

        if user['role'] == 'admin':
            redirect_url = url_for('dashboard')
        elif user['role'] == 'donor':
            redirect_url = url_for('auth_bp.donor_portal')
        else:
            redirect_url = url_for('auth_bp.receiver_portal')

        if request.is_json:
            return jsonify({
                'status': 'success',
                'message': f"Welcome back, {user['name']}!",
                'redirect': redirect_url,
                'user': user
            })

        return redirect(redirect_url)

    return render_template('login.html')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register_page():
    if request.method == 'POST':
        data = request.get_json(silent=True) or request.form
        role = data.get('role', 'donor') # 'donor' or 'receiver'
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        name = data.get('name', '').strip()
        organization = data.get('organization', '').strip()
        contact = data.get('contact', '').strip()
        location = data.get('location', '').strip()
        priority = int(data.get('priority', 5))

        if not username or not password or not name or not contact or not location:
            msg = 'All required fields must be filled.'
            if request.is_json:
                return jsonify({'status': 'error', 'message': msg}), 400
            flash(msg, 'danger')
            return render_template('register.html')

        if role == 'receiver':
            user_id, msg = User.register_recipient(username, password, name, organization, contact, location, priority)
        else:
            user_id, msg = User.register_donor(username, password, name, contact, organization, location)

        if not user_id:
            if request.is_json:
                return jsonify({'status': 'error', 'message': msg}), 400
            flash(msg, 'danger')
            return render_template('register.html')

        flash(f"{role.capitalize()} registration successful! Please log in.", 'success')
        if request.is_json:
            return jsonify({'status': 'success', 'message': msg, 'redirect': url_for('auth_bp.login_page')})
        return redirect(url_for('auth_bp.login_page'))

    return render_template('register.html')

@auth_bp.route('/logout')
def logout():
    name = session.get('name', 'User')
    session.clear()
    flash(f"You have been logged out, {name}.", 'info')
    return redirect(url_for('auth_bp.login_page'))

@auth_bp.route('/donor/portal')
@login_required
def donor_portal():
    donor_id = session.get('donor_id')
    donor_profile = Donor.get_by_id(donor_id) if donor_id else None
    
    # Get all foods and filter by donor_id
    all_foods = Food.get_all()
    my_foods = [f for f in all_foods if f.get('donor_id') == donor_id] if donor_id else all_foods[:4]
    
    # Active requests looking for food
    active_requests = FoodRequest.get_all(status_filter='Pending')

    return render_template('donor_dashboard.html', 
                           donor=donor_profile, 
                           my_foods=my_foods, 
                           total_donated=sum(int(f.get('quantity', 0)) for f in my_foods),
                           active_requests=active_requests[:6])

@auth_bp.route('/receiver/portal')
@login_required
def receiver_portal():
    recipient_id = session.get('recipient_id')
    rec_profile = Recipient.get_by_id(recipient_id) if recipient_id else None
    
    # Get all requests and filter for this recipient
    all_requests = FoodRequest.get_all()
    my_requests = [r for r in all_requests if r.get('recipient_id') == recipient_id] if recipient_id else all_requests[:4]
    
    # Live available surplus food inventory
    available_foods = [f for f in Food.get_all() if f.get('status') == 'Available']

    pending_count = len([r for r in my_requests if r.get('status') == 'Pending'])
    fulfilled_count = len([r for r in my_requests if r.get('status') == 'Processed'])

    return render_template('receiver_dashboard.html',
                           recipient=rec_profile,
                           my_requests=my_requests,
                           pending_count=pending_count,
                           fulfilled_count=fulfilled_count,
                           available_foods=available_foods[:8])
