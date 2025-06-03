
from flask import Flask, render_template, request, redirect, url_for, jsonify
from models import db, ShakhaLocation
from auth import valid_auth_codes

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db/shakha.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

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

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # ✅ Auto-creates the DB if it doesn't exist
    app.run(debug=True)

