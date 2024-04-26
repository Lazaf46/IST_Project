# ist_app/urls.py
from django.contrib import admin
from django.urls import path, include


#app_name = 'IST_APP'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include ('IST_APP.urls') ),
]
