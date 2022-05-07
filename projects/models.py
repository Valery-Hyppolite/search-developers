from django.db import models
import uuid
from users.models import Profile

from django.db.models.base import Model

# Create your models here.
class Project(models.Model):
    owner       = models.ForeignKey(Profile, null=True, blank=True, on_delete=models.CASCADE)
    title       = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    feature_image = models.ImageField(null=True, blank=True, default='default.jpeg')
    demo_link   =  models.CharField(max_length=2000, null=True, blank=True)
    source_link = models.CharField(max_length=2000, null=True, blank=True)
    tags        = models.ManyToManyField('Tag', blank=True)
    vote_total  = models.IntegerField(default=0, null=True, blank=True)
    vote_ratio  = models.IntegerField(default=0, null=True, blank=True)
    create      = models.DateTimeField(auto_now_add=True)
    id          = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.title

    class Meta:
        '''This method also help with pagination. which help yieling consistent result'''
        ordering = ['-vote_ratio', '-vote_total', 'title']
    
    @property
    def image_url(self):
        try:
            img = self.feature_image.url
        except:
            img = ''
        return img

    @property
    def reviewers(self):
        """this function gives a list of all the people that have reviewd projectd"""
        querySet = self.review_set.all().values_list('owner__id', flat=True)
        return querySet

    @property
    def get_vote_count(self):
        '''this function is calculating the total votes and ratio so we can output that dynamically for each project on the view to reflet on the website
        anytime someone add a new comment and vote, this function is run a new calculation and save it.'''
        totalReviews = self.review_set.all()
        upVotes      = totalReviews.filter(value='up').count()
        totalVotes   = totalReviews.count()

        ratio = (upVotes / totalVotes) * 100
        self.vote_total = totalVotes
        self.vote_ratio = ratio
        self.save()


class Review(models.Model):
    VOTE_TYPE = (
        ('up', 'up vote'),
        ('down', 'down vote')
    )
    owner = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    body    = models.TextField(null=True, blank=True)
    value   = models.CharField(max_length=200, choices=VOTE_TYPE)
    create   = models.DateTimeField(auto_now_add=True)
    id      = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    class Meta:
        '''this make sure that only one review per owner can be written per project.'''
        unique_together = [['owner', 'project']]

    def __str__(self):
        return self.value


class Tag(models.Model):
    name  = models.CharField(max_length=200,)
    create = models.DateTimeField(auto_now_add=True)
    id    = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name