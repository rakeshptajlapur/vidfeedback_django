from django.urls import path
from . import views

app_name = 'feedback'

urlpatterns = [
    # Admin/Dashboard routes
    path('forms/', views.form_list, name='form_list'),
    path('forms/create/', views.form_create, name='form_create'),
    path('forms/<str:slug>/edit/', views.form_edit, name='form_edit'),
    
    # Public route
    path('f/<slug:slug>/', views.public_form_view, name='public_form'),
]