from types import BuiltinMethodType
from django.db import models
from django.contrib.auth.models import User
from django.db.models.fields import NullBooleanField
import uuid
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

#from users.views import profiles

# Create your models here.
class Profile(models.Model):
    user            = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)#when a user is delete it, delete the profile
    name            = models.CharField(max_length=200, blank=True, null=True)
    username        = models.CharField(max_length=200, blank=True, null=True)
    location        = models.CharField(max_length=200, blank=True, null=True)
    email           = models.EmailField(max_length=500, blank=True, null=True)
    short_intro     = models.CharField(max_length=200, blank=True, null=True)
    bio             = models.TextField(blank=True, null=True)
    profile_image   = models.ImageField(null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png')
    social_github   = models.CharField(max_length=200, blank=True, null=True)
    social_twiter   = models.CharField(max_length=200, blank=True, null=True)
    social_facebook = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube  = models.CharField(max_length=200, blank=True, null=True)
    social_website  = models.CharField(max_length=200, blank=True, null=True)
    create          = models.DateTimeField(auto_now_add=True)
    id              = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self) -> str:
        return str(self.username)
    
    class Meta:
        ordering = ['create']


    @property
    def image_url(self):
        try:
            img = self.profile_image.url
        except:
            img = ''
        return img

    
class Skill(models.Model):
    owner       = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, blank=True)
    skill_name  = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    create      = models.DateTimeField(auto_now_add=True)
    id          = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False, max_length=36)

    def __str__(self) -> str:
        return str(self.skill_name)

class Message(models.Model):
    sender    = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)
    recipient = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True, related_name='messages')
    name      = models.CharField(max_length=200, null=True, blank=True)
    email     = models.EmailField(max_length=200, null=True, blank=True)
    subject   = models.CharField(max_length=200, null=True, blank=True)
    is_read   = models.BooleanField(default=False, null=True)
    body      = models.TextField()
    create    = models.DateTimeField(auto_now_add=True)
    id        = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self) -> str:
        return str(self.subject)
    class Meta:
        ordering = ['is_read', '-create']
