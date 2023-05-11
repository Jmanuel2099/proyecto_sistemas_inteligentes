from django.urls import path
from file_app.views.file_view import LoadFileView


load_file_view = LoadFileView()

urlpatterns = [
    path('load', load_file_view.load_file)
]