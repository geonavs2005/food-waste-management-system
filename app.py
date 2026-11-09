import os
import datetime
from flask import Flask, render_template, jsonify
from config import Config
from database.db import init_db, query_db
from models.food import Food
from models.donor import Donor
from models.recipient import Recipient
from models.request import FoodRequest
from dsa.stack import global_operations_stack

# Import Blueprints
from routes.food_routes import food_bp
from routes.donor_routes import donor_bp
from routes.recipient_routes import recipient_bp
from routes.request_routes import request_bp
from routes.location_routes import location_bp
from routes.algorithm_routes import algorithm_bp
from routes.auth_routes import auth_bp

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize Database Schema & Seed Data
    try:
        init_db()
        print(">> Database initialized and verified.")
    except Exception as e:
        print(f"!! Database initialization note: {e}")

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(food_bp)
    app.register_blueprint(donor_bp)
    app.register_blueprint(recipient_bp)
    app.register_blueprint(request_bp)
    app.register_blueprint(location_bp)
    app.register_blueprint(algorithm_bp)

    @app.before_request
    def enforce_authentication():
        from flask import session, request, redirect, url_for
        # Allow testing environment to use mock admin session
        if app.config.get('TESTING'):
            if 'user_id' not in session:
                session['role'] = 'admin'
                session['username'] = 'admin'
                session['name'] = 'System Administrator'
                session['user_id'] = 1
            return

        # Public endpoints that do not require login
        public_endpoints = {'auth_bp.login_page', 'auth_bp.register_page', 'static'}
        if request.endpoint in public_endpoints or (request.path and request.path.startswith('/static')):
            return

        # If not logged in, redirect to login page
        if 'user_id' not in session:
            return redirect(url_for('auth_bp.login_page'))

    @app.route('/')
    def dashboard():
        from flask import session, redirect, url_for
        if session.get('role') == 'donor':
            return redirect(url_for('auth_bp.donor_portal'))
        elif session.get('role') == 'receiver':
            return redirect(url_for('auth_bp.receiver_portal'))
        # Compute Dashboard Summary Statistics
        foods = Food.get_all()
        donors = Donor.get_all()
        recipients = Recipient.get_all()
        all_requests = FoodRequest.get_all()
        
        total_food_records = len(foods)
        total_food_quantity = sum(int(f.get('quantity', 0)) for f in foods if f.get('status') == 'Available')
        total_donors = len(donors)
        total_recipients = len(recipients)
        
        pending_requests = [r for r in all_requests if r.get('status') == 'Pending']
        distributed_requests = [r for r in all_requests if r.get('status') == 'Processed']
        
        # Calculate food items expiring today or already expired
        today_str = datetime.date.today().isoformat()
        expiring_today = [f for f in foods if str(f.get('expiry_date')) == today_str]
        
        # Recent operations from Stack
        recent_ops = global_operations_stack.to_list()[:6]
        
        # Top Priority Requests
        top_priority_requests = sorted(pending_requests, key=lambda x: int(x.get('priority', 0)), reverse=True)[:5]

        return render_template('index.html',
                               total_food_records=total_food_records,
                               total_food_quantity=total_food_quantity,
                               total_donors=total_donors,
                               total_recipients=total_recipients,
                               pending_requests_count=len(pending_requests),
                               distributed_count=len(distributed_requests),
                               expiring_today=expiring_today,
                               expiring_count=len(expiring_today),
                               recent_ops=recent_ops,
                               top_priority_requests=top_priority_requests,
                               foods=foods[:5])

    @app.route('/api/dashboard/stats')
    def api_dashboard_stats():
        foods = Food.get_all()
        donors = Donor.get_all()
        recipients = Recipient.get_all()
        all_requests = FoodRequest.get_all()
        today_str = datetime.date.today().isoformat()
        
        return jsonify({
            'status': 'success',
            'stats': {
                'total_food_records': len(foods),
                'available_food_quantity': sum(int(f.get('quantity', 0)) for f in foods if f.get('status') == 'Available'),
                'total_donors': len(donors),
                'total_recipients': len(recipients),
                'pending_requests': len([r for r in all_requests if r.get('status') == 'Pending']),
                'distributed_requests': len([r for r in all_requests if r.get('status') == 'Processed']),
                'expiring_today_count': len([f for f in foods if str(f.get('expiry_date')) == today_str]),
                'stack_operations_count': global_operations_stack.size
            }
        })

    return app

app = create_app()

if __name__ == '__main__':
    # Initial Stack warm-up event
    global_operations_stack.push('SYSTEM_START', 'Food Waste Management System Initialized with Full DSA Suite')
    print("\n=======================================================")
    print(" FOOD WASTE MANAGEMENT SYSTEM (MCA DSA Academic Project)")
    print(" Running locally at: http://127.0.0.1:5000")
    print("=======================================================\n")
    app.run(debug=True, host='0.0.0.0', port=5000)
