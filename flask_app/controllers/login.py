from flask_app import app
from flask import render_template, redirect, session, request, flash

from flask_app.models.users import User

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/users/register', methods=['POST'])
def register_user():
    if User.validate_registration(request.form):

        data = {
            'first_name': request.form['first_name'],
            'last_name': request.form['last_name'],
            'email': request.form['email'],
            'password': bcrypt.generate_password_hash(request.form['password'])
        }

        User.create_user(data)
        return redirect('/')
    #creates user if data is valid then redirects
    return redirect('/')


@app.route('/users/login', methods=['POST'])
def login_user():
    users = User.get_users_with_email(request.form)

    if len(users) != 1:
        flash("User with the given email does not exists")
        return redirect ('/')

    user = users[0]

    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Password for the given user is not right")
        return redirect ('/')

    session ['user_id'] = user.id
    session['user_first_name'] = user.first_name
    session['user_last_name'] = user.last_name

    return redirect('/paintings')


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
