from flask import session, redirect, url_for, flash
from flask_httpauth import HTTPBasicAuth
from functools import wraps

auth = HTTPBasicAuth()

USERS = {
    "admin": "adminadmin",
}

@auth.verify_password
def verify_password(username, password):
    if username in USERS and USERS[username] == password:
        session['logged_in'] = True
        return username
    return None

def logout():
    session.pop('logged_in', None)

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            flash("Please log in to access the admin page", 'warning')
            return redirect(url_for('routes.login'))
        return f(*args, **kwargs)
    return decorated_function



