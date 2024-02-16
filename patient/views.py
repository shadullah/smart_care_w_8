from django.shortcuts import render,redirect
from rest_framework import viewsets
from . import models
from . import serializers
from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from rest_framework.authtoken.models import Token

# for sending email
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string

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
            token = default_token_generator.make_token(user)
            print("token", token)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            print("uid ",uid)
            confirm_link = f"http://127.0.0.1:8000/patient/active/{uid}/{token}"
            email_subject= "confirm your Email"
            email_body= render_to_string('confirm_email.html', {'confirm_link': confirm_link})

            email = EmailMultiAlternatives(email_subject, '', to=[user.email])
            email.attach_alternative(email_body, 'text/html')
            email.send()
            return Response("Check your mail for confirmation")
        return Response(serializer.errors)
    
def activate(req, uid64, token):
    try:
        uid = urlsafe_base64_decode(uid64).decode()
        user = User._default_manager.get(pk=uid)
    except(User.DoesNotExist):
        user=None 

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active=True 
        user.save()
        return redirect('register')
    else:
        return redirect('register')
    
class UserLoginAPIView(APIView):
    def post(self,req):
        serializer = serializers.UserLoginSerializers(data=self.request.data)
        if serializer.is_valid():
            username= serializer.validated_data['username']
            password= serializer.validated_data['password']

            user = authenticate(username=username, password=password)
            login(req, user)
            if user:
                token, _ =Token.objects.get_or_create(user=user)
                return Response({'token': token.key, 'user_id': user.id})
            else:
                return Response({'error': "Invalid Credential"})
        return Response(serializer.errors)
    
class UserLogoutView(APIView):
    def get(self, req):
        req.user.auth_token.delete()
        logout(req)
        return redirect('login')