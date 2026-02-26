import io
from unittest.mock import patch

from PIL import Image
from django.test import TestCase
from rest_framework.test import APIClient

from .image_utils import generate_meme_image, create_sticker
from .models import MemeTemplate


def _make_test_image(width=400, height=300):
    """Create a simple in-memory test image."""
    return Image.new('RGB', (width, height), color='blue')


class ImageUtilsTests(TestCase):
    def test_generate_meme_image_returns_image(self):
        img = _make_test_image()
        result = generate_meme_image(img, 'TOP', 'BOTTOM')
        self.assertIsInstance(result, Image.Image)
        self.assertEqual(result.size, (400, 300))

    def test_generate_meme_image_empty_text(self):
        img = _make_test_image()
        result = generate_meme_image(img, '', '')
        self.assertIsInstance(result, Image.Image)

    def test_create_sticker_returns_webp_bytes(self):
        img = _make_test_image()
        data = create_sticker(img, 'HELLO', '')
        self.assertIsInstance(data, bytes)
        # Verify it's valid WebP by re-opening
        sticker = Image.open(io.BytesIO(data))
        self.assertEqual(sticker.format, 'WEBP')
        self.assertLessEqual(sticker.width, 512)
        self.assertLessEqual(sticker.height, 512)


class MemeTemplateAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_list_templates_empty(self):
        resp = self.client.get('/api/templates/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), [])

    def test_list_memes_empty(self):
        resp = self.client.get('/api/memes/')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.json(), [])


class GenerateMemeAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_generate_requires_input(self):
        resp = self.client.post('/api/memes/generate/', {}, format='json')
        self.assertEqual(resp.status_code, 400)

    @patch('memes.views.urlopen')
    def test_generate_from_url(self, mock_urlopen):
        img = _make_test_image()
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        mock_urlopen.return_value = buf

        resp = self.client.post('/api/memes/generate/', {
            'image_url': 'https://example.com/test.png',
            'top_text': 'HELLO',
            'bottom_text': 'WORLD',
        }, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'image/png')


class StickerAPITests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_sticker_requires_input(self):
        resp = self.client.post('/api/memes/sticker/', {}, format='json')
        self.assertEqual(resp.status_code, 400)

    @patch('memes.views.urlopen')
    def test_sticker_from_url(self, mock_urlopen):
        img = _make_test_image()
        buf = io.BytesIO()
        img.save(buf, format='PNG')
        buf.seek(0)
        mock_urlopen.return_value = buf

        resp = self.client.post('/api/memes/sticker/', {
            'image_url': 'https://example.com/test.png',
            'top_text': 'STICKER',
        }, format='json')
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp['Content-Type'], 'image/webp')
        self.assertIn('sticker.webp', resp['Content-Disposition'])
