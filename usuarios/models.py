from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class UsuarioAdministrador(AbstractUser):
    """
    Modelo personalizado para usuarios, enfocado en administradores.
    Extiende AbstractUser para agregar funcionalidades específicas.
    """
    is_admin = models.BooleanField(default=True)  # Indica que es un usuario administrador

    # Resolver conflictos de relaciones inversas
    groups = models.ManyToManyField(
        Group,
        related_name="usuarioadministrador_set",  # Nombre único para la relación inversa
        blank=True,
        help_text="Los grupos a los que pertenece este usuario.",
        verbose_name="grupos",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="usuarioadministrador_set",  # Nombre único para la relación inversa
        blank=True,
        help_text="Permisos específicos para este usuario.",
        verbose_name="permisos de usuario",
    )

    def __str__(self):
        return self.username