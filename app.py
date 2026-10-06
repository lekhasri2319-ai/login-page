
from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from werkzeug.security import check_password_hash, generate_password_hash
import os
 
app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this-in-production'
 
# User database (Dictionary for faster lookup)
VALID_USERS = {
    "lekha": 'lekha2319',
    "sam": 'sam1909',
    "mega": 'mega1234',    
    "thiloth": 'thiloth0987',
}
 
@app.route('/')
def index():
    """Redirect to login if not authenticated"""
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))
 
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username', '').strip()
        password = data.get('password', '').strip()
        
        
        if not username or not password:
            return jsonify({'success': False, 'message': 'Username and password required'}), 400
        
        # Check credentials
        if username in VALID_USERS and VALID_USERS[username] == password:
            session['username'] = username
            return jsonify({'success': True, 'message': 'Login successful!'})
        else:
            return jsonify({'success': False, 'message': 'Invalid username or password'}), 401
    
    return render_template('login.html')
 
@app.route('/dashboard')
def dashboard():
    """Dashboard page - only accessible after login"""
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])
 
@app.route('/logout')
def logout():
    """Logout user"""
    session.clear()
    return redirect(url_for('login'))
 
@app.route('/api/profile')
def get_profile():
    """Get user profile data"""
    if 'username' not in session:
        return jsonify({'success': False, 'message': 'Not authenticated'}), 401
    
    return jsonify({
        'success': True,
        'username': session['username'],
        'login_time': request.headers.get('Date', 'N/A')
    })
 
if __name__ == '__main__':
    app.run(debug=True, host='localhost', port=5000)
 
