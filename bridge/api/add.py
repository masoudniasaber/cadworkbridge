from ninja import Router

router_add = Router(tags=["Math Operations"])

@router_add.get("/")
def get_add(request, a: int, b: int):
    return {"result": a + b}
