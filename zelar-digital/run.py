from flask import Flask
from dotenv import load_dotenv
from flask_login import LoginManager
from app.models.db import mysql
from app.models.user_model import User
import os

load_dotenv()

app = Flask(__name__)

app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

mysql.init_app(app)

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)
@login_manager.user_loader
def load_user(user_id):

    cursor = mysql.connection.cursor()

    cursor.execute(
        "SELECT * FROM users WHERE id = %s",
        [user_id]
    )

    user = cursor.fetchone()

    cursor.close()

    if user:
        return User(user[0], user[1], user[2])

    return None

from app.routes.auth_routes import auth
from app.routes.report_routes import reports

app.register_blueprint(auth)
app.register_blueprint(reports)

if __name__ == '__main__':
    app.run(debug=True) 