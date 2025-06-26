from ninja import Router

router_hello = Router(tags=["Hello"])

@router_hello.get("/")
def get_hello(request):
    return {"message": "Hello from Django Ninja"}
