from django.contrib import admin
from django.urls import path, include
from nightstand_dashboard.views import index

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('nightstand_dashboard.urls')),
]
