from django.urls import path
from . import views

urlpatterns = [
    path('home', views.home, name='home'),
    path('eventos/<int:id>/', views.details, name='details'),
    path('', views.login, name='login'),

]