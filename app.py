from bottle import Bottle, static_file, run, template, request
import json

app = Bottle()

@app.route('/')
def home():
    print("In Home: ")
    total_credits = 0
    gpa = 0
    return template('home', total_credits=total_credits, gpa=gpa)

@app.route('/save', method='POST')
def save():
    courses = request.forms.getall('course')
    credits = request.forms.getall('credits')
    grades = request.forms.getall('grade')

    grade_points = {
        'A+': 4.0, 'A': 4.0, 'A-': 3.7,
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

    return template('home', total_credits=total_credits, gpa=gpa)

@app.route('/subjects.json')
def serve_subjects():
    return static_file('subjects.json', root='./')

@app.route('/favicon.ico')
def serve_favicon():
    return static_file('favicon.ico', root='./static')

if __name__ == '__main__':
    run(app = app, port=8080, debug=True, reloader=True)