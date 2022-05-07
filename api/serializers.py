from django.db import models
from django.http import response
from rest_framework import fields, serializers
from projects.models import Project, Tag, Review
from users.models import Profile


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'


#We made owner = to ProfileSerializer to overide  what is the the orojectsterializer. that owner field is now going to use the profile feild to return the owner not eh project model.
# this owner is going to render out the entire user profile, evething in the user model.
class ProjectSerializers(serializers.ModelSerializer):
    owner = ProfileSerializer(many=False)
    tags = TagSerializer(many=True)
    review = serializers.SerializerMethodField()
    
    class Meta:
        model = Project
        fields = '__all__'

    def get_review(self, obj):
        reviews = obj.review_set.all()
        serializer = ReviewSerializer(reviews, many=True)
        return serializer.data