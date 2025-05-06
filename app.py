from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import configparser
import os

# Read configuration
config = configparser.ConfigParser()
config.read('config.ini')

app = Flask(__name__)
db_config = config['database']
app.config['SQLALCHEMY_DATABASE_URI'] = f"mysql://{db_config['db_user']}:{db_config['db_password']}@{db_config['db_host']}/{db_config['db_name']}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(50), nullable=False)
    lastname = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    phone_type = db.Column(db.String(10), nullable=False)  # home/work/mobile
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'firstname': self.firstname,
            'lastname': self.lastname,
            'email': self.email,
            'phone': self.phone,
            'phone_type': self.phone_type,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }

@app.route('/')
def index():
    contacts = Contact.query.all()
    return render_template('index.html', contacts=contacts)

@app.route('/add', methods=['GET', 'POST'])
def add_contact():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        phone = request.form['phone']
        phone_type = request.form['phone_type']

        new_contact = Contact(
            firstname=firstname,
            lastname=lastname,
            email=email,
            phone=phone,
            phone_type=phone_type
        )

        try:
            db.session.add(new_contact)
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f"An error occurred: {str(e)}"

    return render_template('add.html')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_contact(id):
    contact = Contact.query.get_or_404(id)
    
    if request.method == 'POST':
        contact.firstname = request.form['firstname']
        contact.lastname = request.form['lastname']
        contact.email = request.form['email']
        contact.phone = request.form['phone']
        contact.phone_type = request.form['phone_type']

        try:
            db.session.commit()
            return redirect(url_for('index'))
        except Exception as e:
            return f"An error occurred: {str(e)}"

    return render_template('edit.html', contact=contact)

# API Endpoints
@app.route('/api/contacts', methods=['GET'])
def get_contacts():
    # Get query parameters
    search = request.args.get('search', '')
    phone_type = request.args.get('phone_type', '')
    sort_by = request.args.get('sort_by', 'firstname')
    sort_order = request.args.get('sort_order', 'asc')
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    # Start with base query
    query = Contact.query

    # Apply search filter if provided
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            db.or_(
                Contact.firstname.ilike(search_term),
                Contact.lastname.ilike(search_term),
                Contact.email.ilike(search_term),
                Contact.phone.ilike(search_term)
            )
        )

    # Apply phone type filter if provided
    if phone_type:
        query = query.filter(Contact.phone_type == phone_type)

    # Apply sorting
    if sort_order == 'desc':
        query = query.order_by(getattr(Contact, sort_by).desc())
    else:
        query = query.order_by(getattr(Contact, sort_by).asc())

    # Apply pagination
    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    contacts = pagination.items

    # Prepare response
    response = {
        'contacts': [contact.to_dict() for contact in contacts],
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total': pagination.total,
            'pages': pagination.pages
        }
    }

    return jsonify(response)

@app.route('/api/contacts/<int:id>', methods=['GET'])
def get_contact(id):
    contact = Contact.query.get_or_404(id)
    return jsonify(contact.to_dict())

@app.route('/api/contacts', methods=['POST'])
def create_contact():
    data = request.get_json()
    
    try:
        new_contact = Contact(
            firstname=data['firstname'],
            lastname=data['lastname'],
            email=data['email'],
            phone=data['phone'],
            phone_type=data['phone_type']
        )
        db.session.add(new_contact)
        db.session.commit()
        return jsonify(new_contact.to_dict()), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/contacts/<int:id>', methods=['PUT'])
def update_contact(id):
    contact = Contact.query.get_or_404(id)
    data = request.get_json()
    
    try:
        contact.firstname = data.get('firstname', contact.firstname)
        contact.lastname = data.get('lastname', contact.lastname)
        contact.email = data.get('email', contact.email)
        contact.phone = data.get('phone', contact.phone)
        contact.phone_type = data.get('phone_type', contact.phone_type)
        
        db.session.commit()
        return jsonify(contact.to_dict())
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/contacts/<int:id>', methods=['DELETE'])
def delete_contact(id):
    contact = Contact.query.get_or_404(id)
    try:
        db.session.delete(contact)
        db.session.commit()
        return '', 204
    except Exception as e:
        return jsonify({'error': str(e)}), 400

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True) 