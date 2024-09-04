from aiohttp import web
from aiohttp_middlewares import cors_middleware
from routes import setup_routes
from middleware import main_middleware
from aiohttp_middlewares import error_middleware, timeout_middleware

def create_app():
    
       # Define allowed origins
    cors_config = {
        "*": {  # Replace * with specific domain e.g., 'https://example.com'
            "allow_credentials": True,
            "allow_methods": ["GET"],  # Specify allowed HTTP methods
            "allow_headers": ["api-key", "date", "Content-Type"],  # Allowed headers
        }
    }
    
    # Create the application
    app = web.Application()

    # Add middleware to all routes
    app.middlewares.append(main_middleware)

    # Add CORS middleware with more restricted rules
    app.middlewares.append(cors_middleware(
        allow_all=False,  # Disable allow_all
        origins=cors_config  # Specify allowed origins and options
    ))

    # Add timeout middleware
    #app.middlewares.append(timeout_middleware(29.5)) # stop the request after 29.5 seconds

    # Setup routes
    setup_routes(app)

    return app
