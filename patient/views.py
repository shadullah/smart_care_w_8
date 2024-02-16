from django.shortcuts import render
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response

# Create your views here.
class PatientViewset(viewsets.ModelViewSet):
    queryset = models.Patient.objects.all()
    serializer_class = serializers.PatientSerializer

class UserRegistrationApiView(APIView):
    serializer_class = serializers.RegistrationSerializer

    def post(self, req):
        serializer = self.serializer_class(data=req.data)

        if serializer.is_valid():
            user = serializer.save()
            print(user)
            return Response("form done")
        return Response(serializer.errors)