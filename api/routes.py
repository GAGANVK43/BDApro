"""
routes.py - Flask Web Page View Routes
Renders Jinja2 HTML templates for each section of the analytics platform.
"""

from flask import Blueprint, render_template

views_bp = Blueprint("views", __name__)


@views_bp.route("/")
@views_bp.route("/dashboard")
def dashboard_view():
    """Main Executive Analytics Dashboard."""
    return render_template("dashboard.html", active_page="dashboard")


@views_bp.route("/genres")
def genres_view():
    """Genre Distribution & Analytics."""
    return render_template("genres.html", active_page="genres")


@views_bp.route("/ratings")
def ratings_view():
    """Maturity & Content Rating Patterns."""
    return render_template("ratings.html", active_page="ratings")


@views_bp.route("/releases")
def releases_view():
    """Historical Release Trends & Timeline."""
    return render_template("releases.html", active_page="releases")


@views_bp.route("/countries")
def countries_view():
    """Geographic & Country Distribution."""
    return render_template("countries.html", active_page="countries")


@views_bp.route("/movies")
def movies_view():
    """Interactive Movie Explorer & Metadata Modal."""
    return render_template("movies.html", active_page="movies")


@views_bp.route("/pipeline")
def pipeline_view():
    """Big Data Pipeline & System Health Monitor."""
    return render_template("pipeline.html", active_page="pipeline")


@views_bp.route("/database")
def database_view():
    """MongoDB Atlas Collections & Database Architecture."""
    return render_template("database.html", active_page="database")


@views_bp.route("/about")
def about_view():
    """About Project, Architecture & Faculty Viva Voce Guide."""
    return render_template("about.html", active_page="about")
