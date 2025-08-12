from django.contrib.auth import authenticate
from inflection import parameterize
from rest_framework import generics, status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response
from my_scraper.models import User
from my_scraper.serializers import UserSerializer
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes, OpenApiParameter

class UserViewSetApiView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # permission_classes = [IsAuthenticated]

    # permission class
    def get_permissions(self):
        if self.action in ['create']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': serializer.data,
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }, status=status.HTTP_201_CREATED)



