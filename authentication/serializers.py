from rest_framework import serializers
from .models import CustomUser



class CustomUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'url', 'first_name', 'middle_name', 'last_name',
                  'email', 'password', 'updated_at', 'created_at', 'role', 'is_active')
