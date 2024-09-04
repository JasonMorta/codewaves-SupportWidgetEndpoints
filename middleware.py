from aiohttp import web
import asyncio


async def main_middleware(app, handler):
    
    async def middleware_handler(request):

            print(f"🟢URL: {request.url}")
            print(f"🟢Method: {request.method}")
            print(f"🟢Headers: {request.headers}")
            print(f"🟢Query: {request.query}")
            print(f"🟢Match info: {request.match_info}")
            print(f"🟢Body exists: {request.body_exists}")
            print(f"🟢Content type: {request.content_type}")
            print(f"🟢Content length: {request.content_length}")
            
            
            

            # check headers 'api-key' == '123'
            if request.headers.get('api-key') == '123':
                
                try:
                 # Call the CORS middleware handler
                    response = await handler(request)
                    return response
            
                except asyncio.TimeoutError:
                    return web.Response(text="Request timed out", status=504)
                
            else:
                return web.Response(text="API key is missing or invalid", status=401)
               
 
          
    
    return middleware_handler