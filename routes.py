from aiohttp import web
from controllers.controller_get import get_req
from controllers.controller_post import post_req
from controllers.controller_put import put_req
from controllers.controller_delete import delete_req
from controllers.controller_patch import patch_req
from controllers.controller_options import options_req
from controllers.controller_head import head_req

# Routes can be accessed at http://localhost:8080/
def setup_routes(app):
    app.router.add_route('GET', '/', get_req)
    # app.router.add_route('POST', '/', post_req)
    # app.router.add_route('PUT', '/', put_req)
    # app.router.add_route('DELETE', '/', delete_req)
    # app.router.add_route('PATCH', '/', patch_req)
    # app.router.add_route('OPTIONS', '/', options_req)
    # app.router.add_route('HEAD', '/', head_req)