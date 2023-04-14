from django.contrib import admin
from django.urls import path
from .views import HomePageView,coursePage,SignupView,LoginView,signout,checkout,verifyPayment,my_courses
from django.conf.urls.static import static
from book_store.settings import MEDIA_ROOT, MEDIA_URL
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

] + static(MEDIA_URL, document_root=MEDIA_ROOT)

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
