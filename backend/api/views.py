# views.py
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import permission_classes, api_view
from django.contrib.auth import authenticate, login
from django.http import JsonResponse

from .serializers import UserSerializer

class UserRegistrationView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
        except Exception as e:
            return Response({"detail": "Invalid data provided"}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()

        response_data = {
            'user_id': user.id,
            'username': user.username,
            'email': user.email,
            'message': 'Registration successful'
        }

        return Response(response_data, status=status.HTTP_201_CREATED)
    
class UserLoginView(CreateAPIView):
    permission_classes = [AllowAny]
    serializer_class = UserSerializer

    @api_view(['POST'])
    def create(self, request, *args, **kwargs):
        print(request.data)
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            response_data = {
                'user_id': user.id,
                'username': user.username,
                'email': user.email,
                'message': 'Login successful'
            }

            return JsonResponse(response_data, status=200)

        else:
            return JsonResponse({'detail': 'Invalid login credentials'}, status=401)