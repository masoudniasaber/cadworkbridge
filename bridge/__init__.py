from ninja import NinjaAPI
from .routers.math_router import router_math
from .routers.chatbot_router import router_chatbot
from .routers.spellchecker_router import router_spellchecker  # ✅ Add this line

api = NinjaAPI()

api.add_router("/math/", router_math)
api.add_router("/chatbot/", router_chatbot)
api.add_router("/spellcheck/", router_spellchecker)  # ✅ Register the new router
