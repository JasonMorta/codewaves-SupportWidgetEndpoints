from aiohttp import web

async def delete_req(request):
    # Logic to handle DELETE request
    # Example: Delete a resource based on the request
    resource_id = request.match_info.get('id')  # Assuming resource ID is passed in the URL
    # Perform deletion logic based on resource ID
    return web.Response(text=f"Resource with ID {resource_id} deleted successfully")


""" 
The DELETE method is used to remove a resource from the server.

It requests that the server delete the resource identified by the Request-URI.
"""