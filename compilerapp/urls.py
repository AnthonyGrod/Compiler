from django.urls import path

from . import views

app_name = 'compilerapp'
urlpatterns = [
    path('', views.index, name='index'),
]