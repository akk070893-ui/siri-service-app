import os
from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
import uuid
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

ADMIN_USER = os.getenv('ADMIN_USER', 'admin')
ADMIN_PASS = os.getenv('ADMIN_PASS', 'siriadmin123')  # change this in production!

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY', 'change_this_secret')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///database.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Complaint(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    customer_name = db.Column(db.String(100))
    contact_number = db.Column(db.String(20))
    item_name = db.Column(db.String(100))
    accessories = db.Column(db.String(200))
    complaint = db.Column(db.String(500))
    estimation = db.Column(db.String(100))
    in_date = db.Column(db.String(50))
    status = db.Column(db.String(50), default="Pending")
    public_link = db.Column(db.String(100), unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

@app.before_first_request
def create_tables():
    db.create_all()

@app.route('/')
def index():
    # admin view will show all; public index shows form + recent entries limited
    return render_template('index.html')

@app.route('/new', methods=['GET', 'POST'])
def new_complaint():
    if request.method == 'POST':
        uid = str(uuid.uuid4())[:8]
        c = Complaint(
            customer_name=request.form.get('customer_name'),
            contact_number=request.form.get('contact_number'),
            item_name=request.form.get('item_name'),
            accessories=request.form.get('accessories'),
            complaint=request.form.get('complaint'),
            estimation=request.form.get('estimation'),
            in_date=request.form.get('in_date'),
            public_link=uid
        )
        db.session.add(c)
        db.session.commit()
        link = url_for('complaint_status', uid=uid, _external=True)
        return render_template('created.html', link=link)
    return render_template('complaint_form.html')

@app.route('/status/<uid>')
def complaint_status(uid):
    complaint = Complaint.query.filter_by(public_link=uid).first()
    if complaint:
        return render_template('status_page.html', complaint=complaint)
    return render_template('not_found.html'), 404

# --- Simple admin auth ---
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if username == ADMIN_USER and password == ADMIN_PASS:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        flash('Invalid credentials', 'danger')
    return render_template('admin_login.html')

@app.route('/admin/logout')
def admin_logout():
    session.pop('admin', None)
    return redirect(url_for('admin_login'))

def admin_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('admin'):
            return redirect(url_for('admin_login'))
        return f(*args, **kwargs)
    return decorated

@app.route('/admin')
@admin_required
def admin_dashboard():
    complaints = Complaint.query.order_by(Complaint.created_at.desc()).all()
    return render_template('admin_dashboard.html', complaints=complaints)

@app.route('/admin/edit/<int:c_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit(c_id):
    c = Complaint.query.get_or_404(c_id)
    if request.method == 'POST':
        c.status = request.form.get('status')
        c.estimation = request.form.get('estimation')
        db.session.commit()
        flash('Updated successfully', 'success')
        return redirect(url_for('admin_dashboard'))
    return render_template('admin_edit.html', complaint=c)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)))
