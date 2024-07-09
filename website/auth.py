from flask import Blueprint, render_template, redirect, request, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__)

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == 'POST':
        # Get form data and convert email and matric_no to lowercase
        matric_no = request.form.get("matric_no").lower()
        full_name = request.form.get("full_name")
        phone_number = request.form.get("phone_number")
        email = request.form.get("email").lower()
        password = request.form.get("password")

        # Validate form data
        if not all([matric_no, full_name, phone_number, email, password]):
            flash('Please fill in all the fields.', 'error')
            return redirect(url_for('auth.signup'))

        # Check if the email is already registered
        if User.find_by_email(email):
            flash('Email is already registered. Please use a different email.', 'error')
            return redirect(url_for('auth.signup'))

        # Check if the matric_no is already registered
        if User.find_by_matric_no(matric_no):
            flash('Matric number is already registered. Please use a different matric number.', 'error')
            return redirect(url_for('auth.signup'))

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Create new user
        new_user = User(matric_no=matric_no, full_name=full_name, phone_number=phone_number, email=email, password=hashed_password)
        new_user.save()

        flash('Account created successfully! You can now log in.', 'success')
        return redirect(url_for("auth.login"))

    return render_template('register.html')


@auth.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        # Get form data and convert matric_no to lowercase
        matric_no = request.form["matric_no"].lower()
        password = request.form["password"]
        
        # Query user
        user = User.find_by_matric_no(matric_no)

        if user and check_password_hash(user['password'], password):
            login_user(User(user['matric_no'], user['full_name'], user['phone_number'], user['email'], user['password']))
            flash('Login successful!', 'success')
            return redirect(url_for('views.index'))
        else:
            flash('Invalid credentials. Please try again.', 'error')

    return render_template('login.html')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
