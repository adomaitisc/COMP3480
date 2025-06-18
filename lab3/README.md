# Express.js Routes Demo

## Introduction

This is a demo project using Express.js that implements various types of routes and pages. The application includes:

- 5 Static HTML Pages
- 5 Routes with Query Parameters
- 1 Route with Header Parameter
- 1 Route with Body Input (Form Processing)

## Project Structure

- `index.js` - Main application file with all routes and server logic
- `pages/` - Directory containing HTML files
  - `index.html` - Home page
  - `about.html` - About page
  - `things.html` - Things page
  - `contact.html` - Contact page
  - `portal.html` - Portal page with form

## Setup and Running

1. Install dependencies:

   ```
   npm install
   ```

2. Start the server:

   ```
   node index.js
   ```

3. Access the application at [http://localhost:8080](http://localhost:8080)

## Available Routes

### HTML Pages

- `/` - Home page
- `/about` - About page
- `/things` - Things page
- `/contact` - Contact page
- `/portal` - Portal page

### Query Parameter Routes

- `/greet?name=value` - Displays a greeting with the provided name
- `/post?page=number` - Shows a page number with navigation
- `/search?q=query` - Displays search results
- `/user?id=userId` - Shows user profile
- `/gps?lat=value&lon=value` - Displays GPS coordinates

### Special Routes

- `POST /header-check` - Checks for 'x-header' header parameter
- `POST /portal` - Processes form data and redirects to greeting

## Testing the API

You can test the API endpoints using tools like cURL or HTTPie/Postman/Insomnia:

### Example Header Check:

```bash
curl -X POST http://localhost:8080/header-check \
  -H "x-header: my-header"
```

### Example Form Submission:

```bash
curl -X POST http://localhost:8080/portal \
  -H "Content-Type: application/json" \
  -d '{"name": "James Webb ST"}'
```
