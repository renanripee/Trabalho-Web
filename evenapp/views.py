from django.shortcuts import render, get_object_or_404 # type: ignore
from .models import Evento

def home(request):
    eventos = Evento.objects.all()
    return render(request, 'events/home.html', {'eventos': eventos})

def details(request, id):
    evento = get_object_or_404(Evento, id=id)
    return render(request, 'events/details.html', {'evento': evento})

def login(request):
    return render(request, 'login.html')

def createUser(request):
    return render(request, 'users/create-user.html')

def createEvent(request):
    return render(request, 'events/create-event.html')