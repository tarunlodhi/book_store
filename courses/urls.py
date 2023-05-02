from django.contrib import admin
from django.urls import path
from .views import HomePageView,coursePage,SignupView,LoginView,signout,checkout,verifyPayment,my_courses,success,token_send
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', HomePageView.as_view() ,name="home"),
    path('signup', SignupView.as_view() ,name="signup"),
    path('login', LoginView.as_view() ,name="login"),
    path('logout', signout ,name="logout"),
    path('my-courses', my_courses ,name="my-courses"),
    path('course/<str:slug>', coursePage ,name="coursepage"),
    path('check-out/<str:slug>', checkout ,name="check-out"),
    path('verify_payment', verifyPayment ,name="verify_payment"),
    path('token',token_send,name='token_send'),
    path('success',success,name='success')

]
