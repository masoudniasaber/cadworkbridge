# cadworkbridge/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('bridge.urls')),  # ✅ mount bridge app's API
]
