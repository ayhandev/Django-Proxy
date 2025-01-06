
# Django Proxy Server

This project is a proxy server that allows requests to be redirected to a specified hidden URL. It supports redirecting CSS, JS, images and other resources, and exploiting errors with clear messages in both English and English.

## Functionality
- Redirect requests to the specified target server.
- Substitution of links to resources (CSS, JS, images) for the correct display of sites.
- Error handling with displaying a beautiful HTML page.
- Support for redirects on the target server in Russian and English.

## Installation and launch

### Step 1: Clone the project
```bash
https://github.com/ayhandev/Django-Proxy.git
```

### Step 2: Install dependencies
Make sure you have Python installed (version 3.9+ recommended). Then create a virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate # For Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Step 3: Start the development server
Run the following commands:
```bash
python manage.py migrate
python manage.py runserver
```

The server will be available at: `http://127.0.0.1:8000`.

### Step 5: Use
To use a proxy, send a GET request to the following URL:
```
http://127.0.0.1:8000/proxy/<target URL>
```

Example:
```
http://127.0.0.1:8000/proxy/www.example.com
```

---

## How it works
1. **Main route:** `/proxy/<target_url>`:
   - Accepts the URL to which the request will be sent.
   - Replaces paths to resources (CSS, JS, images) so that the site looks correct.

2. **Error handling**:
   - If an error occurs, an HTML page is displayed with a message in English.

---

## Project files
- `home/views.py` — Basic logic of the proxy server.
- `home/urls.py` — Route configuration.

---

## Usage example
After starting the project, open in your browser:
```
http://127.0.0.1:8000/proxy/www.google.com
```

---

## Notes
- Make sure the target server supports access from your region.
- If errors such as `Connection refused` occur, check the availability of the target server.
- But you can also use it in servers located in other regions. :)


