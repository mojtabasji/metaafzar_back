from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from my_scraper.models import User, IGPage
from my_scraper.serializers import UserSerializer, IGPageSerializer, LoginSerializer

# Create your views here.
class UserListView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    # parser_classes = [FormParser, MultiPartParser]

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthenticated()]
        return [AllowAny()]

    @swagger_auto_schema(
        operation_description="List all users or create a new user",
        responses={
            200: UserSerializer(many=True),
            201: UserSerializer,
            204: "No Content"
        }
    )
    def get(self, request):
        # just authenticated users can access this view
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        operation_description="Create a new user, some parameters should be add.",
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_QUERY, description="Username of the user",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('email', openapi.IN_QUERY, description="Email of the user",
                              type=openapi.TYPE_STRING),
            openapi.Parameter('first_name', openapi.IN_QUERY, description="First name of the user", type=openapi.TYPE_STRING),
            openapi.Parameter('last_name', openapi.IN_QUERY, description="Last name of the user", type=openapi.TYPE_STRING),
            openapi.Parameter('phone', openapi.IN_QUERY, description="Phone number of the user", type=openapi.TYPE_STRING),
            openapi.Parameter('password', openapi.IN_QUERY, description="Password of the user",
                              type=openapi.TYPE_STRING),
        ],
        responses={
            201: UserSerializer,
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=201)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        """
        Delete all users (not recommended for production).
        """
        User.objects.all().delete()
        return Response(status=204)

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Get, update or delete a user by ID",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID of the user", type=openapi.TYPE_INTEGER)
        ],
        responses={
            200: UserSerializer,
            404: "User not found",
            400: "Bad Request"
        }
    )
    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

    @swagger_auto_schema(
        operation_description="Update a user by ID",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID of the user", type=openapi.TYPE_INTEGER),
            openapi.Parameter('username', openapi.IN_QUERY, description="Username of the user", type=openapi.TYPE_STRING),
            openapi.Parameter('email', openapi.IN_QUERY, description="Email of the user", type=openapi.TYPE_STRING),
            openapi.Parameter('first_name', openapi.IN_QUERY, description="First name of the user", type=openapi.TYPE_STRING),
            openapi.Parameter('last_name', openapi.IN_QUERY, description="Last name of the user", type=openapi.TYPE_STRING),
            openapi.Parameter('phone', openapi.IN_QUERY, description="Phone number of the user", type=openapi.TYPE_STRING),
            openapi.Parameter('password', openapi.IN_QUERY, description="Password of the user", type=openapi.TYPE_STRING),
        ],
        request_body=UserSerializer,
        responses={
            200: UserSerializer,
            404: "User not found",
            400: "Bad Request"
        }
    )
    def put(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user, data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                return Response(UserSerializer(user).data)
            return Response(serializer.errors, status=400)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


    @swagger_auto_schema(
        operation_description="Delete a user by ID",
        manual_parameters=[
            openapi.Parameter('id', openapi.IN_PATH, description="ID of the user", type=openapi.TYPE_INTEGER)
        ],
        responses={
            204: "No Content",
            404: "User not found"
        }
    )
    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
            user.delete()
            return Response(status=204)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

class UserLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    @swagger_auto_schema(
        operation_description="Login a user",
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_QUERY, description="Username of the user", type=openapi.TYPE_STRING),
            openapi.Parameter('password', openapi.IN_QUERY, description="Password of the user", type=openapi.TYPE_STRING)
        ],
        responses={
            200: openapi.Response(description="Login successful", examples={"application/json": {"refresh": "token", "access": "token", "message": "Login successful", "user": "username"}}),
            400: "Invalid username or password"
        }
    )
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                # You can return a token or user details here
                user = serializer.validated_data['user']
                refresh = RefreshToken.for_user(user)
                response = Response({
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                    "message": "Login successful", "user": user.username}, status=status.HTTP_200_OK)

                # Set tokens in cookies
                response.set_cookie('refresh_token', str(refresh), httponly=True)
                response.set_cookie('access_token', str(refresh.access_token), httponly=True)

                # Set tokens in headers
                response['Authorization'] = f'Bearer {str(refresh.access_token)}'
                return response
            else:
                return Response({"error": "Invalid username or password"}, status=400)

class UserIGPageListView(generics.ListAPIView):
    serializer_class = IGPageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return IGPage.objects.filter(user=user)

    def get(self, request):
        igpages = self.get_queryset()
        serializer = IGPageSerializer(igpages, many=True)
        return Response(serializer.data)

# authentication check endpoint
class UserAuthCheckView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    # no need to serializer class here, just return user info if authenticated
    def get_serializer_class(self):
        return None

    @swagger_auto_schema(
        operation_description="Check if the user is authenticated",
        responses={
            200: openapi.Response(description="User is authenticated", examples={"application/json": {"message": "User is authenticated", "username": "example_user"}}),
            401: "User is not authenticated"
        }
    )
    def get(self, request):
        user = request.user
        if user.is_authenticated:
            return Response({"message": "User is authenticated", "username": user.username}, status=status.HTTP_200_OK)
        return Response({"error": "User is not authenticated"}, status=status.HTTP_401_UNAUTHORIZED)

