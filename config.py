import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'premium-streaming-secret-key-123'
    
    # Database configuration for MySQL
    # Note: '@' in password must be escaped as '%40'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:yukt%402006@localhost/database'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # File Upload Configuration
    UPLOAD_FOLDER_IMAGES = os.path.join(BASE_DIR, 'app', 'static', 'images')
    UPLOAD_FOLDER_VIDEOS = os.path.join(BASE_DIR, 'app', 'static', 'videos')
    MAX_CONTENT_LENGTH = 500 * 1024 * 1024  # 500 MB max upload size
    ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'webm', 'mkv', 'avi'}
