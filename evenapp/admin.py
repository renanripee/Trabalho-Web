from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario, Evento, Inscricao

class UsuarioAdmin(UserAdmin):
    model = Usuario
    list_display = ('email', 'first_name', 'last_name', 'tipo', 'is_staff', 'is_active')
    list_filter = ('tipo', 'is_staff', 'is_active')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações Pessoais', {'fields': ('first_name', 'last_name', 'telefone', 'tipo')}),
        ('Permissões', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'telefone', 'tipo', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)

admin.site.register(Usuario, UsuarioAdmin)
admin.site.register(Evento)
admin.site.register(Inscricao)
