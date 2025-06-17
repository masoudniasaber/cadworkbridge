from ninja import NinjaAPI  # ✅ This is correct even with django-ninja

api = NinjaAPI()

@api.get("/hello")
def hello(request):
    return {"message": "Hello from Django Ninja"}
