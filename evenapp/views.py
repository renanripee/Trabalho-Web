from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from .models import Evento, Usuario
from django.contrib.auth.decorators import login_required #type: ignore
from django.contrib.auth import authenticate, login as auth_login #type: ignore
from django.contrib.auth import logout as django_logout #type: ignore
from django.contrib import messages #type: ignore
from datetime import datetime
from django.http import HttpResponseForbidden #type: ignore
from functools import wraps

def user_type_required(*tipos_permitidos):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.tipo in tipos_permitidos:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("Acesso negado.")
        return wrapper
    return decorator


def home(request):
    eventos = Evento.objects.all()
    return render(request, 'events/home.html', {'eventos': eventos})


def details(request, id):
    evento = get_object_or_404(Evento, id=id)
    return render(request, 'events/details.html', {'evento': evento})

def subscribers(request):
    subscribers = Usuario.objects.all()
    return render(request, 'events/subscribers.html', {'subscribers': subscribers})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        usuario = authenticate(request, username=email, password=senha)

        if usuario is not None:
            auth_login(request, usuario)
            return redirect('home')
        else:
            messages.error(request, 'Email ou senha inválidos.')

    return render(request, 'login.html')

def logout(request):
    django_logout(request)
    return redirect('login')

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
            return redirect('login')
        
        except Exception as e:
            return render(request, 'users/create-user.html', {'erro': str(e)})

    return render(request, 'users/create-user.html')

def editUser(request):
    usuario = request.user

    if request.method == 'POST':
        usuario.first_name = request.POST.get('first_name')
        usuario.last_name = request.POST.get('last_name')
        usuario.telefone = request.POST.get('telefone')
        usuario.save()
        return redirect('home')

    return render(request, 'users/create-user.html', {
        'usuario': usuario,
        'modo_edicao': True
    })


@user_type_required('criador')
def createEvent(request):
    
    if request.method == 'POST':
        titulo = request.POST.get('titulo')
        data_str = request.POST.get('data')
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