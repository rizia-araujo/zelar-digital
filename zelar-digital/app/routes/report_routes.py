from flask import Blueprint, render_template, request, redirect, current_app, flash, url_for
from app.models.db import mysql
from flask_login import login_required, current_user
import os
from werkzeug.utils import secure_filename
import uuid
from datetime import datetime

reports = Blueprint('reports', __name__)


def _fetch_report_stats(cursor):
    cursor.execute("SELECT COUNT(*) AS total FROM reports")
    total = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM reports WHERE status = 'recebido'")
    received = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM reports WHERE status = 'em andamento'")
    progress = cursor.fetchone()["total"]

    cursor.execute("SELECT COUNT(*) AS total FROM reports WHERE status = 'resolvido'")
    resolved = cursor.fetchone()["total"]

    return {
        "total": total,
        "received": received,
        "progress": progress,
        "resolved": resolved,
    }

@reports.route("/")
def home():
    cursor = mysql.connection.cursor()

    cursor.execute(
        """
        SELECT
            id,
            title,
            description,
            image,
            latitude,
            longitude,
            status,
            created_at
        FROM reports
        ORDER BY created_at DESC
        LIMIT 4
        """
    )
    recent_reports = cursor.fetchall()
    stats = _fetch_report_stats(cursor)
    cursor.close()

    return render_template(
        "index.html",
        recent_reports=recent_reports,
        stats=stats
    )

@reports.route("/create-report", methods=["GET", "POST"])
@login_required
def create_report():
    if request.method == "POST":
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        latitude = request.form.get("latitude", "").strip()
        longitude = request.form.get("longitude", "").strip()
        image = request.files.get("image")

        if not title or not description or not latitude or not longitude or not image:
            flash("Preencha todos os campos e selecione uma imagem.", "error")
            return render_template("create_report.html")

        filename = secure_filename(image.filename)
        extension = os.path.splitext(filename)[1].lower()
        unique_name = f"{uuid.uuid4().hex}_{datetime.utcnow().strftime('%Y%m%d%H%M%S')}{extension}"
        upload_folder = os.path.join(current_app.root_path, "app", "static", "uploads")
        os.makedirs(upload_folder, exist_ok=True)
        image_path = os.path.join(upload_folder, unique_name)
        image.save(image_path)

        cursor = mysql.connection.cursor()
        cursor.execute(
            """
            INSERT INTO reports
            (title, description, image, latitude, longitude, status, user_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            """,
            (title, description, unique_name, latitude, longitude, "recebido", current_user.id)
        )
        mysql.connection.commit()
        cursor.close()

        flash("Ocorrência enviada com sucesso.", "success")
        return redirect(url_for("reports.list_reports"))

    return render_template("create_report.html")

@reports.route("/reports")
def list_reports():
    status_filter = request.args.get("status", "").strip()

    cursor = mysql.connection.cursor()

    query = """
        SELECT
            id,
            title,
            description,
            image,
            latitude,
            longitude,
            status,
            created_at
        FROM reports
    """
    params = []

    if status_filter:
        query += " WHERE status = %s"
        params.append(status_filter)

    query += " ORDER BY created_at DESC"

    cursor.execute(query, params)
    reports_data = cursor.fetchall()

    cursor.execute("SELECT COUNT(*) AS total FROM reports")
    total = cursor.fetchone()["total"]
    cursor.close()

    return render_template(
        "reports.html",
        reports=reports_data,
        total_reports=total,
        active_status=status_filter
    )