from django.shortcuts import render,redirect
from courses.models import Course,Video,UserCourse
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView

@login_required(login_url="login")
def my_courses(request):
    user = request.user
    user_course = UserCourse.objects.filter(user = user)
    context ={
         "user_courses" : user_course
    }
    return render(request,template_name="my-courses.html",context=context)

def coursePage(request,slug):
        course = Course.objects.get(slug  = slug)
        serial_number  = request.GET.get('lecture')
        videos = course.video_set.all().order_by("serial_number")
        next_lecture = 2
        previous_lecture = None
        if serial_number is None:
            serial_number = 1 
        else:
            next_lecture = int(serial_number) + 1
            if len(videos)<next_lecture:
                  next_lecture=None
            
            if int(serial_number)>1:
                previous_lecture = int(serial_number) - 1

        video = Video.objects.get(serial_number = serial_number , course = course)

        if (video.is_preview is False):

            if request.user.is_authenticated is False:
                return redirect("login")
            else:
                user = request.user
                try:
                    user_course = UserCourse.objects.get(user = user  , course = course)
                except:
                    return redirect("check-out" , slug=course.slug)
            
            
        context = {
            "course" : course , 
            "video" : video , 
            'videos':videos,
            "next_lecture":next_lecture,
            "previous_lecture":previous_lecture
        }
        return  render(request , template_name="course_page.html" , context=context )    