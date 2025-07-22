from rest_framework import routers
from school.viewsets import SchoolViewSet

router = routers.DefaultRouter()
router.register('school', SchoolViewSet)