class UserRegisterView(generics.CreateAPIView):
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    # parser_classes = [FormParser, MultiPartParser]
    # remove some fields from the serializer
    def get_serializer(self, *args, **kwargs):
        serializer = super().get_serializer(*args, **kwargs)
        serializer.fields.pop('last_login', None)
        serializer.fields.pop('is_active', None)
        serializer.fields.pop('is_staff', None)
        serializer.fields.pop('is_superuser', None)
        serializer.fields.pop('date_joined', None)
        serializer.fields.pop('groups', None)
        serializer.fields.pop('user_permissions', None)
        serializer.fields.pop('role', None)
        serializer.fields.pop('profile_picture', None)
        return serializer

    @swagger_auto_schema(
        operation_description="Register a new user",
        manual_parameters=[
            openapi.Parameter('username', openapi.IN_QUERY, description="Username of the user", type=openapi.TYPE_STRING),
            openapi.Parameter('email', openapi.IN_QUERY, description="Email of the user", type=openapi.TYPE_STRING),
            openapi.Parameter('first_name', openapi.IN_QUERY, description="First name of the user", type=openapi.TYPE_STRING),
            openapi.Parameter('last_name', openapi.IN_QUERY, description="Last name of the user", type=openapi.TYPE_STRING),
            openapi.Parameter('phone', openapi.IN_QUERY, description="Phone number of the user", type=openapi.TYPE_STRING),
            openapi.Parameter('password', openapi.IN_QUERY, description="Password of the user", type=openapi.TYPE_STRING),
        ],
        responses={
            201: UserSerializer,
            400: "Bad Request"
        }
    )
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Automatically log in the user after registration
            refresh = RefreshToken.for_user(user)
            response = Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                "message": "Registration successful", "user": user.username}, status=status.HTTP_201_CREATED)
            # Set tokens in cookies
            response.set_cookie('refresh_token', str(refresh), httponly=True)
            response.set_cookie('access_token', str(refresh.access_token), httponly=True)

            return response
        return Response(serializer.errors, status=400)

class UserLogoutView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_description="Log out the user",
        responses={
            200: "Logged out successfully",
            401: "Unauthorized"
        }
    )
    def post(self, request):
        response = Response({"message": "Logged out successfully"}, status=status.HTTP_200_OK)
        response.delete_cookie('refresh_token')
        response.delete_cookie('access_token')
        return response

class IGPageListView(generics.ListCreateAPIView):
    serializer_class = IGPageSerializer

    def get(self, request):
        igpages = IGPage.objects.all()
        serializer = IGPageSerializer(igpages, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = IGPageSerializer(data=request.data)
        if serializer.is_valid():
            igpage = serializer.save()
            return Response(IGPageSerializer(igpage).data, status=201)
        return Response(serializer.errors, status=400)

class AttachNewIGPageView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]
    # no need to serializer class here,
    def get_serializer_class(self):
        return None

    def get(self, request):
        user = request.user
        # get page details and tokens and add to user pages    #todo
        print("User is authenticated:", user.is_authenticated)
        print("request parameters:", request.query_params)
        ig_username = request.query_params.get('username')
        access_token = request.query_params.get('access_token')
        if not ig_username or not access_token:
            return Response({"error": "Instagram username and access token are required"}, status=400)
        # Check if the user already has an IGPage with this username
        if IGPage.objects.filter(username=ig_username, user=user).exists():
            # update the existing IGPage
            igpage = IGPage.objects.get(username=ig_username, user=user)
            igpage.token = access_token
            igpage.save()
            return Response({"message": "Instagram page updated successfully", "igpage": IGPageSerializer(igpage).data}, status=200)
        # Create a new IGPage for the user
        igpage = IGPage.objects.create(
            username=ig_username,
            token=access_token,
            user=user
        )
        return Response({"message": "Instagram page attached successfully", "igpage": IGPageSerializer(igpage).data}, status=201)

class IGPageDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IGPageSerializer

    def get(self, request, id):
        try:
            igpage = IGPage.objects.get(id=id)
            serializer = IGPageSerializer(igpage)
            return Response(serializer.data)
        except IGPage.DoesNotExist:
            return Response({"error": "Instagram page not found"}, status=404)

    def put(self, request, id):
        try:
            igpage = IGPage.objects.get(id=id)
            serializer = IGPageSerializer(igpage, data=request.data)
            if serializer.is_valid():
                igpage = serializer.save()
                return Response(IGPageSerializer(igpage).data)
            return Response(serializer.errors, status=400)
        except IGPage.DoesNotExist:
            return Response({"error": "Instagram page not found"}, status=404)

    def delete(self, request, id):
        try:
            igpage = IGPage.objects.get(id=id)
            igpage.delete()
            return Response(status=204)
        except IGPage.DoesNotExist:
            return Response({"error": "Instagram page not found"}, status=404)
