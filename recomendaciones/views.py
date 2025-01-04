from django.shortcuts import render,get_object_or_404, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from .models import Recomendacion

# Create your views here.

def admin_view(request):
    # datos de la tabla
    recommendations = Recomendacion.objects.all()

    # Seleccionamos la primera recomendación como "selected_recommendation"
    selected_recommendation = recommendations[0] if recommendations else None

    return render(request, 'recomendaciones/admin_view.html', {
        'recommendations': recommendations,
        'selected_recommendation': selected_recommendation,
        'external_url': 'https://ia-proyecto-dun.vercel.app/',
    })


def eliminar_recomendacion(request, pk):
    recomendacion = get_object_or_404(Recomendacion, pk=pk)
    recomendacion.delete()
    return redirect(reverse('admin_view'))

class CrearRecomendacionView(CreateView):
    model = Recomendacion
    template_name = 'recomendaciones/crear_recomendacion.html'
    fields = ['nombre_actividad', 'ciudad', 'duracion', 'rango_desde', 'rango_hasta', 'categoria', 'descripcion']
    success_url = reverse_lazy('admin_view') # me manda a la pag principal cuando guarda