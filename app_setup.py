from flask import Flask
from routes import setup_routes

def create_app():
    # Create the Flask app
    app = Flask(__name__)

    # Setup routes
    setup_routes(app)

    return app
