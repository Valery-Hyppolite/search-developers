from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from devsearches.settings import EMAIL_HOST_USER

from users.form import PorfileForm
from .models import Profile


# python signal model that wait for an action to trigger a function such as, deleting a uder, creating a user ect...
#@receiver(post_save, sender=Profile) # this does the same function as the post_save.connect below. 
def create_profile(sender, instance, created, **kwargs):
    """when a user is created, associate profile to that user or create a profile for that user."""
    if created:
        user = instance
        profile = Profile.objects.create(
            user = user,
            username = user.username,
            email = user.email,
            name = user.first_name
        )

        subject = 'Welcome to Dev Search!'
        message = 'We are glad you decided to be part of this community.'
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [profile.email],
            fail_silently=False
        )

def updateUser(sender, instance, created, **kwargs):
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email

        

def deleteUser(sender, instance, **kwargs):
    """when a profile is deleted, delete the user"""
    try:
        user = instance.user # get the user connected to the profile 
        user.delete()
    except:
        pass
    print('deleting user ...')
    print('instance',instance, 'sender', sender)

post_save.connect(updateUser, sender=Profile)
post_save.connect(create_profile, sender=User)
post_delete.connect(deleteUser, sender=Profile)