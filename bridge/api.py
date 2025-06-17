from ninja import NinjaAPI

api = NinjaAPI()

@api.get("/add")
def add(request, a: int, b: int):
    return {"result": a + b}

@api.get("/hello")
def hello(request):
    return {"message": "Hello from Django Ninja"}
