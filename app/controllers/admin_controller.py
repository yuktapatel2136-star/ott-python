from app.models.category_model import Category
from app import db

def get_dashboard_data():
    total_categories = Category.query.count()
    return {"total_categories": total_categories}

def get_all_categories_admin():
    return Category.query.all()

def create_category(name, image):
    category = Category(name=name, image=image)
    db.session.add(category)
    db.session.commit()

def get_category_by_id(id):
    return Category.query.get(id)

def edit_category_data(id, name, image):
    category = Category.query.get(id)
    if category:
        category.name = name
        category.image = image
        db.session.commit()

def remove_category(id):
    category = Category.query.get(id)
    if category:
        db.session.delete(category)
        db.session.commit()