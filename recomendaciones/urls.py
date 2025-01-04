from django.urls import path
from .views import admin_view, CrearRecomendacionView, eliminar_recomendacion

urlpatterns = [
    path('recommendations/', admin_view, name='admin_view'),
    path('recommendations/create/', CrearRecomendacionView.as_view(), name='crear_recomendacion'),
    path('recommendations/delete/<int:pk>/', eliminar_recomendacion, name='eliminar_recomendacion'),

]