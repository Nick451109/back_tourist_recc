from django.shortcuts import render,get_object_or_404, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from .models import Recomendacion
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
from io import BytesIO
from PIL import Image
from .models import UploadedImage
from django.conf import settings
import os
import json

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


MEDIA_DIR = "media/images"

@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            image_data = body.get("image")

            if not image_data:
                return JsonResponse({"error": "No se proporcionó una imagen válida"}, status=400)

            # Eliminar el prefijo "data:image/png;base64,"
            if image_data.startswith("data:image/"):
                image_data = image_data.split(",")[1]

            # Decodificar la imagen base64
            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes))

            # Guardar la imagen original
            original_path = os.path.join(MEDIA_DIR, "original", "original_image.png")
            os.makedirs(os.path.dirname(original_path), exist_ok=True)
            image.save(original_path)

            # Procesar la imagen (ejemplo: convertir a escala de grises)
            # TODO: procesar con el modelo de IA

            #processed_image = image.convert("L")
            #processed_path = os.path.join(MEDIA_DIR, "procesada", "processed_image.png")
            #os.makedirs(os.path.dirname(processed_path), exist_ok=True)
            #processed_image.save(processed_path)

            # Responder con las rutas de las imágenes
            return JsonResponse({
                "message": "Imagen procesada exitosamente",
                "original_image_url": f"/media/images/original/original_image.png",
                #"processed_image_url": f"/media/images/procesada/processed_image.png"
            }, status=200)

        except Exception as e:
            return JsonResponse({"error": f"Error al procesar la imagen: {str(e)}"}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)

class CrearRecomendacionView(CreateView):
    model = Recomendacion
    template_name = 'recomendaciones/crear_recomendacion.html'
    fields = ['nombre_actividad', 'ciudad', 'duracion', 'rango_desde', 'rango_hasta', 'categoria', 'descripcion']
    success_url = reverse_lazy('admin_view') # me manda a la pag principal cuando guarda