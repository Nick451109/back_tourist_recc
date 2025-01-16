from datetime import timedelta
from recomendaciones.models import Recomendacion

def create_initial_data(sender, **kwargs):
    """
    Crea datos iniciales en la tabla recomendaciones_recomendacion después de aplicar las migraciones.
    """
    if not Recomendacion.objects.exists():
        Recomendacion.objects.create(
            nombre_actividad="Jardín Botánico de Quito",
            ciudad="Quito",
            rango_desde=1,
            rango_hasta=5,
            categoria="Infante",
            duracion=timedelta(hours=1, minutes=30),
            descripcion="Un espacio verde donde los más pequeños pueden explorar la naturaleza.",
        )
        Recomendacion.objects.create(
            nombre_actividad="Museo Interactivo de Ciencia",
            ciudad="Quito",
            rango_desde=2,
            rango_hasta=5,
            categoria="Infante",
            duracion=timedelta(hours=2),
            descripcion="Actividades prácticas y educativas para niños.",
        )

        Recomendacion.objects.create(
            nombre_actividad="Parque La Carolina",
            ciudad="Quito",
            rango_desde=3,
            rango_hasta=5,
            categoria="Ninez",
            duracion=timedelta(hours=2, minutes=30),
            descripcion="Parque con áreas de juego y actividades al aire libre.",
        )
        Recomendacion.objects.create(
            nombre_actividad="Acuario de Manta",
            ciudad="Manta",
            rango_desde=2,
            rango_hasta=5,
            categoria="Ninez",
            duracion=timedelta(hours=2),
            descripcion="Explora la vida marina con exhibiciones interactivas.",
        )

        Recomendacion.objects.create(
            nombre_actividad="Ruta de las Cascadas",
            ciudad="Baños de Agua Santa",
            rango_desde=4,
            rango_hasta=5,
            categoria="Adolescencia",
            duracion=timedelta(hours=3),
            descripcion="Un recorrido emocionante en bicicleta por varias cascadas.",
        )
        Recomendacion.objects.create(
            nombre_actividad="Parque de Aventuras Aventura Amazonica",
            ciudad="Tena",
            rango_desde=3,
            rango_hasta=5,
            categoria="Adolescencia",
            duracion=timedelta(hours=3, minutes=30),
            descripcion="Deportes extremos y tirolesa en un ambiente selvático.",
        )

        Recomendacion.objects.create(
            nombre_actividad="Ruta del Spondylus",
            ciudad="Montañita",
            rango_desde=4,
            rango_hasta=5,
            categoria="Adulto Joven",
            duracion=timedelta(hours=4),
            descripcion="Surf, comida local y una experiencia bohemia en la costa.",
        )
        Recomendacion.objects.create(
            nombre_actividad="Senderismo en el Quilotoa",
            ciudad="Quilotoa",
            rango_desde=2,
            rango_hasta=5,
            categoria="Adulto Joven",
            duracion=timedelta(hours=5),
            descripcion="Explora la majestuosa laguna del Quilotoa y sus alrededores.",
        )

        Recomendacion.objects.create(
            nombre_actividad="Caminata en el Parque Nacional Cotopaxi",
            ciudad="Latacunga",
            rango_desde=3,
            rango_hasta=5,
            categoria="Adulto",
            duracion=timedelta(hours=3, minutes=30),
            descripcion="Disfruta de vistas espectaculares del volcán Cotopaxi.",
        )
        Recomendacion.objects.create(
            nombre_actividad="Museo del Banco Central",
            ciudad="Cuenca",
            rango_desde=2,
            rango_hasta=5,
            categoria="Adulto",
            duracion=timedelta(hours=2),
            descripcion="Conoce la historia y la cultura ecuatoriana en este emblemático museo.",
        )

        Recomendacion.objects.create(
            nombre_actividad="Tour en el Tren Ecuador",
            ciudad="Riobamba",
            rango_desde=1,
            rango_hasta=5,
            categoria="Adulto Mayor",
            duracion=timedelta(hours=4, minutes=30),
            descripcion="Un recorrido relajante con vistas espectaculares de los Andes.",
        )
        Recomendacion.objects.create(
            nombre_actividad="Jardín Botánico de Guayaquil",
            ciudad="Guayaquil",
            rango_desde=2,
            rango_hasta=5,
            categoria="Adulto Mayor",
            duracion=timedelta(hours=2),
            descripcion="Explora especies exóticas de plantas y un ambiente tranquilo.",
        )

        print("Datos iniciales creados en la tabla recomendaciones_recomendacion.")
