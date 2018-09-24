# coding: utf-8
# Python imports.
from flask import Flask, flash, Blueprint, render_template, request, redirect, url_for, session
from passlib.hash import bcrypt
from flask_login import LoginManager, current_user, login_user, logout_user

# Local imports.
from forms import *
from models import *

# Values.
urls_blueprint = Blueprint("urls", __name__,)

# Routes.
# Index.
@urls_blueprint.route('/')
def index():
    return render_template('home.html') 

# Exams.
@urls_blueprint.route('/exam')
def exam():
    return render_template('home.html')

# Functions.
# Adding values to database.
def add_to_database(table_data):
    # Check for model, add data to object, save to database.
    pass

# Add exam.
@urls_blueprint.route('/add_exam', methods=['GET','POST'])
def add_exam():
    form = examForm(request.form)

    if request.method == 'POST' and form.validate():
        course_name = form.course_name.data
        course_code = form.course_code.data
        university = form.university.data
        semester = form.semester.data
        amountOfQuestions = form.questions.data

        ex = Exam(course_name = course_name, course_code = course_code, university = university, semester = semester)
        db.session.add(ex)
        return redirect('/add_questions')
    
    return render_template('add_exam.html', examForm = form)

# Register user.
@urls_blueprint.route('/register', methods=['GET', 'POST'])
def register():
    form = registerForm(request.form)

    if request.method == 'POST' and form.validate():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        bcrypt_password = bcrypt.encrypt(password)

        # Creating user.
        user = User(username = username, email = email, password = bcrypt_password)
        
        db.session.add(user)
        db.session.commit()

        flash('You are now registered and can log in', 'success')

        return redirect('/')
    
    return render_template('register.html', registerForm=form)

# User login.
@urls_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('/'))

    form = loginForm(request.form)
    
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        
        if user is None or not user.check_password(form.password.data):    
            flash('Invalid username or password')
            return redirect(url_for('login'))
        
        login_user(user, remember=form.remember_me.data)
        
        return redirect(url_for('/'))
    
    return render_template('login.html', title='Sign In', loginForm=form)

# User logout.
@urls_blueprint.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('/'))
