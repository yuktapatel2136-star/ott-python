from app import create_app, db
from app.models.models import User, Movie, Category

app = create_app()

def init_db():
    with app.app_context():
        # Create database tables
        db.create_all()
        print("Database tables ensured!")
        
        # Add default categories if empty
        if Category.query.count() == 0:
            print("Adding default categories...")
            categories = [
                Category(name='Action', type='genre'),
                Category(name='Comedy', type='genre'),
                Category(name='Drama', type='genre'),
                Category(name='Horror', type='genre'),
                Category(name='Sci-Fi', type='genre'),
                Category(name='English', type='language'),
                Category(name='Hindi', type='language'),
                Category(name='2024', type='year')
            ]
            db.session.add_all(categories)
            db.session.commit()

        # Check if admin already exists
        if not User.query.filter_by(role='admin').first():
            print("Creating default admin account...")
            admin = User(username='admin', email='admin@streamhub.com')
            admin.set_password('admin123')
            admin.role = 'admin'
            admin.is_subscribed = True
            db.session.add(admin)
            db.session.commit()
            print("Admin account created (admin/admin123)")

if __name__ == '__main__':
    init_db()
    # Run the Flask app
    app.run(debug=True)
