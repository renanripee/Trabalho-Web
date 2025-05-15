from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

class UsuarioManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('O email é obrigatório')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Apenas UM superusuário pode existir, e não cria outros.
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if Usuario.objects.filter(is_superuser=True).exists():
            raise ValueError('Já existe um superusuário.')
        return self.create_user(email, password, **extra_fields)

class Usuario(AbstractBaseUser, PermissionsMixin):
    TIPO_USUARIO_CHOICES = [
        ('admin', 'Administrador'),
        ('criador', 'Criador de Evento'),
        ('normal', 'Usuário Normal'),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    telefone = models.CharField(max_length=20, blank=True)
    tipo = models.CharField(max_length=10, choices=TIPO_USUARIO_CHOICES, default='normal')

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)  # necessário para acessar o admin
    date_joined = models.DateTimeField(default=timezone.now)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'telefone']

    def __str__(self):
        return f"{self.email} ({self.tipo})"

    def is_criador(self):
        return self.tipo == 'criador'

    def is_normal(self):
        return self.tipo == 'normal'

    def is_admin_personalizado(self):
        return self.tipo == 'admin' and self.is_superuser

class Evento(models.Model):
    titulo = models.CharField(max_length=255)
    data = models.DateTimeField()
    local = models.CharField(max_length=255)
    organizador = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='eventos_organizados'
    )

    def __str__(self):
        return self.titulo

class Inscricao(models.Model):
    usuario = models.ForeignKey(
        Usuario,
        on_delete=models.CASCADE,
        related_name='inscricoes'
    )
    evento = models.ForeignKey(
        Evento,
        on_delete=models.CASCADE,
        related_name='inscricoes'
    )
    data_inscricao = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'evento')
        verbose_name = 'Inscrição'
        verbose_name_plural = 'Inscrições'

    def __str__(self):
        return f"{self.usuario.email} em {self.evento.titulo}"

