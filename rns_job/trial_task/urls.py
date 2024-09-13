# Import path and view.
from django.urls import path
from .views import process_uploaded_file

urlpatterns = [
    path('upload/', process_uploaded_file, name='upload'),
]