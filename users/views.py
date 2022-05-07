from django.http import request
from django.shortcuts import render, redirect
from .models import Profile, Skill
from projects.models import Project
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django. contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .form import CustomUserCreationForm,  PorfileForm, SkillForm, MessageForm
from .utils  import searchProfiles, paginateProfiles
#from django.contrib.auth.forms import UserCreationForm




# Create your views here.
# user log in and log out section

def loginUser(request):
    page = 'login'

    if request.user.is_authenticated: # if user is alredy authenticated, do not allow them to see the login page, send then directky to the profilespage.
        return redirect('profiles')

    if request.method == 'POST':
        print(request.POST['username'])
        username = request.POST['username'].lower()
        password = request.POST['password']
        try:
            user = User.objects.get(username=username) # check to see if user exist
        except:
            messages.error(request, 'Username does not exist')
        
        user = authenticate(request, username=username, password=password) # if user exist, check their usename and password in data base
        if user is not None:
            login(request, user)
            messages.info(request, 'Logged in successfully')

            return redirect(request.GET['next'] if 'next' in request.GET else 'useraccount')
        else:
            pass
            messages.error(request, 'Username or Password is incorrect')

    return render(request, 'users/loginregister.html')



def logoutUser(request):
    logout(request)
    messages.info(request, 'User successfully logged out')
    return redirect('login')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()

    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request,'User account was created!')

            login(request, user)
            return redirect('edit-account')
        else:
            messages.error(request,'An error has occurred during resgistration')



    context = {'page': page, 'form': form}
    return render(request, 'users/loginregister.html', context)


# template routing section

def profiles(request):
    profiles, search_query = searchProfiles(request)
    custom_range, profiles =  paginateProfiles(request, profiles, result=2)

    # search_query = ''

    # if request.GET.get('search_query'):
    #     search_query = request.GET.get('search_query')
    # skills = Skill.objects.filter(skill_name__iexact=search_query)
    # profiles = Profile.objects.distinct().filter(
    #     Q(name__icontains=search_query) | 
    #     Q(short_intro__icontains=search_query) | 
    #     Q(skill__in=skills))
    #profiles = Profile.objects.all() this show all the developers. the above function allow query functionality, this with  .all()  does not. thi render all the developers that exist in this database
    #skills = Skill.objects.all()

    context = {'profiles': profiles, 'search_query':search_query, 'custom_range':custom_range}
    return render(request, 'users/profiles.html', context)



def user_profile(request, pk):
    user_profile = Profile.objects.get(id=pk)
    #user_project = Project.objects.get(id=pk)
    skills = user_profile.skill_set.exclude(description='')
    otherskills = user_profile.skill_set.filter(description='')

    context = {'profile': user_profile, 'skills': skills, 'otherskills': otherskills}
    return render(request, 'users/user-profile.html', context)



@login_required(login_url='login')
def user_account(request):

    user_profile = request.user.profile
    skills = user_profile.skill_set.all()
    projects = user_profile.project_set.all()

    context = {'skills': skills, 'profile': user_profile, 'projects':projects}
    return render(request, 'users/account.html', context)


@login_required(login_url='login')
def edit_account(request):
    '''when the user request to update their profile, this view will process the form and save it.'''
    profile = request.user.profile # get the user prfile that is sending the data.
    form = PorfileForm(instance=profile)

    if request.method == 'POST':
        form = PorfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('useraccount')

    context = {'form': form}
    return render(request, 'users/profile_form.html', context)



# create and add skill section


@login_required(login_url='login')
def create_skill(request):
    profile = request.user.profile
    form = SkillForm()

    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill =  form.save(commit=False)
            skill.owner = profile
            skill.save()
            messages.success(request, 'Skill was sucessfully added!')
            return redirect('useraccount')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)



@login_required(login_url='login')
def update_skill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    form = SkillForm(instance=skill) # preload the page with the informationj

    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, 'Skill was updated successfully')
            return redirect('useraccount')

    context = {'form': form}
    return render(request, 'users/skill_form.html', context)
    

@login_required(login_url='login')
def deleteskill(request, pk):
    profile = request.user.profile
    skill = profile.skill_set.get(id=pk)
    if request.method == 'POST':
        skill.delete()
        messages.success(request, 'skill was deleted successfully!')
        return redirect('useraccount')

    context = {'object': skill}
    return render(request, 'delete_object.html', context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messagesRequest = profile.messages.all()
    unreadCount = messagesRequest.filter(is_read=False).count()

    context = {'messagesRequest':messagesRequest, 'unreadCount':unreadCount}
    return render(request, 'users/inbox.html', context)

@login_required(login_url='login')
def each_message(request, pk):
    profile = request.user.profile
    message_Request = profile.messages.get(id=pk)

    # this section mark the message as read once the user click on it.
    if message_Request.is_read == False:
        message_Request.is_read = True
        message_Request.save()
    
    context = {'message_request':message_Request}
    return render(request, 'users/messages.html', context)



def sendMessage(request, pk):
    form = MessageForm()
    recipient = Profile.objects.get(id=pk)
    try:
        sender = request.user.profile
    except:
        sender = None
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient

            if sender:
                message.name = sender.name
                message.email = sender.email
                
            message.save()
            messages.success(request, 'Your message was sent sucesfully')
            return redirect('userprofile', pk=recipient.id)

    context = {'form': form, 'recipient': recipient}
    return render(request, 'users/message_form.html', context)
