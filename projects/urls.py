
from django.contrib import admin
from django.urls import path
from projects.views import projects_view, project_view, createproject, updateproject, deleteproject

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', projects_view, name='projects'),
    path('project/<str:pk>/', project_view, name='project'),
    path('createproject/', createproject, name='createproject'),
    path('updateproject/<str:pk>/', updateproject, name='updateproject'),
    path('deleteproject/<str:pk>/', deleteproject, name='deleteproject')

]