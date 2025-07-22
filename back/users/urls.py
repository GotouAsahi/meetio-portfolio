from django.urls import path, include
from . import views

urlpatterns = [
    path('api/v1/verify-token/', views.verifyToken, name='verify-token'),
]