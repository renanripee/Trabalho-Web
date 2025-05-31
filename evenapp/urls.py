from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('home', views.home, name='home'),
    path('eventos/<int:id>/', views.details, name='details'),
    path('subscribers', views.subscribers, name='subscribers'),
    path('user/create', views.createUser, name='createUser'),
    path('event/create', views.createEvent, name='createEvent'),
]