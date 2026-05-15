from flask import Blueprint, render_template, request, redirect
from app.models.db import mysql
from flask_login import login_required, current_user
import os

reports = Blueprint('reports', __name__)


@reports.route('/')
def home():
    return render_template('index.html')


@reports.route('/create-report', methods=['GET', 'POST'])
@login_required
def create_report():

    if request.method == 'POST':

        title = request.form['title']
        description = request.form['description']
        latitude = request.form['latitude']
        longitude = request.form['longitude']

        image = request.files['image']

        image_path = os.path.join(
            'app/static/uploads',
            image.filename
        )

        image.save(image_path)

        cursor = mysql.connection.cursor()

        cursor.execute(
            """
            INSERT INTO reports
            (
                title,
                description,
                image,
                latitude,
                longitude,
                status,
                user_id
            )
            VALUES(%s, %s, %s, %s, %s, %s, %s)
            """,
            (
                title,
                description,
                image.filename,
                latitude,
                longitude,
                'recebido',
                current_user.id
            )
        )

        mysql.connection.commit()
        cursor.close()

        return redirect('/')

    return render_template('create_report.html')