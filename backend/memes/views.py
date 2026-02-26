import io
from urllib.request import urlopen
from urllib.error import URLError

from PIL import Image
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse

from .models import MemeTemplate, GeneratedMeme
from .serializers import (
    MemeTemplateSerializer,
    GeneratedMemeSerializer,
    GenerateMemeRequestSerializer,
    StickerRequestSerializer,
)
from .image_utils import generate_meme_image, create_sticker


class MemeTemplateListView(generics.ListCreateAPIView):
    """GET  /api/templates/  – list templates
       POST /api/templates/  – upload a new template"""
    queryset = MemeTemplate.objects.all()
    serializer_class = MemeTemplateSerializer


class GeneratedMemeListView(generics.ListAPIView):
    """GET /api/memes/ – list previously generated memes."""
    queryset = GeneratedMeme.objects.all()
    serializer_class = GeneratedMemeSerializer


def _load_image(template_id=None, image_url=None):
    """Load an image from a template or a URL."""
    if template_id:
        try:
            template = MemeTemplate.objects.get(pk=template_id)
        except MemeTemplate.DoesNotExist:
            return None, Response(
                {'error': 'Template not found.'},
                status=status.HTTP_404_NOT_FOUND,
            )
        img = Image.open(template.image.path)
        return img, None

    if image_url:
        try:
            resp = urlopen(image_url, timeout=10)  # noqa: S310
            img = Image.open(io.BytesIO(resp.read()))
            return img, None
        except (URLError, OSError):
            return None, Response(
                {'error': 'Could not fetch image from URL.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

    return None, Response(
        {'error': 'Provide template_id or image_url.'},
        status=status.HTTP_400_BAD_REQUEST,
    )


class GenerateMemeView(APIView):
    """POST /api/memes/generate/ – create a meme with text overlay."""

    def post(self, request):
        serializer = GenerateMemeRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        img, err = _load_image(data.get('template_id'), data.get('image_url'))
        if err:
            return err

        result = generate_meme_image(img, data['top_text'], data['bottom_text'])
        buf = io.BytesIO()
        result.save(buf, format='PNG')
        buf.seek(0)

        return HttpResponse(buf, content_type='image/png')


class CreateStickerView(APIView):
    """POST /api/memes/sticker/ – convert to WhatsApp sticker (512×512 WebP)."""

    def post(self, request):
        serializer = StickerRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        img, err = _load_image(data.get('template_id'), data.get('image_url'))
        if err:
            return err

        sticker_bytes = create_sticker(img, data['top_text'], data['bottom_text'])

        response = HttpResponse(sticker_bytes, content_type='image/webp')
        response['Content-Disposition'] = 'attachment; filename="sticker.webp"'
        return response
