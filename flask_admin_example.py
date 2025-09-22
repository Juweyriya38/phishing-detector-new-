"""
Flask Admin System Example
Complete admin system with login, dashboard, user management, and trash pages
"""

from flask import Flask, render_template, request, redirect, url_for, flash, session
from functools import wraps
import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Change this in production

# Sample data (replace with database in production)
ADMIN_CREDENTIALS = {
    'admin': 'admin123',
    'superadmin': 'super456'
}

SAMPLE_USERS = [
    {'id': 1, 'username': 'john_doe', 'email': 'john@example.com', 'is_active': True},
    {'id': 2, 'username': 'jane_smith', 'email': 'jane@example.com', 'is_active': True},
    {'id': 3, 'username': 'bob_wilson', 'email': 'bob@example.com', 'is_active': False},
]

SAMPLE_DELETED_USERS = [
    {
        'id': 10, 
        'username': 'deleted_user', 
        'email': 'deleted@example.com',
        'deleted_reason': 'admin',
        'deleted_at': datetime.datetime.now() - datetime.timedelta(days=5),
        'profile_image_url': None
    },
]

SAMPLE_STATS = {
    'total_users': len(SAMPLE_USERS),
    'reports': 25,
    'active_links': 12,
    'trash_items': len(SAMPLE_DELETED_USERS)
}

# Admin authentication decorator
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'admin_logged_in' not in session:
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated_function

# Routes
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in ADMIN_CREDENTIALS and ADMIN_CREDENTIALS[username] == password:
            session['admin_logged_in'] = True
            session['admin_username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('admin_home'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('admin_login.html')

@app.route('/admin/logout')
@admin_required
def admin_logout():
    session.clear()
    flash('You have been logged out', 'success')
    return redirect(url_for('admin_login'))

@app.route('/admin')
@app.route('/admin/home')
@admin_required
def admin_home():
    return render_template('admin_home_flask.html', stats=SAMPLE_STATS)

@app.route('/admin/users')
@admin_required
def admin_users():
    return render_template('admin_users_flask.html', users=SAMPLE_USERS)

@app.route('/admin/users/<int:user_id>/edit')
@admin_required
def admin_edit_user(user_id):
    # In a real app, you'd fetch the user from database and show edit form
    flash(f'Edit user {user_id} functionality would go here', 'info')
    return redirect(url_for('admin_users'))

@app.route('/admin/users/<int:user_id>/delete', methods=['POST'])
@admin_required
def admin_delete_user(user_id):
    # In a real app, you'd move user to trash/deleted_users table
    global SAMPLE_USERS
    SAMPLE_USERS = [u for u in SAMPLE_USERS if u['id'] != user_id]
    flash(f'User {user_id} has been deleted', 'success')
    return redirect(url_for('admin_users'))

@app.route('/admin/trash')
@admin_required
def admin_trash():
    return render_template('admin_trash_flask.html', deleted_users=SAMPLE_DELETED_USERS)

# Error handlers
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)