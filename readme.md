# Flask Inventory Management System (API)

Lightweight Flask-based inventory management API with GraphQL (Ariadne), WebSocket chat (Flask-SocketIO), SSE demo, rate limiting and JWT auth.

## Features
- GraphQL endpoint (/graphql)
- WebSocket chat UI (/chatt)
- Server-Sent Events demo (/events, /response)
- JWT & HTTP Basic auth
- Rate limiting (Flask-Limiter)
- Caching support
- Socket.IO for real-time features

## Requirements
- Docker (recommended)
- Or Python 3.10+ and pip

## Environment
Create a `.env` file in project root with at minimum:
- SECRET_KEY=your_secret_key
- (any DB or other env variables used by your app modules)

## Quickstart (Docker)
1. Build and run:
   docker-compose up --build -d
2. Open:
   - App: http://localhost:5000/
   - GraphQL (POST): http://localhost:5000/graphql
   - Chat UI: http://localhost:5000/chatt
   - SSE demo: http://localhost:5000/response

## Quickstart (local)
1. Create virtualenv and install:
   python -m venv venv
   venv\Scripts\activate
   pip install -r requirements.txt
2. Set env vars (or create `.env`) and run:
   python -m gunicorn -k eventlet -w 1 Ecommerce.app:app -b 0.0.0.0:5000

## Development notes
- GraphQL types are in `graphql/types`
- App factory at `Ecommerce.apps.create_app`
- SocketIO instance is in `Ecommerce.chat`
- Adjust SESSION_COOKIE_SECURE for production (set True for HTTPS)

## Docker tips
- Use production-ready secrets and a proper WSGI server config (gunicorn + eventlet shown).
- Add database services to docker-compose if required by your project.

## Troubleshooting
- If using Socket.IO in production ensure eventlet is installed and gunicorn uses `-k eventlet`.
- Check logs: docker-compose logs -f web

License: Project-specific or add your license file.
