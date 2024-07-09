from flask import Flask
from flask_login import LoginManager
import cloudinary
import cloudinary.uploader
import cloudinary.api
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Initialize Flask extensions
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "Oyemdade George")
    app.config['CLOUDINARY_URL'] = os.getenv('CLOUDINARY_URL')

    # Initialize Cloudinary
    cloudinary.config(
        cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
        api_key=os.getenv("CLOUDINARY_API_KEY"),
        api_secret=os.getenv("CLOUDINARY_API_SECRET")
    )

    # Initialize Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  

    # Import blueprints and register them
    from .auth import auth
    from .views import views
    from .message import message

    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(message, url_prefix='/')

    return app
