from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic.edit import CreateView
from django.urls import reverse_lazy, reverse
from .models import Recomendacion
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import base64
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from .models import UploadedImage
from django.conf import settings
import os
import json
import numpy as np
import tensorflow as tf
import cv2

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
MODEL_PATH = os.path.join(settings.BASE_DIR, 'models/modelo_ultimaVersion.h5')
TEST_IMAGE_PATH = os.path.join(settings.BASE_DIR, 'models/imagen.png')

def obtener_recomendaciones_por_categoria(request, categoria):
    """
    Obtiene todas las recomendaciones que coincidan con una categoría específica.

    Args:
        request: El objeto HttpRequest.
        categoria (str): La categoría a buscar.

    Returns:
        JsonResponse: Una respuesta JSON con las recomendaciones encontradas o un mensaje de error si no se encuentran.
    """
    try:
        # Filtrar recomendaciones por categoría
        recomendaciones = Recomendacion.objects.filter(categoria__iexact=categoria)

        if recomendaciones.exists():
            # Serializar las recomendaciones en una lista de diccionarios
            data = [
                {
                    "id": recomendacion.id,
                    "nombre_actividad": recomendacion.nombre_actividad,
                    "ciudad": recomendacion.ciudad,
                    "duracion": recomendacion.duracion,
                    "rango_desde": recomendacion.rango_desde,
                    "rango_hasta": recomendacion.rango_hasta,
                    "categoria": recomendacion.categoria,
                    "descripcion": recomendacion.descripcion,
                }
                for recomendacion in recomendaciones
            ]

            return JsonResponse({"success": True, "recomendaciones": data}, status=200)
        else:
            return JsonResponse({"success": False, "message": "No se encontraron recomendaciones para la categoría especificada."}, status=404)

    except Exception as e:
        return JsonResponse({"success": False, "error": str(e)}, status=500)


@csrf_exempt
def upload_image(request):
    if request.method == "POST":
        try:
            body = json.loads(request.body)
            image_data = body.get("image")

            if not image_data:
                return JsonResponse({"error": "No se proporcionó una imagen válida"}, status=400)

            if image_data.startswith("data:image/"):
                image_data = image_data.split(",")[1]

            image_bytes = base64.b64decode(image_data)
            image = Image.open(BytesIO(image_bytes))

            if image.mode == "RGBA":
                image = image.convert("RGB")

            orig_w, orig_h = image.size

            image_np = np.array(image)
            image_resized = cv2.resize(image_np, (224, 224))
            image_array = np.expand_dims(image_resized, axis=0) / 255.0

            model = tf.keras.models.load_model(MODEL_PATH, compile=False)
            predictions = model.predict(image_array)[0].reshape(-1, 4)
            bounding_boxes = process_predictions(predictions, orig_w, orig_h)

            gender_model_path = os.path.join(settings.BASE_DIR, 'models/GenderFinal.keras')
            gender_model = tf.keras.models.load_model(gender_model_path, compile=False)

            age_model_path = os.path.join(settings.BASE_DIR, 'models/AgeFinal.keras')
            age_model = tf.keras.models.load_model(age_model_path, compile=False)
            age_labels = ["Infante", "Ninez", "Adolescencia", "Adulto Joven", "Adulto", "Adulto Mayor"]

            dataPeople = []
            age_counts = {label: 0 for label in age_labels}  # Inicializar contador de edades

            for bbox in bounding_boxes:
                face = image_np[bbox["y_min"]:bbox["y_max"], bbox["x_min"]:bbox["x_max"]]
                face_resized = cv2.resize(face, (224, 224)) / 255.0
                face_array = np.expand_dims(face_resized, axis=0)

                gender_prediction = gender_model.predict(face_array)[0][0]
                gender_label = "Femenino" if gender_prediction > 0.5 else "Masculino"

                age_prediction = age_model.predict(face_array)[0]
                age_label = age_labels[np.argmax(age_prediction[:6])]

                dataPeople.append({
                    "gender": gender_label,
                    "confidence": float(gender_prediction),
                    "age": age_label,
                    "bbox": bbox
                })

                age_counts[age_label] += 1

            # Guardar la imagen original
            original_path = os.path.join(MEDIA_DIR, "original", "original_image.png")
            os.makedirs(os.path.dirname(original_path), exist_ok=True)
            image.save(original_path)

            # Dibujar bounding boxes y etiquetas en la imagen
            processed_image = image.copy()
            draw = ImageDraw.Draw(processed_image)
            font_size = 30  # Tamaño de la fuente más grande
            font_path = os.path.join(settings.BASE_DIR, "fonts/arial.ttf")
            try:
                font = ImageFont.truetype(font_path, font_size)  # Cargar la fuente desde el archivo local
            except IOError:
                font = ImageFont.load_default()  # Usar fuente predeterminada si ocurre un error

            for person in dataPeople:
                bbox = person["bbox"]
                gender_label = person["gender"]
                age_label = person["age"]
                draw.rectangle(
                    [bbox["x_min"], bbox["y_min"], bbox["x_max"], bbox["y_max"]],
                    outline="green",
                    width=4  # Hacer los bordes más gruesos
                )
                # Definir el tamaño del texto y el fondo
                text = f"{gender_label}, {age_label}"
                text_bbox = draw.textbbox((0, 0), text, font=font)
                text_width = text_bbox[2] - text_bbox[0]
                text_height = text_bbox[3] - text_bbox[1]

                # Coordenadas del rectángulo de fondo
                background_coords = [
                    (bbox["x_min"], bbox["y_min"] - text_height),
                    (bbox["x_min"] + text_width, bbox["y_min"])
                ]


                # Dibujar el rectángulo de fondo negro
                draw.rectangle(background_coords, fill="black")

                # Dibujar el texto blanco sobre el fondo negro
                draw.text((bbox["x_min"], bbox["y_min"] - text_height), text, fill="white", font=font)

            # Guardar la imagen procesada
            processed_path = os.path.join(MEDIA_DIR, "procesada", "processed_image.png")
            os.makedirs(os.path.dirname(processed_path), exist_ok=True)
            processed_image.save(processed_path)

            # Convertir la imagen procesada a base64 para enviar al frontend
            buffered = BytesIO()
            processed_image.save(buffered, format="PNG")
            processed_image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")

            # Identificar categorías en orden de prioridad
            sorted_ages = sorted(age_counts.items(), key=lambda x: x[1], reverse=True)
            predominant_age = sorted_ages[0][0]

            # Obtener recomendaciones priorizadas
            recomendaciones = []
            for age, count in sorted_ages:
                if count > 0:
                    response = obtener_recomendaciones_por_categoria(request, age)
                    data = json.loads(response.content).get("recomendaciones", [])
                    recomendaciones.extend(data)

            return JsonResponse({
                "message": "Imagen procesada exitosamente",
                "predominant_age": predominant_age,
                "dataPeople": dataPeople,
                "recomendaciones": recomendaciones,  # Recomendaciones ordenadas por prioridad
                "age_counts": age_counts,
                "original_image_url": f"/media/images/original/original_image.png",
                "processed_image_url": f"/media/images/procesada/processed_image.png",
                "processed_image_base64": f"data:image/png;base64,{processed_image_base64}",
            }, status=200)

        except Exception as e:
            return JsonResponse({"error": f"Error al procesar la imagen: {str(e)}"}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)


