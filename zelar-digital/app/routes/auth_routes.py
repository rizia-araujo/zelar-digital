from flask import Blueprint, render_template, request, redirect, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from ..models.db import mysql
from flask_login import login_user, logout_user, current_user
from ..models.user_model import User
auth = Blueprint("auth", __name__)

@auth.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("reports.home"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE email = %s", [email])
        user = cursor.fetchone()
        cursor.close()

        if user and check_password_hash(user["password"], password):
            logged_user = User(user["id"], user["username"], user["email"])
            login_user(logged_user)
            flash("Bem-vindo de volta!", "success")
            return redirect(url_for("reports.home"))

        flash("Email ou senha inválidos.", "error")

    return render_template("login.html")

@auth.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("reports.home"))

    if request.method == "POST":
        username = request.form.get("username", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        if len(username) < 3:
            flash("Informe um nome com pelo menos 3 caracteres.", "error")
            return render_template("register.html")

        if len(password) < 6:
            flash("A senha deve ter pelo menos 6 caracteres.", "error")
            return render_template("register.html")

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT id FROM users WHERE email = %s", [email])
        existing = cursor.fetchone()

        if existing:
            cursor.close()
            flash("Esse email já está cadastrado.", "error")
            return render_template("register.html")

        hashed_password = generate_password_hash(password)
        cursor.execute(
            "INSERT INTO users (username, email, password) VALUES (%s, %s, %s)",
            (username, email, hashed_password)
        )
        mysql.connection.commit()
        cursor.close()

        flash("Conta criada com sucesso. Faça login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")

@auth.route("/logout")
def logout():
    logout_user()
    flash("Você saiu da sua conta.", "success")
    return redirect(url_for("auth.login"))
