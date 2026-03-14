from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from app import db
from app.models.models import Movie, User, Category, SubscriptionPlan
from flask_login import login_required, current_user
from functools import wraps
import os
from werkzeug.utils import secure_filename

admin_bp = Blueprint('admin', __name__)

def allowed_image(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_IMAGE_EXTENSIONS']

def allowed_video(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_VIDEO_EXTENSIONS']

def save_file(file, folder):
    """Save uploaded file to specified folder and return filename."""
    filename = secure_filename(file.filename)
    os.makedirs(folder, exist_ok=True)
    filepath = os.path.join(folder, filename)
    file.save(filepath)
    return filename

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Admin access required.', 'danger')
            return redirect(url_for('main.home'))
        return f(*args, **kwargs)
    return decorated_function

@admin_bp.route('/admin/')
@login_required
@admin_required
def dashboard():
    total_movies = Movie.query.count()
    total_users = User.query.count()
    categories = Category.query.all()
    movies = Movie.query.all()
    users = User.query.all()
    
    # Simple metrics
    most_watched = Movie.query.order_by(Movie.views.desc()).limit(5).all()
    subscribed_users = User.query.filter_by(is_subscribed=True).count()
    simulated_revenue = subscribed_users * 499 
    
    # Calculate percentage safely
    sub_percent = round((subscribed_users / total_users * 100), 1) if total_users > 0 else 0
    
    return render_template('admin/dashboard.html', 
                         total_movies=total_movies, 
                         total_users=total_users,
                         subscribed_users=subscribed_users,
                         sub_percent=sub_percent,
                         simulated_revenue=simulated_revenue,
                         most_watched=most_watched,
                         categories=categories,
                         movies=movies, 
                         users=users)

@admin_bp.route('/admin/add_movie', methods=['GET', 'POST'])
@login_required
@admin_required
def add_movie():
    categories = Category.query.all()
    if request.method == 'POST':
        title = request.form.get('title')
        description = request.form.get('description')
        category_id = request.form.get('category_id')
        language = request.form.get('language')
        year = request.form.get('year')
        is_featured = 'is_featured' in request.form
        is_trending = 'is_trending' in request.form
        
        # Handle image upload
        thumbnail = ''
        image_file = request.files.get('image_file')
        if image_file and image_file.filename != '':
            if allowed_image(image_file.filename):
                filename = save_file(image_file, current_app.config['UPLOAD_FOLDER_IMAGES'])
                thumbnail = url_for('static', filename=f'images/{filename}')
            else:
                flash('Invalid image format! Allowed: png, jpg, jpeg, gif, webp', 'danger')
                return render_template('admin/add_movie.html', categories=categories)

        # Handle video upload
        video_url = ''
        video_file = request.files.get('video_file')
        if video_file and video_file.filename != '':
            if allowed_video(video_file.filename):
                filename = save_file(video_file, current_app.config['UPLOAD_FOLDER_VIDEOS'])
                video_url = url_for('static', filename=f'videos/{filename}')
            else:
                flash('Invalid video format! Allowed: mp4, webm, mkv, avi', 'danger')
                return render_template('admin/add_movie.html', categories=categories)

        if not thumbnail or not video_url:
            flash('Please upload both a poster image and a video file!', 'warning')
            return render_template('admin/add_movie.html', categories=categories)
        
        cat = Category.query.get(category_id)
        
        new_movie = Movie(
            title=title, 
            description=description, 
            video_url=video_url, 
            thumbnail=thumbnail, 
            category_id=category_id,
            category_name=cat.name if cat else "Uncategorized",
            language=language,
            release_year=year,
            is_featured=is_featured,
            is_trending=is_trending
        )
        db.session.add(new_movie)
        db.session.commit()
        flash(f'"{title}" added successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
        
    return render_template('admin/add_movie.html', categories=categories)

@admin_bp.route('/admin/edit_movie/<int:movie_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_movie(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    categories = Category.query.all()
    if request.method == 'POST':
        movie.title = request.form.get('title')
        movie.description = request.form.get('description')
        movie.category_id = request.form.get('category_id')
        movie.language = request.form.get('language')
        movie.release_year = request.form.get('year')
        movie.is_featured = 'is_featured' in request.form
        movie.is_trending = 'is_trending' in request.form
        
        # Handle new image upload (optional - keep existing if none uploaded)
        image_file = request.files.get('image_file')
        if image_file and image_file.filename != '':
            if allowed_image(image_file.filename):
                filename = save_file(image_file, current_app.config['UPLOAD_FOLDER_IMAGES'])
                movie.thumbnail = url_for('static', filename=f'images/{filename}')
            else:
                flash('Invalid image format!', 'danger')
                return render_template('admin/edit_movie.html', movie=movie, categories=categories)

        # Handle new video upload (optional - keep existing if none uploaded)
        video_file = request.files.get('video_file')
        if video_file and video_file.filename != '':
            if allowed_video(video_file.filename):
                filename = save_file(video_file, current_app.config['UPLOAD_FOLDER_VIDEOS'])
                movie.video_url = url_for('static', filename=f'videos/{filename}')
            else:
                flash('Invalid video format!', 'danger')
                return render_template('admin/edit_movie.html', movie=movie, categories=categories)
        
        cat = Category.query.get(movie.category_id)
        movie.category_name = cat.name if cat else "Uncategorized"
        
        db.session.commit()
        flash(f'"{movie.title}" updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))
        
    return render_template('admin/edit_movie.html', movie=movie, categories=categories)

@admin_bp.route('/admin/delete_movie/<int:movie_id>')
@login_required
@admin_required
def delete_movie(movie_id):
    from app.models.models import WatchHistory, Rating
    movie = Movie.query.get_or_404(movie_id)
    title = movie.title
    
    # Delete related records first
    WatchHistory.query.filter_by(movie_id=movie_id).delete()
    Rating.query.filter_by(movie_id=movie_id).delete()
    
    db.session.delete(movie)
    db.session.commit()
    flash(f'"{title}" deleted successfully!', 'info')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/admin/categories', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_categories():
    if request.method == 'POST':
        name = request.form.get('name')
        type = request.form.get('type')
        if name:
            new_cat = Category(name=name, type=type)
            db.session.add(new_cat)
            db.session.commit()
            flash('Category added!', 'success')
    
    categories = Category.query.all()
    return render_template('admin/categories.html', categories=categories)

@admin_bp.route('/admin/delete_category/<int:cat_id>')
@login_required
@admin_required
def delete_category(cat_id):
    cat = Category.query.get_or_404(cat_id)
    db.session.delete(cat)
    db.session.commit()
    flash('Category deleted!', 'info')
    return redirect(url_for('admin.manage_categories'))

# ── User Management ──────────────────────────────────────────────────────────

@admin_bp.route('/admin/edit_user/<int:user_id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        email    = request.form.get('email', '').strip()
        role     = request.form.get('role', 'user')
        is_subscribed = 'is_subscribed' in request.form

        # Check uniqueness (exclude current user)
        existing_username = User.query.filter(User.username == username, User.id != user_id).first()
        existing_email    = User.query.filter(User.email == email,    User.id != user_id).first()

        if existing_username:
            flash('Username already taken by another user.', 'danger')
            return render_template('admin/edit_user.html', user=user)
        if existing_email:
            flash('Email already in use by another user.', 'danger')
            return render_template('admin/edit_user.html', user=user)

        user.username     = username
        user.email        = email
        user.role         = role
        user.is_subscribed = is_subscribed

        # Optional password reset
        new_password = request.form.get('new_password', '').strip()
        if new_password:
            user.set_password(new_password)

        db.session.commit()
        flash(f'User "{user.username}" updated successfully!', 'success')
        return redirect(url_for('admin.dashboard'))

    return render_template('admin/edit_user.html', user=user)


@admin_bp.route('/admin/delete_user/<int:user_id>')
@login_required
@admin_required
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Aap apna account delete nahi kar sakte!', 'warning')
        return redirect(url_for('admin.dashboard'))
    username = user.username
    db.session.delete(user)
    db.session.commit()
    flash(f'User "{username}" deleted successfully!', 'info')
    return redirect(url_for('admin.dashboard'))
