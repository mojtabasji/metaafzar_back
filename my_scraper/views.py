from django.contrib.auth import authenticate
from inflection import parameterize
from rest_framework import generics, status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response
from my_scraper.models import User, IGPage
from my_scraper.serializers import UserSerializer, IGPageSerializer
from rest_framework.decorators import action
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes, OpenApiParameter

class UserViewSetApiView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    # permission class
    def get_permissions(self):
        if self.action in ['create']:
            return [AllowAny()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action == 'igpages':
            return IGPageSerializer
        return super().get_serializer_class()

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

    @action(
        detail=False,
        methods=['get', 'post'],
        permission_classes=[IsAuthenticated]
    )
    def igpages(self, request):
        user = request.user
        if request.method == 'GET':
            pages = IGPage.objects.filter(user=user)
            serializer = IGPageSerializer(pages, many=True)
            return Response(serializer.data)
        elif request.method == 'POST':
            serializer = IGPageSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=True,
        methods=['delete'],
        permission_classes=[IsAuthenticated]
    )
    def delete_igpage(self, request, pk=None):
        try:
            igpage = IGPage.objects.get(pk=pk, user=request.user)
        except IGPage.DoesNotExist:
            raise NotFound("IGPage not found or not owned by user.")
        igpage.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


