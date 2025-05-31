from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from .models import Evento, Usuario
from django.contrib.auth.decorators import login_required #type: ignore
from datetime import datetime

def home(request):
    eventos = Evento.objects.all()
    return render(request, 'events/home.html', {'eventos': eventos})


def details(request, id):
    evento = get_object_or_404(Evento, id=id)
    return render(request, 'events/details.html', {'evento': evento})

def subscribers(request):
    subscribers = Usuario.objects.all()
    return render(request, 'events/subscribers.html', {'subscribers': subscribers})

def login(request):
    return render(request, 'login.html')

def createUser(request):
    return render(request, 'users/create-user.html')

@login_required
def createEvent(request):
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        data_str = request.POST.get('data')  # Ex: '2025-08-01T21:00'
        data = datetime.strptime(data_str, '%Y-%m-%dT%H:%M')
        local = request.POST.get('local')
        descricao = request.POST.get('descricao')

        Evento.objects.create(
            titulo=titulo,
            data=data,
            local=local,
            descricao=descricao,
            organizador=request.user
        )

        return redirect('home')

    return render(request, 'events/create-event.html')