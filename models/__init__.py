from main import db
from sqlalchemy.sql import func

class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name= db.Column(db.String(100), nullable=False)
    last_name= db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(80), unique=True ,nullable=False)
    date_of_birth = db.Column(db.Date(), nullable=False)
    bio = db.Column(db.String(500))
    password = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())
    updated_at = db.Column(db.DateTime(timezone=True), server_default=func.now())