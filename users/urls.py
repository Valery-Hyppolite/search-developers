#from django.contrib import admin
from django.urls import path
from users.views import profiles, user_profile, loginUser, logoutUser, registerUser, user_account, edit_account, create_skill, update_skill, deleteskill, inbox, each_message, sendMessage

urlpatterns = [
    #path('admin/', admin.site.urls)
    path('login/', loginUser, name='login'),
    path('', profiles, name='profiles'),
    path('logout/', logoutUser, name='logout'),

    path('register/', registerUser, name='register'),
    path('user-profile/<str:pk>/', user_profile, name='userprofile'),

    path('user-account/', user_account, name='useraccount'),
    path('edit-account/', edit_account, name='edit-account'),

    path('createskill/', create_skill, name='createskill'),
    path('update-skill/<str:pk>/', update_skill, name='updateskill'),
    path('delete-skill/<str:pk>/', deleteskill, name='deleteskill'),

    path('inbox/', inbox, name='inbox'),
    path('message/<str:pk>/', each_message, name='message'),
    path('send-message/<str:pk>/', sendMessage, name='send_message'),

    #path('project/<str:pk>/', project_view, name='project'),

]