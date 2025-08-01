from django.contrib.auth import authenticate
from rest_framework import generics, status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.parsers import FormParser, MultiPartParser, JSONParser
from rest_framework.response import Response

from my_scraper.models import User, IGPage
from my_scraper.serializers import UserSerializer, IGPageSerializer, LoginSerializer

# Create your views here.
class UserListView(generics.ListCreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    parser_classes = [FormParser, MultiPartParser]

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request):
        # just authenticated users can access this view
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

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

    def get(self, request, id):
        try:
            user = User.objects.get(id=id)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)

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

    def delete(self, request, id):
        try:
            user = User.objects.get(id=id)
            user.delete()
            return Response(status=204)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=404)


class UserLoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
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

class UserLogoutView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [IsAuthenticated]

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
    serializer_class = IGPageSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        # get page details and tokens and add to user pages    #todo


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
