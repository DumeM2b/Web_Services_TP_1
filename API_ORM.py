from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
from random import randint
from datetime import datetime, timedelta
import requests

# Initialize Flask application
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://root:root@localhost:5432/postgres"  # Database configuration
db = SQLAlchemy(app)  # Initialize SQLAlchemy extension for database management
fake = Faker()  # Initialize Faker extension for generating fake data

# Define Users model for the users table
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    firstname = db.Column(db.String(100))
    lastname = db.Column(db.String(100))
    age = db.Column(db.Integer)
    email = db.Column(db.String(100))
    job = db.Column(db.String(100))
    applications = db.relationship('Application', backref='users', lazy=True)

    def __init__(self, firstname, lastname, age, email, job):
        """Initialize a Users object.

        Args:
            firstname (str): The first name of the user.
            lastname (str): The last name of the user.
            age (int): The age of the user.
            email (str): The email address of the user.
            job (str): The job title of the user.
        """
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.email = email
        self.job = job

# Define Application model for the applications table
class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    appname = db.Column(db.String(100))
    username = db.Column(db.String(100))
    lastconnection = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, appname, username, lastconnection, user_id):
        """Initialize an Application object.

        Args:
            appname (str): The name of the application.
            username (str): The username associated with the application.
            lastconnection (datetime): The last connection time of the application.
            user_id (int): The ID of the user associated with the application.
        """
        self.appname = appname
        self.username = username
        self.lastconnection = lastconnection
        self.user_id = user_id

# Route to populate the database with random data
@app.route('/populate')
def populate():
    """Populate the Users and Application tables with random data."""
    db.session.begin()
    for _ in range(10):
        firstname = fake.first_name()
        lastname = fake.last_name()
        age = randint(18, 65)
        email = fake.email()
        job = fake.job()
        user = Users(firstname=firstname, lastname=lastname, age=age, email=email, job=job)
        db.session.add(user)
    
    for user in Users.query.all():
        for _ in range(randint(1, 5)):
            appname = fake.company()
            username = fake.user_name()
            lastconnection = fake.date_time_between(start_date='-30d', end_date='now')
            application = Application(appname=appname, username=username, lastconnection=lastconnection, user_id=user.id)
            db.session.add(application)
    
    db.session.commit()
    return 'Data generated successfully!'

# Route to get and add users
@app.route('/user', methods=['GET', 'POST'])
def user():
    """Route to get and add users."""
    if request.method == 'GET':
        users = Users.query.all()
        users_list = []
        for user in users:
            user_data = {
                'id': user.id,
                'firstname': user.firstname,
                'lastname': user.lastname,
                'age': user.age,
                'email': user.email,
                'job': user.job
            }
            users_list.append(user_data)
        return jsonify(users_list)
    elif request.method == 'POST':
        data = request.json
        firstname = data['firstname']
        lastname = data['lastname']
        age = data['age']
        email = data['email']
        job = data['job']
        new_user = Users(firstname=firstname, lastname=lastname, age=age, email=email, job=job)
        db.session.add(new_user)
        db.session.commit()
        return jsonify({'message': 'User added successfully'})

# Route for the home page
@app.route('/home')
def home():
    """Route for the home page."""
    # Get user data from the Flask API
    response = requests.get('http://localhost:5000/user')

    users = response.json()

    return render_template('home.html', users=users)

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        populate()
    app.run(debug=True)
