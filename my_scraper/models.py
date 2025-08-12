from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    password = models.CharField(max_length=128)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)
    role = models.CharField(max_length=20, choices=[('admin', 'Admin'), ('user', 'User')], default='user')
    last_login = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def set_password(self, raw_password):
        """
        Set the password for the user, hashing it before saving.
        """
        from django.contrib.auth.hashers import make_password
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        """
        Check the provided password against the stored hashed password.
        """
        from django.contrib.auth.hashers import check_password
        return check_password(raw_password, self.password)


class IGPage(models.Model):
    username = models.CharField(max_length=150, unique=True)
    followers = models.IntegerField(default=0)
    following = models.IntegerField(default=0)
    posts = models.IntegerField(default=0)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)
    date_scraped = models.DateTimeField(auto_now_add=True)
    token = models.CharField(max_length=255, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ig_pages')

    def __str__(self):
        return self.username
    

