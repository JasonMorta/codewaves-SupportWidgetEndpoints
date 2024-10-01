from aiohttp import web
from routes import setup_routes

def create_app():
    # Create the application
    app = web.Application()

    # Setup routes
    setup_routes(app)

    # Return the configured app
    return app
