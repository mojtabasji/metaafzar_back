from rest_framework import serializers
from .models import User, IGPage
from django.contrib.auth import authenticate

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'first_name', 'last_name']
        extra_kwargs = {
            'password': {'write_only': True},
            'email': {'required': True, 'allow_blank': False}
        }

    #     unique username and email and required email username and password
    def validate(self, attrs):
        if not attrs.get('username'):
            raise serializers.ValidationError("Username is required.")
        if not attrs.get('email'):
            raise serializers.ValidationError("Email is required.")
        if not attrs.get('password'):
            raise serializers.ValidationError("Password is required.")

        # Check if username or email already exists
        if User.objects.filter(username=attrs['username']).exists():
            raise serializers.ValidationError("Username already exists.")
        if User.objects.filter(email=attrs['email']).exists():
            raise serializers.ValidationError("Email already exists.")

        return attrs


    def update(self, instance, validated_data):
        for attr, value in validated_data.items():
            if attr == 'password':
                instance.set_password(value)
            else:
                setattr(instance, attr, value)
        instance.save()
        return instance

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class IGPageSerializer(serializers.ModelSerializer):
    class Meta:
        model = IGPage
        fields = ['id', 'username', 'ig_user_id', 'followers', 'following', 'posts', 'bio', 'profile_picture', 'date_scraped', 'access_token']

    def create(self, validated_data):
        return IGPage.objects.create(**validated_data)


class add_igpage_to_user_serializer(serializers.Serializer):
    code = serializers.CharField(max_length=150, required=True)
    ig_user_id = serializers.CharField(max_length=100, required=False, allow_blank=True)
