from flask import Blueprint, render_template
from app.controllers.category_controller import get_all_categories

category_bp = Blueprint("category", __name__)

@category_bp.route("/")
def home():
    return render_template("index.html")

@category_bp.route("/category")
def category_page():
    categories = get_all_categories()
    return render_template("category.html", categories=categories)