from django.urls import path # type: ignore
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('logout', views.logout, name='logout'),
    path('home', views.home, name='home'),
    path('eventos/<int:id>/', views.details, name='details'),
    path('subscribers', views.subscribers, name='subscribers'),
    path('user/create', views.createUser, name='createUser'),
    path('user/edit', views.editUser, name='editUser'),
    path('event/create', views.createEvent, name='createEvent'),
    path('event/<int:id>/edit', views.editEvent, name='editEvent'),
    path('event/<int:id>/delete', views.deleteEvent, name='deleteEvent'),
]