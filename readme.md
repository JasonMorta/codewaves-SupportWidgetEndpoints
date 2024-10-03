A simple python sever, thats uses aiohttp.

- Files are mobilized, and the server is run from the server.py file.
- Container controller with simle logic to handle the requests.
- Routes have all HTTP request methods, and are handled by the controllers.
- Middleware are place on all routes, and are used to log the requests going through the server and checks for an API key in the headers of each request.


### Installation
- Install aiohttp and cors
```sh
pip install aiohttp aiohttp-cors aiohttp_middlewares watchdog

```

- Start the server normally
```sh   
python server.py
```

- Start the sever with auto restart when changes are made to the files
```sh
watchmedo auto-restart --patterns="*.py" --recursive -- python server.py
```



