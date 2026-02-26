from django.contrib import admin
from .models import MemeTemplate, GeneratedMeme


@admin.register(MemeTemplate)
class MemeTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'created_at')


@admin.register(GeneratedMeme)
class GeneratedMemeAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'created_at')
