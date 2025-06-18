# FastAPI Routes Containerization Demo

## Intro

This is a demo project using FastAPI and Uvicorn. It implements 10 different routes covering:

- Path & query parameters
- Redirects
- Utility routes (weather, prime check, etc.)
- Even some Cookies

## How to Run

1. Build the Docker Image:

   ```
   docker build -t <tag-name> .
   ```

2. Deploy the Docker Container

   ```
   docker run -p 8000:8000 <tag-name>
   ```

3. Visit:
   - Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## File

- `main.py` – All routes and logic.
- `Dockerfile` – Container and Image configuration
- `requirements.txt` – Python dependencies
