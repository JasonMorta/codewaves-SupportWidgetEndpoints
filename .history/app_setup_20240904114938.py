from aiohttp import web
from aiohttp_middlewares import cors_middleware
from routes import setup_routes
from middleware import main_middleware
from aiohttp_middlewares import error_middleware, timeout_middleware

def create_app():
    # Create the application
    app = web.Application()

    # Add middleware to all routes
    app.middlewares.append(main_middleware)

    # Add CORS middleware
    app.middlewares.append(cors_middleware(
        allow_all=True,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    ))

    # Add timeout middleware
    #app.middlewares.append(timeout_middleware(29.5)) # stop the request after 29.5 seconds

    # Setup routes
    setup_routes(app)

    return app
