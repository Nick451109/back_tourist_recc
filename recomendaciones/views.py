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


@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        image_data = request.POST.get("image")
        if image_data:
            # Decodificar la imagen base64
            format, imgstr = image_data.split(';base64,')  # Dividir datos base64
            ext = format.split('/')[-1]  # Extraer extensión
            img = base64.b64decode(imgstr)

            # Guardar la imagen original en 'images/original'
            original_path = os.path.join(settings.MEDIA_ROOT, 'images/original')
            os.makedirs(original_path, exist_ok=True)
            original_file_name = f"{original_path}/original_image.{ext}"

            with open(original_file_name, "wb") as f:
                f.write(img)

            # Procesar la imagen (ejemplo: redimensionar)
            original_image = Image.open(BytesIO(img))
            processed_image = original_image.resize((400, 400))  # Redimensionar a 400x400

            # Guardar la imagen procesada en 'images/procesada'
            processed_path = os.path.join(settings.MEDIA_ROOT, 'images/procesada')
            os.makedirs(processed_path, exist_ok=True)
            processed_file_name = f"{processed_path}/processed_image.{ext}"
            processed_image.save(processed_file_name)

            # Guardar en el modelo UploadedImage
            uploaded_image = UploadedImage.objects.create(
                original_image=f"images/original/original_image.{ext}",
                processed_image=f"images/procesada/processed_image.{ext}",
            )

            return JsonResponse({
                "message": "Imagen recibida y procesada correctamente",
                "original_image_url": uploaded_image.original_image.url,
                "processed_image_url": uploaded_image.processed_image.url,
            }, status=200)
        return JsonResponse({"error": "No se proporcionó una imagen válida"}, status=400)
    return JsonResponse({"error": "Método no permitido"}, status=405)

class CrearRecomendacionView(CreateView):
    model = Recomendacion
    template_name = 'recomendaciones/crear_recomendacion.html'
    fields = ['nombre_actividad', 'ciudad', 'duracion', 'rango_desde', 'rango_hasta', 'categoria', 'descripcion']
    success_url = reverse_lazy('admin_view') # me manda a la pag principal cuando guarda