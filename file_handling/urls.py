from django.urls import path
from file_handling.views.load_file_view import LoadFileView

load_file = LoadFileView()
urlpatterns = [
    path('load',load_file.load_file)
]