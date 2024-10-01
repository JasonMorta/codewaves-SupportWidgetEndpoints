from controllers.controller_get import get_req
from controllers.controller_customMSG import welcome
# from controllers.controller_put import put_req
# from controllers.controller_delete import delete_req
# from controllers.controller_patch import patch_req
# from controllers.controller_options import options_req
# from controllers.controller_head import head_req

def setup_routes(app):
    # Setting up GET route for fetching tickets and agents
    app.add_url_rule('/', 'get_req', get_req, methods=['GET'])
    app.add_url_rule('/welcome', 'welcome', welcome, methods=['GET'])
    
