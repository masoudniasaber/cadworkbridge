from ninja import NinjaAPI
from .hello import router_hello
from .add import router_add
from .chatbot import router_chatbot
from .pdf_spellcheck import router_pdf

api = NinjaAPI()
api.add_router("/hello/", router_hello)
api.add_router("/add/", router_add)
api.add_router("/chatbot/", router_chatbot)
api.add_router("/pdf/", router_pdf)