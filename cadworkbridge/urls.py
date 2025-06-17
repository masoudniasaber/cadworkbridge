# cadworkbridge/urls.py

from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('homepage.urls')),  # Homepage app mounted at root
    path('api/', include('bridge.urls')),  # ✅ mount bridge app's API
]
