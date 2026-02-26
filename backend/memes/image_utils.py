"""Image processing utilities for meme generation and sticker creation."""

import io
import textwrap

from PIL import Image, ImageDraw, ImageFont


def _get_font(size: int) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    """Return a TrueType font, falling back to the default bitmap font."""
    for path in (
        '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf',
        '/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf',
        '/usr/share/fonts/TTF/DejaVuSans-Bold.ttf',
    ):
        try:
            return ImageFont.truetype(path, size)
        except OSError:
            continue
    return ImageFont.load_default()


def _draw_text(
    draw: ImageDraw.ImageDraw,
    text: str,
    position: str,
    img_width: int,
    img_height: int,
) -> None:
    """Draw outlined meme text at the top or bottom of the image."""
    if not text:
        return

    font_size = max(20, img_width // 12)
    font = _get_font(font_size)
    max_chars = max(10, img_width // (font_size // 2))
    lines = textwrap.wrap(text.upper(), width=max_chars)

    line_height = font_size + 6
    block_height = line_height * len(lines)

    if position == 'top':
        y_start = 10
    else:
        y_start = img_height - block_height - 16

    for i, line in enumerate(lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_width = bbox[2] - bbox[0]
        x = (img_width - text_width) // 2
        y = y_start + i * line_height

        # Draw outline
        outline_range = max(2, font_size // 20)
        for dx in range(-outline_range, outline_range + 1):
            for dy in range(-outline_range, outline_range + 1):
                if dx != 0 or dy != 0:
                    draw.text((x + dx, y + dy), line, font=font, fill='black')
        # Draw text
        draw.text((x, y), line, font=font, fill='white')


def generate_meme_image(
    base_image: Image.Image,
    top_text: str = '',
    bottom_text: str = '',
) -> Image.Image:
    """Overlay top/bottom text on a base image and return the result."""
    img = base_image.convert('RGBA')
    draw = ImageDraw.Draw(img)

    _draw_text(draw, top_text, 'top', img.width, img.height)
    _draw_text(draw, bottom_text, 'bottom', img.width, img.height)

    return img.convert('RGB')


def create_sticker(
    base_image: Image.Image,
    top_text: str = '',
    bottom_text: str = '',
) -> bytes:
    """Create a WhatsApp-compatible sticker (512×512 WebP)."""
    img = generate_meme_image(base_image, top_text, bottom_text)

    # Resize to fit in 512×512 while maintaining aspect ratio
    img.thumbnail((512, 512), Image.LANCZOS)

    # Paste onto a transparent 512×512 canvas
    canvas = Image.new('RGBA', (512, 512), (0, 0, 0, 0))
    offset = ((512 - img.width) // 2, (512 - img.height) // 2)
    canvas.paste(img, offset)

    buf = io.BytesIO()
    canvas.save(buf, format='WEBP', quality=80)
    return buf.getvalue()
