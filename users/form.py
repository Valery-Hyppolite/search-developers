from django.db import models
from django.db.models import fields
from django.db.models.base import Model
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Skill, Message

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2' ]
        labels = {
            'first_name': 'Name',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class PorfileForm(ModelForm):
    class Meta:
        model  = Profile
        fields = [
            'name', 'username', 'email', 'location', 'short_intro', 'bio', 'profile_image', 'social_github',
            'social_twiter', 'social_facebook','social_linkedin', 'social_youtube', 'social_website'
            ]

    def __init__(self, *args, **kwargs):
        super(PorfileForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class SkillForm(ModelForm):
    class Meta:
        model   = Skill
        fields  = '__all__'
        exclude = ['owner', 'id']

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})


class MessageForm(ModelForm):
    class Meta:
        model  = Message
        fields = ['name', 'email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
    