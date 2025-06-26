# bridge/urls.py

from django.urls import path
from bridge import api  # import the NinjaAPI instance

urlpatterns = [
    path("", api.urls),  # Swagger will be at /api/docs
]
