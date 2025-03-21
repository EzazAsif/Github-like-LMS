from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from accounts.models import User
from lms.models import Department,Course

@login_required
# Create your views here.
def departments(request):
    departments=Department.objects.all().order_by('name')
    context={'name':request.user.username,'departments':departments}

    return render(request,"departments.html",context)
@login_required
def courses(request):
    courses = Course.objects.all().order_by('course_name')

    context={'name':request.user.username,'courses':courses}

    return render(request,"courses.html",context)
@login_required
def students(request):
    users=User.objects.all()
    context={'name':request.user.username,'users':users}

    return render(request,"students.html",context)

@login_required
def appoint(request):
    if (request.user.role!='admin' and request.user.role!='master'):
        return redirect('/errors/unauthorizedaccess')
    admins=User.objects.filter(role='admin')
    
    moderators=User.objects.filter(role='mod')
    rusers=User.objects.filter(role='user')
    isMaster=(request.user.role=='master')
    context={'name':request.user.username,'rusers':rusers,'admins':admins,'moderators':moderators,'isMaster':isMaster}
    
    return render(request,"appoint.html",context)



def changerole(request,userid,role):
    if(request.user.role not in ['admin','master']):
        return redirect('/errors/illegalactivity')
        
    if((role=='master' or role=='admin')and request.user.role!='master'):
        return redirect('/errors/illegalactivity')
    user=User.objects.get(id=userid)
    user.role=role
    user.save()
    return redirect('appoint')