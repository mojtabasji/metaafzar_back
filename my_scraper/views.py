from django.contrib.auth import authenticate
from inflection import parameterize
from rest_framework import generics, status, viewsets
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response
from my_scraper.models import User, IGPage
from my_scraper.serializers import UserSerializer, IGPageSerializer, add_igpage_to_user_serializer
from rest_framework.decorators import action, api_view
from rest_framework.exceptions import NotFound
from drf_spectacular.utils import extend_schema, OpenApiResponse, OpenApiTypes, OpenApiParameter
from my_scraper.components import code2token

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
        if self.action == 'add_igpage':
            return add_igpage_to_user_serializer
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
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def igpages(self, request):
        user = request.user
        if request.method == 'GET':
            pages = IGPage.objects.filter(user=user)
            serializer = IGPageSerializer(pages, many=True)
            return Response(serializer.data)

    @extend_schema(
        parameters=[
            OpenApiParameter(
                name='code',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                required=True,
                description='Instagram authorization code'
            )
        ],
        responses={200: OpenApiTypes.OBJECT}
    )
    @action(
        detail=False,
        methods=['get'],
        permission_classes=[IsAuthenticated]
    )
    def add_igpage(self, request, *args, **kwargs):
        serializer = add_igpage_to_user_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # ig_auth_code = request.query_params.get('code').replace('#', '')
        ig_auth_code = serializer.validated_data.get('code', '').replace('#', '')
        code2token(ig_auth_code, request.user) # This function should handle the code exchange and return user info or token.
        # ig_auth_code should send to instagram and get access token and user info
        # then redirect user to front-end view.

        # if not ig_auth_code:
        #     return Response({"error": "IG auth code is required."}, status=status.HTTP_400_BAD_REQUEST)
        return Response({"message": "IG auth code received.", "code": ig_auth_code}, status=status.HTTP_200_OK)

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


