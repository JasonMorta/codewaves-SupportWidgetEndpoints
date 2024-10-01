from controllers.controller_get import get_req
# from controllers.controller_post import post_req
# from controllers.controller_put import put_req
# from controllers.controller_delete import delete_req
# from controllers.controller_patch import patch_req
# from controllers.controller_options import options_req
# from controllers.controller_head import head_req

def setup_routes(app):
    # Setting up GET route for fetching tickets and agents
    app.add_url_rule('/', 'get_req', get_req, methods=['GET'])
    # app.router.add_route('POST', '/', post_req)
    # app.router.add_route('PUT', '/', put_req)
    # app.router.add_route('DELETE', '/', delete_req)
    # app.router.add_route('PATCH', '/', patch_req)
    # app.router.add_route('OPTIONS', '/', options_req)
    # app.router.add_route('HEAD', '/', head_req)