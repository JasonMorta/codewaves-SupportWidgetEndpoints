from aiohttp import web

async def patch_req(request):
    # Logic to handle PATCH request
    # Example: Update specific fields of a resource
    data = await request.json()  # Assuming JSON data is sent in the request body
    print(data)
    # Apply partial updates to the resource
    # Update the resource based on the data received
    return web.Response(text="Resource patched successfully")


""" 
PATCH (PATCH):
The PATCH method is used to apply partial modifications to a resource.
Unlike PUT, which replaces the entire resource, PATCH requests are used 
for making partial updates to the resource.

PATCH requests typically contain instructions on how the resource should 
be modified, rather than the complete representation of the resource.
PATCH requests are also idempotent, meaning that multiple identical PATCH 
requests will have the same effect as a single request.

While you technically can use POST requests for partial updates, using PATCH 
is more aligned with the intended semantics of the HTTP methods and provides a 
clearer indication of your intent to perform a partial modification to a resource.
"""