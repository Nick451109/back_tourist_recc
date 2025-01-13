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

            # Convertir la imagen a RGB si tiene 4 canales
            if image.mode == "RGBA":
                image = image.convert("RGB")

            # Obtener dimensiones originales
            orig_w, orig_h = image.size

            # Convertir la imagen a un formato que el modelo pueda procesar
            image_np = np.array(image)
            image_resized = cv2.resize(image_np, (224, 224))  # Tamaño esperado por el modelo
            image_array = np.expand_dims(image_resized, axis=0) / 255.0

            # Cargar el modelo de detección de bounding boxes
            model = tf.keras.models.load_model(MODEL_PATH, compile=False)
            predictions = model.predict(image_array)[0].reshape(-1, 4)
            bounding_boxes = process_predictions(predictions, orig_w, orig_h)
            
            # Realizar la predicción
            predictions = model.predict(image_array)[0].reshape(-1, 4)

            # Procesar predicciones y escalar a dimensiones originales
            bounding_boxes = process_predictions(predictions, orig_w, orig_h)

            # Cargar el modelo de predicción de género
            gender_model_path = os.path.join(settings.BASE_DIR, 'models/GenderFinal.keras')
            gender_model = tf.keras.models.load_model(gender_model_path, compile=False)

            # Cargar el modelo de predicción de edad
            age_model_path = os.path.join(settings.BASE_DIR, 'models/AgeFinal.keras')
            age_model = tf.keras.models.load_model(age_model_path, compile=False)
            age_labels = ["Infante", "Ninez", "Adolescencia", "Adulto Joven", "Adulto", "Adulto Mayor"]

            # Realizar predicciones de género y edad para cada bounding box
            dataPeople = []
            for bbox in bounding_boxes:
                # Recortar la cara según el bounding box
                face = image_np[bbox["y_min"]:bbox["y_max"], bbox["x_min"]:bbox["x_max"]]
                face_resized = cv2.resize(face, (224, 224)) / 255.0
                face_array = np.expand_dims(face_resized, axis=0)

                # Predicción del modelo de género
                gender_prediction = gender_model.predict(face_array)[0][0]
                gender_label = "Femenino" if gender_prediction > 0.5 else "Masculino"

                # Predicción del modelo de edad
                age_prediction = age_model.predict(face_array)[0]
                age_label = age_labels[np.argmax(age_prediction[:6])]

                dataPeople.append({
                    "gender": gender_label,
                    "confidence": float(gender_prediction),
                    "age": age_label,
                    "bbox": bbox
                })

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

            # Responder con las rutas de las imágenes, bounding boxes, géneros y edades
            return JsonResponse({
                "message": "Imagen procesada exitosamente",
                "original_image_url": f"/media/images/original/original_image.png",
                "processed_image_url": f"/media/images/procesada/processed_image.png",
                "processed_image_base64": f"data:image/png;base64,{processed_image_base64}",
                "dataPeople": dataPeople
            }, status=200)

        except Exception as e:
            return JsonResponse({"error": f"Error al procesar la imagen: {str(e)}"}, status=500)

    return JsonResponse({"error": "Método no permitido"}, status=405)