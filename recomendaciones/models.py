from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Recomendacion(models.Model):
    nombre_actividad = models.CharField(max_length=255)
    ciudad = models.CharField(max_length=255)
    rango_desde = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ],
        help_text="Debe ser un número entre 0 y 10"
    )
    rango_hasta = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(0),
            MaxValueValidator(10)
        ],
        help_text="Debe ser un número entre 0 y 10"
    )
    categoria = models.CharField(max_length=100)
    duracion = models.DurationField()
    descripcion = models.TextField()
    horario = models.CharField(max_length=255)



    def __str__(self):
        return f"{self.nombre_actividad} en {self.ciudad}"

class UploadedImage(models.Model):
    original_image = models.ImageField(upload_to='images/original/')
    processed_image = models.ImageField(upload_to='images/procesada/', null=True, blank=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)