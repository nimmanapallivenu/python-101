"""
Complete Flask REST API Example
A production-ready user management API with CRUD operations
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
from datetime import datetime
from functools import wraps
import jwt
import uuid

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-change-in-production'
CORS(app)

# In-memory database (replace with real database in production)
users_db = {}
tokens_db = set()  # Store valid tokens

# Sample data
users_db['1'] = {
    'id': '1',
    'username': 'admin',
    'email': 'admin@example.com',
    'password': 'admin123',  # In production, use hashed passwords!
    'role': 'admin',
    'created_at': datetime.utcnow().isoformat()
}

users_db['2'] = {
    'id': '2',
    'username': 'user1',
    'email': 'user1@example.com',
    'password': 'user123',
    'role': 'user',
    'created_at': datetime.utcnow().isoformat()
}


# ============================================================================
# AUTHENTICATION DECORATOR
# ============================================================================

def token_required(f):
    """Decorator to protect routes with JWT authentication"""
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        
        # Get token from header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({'error': 'Invalid token format'}), 401
        
        if not token:
            return jsonify({'error': 'Token is missing'}), 401
        
        if token not in tokens_db:
            return jsonify({'error': 'Token is invalid or expired'}), 401
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
            current_user = users_db.get(data['user_id'])
            
            if not current_user:
                return jsonify({'error': 'User not found'}), 401
                
        except jwt.ExpiredSignatureError:
            return jsonify({'error': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'error': 'Invalid token'}), 401
        
        return f(current_user, *args, **kwargs)
    
    return decorated


def admin_required(f):
    """Decorator to require admin role"""
    @wraps(f)
    @token_required
    def decorated(current_user, *args, **kwargs):
        if current_user.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403
        return f(current_user, *args, **kwargs)
    
    return decorated


# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def validate_user_data(data, required_fields=None):
    """Validate user data"""
    if required_fields is None:
        required_fields = ['username', 'email', 'password']
    
    errors = {}
    
    for field in required_fields:
        if field not in data or not data[field]:
            errors[field] = f'{field} is required'
    
    if 'email' in data and '@' not in data['email']:
        errors['email'] = 'Invalid email format'
    
    if 'password' in data and len(data['password']) < 6:
        errors['password'] = 'Password must be at least 6 characters'
    
    return errors


def user_to_dict(user, include_password=False):
    """Convert user object to dictionary (exclude password by default)"""
    user_dict = user.copy()
    if not include_password and 'password' in user_dict:
        del user_dict['password']
    return user_dict


# ============================================================================
# AUTHENTICATION ROUTES
# ============================================================================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    # Validate input
    errors = validate_user_data(data)
    if errors:
        return jsonify({'error': 'Validation failed', 'details': errors}), 400
    
    # Check if username already exists
    for user in users_db.values():
        if user['username'] == data['username']:
            return jsonify({'error': 'Username already exists'}), 400
        if user['email'] == data['email']:
            return jsonify({'error': 'Email already exists'}), 400
    
    # Create new user
    user_id = str(uuid.uuid4())
    new_user = {
        'id': user_id,
        'username': data['username'],
        'email': data['email'],
        'password': data['password'],  # Hash in production!
        'role': data.get('role', 'user'),
        'created_at': datetime.utcnow().isoformat()
    }
    
    users_db[user_id] = new_user
    
    return jsonify({
        'message': 'User registered successfully',
        'user': user_to_dict(new_user)
    }), 201


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Login and get JWT token"""
    data = request.get_json()
    
    if not data or 'username' not in data or 'password' not in data:
        return jsonify({'error': 'Username and password required'}), 400
    
    # Find user
    user = None
    for u in users_db.values():
        if u['username'] == data['username']:
            user = u
            break
    
    if not user or user['password'] != data['password']:
        return jsonify({'error': 'Invalid credentials'}), 401
    
    # Generate JWT token
    token = jwt.encode({
        'user_id': user['id'],
        'username': user['username'],
        'role': user['role'],
        'exp': datetime.utcnow().timestamp() + 3600  # 1 hour expiry
    }, app.config['SECRET_KEY'], algorithm='HS256')
    
    tokens_db.add(token)
    
    return jsonify({
        'message': 'Login successful',
        'token': token,
        'user': user_to_dict(user)
    }), 200


@app.route('/api/auth/logout', methods=['POST'])
@token_required
def logout(current_user):
    """Logout and invalidate token"""
    token = request.headers['Authorization'].split(' ')[1]
    tokens_db.discard(token)
    
    return jsonify({'message': 'Logout successful'}), 200


@app.route('/api/auth/me', methods=['GET'])
@token_required
def get_current_user(current_user):
    """Get current authenticated user"""
    return jsonify(user_to_dict(current_user)), 200


