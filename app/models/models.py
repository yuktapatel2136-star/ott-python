from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime, date
from werkzeug.security import generate_password_hash, check_password_hash

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(10), default='user')  # 'admin' or 'user'

    # Subscription fields
    is_subscribed = db.Column(db.Boolean, default=False)  # kept for backward compat
    subscription_plan = db.Column(db.String(20), default='free')  # 'free', 'basic', 'premium'
    subscription_start = db.Column(db.Date, nullable=True)
    subscription_end = db.Column(db.Date, nullable=True)

    # Relationships
    ratings = db.relationship('Rating', backref='author', lazy=True, cascade='all, delete-orphan')
    watch_history = db.relationship('WatchHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    watch_list = db.relationship('WatchList', backref='user', lazy=True, cascade='all, delete-orphan')

    @property
    def plan_is_active(self):
        """Returns True if the user has an active paid subscription."""
        if self.subscription_plan in ('basic', 'premium') and self.subscription_end:
            return date.today() <= self.subscription_end
        return False

    @property
    def plan_label(self):
        """Human-readable plan badge label."""
        if self.plan_is_active:
            return self.subscription_plan.capitalize()
        return 'Free'

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)
    type = db.Column(db.String(20)) # genre, language, year
    movies = db.relationship('Movie', backref='category_rel', lazy=True)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    video_url = db.Column(db.String(200), nullable=False) 
    thumbnail = db.Column(db.String(200), nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category_name = db.Column(db.String(50)) # For backward compatibility/simplicity
    language = db.Column(db.String(30))
    release_year = db.Column(db.Integer)
    is_featured = db.Column(db.Boolean, default=False)
    is_trending = db.Column(db.Boolean, default=False)
    is_premium = db.Column(db.Boolean, default=False)  # Requires at least Basic plan
    views = db.Column(db.Integer, default=0)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    ratings = db.relationship('Rating', backref='movie', lazy=True, cascade='all, delete-orphan')
    watch_history = db.relationship('WatchHistory', backref='movie', lazy=True, cascade='all, delete-orphan')
    watch_list = db.relationship('WatchList', backref='movie', lazy=True, cascade='all, delete-orphan')

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)

class WatchHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    resume_time = db.Column(db.Float, default=0.0)
    last_watched = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class SubscriptionPlan(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    duration_days = db.Column(db.Integer, nullable=False)

class WatchList(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)
