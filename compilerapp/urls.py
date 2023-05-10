from django.urls import path, include

from . import views

app_name = 'compilerapp'
urlpatterns = [
    path('', views.index, name='index'),
    path('add_catalog/', views.add_catalog, name='add_catalog'),
    path('add_file/', views.add_file, name='add_file'),
    path('delete_file/', views.delete_file, name='delete_file'),
    path('delete_catalog/', views.delete_catalog, name='delete_catalog'),
    path('compile/', views.compile, name='compile'),
    # path('file_contents/<int:catalog_id>/<int:file_id>/', views.file_contents, name='file_contents'),
    # path('open_file/', views.open_file, name='open_file'),
]