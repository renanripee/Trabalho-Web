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
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        telefone = request.POST.get('telefone')
        tipo = request.POST.get('tipo')
        senha = request.POST.get('senha')
        confirmacao = request.POST.get('confirmacao_senha')

        if senha != confirmacao:
            return render(request, 'users/create-user.html', {'erro': 'As senhas não coincidem.'})

        try:
            Usuario.objects.create_user(
                email=email,
                password=senha,
                first_name=first_name,
                last_name=last_name,
                telefone=telefone,
                tipo=tipo
            )
            return redirect('home')
        
        except Exception as e:
            return render(request, 'users/create-user.html', {'erro': str(e)})

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