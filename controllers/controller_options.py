# from aiohttp import web

# async def options_req(request):
#     # Logic to handle OPTIONS request
#     # Typically, you would return a response indicating the supported methods and other capabilities
#     return web.Response(text="Allowed methods: GET, POST, PUT, PATCH, DELETE")


""" 
The OPTIONS method is used to describe the communication options for the target resource.

It is often used by clients to query the server about the supported methods and other 
capabilities for a resource without actually requesting the resource itself.

It allows a client to determine the communication options or requirements of a 
target resource, or the capabilities of a server, without implying a resource action.

"""