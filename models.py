from sqlalchemy import Integer, String, Column, Boolean
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

class Exam(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    ##university = db.Column(db.String(120), nullable=False)
    #semester = db.Column(db.String(120), nullable=False)
    questions = db.relationship('Question', backref='exam')

    def __repr__(self):
        return '<ID %r, Kurs %r>' % (self.id, self.name)

class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), unique=True, nullable=False)
    answers = db.relationship('Answer', backref='question', lazy=True)
    exam_id = db.Column(db.Integer, db.ForeignKey('exam.id'))

class Answer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(300), unique=True, nullable=False)
    correct = db.Column(db.Boolean, default=False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))