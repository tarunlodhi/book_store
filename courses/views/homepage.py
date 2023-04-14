from django.shortcuts import render
from courses.models.course import Course
from django.views.generic import ListView

class HomePageView(ListView):
    template_name="home.html"
    queryset = Course.objects.filter(active=True)
    context_object_name ="courses"