from django.shortcuts import render, get_object_or_404
from .models import Evento

def home(request):
    eventos = Evento.objects.all()
    return render(request, 'events/home.html', {'eventos': eventos})

def details(request, id):
    evento = get_object_or_404(Evento, id=id)
    return render(request, 'events/details.html', {'evento': evento})