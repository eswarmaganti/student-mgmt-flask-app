import traceback
import bcrypt
from flask import Flask, render_template, request, redirect, url_for
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date
from schemas import RegisterStudentForm, EditStudentForm, SearchStudentForm


# create a flask app
app = Flask(__name__)
# database connectivity
db_path = Path().cwd() / 'db/database.db'

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + str(db_path)

db = SQLAlchemy(app)

# importing the models after db is initialized
from models import Student

# defining the routes for the application

'''
method: GET
route: /
description: Index route for flask application
'''
@app.get("/")
def index():
    student_count = Student.query.count()
    return render_template('index.html', page_heading='Dashboard', student_count=student_count, total_courses=10)

'''
method: GET, POST
route: /add_student
description: route to create a new student in database
'''
@app.route('/add_student', methods=('GET','POST'))
def add_student():
    form = RegisterStudentForm(request.form)

    if request.method == 'POST' and form.validate():
        try:
            # mapping the data from request form
            first_name: str = request.form.get('first_name', '').strip()
            last_name: str = request.form.get('last_name', '').strip()
            email: str = request.form.get('email', '').strip()
            date_of_birth: datetime = datetime.strptime(request.form.get('date_of_birth').strip(),'%Y-%m-%d')
            bio: str = request.form.get('bio', '').strip()
            password: str = request.form.get('password','').strip()

            hashed_pass = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            student = Student(first_name=first_name,last_name=last_name,email=email,date_of_birth=date_of_birth,bio=bio,password=hashed_pass)
            db.session.add(student)
            db.session.commit()
            return render_template('add_student.html',page_heading="Add a New Student", form=form, status="success")
        except Exception as e:
            traceback.print_exc()
            return render_template('add_student.html',page_heading="Add a New Student", form=form, status="error")

    return render_template('add_student.html', page_heading="Add a New Student",form=form )


'''
method: GET
route: /view_student
description: route to view the particular student details
'''
@app.get('/view_student/<int:student_id>')
def view_student(student_id):
    student = Student.query.filter_by(id=student_id).first()
    return render_template('view_student.html', page_heading='View Student Details', student=student)



'''
method: GET
route: /get_students
description: Route to display all students details
'''
@app.get('/get_students')
def get_students():
    try:
        # querying all the students
        students = Student.query.all()

        # table headings
        headings = ('ID', 'First Name', 'Last Name', 'Email','Date of Birth' ,'View', 'Action')

        # rendering the template
        return render_template('students.html',page_heading='Students Details', headings=headings, students=students)
    except Exception as e:
        traceback.print_exc()
        print(f'*** Error: Something went wrong while querying the student details from DB: {str(e)} ***')


'''
method: GET, PUT
route: /edit_student/{student_id}
description: route to handle the edit functionality of students
'''
@app.route('/edit_student/<int:student_id>', methods=('GET','POST'))
def edit_student(student_id):

    student = Student.query.get_or_404(student_id)
    form = EditStudentForm(request.form)

    if request.method == 'POST' and form.validate():
        try:
            # updating the existing student details
            student.first_name = request.form.get('first_name','')
            student.last_name = request.form.get('last_name','')
            student.email = request.form.get('email')
            student.date_of_birth = datetime.strptime(request.form.get('date_of_birth'), '%Y-%m-%d')
            student.bio = request.form.get('bio')
            student.updated_at = datetime.now()

            # commiting the changes
            db.session.commit()

            # redirect to students page
            return render_template('edit_student.html', page_heading='Edit Student Details', student=student, status="success", form=form)
        except Exception as e:
            traceback.print_exc()
            return render_template('edit_student.html', page_heading='Edit Student Details', student=student, status="error", form=form)


    return render_template('edit_student.html', page_heading='Edit Student Details', student=student, form=form)


'''
method: DELETE
route: /delete_student/<int: student_id>
description: route to delete a student details from database
'''
@app.post('/delete_student/<int:student_id>')
def delete_student(student_id):
    student = Student.query.get_or_404(student_id)
    db.session.delete(student)
    db.session.commit()
    return redirect(url_for('get_students'))

@app.route('/search_students', methods=('GET','POST'))
def search_students():

    form = SearchStudentForm(request.form)
    if request.method == "POST" and form.validate():
        student_name = request.form.get('student_name','')
        students = Student.query.filter(Student.first_name.like(f'{student_name}%')).all()
        print(students)
        return  render_template('search_students.html', students=students, form=form)
    return render_template('search_students.html', form=form)


if __name__ == "__main__":
    app.run(host="0.0.0.0", PORT="8000")