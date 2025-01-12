from django.urls import path
from .views import admin_view, CrearRecomendacionView, eliminar_recomendacion, upload_image
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('recommendations/', admin_view, name='admin_view'),
    path('recommendations/create/', CrearRecomendacionView.as_view(), name='crear_recomendacion'),
    path('recommendations/delete/<int:pk>/', eliminar_recomendacion, name='eliminar_recomendacion'),
    path('recommendations/upload-image/', upload_image, name='upload_image'),


] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)