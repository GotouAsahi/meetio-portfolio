from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .viewsets import SchoolViewSet,SchoolSuggestViewSet

router = DefaultRouter()
router.register('school', SchoolViewSet)
router.register('school_suggest',SchoolSuggestViewSet)

urlpatterns = [
    path('', include(router.urls)),
]