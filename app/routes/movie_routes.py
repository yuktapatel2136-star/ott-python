from flask import Blueprint, render_template, redirect, url_for, flash, request, send_from_directory
from app import db
from app.models.models import Movie, Rating, WatchHistory, WatchList
from flask_login import login_required, current_user
from datetime import date, timedelta
import os

movie_bp = Blueprint('movie', __name__)

# ── Plan configuration ────────────────────────────────────────────────────────
PLANS = {
    'free': {
        'name': 'Free',
        'price': 0,
        'duration_days': None,
        'features': [
            'Limited movies & shows',
            'SD quality (480p)',
            'Ads supported',
            '1 device at a time',
        ],
        'can_watch_premium': False,
        'color': 'secondary',
        'icon': 'fa-tv',
    },
    'basic': {
        'name': 'Basic',
        'price': 199,
        'duration_days': 30,
        'features': [
            'All movies & shows',
            'HD quality (1080p)',
            'Ad-free experience',
            '2 devices at a time',
        ],
        'can_watch_premium': True,
        'color': 'primary',
        'icon': 'fa-star',
    },
    'premium': {
        'name': 'Premium',
        'price': 499,
        'duration_days': 30,
        'features': [
            'Everything in Basic',
            '4K UHD Streaming',
            'Dolby Atmos Audio',
            '4 devices at a time',
            'Offline Downloads',
            'Early access to new releases',
        ],
        'can_watch_premium': True,
        'color': 'danger',
        'icon': 'fa-crown',
    },
}

# ── Helpers ───────────────────────────────────────────────────────────────────

def user_can_watch():
    """Check whether the current authenticated user has an active subscription."""
    return current_user.subscription_plan in ('basic', 'premium') and current_user.plan_is_active


# ── Movie Routes ──────────────────────────────────────────────────────────────

@movie_bp.route('/movie/<int:movie_id>')
def movie_details(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    is_in_watchlist = False
    if current_user.is_authenticated:
        is_in_watchlist = WatchList.query.filter_by(user_id=current_user.id, movie_id=movie_id).first() is not None
    return render_template('movie_details.html', movie=movie, is_in_watchlist=is_in_watchlist)


@movie_bp.route('/watch/<int:movie_id>')
@login_required
def watch(movie_id):
    movie = Movie.query.get_or_404(movie_id)

    if movie.is_premium and not user_can_watch():
        flash('Yeh content dekhne ke liye pehle subscribe karein! Please subscribe to continue.', 'warning')
        return redirect(url_for('movie.subscription'))

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
    plan = current_user.subscription_plan
    if plan not in ('basic', 'premium') or not current_user.plan_is_active:
        flash('Downloads ke liye Basic ya Premium plan lena hoga! Please subscribe first.', 'warning')
        return redirect(url_for('movie.subscription'))

    movie = Movie.query.get_or_404(movie_id)
    flash(f'Download started for "{movie.title}"!', 'success')
    return redirect(url_for('movie.movie_details', movie_id=movie_id))


@movie_bp.route('/history')
@login_required
def history():
    user_history = WatchHistory.query.filter_by(user_id=current_user.id).order_by(WatchHistory.last_watched.desc()).all()
    return render_template('history.html', history=user_history)


@movie_bp.route('/watchlist')
@login_required
def watchlist():
    user_watchlist = WatchList.query.filter_by(user_id=current_user.id).order_by(WatchList.date_added.desc()).all()
    return render_template('watchlist.html', watchlist=user_watchlist)


@movie_bp.route('/toggle_watchlist/<int:movie_id>', methods=['POST'])
@login_required
def toggle_watchlist(movie_id):
    watchlist_item = WatchList.query.filter_by(user_id=current_user.id, movie_id=movie_id).first()
    if watchlist_item:
        db.session.delete(watchlist_item)
        db.session.commit()
        return {'status': 'removed', 'message': 'Removed from Watch List'}
    else:
        new_watchlist_item = WatchList(user_id=current_user.id, movie_id=movie_id)
        db.session.add(new_watchlist_item)
        db.session.commit()
        return {'status': 'added', 'message': 'Added to Watch List'}


# ── Subscription Routes ───────────────────────────────────────────────────────

@movie_bp.route('/subscription')
@login_required
def subscription():
    return render_template('subscription.html', plans=PLANS, current_plan=current_user.subscription_plan, today=date.today())


@movie_bp.route('/subscribe', methods=['POST'])
@login_required
def subscribe():
    """Legacy endpoint — redirects to new plan-based flow."""
    return redirect(url_for('movie.subscription'))


@movie_bp.route('/checkout/<plan_key>', methods=['GET'])
@login_required
def checkout(plan_key):
    if plan_key not in PLANS or plan_key == 'free':
        flash('Invalid plan selected.', 'danger')
        return redirect(url_for('movie.subscription'))
    plan = PLANS[plan_key]
    return render_template('payment.html', plan=plan, plan_key=plan_key)


@movie_bp.route('/process_payment/<plan_key>', methods=['POST'])
@login_required
def process_payment(plan_key):
    if plan_key not in PLANS or plan_key == 'free':
        flash('Invalid plan.', 'danger')
        return redirect(url_for('movie.subscription'))

    # Simulate payment validation (demo only)
    card_number = request.form.get('card_number', '').replace(' ', '')
    expiry     = request.form.get('expiry', '')
    cvv        = request.form.get('cvv', '')
    name       = request.form.get('name', '').strip()

    errors = []
    if len(card_number) < 12:
        errors.append('Enter a valid card number (min 12 digits).')
    if not expiry:
        errors.append('Enter a valid expiry date.')
    if len(cvv) < 3:
        errors.append('Enter a valid CVV (min 3 digits).')
    if not name:
        errors.append('Cardholder name is required.')

    if errors:
        for e in errors:
            flash(e, 'danger')
        return redirect(url_for('movie.checkout', plan_key=plan_key))

    plan = PLANS[plan_key]
    today = date.today()

    # Activate subscription
    current_user.subscription_plan    = plan_key
    current_user.subscription_start   = today
    current_user.subscription_end     = today + timedelta(days=plan['duration_days'])
    current_user.is_subscribed        = True  

    db.session.commit()

    flash(
        f'Welcome to {plan["name"]} Plan! Your subscription is active until '
        f'{current_user.subscription_end.strftime("%d %b %Y")}.',
        'success'
    )
    return redirect(url_for('main.home'))


@movie_bp.route('/cancel_subscription', methods=['POST'])
@login_required
def cancel_subscription():
    flash('Subscription cancellation is not allowed in this project.', 'warning')
    return redirect(url_for('movie.subscription'))


# ── Rating ────────────────────────────────────────────────────────────────────

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
