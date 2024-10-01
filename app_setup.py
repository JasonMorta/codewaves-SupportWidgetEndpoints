from aiohttp import web
from aiohttp_middlewares import cors_middleware
from routes import setup_routes
from middleware import main_middleware
from aiohttp_middlewares import error_middleware, timeout_middleware

def create_app():
    # Define allowed origins for CORS
    cors_config = {}

    # Create the application
    app = web.Application()

    # Add custom middleware
    app.middlewares.append(main_middleware)

    # Add CORS middleware allowing all origins
    app.middlewares.append(cors_middleware(
      
    ))

    # Add timeout middleware (optional)
    # app.middlewares.append(timeout_middleware(29.5))  # Set request timeout at 29.5 seconds

    # Setup application routes
    setup_routes(app)

    return app
