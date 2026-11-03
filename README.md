# Next_Gen in Christ

The site is built with Django. The home page keeps its sections, styles, scripts,
and images in separate files so each part can be updated independently.

## Run locally

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:DJANGO_DEBUG = "true"
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. Django uses a development-only secret key when
`DJANGO_DEBUG=true`; do not enable debug mode in production.

Run the project checks and tests with:

```powershell
python manage.py check
python manage.py test
```

## Deploy to Vercel

Import the repository into Vercel. Vercel detects the root `manage.py`, installs
`requirements.txt`, and uses the Django WSGI application. It also collects and
serves the files under `website/static/` using `STATIC_ROOT`.

Before deploying, add these environment variables in the Vercel project settings:

- `DJANGO_SECRET_KEY`: a unique, private key for this deployment.
- `DJANGO_DEBUG`: `false`.
- `DJANGO_ALLOWED_HOSTS`: optional comma-separated hostnames if using a custom
  domain. Vercel preview and production domains ending in `.vercel.app` are
  allowed by default.

Generate a key locally with `python -c "import secrets; print(secrets.token_urlsafe(50))"`
and paste its output into the Vercel environment variable. Do not commit the key.

## Project layout

```text
config/                         Django settings, URLs, and WSGI entrypoint
website/
  static/website/css/           Page styles
  static/website/js/            Navigation and event-date behavior
  static/website/images/        Page images
  templates/website/
    base.html                   Shared HTML document
    home.html                   Home page composition
    sections/                   Individual page sections
  tests.py                      Homepage and static asset tests
manage.py                       Django management commands
requirements.txt                Python dependencies
```
