from app.models.category_model import Category

def get_all_categories():
    return Category.query.all()