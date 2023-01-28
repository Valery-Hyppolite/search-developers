#from django.http import JsonResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import serializers, status  
from .serializers import ProjectSerializers, ProfileSerializer
from projects.models import Project, Review, Tag, Profile


@api_view(['GET'])
def getRoutes(request):

    routes = [
        {'GET': '/api/projects'},
        {'GET': '/api/projects/id'},
        {'POST': '/api/projects/id/vote'},

         {'GET': '/api/users'},
        {'GET': '/api/users/id'},

        {'POST': '/api/users/token'},
        {'POST': '/api/users/token/refresh'}
    ]
    return Response(routes)


@api_view(['GET'])
def getProjects(request):
    projects = Project.objects.all()
    serializer_projects = ProjectSerializers(projects, many=True)
    return Response(serializer_projects.data)

@api_view(['GET'])
def getProject(request, pk):
    projects = Project.objects.get(id=pk)
    serializer_projects = ProjectSerializers(projects, many=False)
    return Response(serializer_projects.data)

@api_view(['GET'])
def getProfiles(request):
    profiles = Profile.objects.all()
    serializer_profiles = ProfileSerializer(profiles, many=True)
    return Response(serializer_profiles.data)


@api_view(['GET'])
def getProfile(request, pk):
    userProfile = Profile.objects.get(id=pk)
    #projects = userProfile.project_set.all()
    serializer_profile = ProfileSerializer(userProfile, many=False)
    #user_projects_serializers = ProjectUserSerializer(projects, many=True)
    return Response(serializer_profile.data)


def projectVote(request, pk):
    project = Project.objects.get(id=pk)
    user = request.user.profile
    data = request.data
    review, created = Review.objects.get_or_create(owner=user, project=project)
    review.value = data['value']
    review.save()
    project.get_vote_count

    print('data', data)

    serializer = ProjectSerializers(project, many=False)
    return Response(serializer.data)

@api_view(['DELETE'])
def remove_tag(request):
    tag_id = request.data['tag']
    project_id = request.data['project']

    project = Project.objects.get(id=project_id)
    tag = Tag.objects.get(id=tag_id)
    project.tags.remove(tag)

    return Response('Tag was removed')


# def getRoutes(request):

#     routes = [
#         {'GET': '/api/projects'},
#         {'GET': '/api/projects/id'},
#         {'POST': '/api/projects/id/vote'},

#         {'POST': '/api/users/token'},
#         {'POST': '/api/users/token/refresh'}
#     ]
#     return JsonResponse(routes, safe=False)