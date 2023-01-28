from django.urls import path
from . import views

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [

    path('users/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('', views.getRoutes),
    path('projects/', views.getProjects),
    path('profiles/', views.getProfiles),
    path('project/<str:pk>', views.getProject),
     path('profile/<str:pk>', views.getProfile),
    path('project/<str:pk>/vote/', views.projectVote),

    path('remove_tag/', views.remove_tag),
]