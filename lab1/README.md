# FastAPI Routes Demo

## Intro

This is a demo project using FastAPI and Uvicorn. It implements 10 different routes covering:

- Path & query parameters  
- Redirects  
- Utility routes (weather, prime check, etc.)
- Even some Cookies

## How to Run

1. Install requirements:
   ```
   pip3 install fastapi uvicorn
   ```

2. Start the server:
   ```
   uvicorn main:app --reload
   ```

3. Visit:
   - Docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Redoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

## File

- `main.py` – All routes and logic.
