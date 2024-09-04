from aiohttp import web

async def head_req(request):
    # Logic to handle HEAD request
    # Typically, you would check the existence of a resource or retrieve metadata without returning the body
    # Example: Check if a resource exists
    # Check the existence of the resource
    resource_exists = True  # Placeholder, replace with actual logic
    if resource_exists:
        return web.Response(status=200)  # Resource exists
    else:
        return web.Response(status=404)  # Resource not found


""" 
The HEAD method is similar to the GET method, 
but the server does not return a message body in the response.

It's used to request headers that would be returned if the HEAD 
request's URL was instead requested with the GET method.

HEAD requests are useful for checking if a resource exists or for 
obtaining metadata about a resource without retrieving the entire content.

"""