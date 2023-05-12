from django.urls import path
from file_app.views.file_view import LoadFileView


load_file_view = LoadFileView()

urlpatterns = [
    path('load', load_file_view.load_file),
    path('describe', load_file_view.describe_file),
    path('missingdata/<int:method_id>', load_file_view.statistical_analysis)
]