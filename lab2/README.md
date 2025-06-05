# FastAPI Routes Demo

## Intro

This is a demo project using FastAPI and Uvicorn. It implements 10 different routes covering:

- Path & query parameters  
- Redirects  
- Utility routes (weather, prime check, etc.)
- Headers and Cookies

It also includes a testing file, which tests all of our different routes, and a Command Line Driver, to call routes from within the terminal.

## Run the Application
1. Install deps:
   ```
   pip3 install uvicorn fastapi
   ```

## Run the Tests

2. On another terminal tab/window:
   ```
   python3 tester.py
   ```

## Run the Command Line Driver

2. On another terminal tab/window: (use argument -h for details)
   ```
   python3 driver.py <route> <arguments>
   ```

