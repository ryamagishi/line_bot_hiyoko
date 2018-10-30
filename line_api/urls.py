from django.urls import path

from line_api import views

app_name = 'line_api'
urlpatterns = [
    path('', views.main, name='main'),
]
