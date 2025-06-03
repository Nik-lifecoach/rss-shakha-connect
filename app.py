
from flask import Flask, render_template, request, redirect, url_for, jsonify, session, flash
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.secret_key = "super_secret_admin_key"

# Setup SQLite database
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, 'shakha.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class ShakhaLocation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    state = db.Column(db.String(100))
    district = db.Column(db.String(100))
    city = db.Column(db.String(100))
    basti = db.Column(db.String(100))
    shakha_name = db.Column(db.String(100))
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)

# Auth codes
valid_auth_codes = ['123456', '654321', '112233']

@app.route('/')
def index():
    shakhas = ShakhaLocation.query.all()
    return render_template('index.html', shakhas=shakhas)

@app.route('/add', methods=['GET', 'POST'])
def add_location():
    if request.method == 'POST':
        code = request.form['auth_code']
        if code not in valid_auth_codes:
            return "Unauthorized: Invalid Code", 403
        data = request.form
        new_location = ShakhaLocation(
            state=data['state'],
            district=data['district'],
            city=data['city'],
            basti=data['basti'],
            shakha_name=data['shakha'],
            latitude=data['latitude'],
            longitude=data['longitude']
        )
        db.session.add(new_location)
        db.session.commit()
        return redirect('/')
    return render_template('add_location.html')

@app.route('/get_location/<int:id>')
def get_location(id):
    loc = ShakhaLocation.query.get(id)
    return jsonify({
        'state': loc.state,
        'district': loc.district,
        'city': loc.city,
        'basti': loc.basti,
        'shakha': loc.shakha_name,
        'lat': loc.latitude,
        'lng': loc.longitude
    })

@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin123':
            session['admin'] = True
            return redirect('/admin/dashboard')
        else:
            flash("Invalid credentials", "danger")
            return redirect('/admin/login')
    return render_template('admin_login.html')

@app.route('/admin/dashboard')
def admin_dashboard():
    if not session.get('admin'):
        return redirect('/admin/login')
    shakhas = ShakhaLocation.query.all()
    return render_template('admin_dashboard.html', shakhas=shakhas)

@app.route('/admin/edit/<int:id>', methods=['GET', 'POST'])
def admin_edit(id):
    if not session.get('admin'):
        return redirect('/admin/login')
    loc = ShakhaLocation.query.get_or_404(id)
    if request.method == 'POST':
        loc.state = request.form['state']
        loc.district = request.form['district']
        loc.city = request.form['city']
        loc.basti = request.form['basti']
        loc.shakha_name = request.form['shakha']
        loc.latitude = request.form['latitude']
        loc.longitude = request.form['longitude']
        db.session.commit()
        flash("Location updated successfully.", "success")
        return redirect('/admin/dashboard')
    return render_template('admin_edit.html', location=loc)

@app.route('/admin/delete/<int:id>')
def admin_delete(id):
    if not session.get('admin'):
        return redirect('/admin/login')
    loc = ShakhaLocation.query.get_or_404(id)
    db.session.delete(loc)
    db.session.commit()
    flash("Location deleted successfully.", "success")
    return redirect('/admin/dashboard')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)
