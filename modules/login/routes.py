from flask import Blueprint, render_template, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, login_required, logout_user, current_user
from app import db, login_manager, admin
from modules.login.forms import LoginForm, RegisForm
from modules.login.user import User

login_bp = Blueprint('login_bp',__name__,static_folder='static',template_folder='templates')

# Sign in route
@login_bp.route('/login', methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('user_bp.dashboard'))
        

    # Creates a login form and validates the form. If the form is validated, then validate from DB
    logForm = LoginForm()
    if logForm.validate_on_submit():
        # Checks to see if user in DB
        user = User.query.filter_by(userN=logForm.userN.data).first()
        if user:
            # Checks the password through werkzeug hash
            if check_password_hash(user.passW, logForm.passW.data):
                # Logs in the user
                login_user(user, remember=logForm.rememberBox.data)
                return redirect(url_for('user_bp.dashboard'))

        flash('Invalid Credentials')

    return render_template('login.html', form=logForm)


# Registration route
@login_bp.route('/signup', methods=['GET', 'POST'])
def signup():

    if current_user.is_authenticated:
        return redirect(url_for('user_bp.dashboard'))

    # Creates a registration form and validates the form. If form is validated then submit to DB
    regForm = RegisForm()
    if regForm.validate_on_submit():
        existing_user = User.query.filter_by(userN=regForm.userN.data).first()
        if existing_user is None:
            existing_user = User.query.filter_by(email=regForm.email.data).first()
            if existing_user is None:
                # Generate a hash Password
                # hashed_pass = generate_password_hash(regForm.passW.data, method='sha256')

                new_user = User(userN=regForm.userN.data, email=regForm.email.data, passW=regForm.passW.data, isAdmin=False)
                db.session.add(new_user)
                db.session.commit()

                return render_template('success.html')
            else:
                flash('Email is already used')
        else:
            flash('That user name is already taken')


    return render_template('signup.html', form=regForm)

@login_bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))