from rest_framework import serializers
from . import models

class ContactusSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ContactUs
        fields='__all__'