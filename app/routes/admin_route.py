from flask import Blueprint, render_template, redirect, url_for
from app.forms.category_form import CategoryForm
from app.controllers.admin_controller import *

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")

@admin_bp.route("/dashboard")
def dashboard():
    data = get_dashboard_data()
    return render_template("admin/dashboard.html", data=data)

@admin_bp.route("/categories")
def category_list():
    categories = get_all_categories_admin()
    return render_template("admin/category_list.html", categories=categories)

@admin_bp.route("/category/add", methods=["GET", "POST"])
def add_category():
    form = CategoryForm()
    if form.validate_on_submit():
        create_category(form.name.data, form.image.data)
        return redirect(url_for("admin.category_list"))
    return render_template("admin/add_category.html", form=form)

@admin_bp.route("/category/edit/<int:id>", methods=["GET", "POST"])
def edit_category(id):
    category = get_category_by_id(id)
    form = CategoryForm(obj=category)

    if form.validate_on_submit():
        edit_category_data(id, form.name.data, form.image.data)
        return redirect(url_for("admin.category_list"))

    return render_template("admin/edit_category.html", form=form)

@admin_bp.route("/category/delete/<int:id>")
def delete_category(id):
    remove_category(id)
    return redirect(url_for("admin.category_list"))