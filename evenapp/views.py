from django.shortcuts import render, redirect, get_object_or_404 # type: ignore
from .models import Evento, Usuario, Inscricao
from django.contrib.auth.decorators import login_required #type: ignore
from django.contrib.auth import authenticate, login as auth_login #type: ignore
from django.contrib.auth import logout as django_logout #type: ignore
from django.contrib import messages #type: ignore
from datetime import datetime
from django.http import HttpResponseForbidden #type: ignore
from functools import wraps
from datetime import date

def user_type_required(*tipos_permitidos):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.tipo in tipos_permitidos:
                return view_func(request, *args, **kwargs)
            return HttpResponseForbidden("Acesso negado.")
        return wrapper
    return decorator

@user_type_required('normal')
def subscribe(request, id):
    if request.method == 'POST' and request.user.is_authenticated and request.user.tipo == 'normal':
        evento = get_object_or_404(Evento, pk=id)

        if not Inscricao.objects.filter(usuario=request.user, evento=evento).exists():
            Inscricao.objects.create(usuario=request.user, evento=evento)
            messages.success(request, 'Inscrição realizada com sucesso!')
        else:
            messages.warning(request, 'Você já está inscrito neste evento.')
    return redirect('details', id=id)

@user_type_required('normal')
def cancelSubscribe(request, id):
    evento = get_object_or_404(Evento, id=id)
    inscricao = Inscricao.objects.filter(evento=evento, usuario=request.user).first()
    if inscricao:
        inscricao.delete()
        messages.success(request, "Inscrição cancelada com sucesso.")
    else:
        messages.error(request, "Você não está inscrito neste evento.")
    return redirect('details', id=id)


@user_type_required('criador', 'admin')
def listSubscribers(request, id):
    evento = get_object_or_404(Evento, pk=id)
    subscriptions = Inscricao.objects.filter(evento=evento)
    subscribers = [subscription.usuario for subscription in subscriptions]
    return render(request, 'events/subscribers.html', {
        'evento': evento,
        'subscribers': subscribers
    })

@user_type_required('normal')
def mysubscriptions(request):
    subscriptions = Inscricao.objects.filter(usuario=request.user)
    events = [subscription.evento for subscription in subscriptions ]
    return render(request, 'events/home.html', {
        'eventos': events,
        'tipo': 'Minhas Inscrições'
    })

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

@user_type_required('admin')
def users(request):
    subscribers = Usuario.objects.all()
    return render(request, 'events/subscribers.html', {'subscribers': subscribers})

def createUser(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        telefone = request.POST.get('telefone')
        tipo = request.POST.get('tipo') or 'normal'
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

    return render(request, 'users/create-user.html', {
        'modo_edicao': False
    })

@login_required
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

def home(request):
    events = Evento.objects.all()
    return render(request, 'events/home.html', {
        'eventos': events,
        'tipo': 'Eventos'
    })

@user_type_required('criador', 'admin')
def myevents(request): 
    events = Evento.objects.filter(organizador=request.user)
    return render(request, 'events/home.html', {
        'eventos': events,
        'tipo': 'Meus Eventos'
    })

def details(request, id):
    evento = Evento.objects.get(id=id)
    inscrito = False
    past_date = evento.data.date() < date.today()

    if request.user.is_authenticated and request.user.tipo == 'normal':
        inscrito = Inscricao.objects.filter(evento=evento, usuario=request.user).exists()
    return render(request, 'events/details.html', {
        'evento': evento,
        'inscrito': inscrito,
        'past_date': past_date,
    })

@user_type_required('criador', 'admin')
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

    return render(request, 'events/create-event.html', {
        'modo_edicao': False
    })

@user_type_required('criador', 'admin')
def editEvent(request, id):
    evento = get_object_or_404(Evento, id=id)

    if request.method == 'POST':
        evento.titulo = request.POST.get('titulo')
        evento.data = request.POST.get('data')
        evento.local = request.POST.get('local')
        evento.descricao = request.POST.get('descricao')
        evento.save()
        return redirect('details', id=evento.id)

    return render(request, 'events/create-event.html', {
        'evento': evento,
        'modo_edicao': True
    })

@user_type_required('criador', 'admin')
def deleteEvent(request, id):
    evento = get_object_or_404(Evento, id=id)

    if evento.organizador != request.user:
        messages.error(request, "Você não tem permissão para deletar este evento.")
        return redirect('home')

    if request.method == 'POST':
        evento.delete()
        return redirect('home')

    return redirect('details', id=id)