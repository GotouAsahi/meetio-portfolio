from rest_framework import serializers
from .models import School

class SchoolSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = '__all__'

class SchoolSuggestSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = 'name','department'