from flask import Blueprint, render_template, request
from app.models.models import Movie, Category

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
@main_bp.route('/home')
def home():
    featured = Movie.query.filter_by(is_featured=True).all()
    trending = Movie.query.filter_by(is_trending=True).all()
    latest = Movie.query.order_by(Movie.date_added.desc()).limit(10).all()
    categories = Category.query.all()
    
    # Get user's watchlist IDs for initial icon state
    watchlist_ids = []
    from flask_login import current_user
    if current_user.is_authenticated:
        from app.models.models import WatchList
        watchlist_ids = [item.movie_id for item in WatchList.query.filter_by(user_id=current_user.id).all()]
    
    # Simple search
    search_query = request.args.get('search')
    if search_query:
        latest = Movie.query.filter(Movie.title.contains(search_query)).all()
        return render_template('search_results.html', movies=latest, query=search_query, watchlist_ids=watchlist_ids)

    return render_template('home.html', 
                         featured=featured, 
                         trending=trending, 
                         latest=latest,
                         categories=categories,
                         watchlist_ids=watchlist_ids)

@main_bp.route('/category/<int:cat_id>')
def category_filter(cat_id):
    category = Category.query.get_or_404(cat_id)
    movies = Movie.query.filter_by(category_id=cat_id).all()
    
    # Get user's watchlist IDs
    watchlist_ids = []
    from flask_login import current_user
    if current_user.is_authenticated:
        from app.models.models import WatchList
        watchlist_ids = [item.movie_id for item in WatchList.query.filter_by(user_id=current_user.id).all()]
        
    return render_template('category_view.html', category=category, movies=movies, watchlist_ids=watchlist_ids)
