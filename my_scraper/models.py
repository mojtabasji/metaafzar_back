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
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)
    ig_user_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    followers = models.IntegerField(default=0, null=True, blank=True)
    following = models.IntegerField(default=0, null=True, blank=True)
    posts = models.IntegerField(default=0, null=True, blank=True)
    bio = models.TextField(blank=True, null=True)
    profile_picture = models.URLField(blank=True, null=True)
    date_scraped = models.DateTimeField(auto_now_add=True, null=True)
    access_token = models.CharField(max_length=400, blank=True, null=True)
    token_expiry = models.DateTimeField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ig_pages')
    permissions = models.CharField(max_length=400, blank=True, null=True)

    def __str__(self):
        return self.username

    # if on create instance with ig_user_id exists, update it
    def save(self, *args, **kwargs):
        if not self.pk and self.ig_user_id:
            try:
                existing = IGPage.objects.get(ig_user_id=self.ig_user_id)
                self.pk = existing.pk  # Update existing instance
            except IGPage.DoesNotExist:
                pass  # No existing instance, proceed to create new
        super().save(*args, **kwargs)

    

