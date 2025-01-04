from django.db import models

# Create your models here.

class Itinerario(models.Model):
    dia = models.CharField(max_length=255)
    medio_dia = models.CharField(max_length=255)
    noche = models.CharField(max_length=255)


    def __str__(self):
        return f"Dia: {self.dia} Medio dia: {self.medio_dia }Noche: {self.noche}"