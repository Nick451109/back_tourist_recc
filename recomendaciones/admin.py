from django.contrib import admin
from .models import UploadedImage


# Register your models here.

@admin.register(UploadedImage)
class UploadedImageAdmin(admin.ModelAdmin):
    list_display = ('original_image', 'processed_image', 'uploaded_at')