
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from projects.models import Project, Tag
from django.db.models import Q

def paginateProjects(request, projects, result):

    page = request.GET.get('page')
    result = 6
    paginator = Paginator(projects, result)
    try:
        projects = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        projects = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)
    
    leftIndex = (int(page) - 1)
    if leftIndex < 1:
        leftIndex = 1
    
    rightIndex = (int(page) + 2)
    if rightIndex  >  paginator.num_pages:
        rightIndex = paginator.num_pages +  1

    custom_range = range(leftIndex, rightIndex)  
# this  custom  indexes handle how many pagination you see as you move  left  and  right  to  the next  or  previous page. I set it  to  show 1 previus page  to the left and right.
# the order of the cusom range and project matter in the view page. their position need to match in the view.py when using them or an error willl be thrown.
    return custom_range, projects



def searchProject(request):
    search_query =  ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        
    projects_tags = Tag.objects.filter(name__icontains=search_query)
    projects = Project.objects.distinct().filter(Q(title__icontains=search_query)| Q(owner__name__icontains=search_query) | Q(tags__in=projects_tags))
    
    
    return search_query, projects