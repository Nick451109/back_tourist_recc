from django.shortcuts import render
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy
from .models import Recomendacion

# Create your views here.

def admin_view(request):
    recommendations = [
        {'name': 'Museo de Arte', 'city': 'Ciudad X', 'duration': '2 horas', 'category': 'Cultural', 'description': 'Un museo increíble.'},
        {'name': 'Parque Nacional', 'city': 'Ciudad Y', 'duration': '4 horas', 'category': 'Aventura', 'description': 'Un parque con paisajes hermosos.'},
    ]
    selected_recommendation = recommendations[0] if recommendations else None
    return render(request, 'recomendaciones/admin_view.html', {
        'recommendations': recommendations,
        'selected_recommendation': selected_recommendation,
        'external_url': 'https://ia-proyecto-dun.vercel.app/',
    })


class CrearRecomendacionView(CreateView):
    model = Recomendacion
    template_name = 'recomendaciones/crear_recomendacion.html'  # Ruta al template del formulario
    fields = ['nombre_actividad', 'ciudad', 'duracion', 'rango_desde', 'rango_hasta', 'categoria', 'descripcion']
    success_url = reverse_lazy('admin_view')  # Redirige a la página principal después de guardar