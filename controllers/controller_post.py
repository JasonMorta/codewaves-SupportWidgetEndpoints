from aiohttp import web


# post request to receive a message
async def post_req(request):
    
    # response to server
    return web.Response(text="Received POST request")


""" 
POST (POST):
The POST method is used to submit data to be processed to a specified 
resource. It can be used to create a new resource on the server.
POST requests are often used when you want to add a new record to a 
collection or submit form data to the server.
In RESTful APIs, POST requests are commonly used for creating new resources.

"""