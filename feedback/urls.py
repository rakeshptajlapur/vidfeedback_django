from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    # Will add paths here as we develop views
    path('', views.home, name='home'),
]