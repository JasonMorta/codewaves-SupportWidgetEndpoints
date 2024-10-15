from aiohttp import web

async def hello_world(request):
    return web.json_response({"message": "Hello, World!"})

def setup_routes(app):
    app.router.add_get('/hello', hello_world)
