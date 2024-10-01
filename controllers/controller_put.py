# from aiohttp import web


# # post request to receive a message
# async def put_req(request):
    
#     # response to server
#     return web.Response(text="Received POST request")


""" 
The PUT method is used to update a resource or create a new resource if it doesn't exist.
It replaces the entire resource with the representation provided in the request.


The PUT method is not the same as the POST method. While they both are used to send 
data to the server, they have different semantics and are typically used in different scenarios;



PUT (PUT): Designed for full updates or replacements of a resource.
The PUT method is used to send data to the server to update or replace 
the resource identified by the request URI.
Unlike POST, which is used to create a new resource, PUT is used to update 
an existing resource or create a new one if it doesn't exist.
In RESTful APIs, PUT requests are typically used for updating existing 
resources, and the entire resource representation is sent in the request body.


"""