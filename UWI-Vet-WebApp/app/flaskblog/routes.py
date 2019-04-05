from flask import render_template, url_for, flash, redirect, request, jsonify
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, EvaluateForm, StudentSearchForm, RotationForm #StudentRegForm
from flaskblog.models import User, Post, Comp, Student
from flask_login import login_user, current_user, logout_user, login_required
import flask_excel as excel

posts = [

    {
        'author': 'Corey Schfer',
        'title': 'Note 1',
        'content': 'First Persons Content',
        'date_posted': 'April 20, 2018'
    },
    {
        'title': 'Note 2',
        'content': 'Second Persons Content',
        'date_posted': 'April 21, 2018'
    },

]
@app.before_first_request
def setup():
    db.Model.metadata.create_all(bind=db.engine)

@app.route("/")

@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

@app.route("/about", methods=['GET', 'POST'])
def about():
    if request.method == 'POST':
        def comp_init_func(row):
            c = Comp(row['Code'],row['Rotation Name'], row['Description'])
            return c
            
        request.save_to_database(
            field_name ='file', session=db.session,
            table=Comp,
            initializer=comp_init_func)
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful, Please check email and Password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account.html')

@app.route("/competancy")
@login_required
def competancy():
    return render_template('competancy.html', title='Competancy.html')

@app.route("/rotations", methods=['GET'])
@login_required
def rotations():
    records = Comp.query.all()
    return render_template('rotations.html', title='Rotations.html', Comp=records)

@app.route("/evaluate", methods=['GET', 'POST'])
@login_required
def evaluate():
    form = EvaluateForm()
    if form.validate_on_submit():
        return redirect(url_for('home'))
    return render_template('evaluate.html', title='Evaluate.html', form=form)

@app.route("/students", methods=['GET', 'POST'])
@login_required
def students():
    #form = StudentSearchForm()
    if request.method == 'POST':
        def stu_init_func(row):
            s = Student(row['id'],row['Student Name'], row['Date Enrolled'], row['Email'])
            return s
            
        request.save_to_database(
            field_name ='file', session=db.session,
            table=Student,
            initializer=stu_init_func)
    records = Student.query.all()
    return render_template('students.html', title='Students.html', Student=records)

@app.route("/reports")
@login_required
def reports():
    return render_template('reports.html', title='Reports.html')

@app.route("/reminders")
@login_required
def reminders():
    return render_template('reminders.html', title='Reminders.html')

@app.route("/studentRecord")
@login_required
def studentRecord():
    return render_template('studentRecord.html', title='studentRecord.html')