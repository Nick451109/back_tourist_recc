from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import UsuarioAdministrador

@admin.register(UsuarioAdministrador)
class UsuarioAdministradorAdmin(UserAdmin):
    # Campos que se muestran en la lista de usuarios
    list_display = ('username', 'email', 'is_admin', 'is_staff', 'is_superuser')
    list_filter = ('is_admin', 'is_staff', 'is_superuser')
    
    # Campos para editar usuarios en el formulario
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('is_admin',)}),
    )