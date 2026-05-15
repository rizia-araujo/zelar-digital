from flask import Blueprint, render_template, request, redirect
from werkzeug.security import generate_password_hash
from app.models.db import mysql

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=['GET', 'POST'])
def register():

    if request.method == 'POST':

        username = request.form['username']
        email = request.form['email']
        password = generate_password_hash(request.form['password'])

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            INSERT INTO users(username, email, password)
            VALUES(%s, %s, %s)
            """,
            (username, email, password)
        )

        mysql.connection.commit()
        cursor.close()

        return redirect('/login')

    return render_template('register.html')
from werkzeug.security import check_password_hash

@auth.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':

        email = request.form['email']
        password = request.form['password']

        cursor = mysql.connection.cursor()

        cursor.execute(
            "SELECT * FROM users WHERE email=%s",
            [email]
        )

        user = cursor.fetchone()

        cursor.close()

        if user and check_password_hash(user[3], password):
            return redirect('/')

    return render_template('login.html')