# ============================================================================
# USER CRUD ROUTES
# ============================================================================

@app.route('/api/users', methods=['GET'])
@token_required
def get_users(current_user):
    """Get all users (paginated)"""
    # Query parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    search = request.args.get('search', '', type=str)
    
    # Filter users
    filtered_users = []
    for user in users_db.values():
        if search.lower() in user['username'].lower() or search.lower() in user['email'].lower():
            filtered_users.append(user_to_dict(user))
    
    # Pagination
    total = len(filtered_users)
    start = (page - 1) * per_page
    end = start + per_page
    paginated_users = filtered_users[start:end]
    
    return jsonify({
        'users': paginated_users,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': total,
            'pages': (total + per_page - 1) // per_page
        }
    }), 200


@app.route('/api/users/<user_id>', methods=['GET'])
@token_required
def get_user(current_user, user_id):
    """Get user by ID"""
    user = users_db.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Users can only view their own profile unless admin
    if current_user['id'] != user_id and current_user['role'] != 'admin':
        return jsonify({'error': 'Access denied'}), 403
    
    return jsonify(user_to_dict(user)), 200


@app.route('/api/users/<user_id>', methods=['PUT'])
@token_required
def update_user(current_user, user_id):
    """Update user"""
    user = users_db.get(user_id)
    
    if not user:
        return jsonify({'error': 'User not found'}), 404
    
    # Users can only update their own profile unless admin
    if current_user['id'] != user_id and current_user['role'] != 'admin':
        return jsonify({'error': 'Access denied'}), 403
    
    data = request.get_json()
    
    # Validate
    errors = validate_user_data(data, required_fields=[])
    if errors:
        return jsonify({'error': 'Validation failed', 'details': errors}), 400
    
    # Update fields
    if 'username' in data:
        user['username'] = data['username']
    if 'email' in data:
        user['email'] = data['email']
    if 'password' in data:
        user['password'] = data['password']  # Hash in production!
    
    # Only admin can change role
    if 'role' in data and current_user['role'] == 'admin':
        user['role'] = data['role']
    
    user['updated_at'] = datetime.utcnow().isoformat()
    
    return jsonify({
        'message': 'User updated successfully',
        'user': user_to_dict(user)
    }), 200


@app.route('/api/users/<user_id>', methods=['DELETE'])
@admin_required
def delete_user(current_user, user_id):
    """Delete user (admin only)"""
    if user_id not in users_db:
        return jsonify({'error': 'User not found'}), 404
    
    # Prevent deleting yourself
    if current_user['id'] == user_id:
        return jsonify({'error': 'Cannot delete your own account'}), 400
    
    del users_db[user_id]
    
    return jsonify({'message': 'User deleted successfully'}), 200


# ============================================================================
# UTILITY ROUTES
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'message': 'API is running',
        'timestamp': datetime.utcnow().isoformat(),
        'users_count': len(users_db)
    }), 200


@app.route('/api/stats', methods=['GET'])
@admin_required
def get_stats(current_user):
    """Get API statistics (admin only)"""
    return jsonify({
        'total_users': len(users_db),
        'active_tokens': len(tokens_db),
        'users_by_role': {
            'admin': sum(1 for u in users_db.values() if u['role'] == 'admin'),
            'user': sum(1 for u in users_db.values() if u['role'] == 'user')
        }
    }), 200


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Resource not found'}), 404


@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad request'}), 400


@app.errorhandler(500)
def internal_error(error):
    return jsonify({'error': 'Internal server error'}), 500


@app.errorhandler(Exception)
def handle_exception(error):
    """Handle unexpected exceptions"""
    app.logger.error(f'Unhandled exception: {str(error)}')
    return jsonify({'error': 'An unexpected error occurred'}), 500


# ============================================================================
# MAIN
# ============================================================================

if __name__ == '__main__':
    print("=" * 60)
    print("Flask REST API Server")
    print("=" * 60)
    print("\nEndpoints:")
    print("  POST   /api/auth/register  - Register new user")
    print("  POST   /api/auth/login     - Login and get token")
    print("  POST   /api/auth/logout    - Logout")
    print("  GET    /api/auth/me        - Get current user")
    print("  GET    /api/users          - Get all users")
    print("  GET    /api/users/<id>     - Get user by ID")
    print("  PUT    /api/users/<id>     - Update user")
    print("  DELETE /api/users/<id>     - Delete user (admin)")
    print("  GET    /api/health         - Health check")
    print("  GET    /api/stats          - API statistics (admin)")
    print("\nDefault credentials:")
    print("  Username: admin")
    print("  Password: admin123")
    print("\nServer running on http://localhost:5000")
    print("=" * 60)
    
    app.run(debug=True, host='0.0.0.0', port=5000)

# Made with Bob
