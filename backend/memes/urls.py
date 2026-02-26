from django.urls import path
from . import views

urlpatterns = [
    path('templates/', views.MemeTemplateListView.as_view(), name='template-list'),
    path('memes/', views.GeneratedMemeListView.as_view(), name='meme-list'),
    path('memes/generate/', views.GenerateMemeView.as_view(), name='meme-generate'),
    path('memes/sticker/', views.CreateStickerView.as_view(), name='meme-sticker'),
]
