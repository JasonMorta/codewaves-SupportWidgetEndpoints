import asyncio


async def main_middleware(app, handler):
    
    async def middleware_handler(request):

            # check headers 'api-key' == '123'
            if request.headers.get('api_key') == '123':
                try:
                 # Call the CORS middleware handler
                    response = await handler(request)
                    return response
                except asyncio.TimeoutError:
                    return web.Response(text="Request timed out", status=504)
            else:
                return web.Response(text="API key is missing or invalid", status=401)
               
    
    return middleware_handler