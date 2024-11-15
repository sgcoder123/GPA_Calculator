from bottle import Bottle, static_file, run, template, request, redirect
import json
import os

app = Bottle()
DATA_FILE = 'grades.json'

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file, indent=4)

@app.route('/login')
def login():
    email = request.query.email or None
    return template('login', error=None, email=email)

@app.route('/login', method='POST')
def do_login():
    email = request.forms.get('email')
    if email:
        redirect(f'/?email={email}')
    else:
        return template('login', error="Email is required")

@app.route('/subjects.json')
def subjects():
    return static_file('subjects.json', root='.')

@app.route('/')
def home():
    email = request.query.email
    if not email:
        redirect('/login')
    
    total_credits = 0
    gpa = 0
    data = load_data()
    return template('home', total_credits=total_credits, gpa=gpa, data=data, email=email)
@app.route('/user_info')
def user_info():
    email = request.query.email
    if not email:
        redirect('/login')
    
    data = load_data()
    user_data = [entry for entry in data if entry.get('email') == email]
    
    print("User Data:", user_data)  # Debugging line
    
    gpa = user_data[0].get('gpa') if user_data else None
    
    return template('user_info', data=user_data, email=email, gpa=gpa)

@app.route('/save', method='POST')
def save():
    email = request.query.email
    courses = request.forms.getall('course')
    credits = request.forms.getall('credits')
    grades = request.forms.getall('grade')

    grade_points = {
        'A+': 4.3, 'A': 4.0, 'A-': 3.7,
        'B+': 3.3, 'B': 3.0, 'B-': 2.7,
        'C+': 2.3, 'C': 2.0, 'C-': 1.7,
        'D+': 1.3, 'D': 1.0, 'F': 0.0
    }

    total_credits = 0
    total_points = 0

    for course, credit, grade in zip(courses, credits, grades):
        credit = float(credit)
        total_credits += credit
        total_points += credit * grade_points[grade]

    gpa = total_points / total_credits if total_credits > 0 else 0
    gpa = round(gpa, 2)  # Limit GPA to 2 decimal places

    # Load existing data
    data = load_data()

    # Append new data
    data.append({
        'email': email,
        'courses': courses,
        'credits': credits,
        'grades': grades,
        'total_credits': total_credits,
        'gpa': gpa
    })

    # Save updated data
    save_data(data)

    return template('home', total_credits=total_credits, gpa=gpa, data=data, email=email)

if __name__ == '__main__':
    run(app=app, port=8080, debug=True, reloader=True)