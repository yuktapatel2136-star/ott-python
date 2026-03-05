from app import db

class Category(db.Model):
    __bind_key__ = "category_db"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    image = db.Column(db.String(200))