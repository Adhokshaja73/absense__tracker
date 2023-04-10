from django.urls import path
from . import views

urlpatterns = [

    # ------------------ Account URLS ---------------------------------------------------
    path('create_user_profile/', views.create_user_profile, name='create_user_profile'),
    path('accounts/profile/', views.dashboard, name='dashboard_url'),

    # ------------------ Dashboard URLS ---------------------------------------------------
    path('', views.dashboard, name='dashboard'),
]
