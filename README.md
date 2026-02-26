# Dream Big · Meme Lab

A modern meme engine with a **Django + Pillow** backend and a **Vite + React** frontend.  
Browse curated classics, create memes with text overlays, and export WhatsApp stickers — all from one dashboard.

## Features
- 🔍 Search by title or tag
- 🎚️ Vibe filters (wholesome, chaotic, savage, classics)
- 🔀 Surprise spotlight button
- 📎 Quick copy of the image link + source attribution
- ✨ Glassy dark UI with responsive grid
- 🎨 **Meme Studio** — pick a template, add top/bottom text, generate memes via the backend
- 📱 **WhatsApp Sticker** — one-click 512×512 WebP export ready for WhatsApp
- 🖼️ **Pillow image processing** — server-side text overlay with outlined white-on-black meme text

## Architecture

```
frontend (Vite + React)          backend (Django + DRF + Pillow)
──────────────────────────        ──────────────────────────────
 Gallery view                     GET  /api/templates/
 Meme Studio view  ──────────►    POST /api/memes/generate/
 Sticker download  ──────────►    POST /api/memes/sticker/
```

## Getting Started

### 1. Backend (Django)

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The API will be available at `http://localhost:8000/api/`.

### 2. Frontend (Vite + React)

```bash
npm install
npm run dev
```

The app starts on `http://localhost:5173` and proxies API requests to the Django backend.

### Production build

```bash
npm run build
npm run preview
```

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/templates/` | List uploaded meme templates |
| POST | `/api/templates/` | Upload a new template image |
| GET | `/api/memes/` | List previously generated memes |
| POST | `/api/memes/generate/` | Generate a meme (returns PNG) |
| POST | `/api/memes/sticker/` | Create a WhatsApp sticker (returns 512×512 WebP) |

### Generate Meme / Sticker Request Body

```json
{
  "image_url": "https://i.imgflip.com/1ur9b0.jpg",
  "top_text": "WHEN YOU PUSH TO MAIN",
  "bottom_text": "WITHOUT TESTING"
}
```

Or use a template uploaded via the admin:

```json
{
  "template_id": 1,
  "top_text": "HELLO",
  "bottom_text": "WORLD"
}
```

## Running Tests

```bash
cd backend
python manage.py test memes
```

## Notes
- All meme references use public template links for quick remixing.
- Upload your own templates via the Django admin at `/admin/`.
- Feel free to extend `src/data/memes.js` with your own favorites.
