from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash
from app.models.db import mysql
from flask_login import login_user, logout_user
from app.models.user_model import User

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email = %s",
            [email]
        )

        user = cursor.fetchone()

        cursor.close()

        if user and check_password_hash(user[3], password):

            logged_user = User(
                user[0],
                user[1],
                user[2]
            )

            login_user(logged_user)

            return redirect('/')

    return render_template('login.html')
@auth.route('/logout')
def logout():

    logout_user()

    return redirect('/login')