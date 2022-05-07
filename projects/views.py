from os import name
from django.shortcuts import redirect, render
from django. contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.contrib import messages
from projects.models import Project, Tag
from .forms import ProjectForm, ReviewForm
from django.db.models import Q
from .search_function import searchProject, paginateProjects


# Create your views here.

def projects_view(request):

    search_query, projects = searchProject(request)
    custom_range, projects =  paginateProjects(request, projects, result=6)
    #projects = Project.objects.all()

    context = {'projects': projects, 'search_query':search_query, 'custom_range':custom_range}
    return render(request, 'projects/projects.html', context)


def project_view(request, pk):
    object = Project.objects.get(id=pk)
    form = ReviewForm()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.project = object
            review.owner = request.user.profile
            review.save()
            object.get_vote_count
            messages.success(request, 'Your review was sucesfuly submitted')
            return redirect('project', pk=object.id) #the redirect simply refhresh the page and clear the comment section.

    #tags = object.tags.all()
    context = {'obj': object, 'form':form}

    return render(request, 'projects/project.html', context)

@login_required(login_url='login')   # this require the user to be authenticated to be able to see this age.
def createproject(request):
    profile =  request.user.profile
    form = ProjectForm()

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace("," , " ").split()
        #print(request.POST)
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile # this part connect the profject to the profile owner
            project.save()
            
            for tag in newtags: 
                tag,  created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('useraccount')
        else:
            print('invalid form')



    context = {'form': form}
    return render(request, 'projects/projects_form.html', context)

@login_required(login_url='login')
def updateproject(request, pk):
    profile = request.user.profile # get the user that is currenlty logged in
    # project = Project.objects.get(id=pk) this one isjust getting the object by it id. 
    project = profile.project_set.get(id=pk) # get all the projects of that user, then getting  the specific project that the user wants to edit.
    form = ProjectForm(instance=project)

    if request.method == 'POST':
        newtags = request.POST.get('newtags').replace("," , " ").split()
        print(newtags)
        #print(request.POST)
        form = ProjectForm(request.POST, request.FILES, instance=project)
        if form.is_valid():
            project = form.save()
            for tag in newtags: 
                tag,  created = Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            messages.success(request, 'project was updated successfully!')
            return redirect('useraccount')
        else:
            print('invalid form')


    context = {'form': form, 'project':project}
    return render(request, 'projects/projects_form.html', context)

@login_required(login_url='login')
def deleteproject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    #project = Project.objects.get(id=pk) again only getting the project by its id, not associated with any profile
    if request.method == 'POST':
        project.delete()
        messages.success(request, 'project was deleted successfully!')
        return redirect('useraccount')

    context = {'object': project}
    return render(request, 'delete_object.html', context)


