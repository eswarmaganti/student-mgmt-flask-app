from wtforms import Form, StringField, EmailField, validators, DateField,PasswordField, TextAreaField

# schema class for Register student
class RegisterStudentForm(Form):
    first_name = StringField('first_name',[validators.Length(min=2, max=50), validators.DataRequired()])
    last_name = StringField('last_name',[validators.Length(min=2, max=50), validators.DataRequired()])
    email = EmailField('email', [validators.Length(min=6,max=50), validators.Email(),validators.DataRequired()])
    date_of_birth = DateField('date_of_birth' ,format="%Y-%m-%d")
    bio = TextAreaField('bio',[validators.Length(min=4), validators.DataRequired()])
    password = PasswordField("password",[validators.Length(min=6, max=30), validators.DataRequired()])
    confirm_password  = PasswordField("confirm_password",[validators.EqualTo('password')])


# Schema for edit student
class EditStudentForm(Form):
    first_name = StringField('first_name', [validators.Length(min=2, max=50), validators.DataRequired()])
    last_name = StringField('last_name', [validators.Length(min=2, max=50), validators.DataRequired()])
    email = EmailField('email', [validators.Length(min=6, max=50), validators.Email(), validators.DataRequired()])
    date_of_birth = DateField('date_of_birth', format="%Y-%m-%d")
    bio = TextAreaField('bio', [validators.Length(min=4), validators.DataRequired()])

# schema for search student
class SearchStudentForm(Form):
    student_name = StringField("student_name", [validators.Length(min=2, max=50), validators.DataRequired()])