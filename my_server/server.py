import asyncio
import aiohttp_cors
from aiohttp import web
from aiohttp_middlewares import cors_middleware, error_middleware
from routes import setup_routes

async def start_server():
    app = web.Application(middlewares=[
        cors_middleware(allow_all=True),
        error_middleware(),
    ])

    # Setup CORS
    cors = aiohttp_cors.setup(app, defaults={
        "*": aiohttp_cors.ResourceOptions(allow_credentials=True, expose_headers="*", allow_headers="*")
    })

    # Add routes
    setup_routes(app)

    # Apply CORS to all routes
    for route in list(app.router.routes()):
        cors.add(route)

    # Start the server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)  # Use 0.0.0.0 to accept external connections
    await site.start()
    print("======= Serving on http://localhost:8080/ ======")

    try:
        while True:
            await asyncio.sleep(3600)  # Keep the server running
    except KeyboardInterrupt:
        pass

if __name__ == '__main__':
    asyncio.run(start_server())
