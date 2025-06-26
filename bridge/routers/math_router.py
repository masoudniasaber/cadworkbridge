from ninja import Router
from bridge.services.math_service import add, subtract, multiply, divide
from bridge.schemas.math_schema import MathInput, MathResult, MathError

router_math = Router(tags=["Math Operations"])

@router_math.post("/add", response={200: MathResult})
def add_route(request, payload: MathInput):
    result = add(payload.a, payload.b)
    return {"result": result}

@router_math.post("/subtract", response={200: MathResult})
def subtract_route(request, payload: MathInput):
    result = subtract(payload.a, payload.b)
    return {"result": result}

@router_math.post("/multiply", response={200: MathResult})
def multiply_route(request, payload: MathInput):
    result = multiply(payload.a, payload.b)
    return {"result": result}

@router_math.post("/divide", response={200: MathResult, 400: MathError})
def divide_route(request, payload: MathInput):
    try:
        result = divide(payload.a, payload.b)
        return {"result": result}
    except ValueError as e:
        return 400, {"error": str(e)}
