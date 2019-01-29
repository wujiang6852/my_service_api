from rest_framework import serializers

from app01.models import Admin, Picture


class AdminSerializer(serializers.ModelSerializer):
    Meta = Admin
    fields = '__all__'
