from rest_framework import viewsets, filters
from .models import School
from .serializers import SchoolSerializer,SchoolSuggestSerializer

class SchoolViewSet(viewsets.ModelViewSet):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer
    filter_backends = (filters.SearchFilter,)
    search_fields = ('user_id','grade','classification','department','name','graduation_year')

class SchoolSuggestViewSet(viewsets.ModelViewSet):
    queryset = School.objects.values("name",'department').distinct()
    serializer_class = SchoolSuggestSerializer
    filter_backends = (filters.SearchFilter,)
    