def process_predictions(predictions, orig_w, orig_h):
    bounding_boxes = []
    min_area_threshold = 1500  # Umbral de área mínima

    for bbox in predictions:
        x_min, y_min, x_max, y_max = bbox
        x_min = int(x_min * orig_w / 224)
        y_min = int(y_min * orig_h / 224)
        x_max = int(x_max * orig_w / 224)
        y_max = int(y_max * orig_h / 224)

        # Calcular el área y filtrar bounding boxes pequeños
        area = (x_max - x_min) * (y_max - y_min)
        if x_max > x_min and y_max > y_min and area > min_area_threshold:
            bounding_boxes.append({
                "x_min": x_min,
                "y_min": y_min,
                "x_max": x_max,
                "y_max": y_max
            })

    return bounding_boxes

# def process_predictions(predictions):
#     bounding_boxes = []

#     # Asegúrate de que las predicciones tienen el formato esperado
#     for bbox in predictions:
#         if len(bbox) == 4:  # Si las predicciones tienen las 4 coordenadas esperadas
#             x_min, y_min, x_max, y_max = bbox

#             # Validar que los valores sean coherentes
#             if x_max > x_min and y_max > y_min:
#                 bounding_boxes.append({
#                     "x_min": int(x_min),
#                     "y_min": int(y_min),
#                     "x_max": int(x_max),
#                     "y_max": int(y_max)
#                 })
#         else:
#             print(f"Formato inesperado de predicción: {bbox}")

#     return bounding_boxes


class CrearRecomendacionView(CreateView):
    model = Recomendacion
    template_name = 'recomendaciones/crear_recomendacion.html'
    fields = ['nombre_actividad', 'ciudad', 'duracion', 'rango_desde', 'rango_hasta', 'categoria', 'descripcion']
    success_url = reverse_lazy('admin_view') # me manda a la pag principal cuando guarda