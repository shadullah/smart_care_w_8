from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class DoctorViewset(viewsets.ModelViewSet):
    queryset = models.Doctor.objects.all()
    serializer_class = serializers.DoctorSerializer

class SpecializationViewset(viewsets.ModelViewSet):
    queryset = models.Speacialization.objects.all()
    serializer_class = serializers.SpecializationSerializer

class AvailabletimeViewset(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    queryset = models.AvailableTime.objects.all()
    serializer_class = serializers.AvailableTimeSerializer

class DesignationViewset(viewsets.ModelViewSet):
    queryset = models.Designation.objects.all()
    serializer_class = serializers.DesignationSerializer

class ReviewViewset(viewsets.ModelViewSet):
    queryset = models.Review.objects.all()
    serializer_class = serializers.ReviewSerializer