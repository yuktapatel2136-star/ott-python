from flask import Blueprint, render_template, redirect, url_for, flash, request, send_from_directory
from app import db
from app.models.models import Movie, Rating, WatchHistory
from flask_login import login_required, current_user
import os

movie_bp = Blueprint('movie', __name__)

@movie_bp.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    return render_template('movie_details.html', movie=movie)

@movie_bp.route('/watch/<int:movie_id>')
@login_required
def watch(movie_id):
    if not current_user.is_subscribed:
        flash('Please subscribe to watch movies!', 'warning')
        return redirect(url_for('movie.subscription'))
    
    movie = Movie.query.get_or_404(movie_id)
    
    # Increment views
    movie.views += 1
    
    # Track history
    history = WatchHistory.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
    if not history:
        history = WatchHistory(user_id=current_user.id, movie_id=movie_id)
        db.session.add(history)
    
    db.session.commit()
    
    return render_template('watch.html', movie=movie, history=history)

@movie_bp.route('/update_resume_point/<int:movie_id>', methods=['POST'])
@login_required
def update_resume_point(movie_id):
    resume_time = request.json.get('resume_time')
    history = WatchHistory.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
    if history and resume_time is not None:
        history.resume_time = resume_time
        db.session.commit()
    return {'status': 'success'}

@movie_bp.route('/download/<int:movie_id>')
@login_required
def download(movie_id):
    if not current_user.is_subscribed:
        flash('Only subscribers can download movies!', 'danger')
        return redirect(url_for('movie.subscription'))
    
    movie = Movie.query.get_or_404(movie_id)
    # For a real app, you'd serve the file. 
    # For a demo, we might just redirect to the URL or show a message.
    flash(f'Download started for {movie.title}!', 'success')
    return redirect(url_for('movie.movie_details', movie_id=movie_id))

@movie_bp.route('/history')
@login_required
def history():
    user_history = WatchHistory.query.filter_by(user_id=current_user.id).order_by(WatchHistory.last_watched.desc()).all()
    return render_template('history.html', history=user_history)

@movie_bp.route('/subscription')
@login_required
def subscription():
    return render_template('subscription.html')

@movie_bp.route('/subscribe', methods=['POST'])
@login_required
def subscribe():
    current_user.is_subscribed = True
    db.session.commit()
    flash('Successfully subscribed!', 'success')
    return redirect(url_for('main.home'))

@movie_bp.route('/rate/<int:movie_id>', methods=['POST'])
@login_required
def rate_movie(movie_id):
    score = request.form.get('score')
    if score:
        existing_rating = Rating.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
        if existing_rating:
            existing_rating.score = score
        else:
            new_rating = Rating(score=score, user_id=current_user.id, movie_id=movie_id)
            db.session.add(new_rating)
        db.session.commit()
        flash('Thank you for rating!', 'info')
    return redirect(url_for('movie.movie_details', movie_id=movie_id))
