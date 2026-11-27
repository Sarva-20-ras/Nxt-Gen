# Next_Gen in Christ

The site is built with Django. The home page keeps its sections, styles, scripts,
and images in separate files so each part can be updated independently.

## Run locally

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
$env:DJANGO_DEBUG = "true"
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Open `http://127.0.0.1:8000/`. Django uses a development-only secret key when
`DJANGO_DEBUG=true`; do not enable debug mode in production.

Local development uses SQLite and saves uploaded images under `media/`. Run the
project checks and tests with:

```powershell
$env:DJANGO_DEBUG = "true"
python manage.py check
python manage.py test
```

## Pages and content management

The site has dedicated `/story/`, `/team/`, and `/gallery/` pages while keeping
previews on the homepage. `/sitemap.xml` lists the public pages and `/robots.txt`
points crawlers to the sitemap.

Authorized staff manage team cards and gallery photos at `/admin/`. There is no
public signup. Create staff users deliberately and grant only the needed model
permissions:

- Team editors need `view`, `add`, and `change` permissions for Team members.
- Gallery editors need `view`, `add`, and `change` permissions for Gallery
  photos. They can submit photos but cannot publish them.
- Gallery approvers also need the custom `Can approve gallery photos`
  permission. They can approve selected submissions from the Gallery Photos
  admin list.

Gallery uploads start unpublished. Image uploads must be JPG, PNG, or WebP and
no larger than 4 MB. The limit keeps admin photo submissions within Vercel's
request-size limit; compress larger phone photos before uploading. Only upload
photos that the people pictured have permission to publish.
Only upload photos that the people pictured have permission to publish.

## Deploy to Vercel

Import the repository into Vercel. Vercel detects the root `manage.py`, installs
`requirements.txt`, and uses the Django WSGI application. It also collects and
serves the files under `website/static/` using `STATIC_ROOT`.

Add these environment variables in the Vercel project settings:

- `DJANGO_SECRET_KEY`: a unique, private key for this deployment.
- `DJANGO_DEBUG`: `false`.
- `DATABASE_URL`: the Neon PostgreSQL connection string. Production refuses to
  start without a persistent database.
- `CLOUDINARY_URL`: the Cloudinary connection URL. Production refuses to start
  without durable image storage.
- `SITE_URL`: the public canonical origin, currently
  `https://nextgeninchrist.vercel.app`. Set this to the primary custom domain if
  one is connected; canonical links and the sitemap use this value.
- `DJANGO_ALLOWED_HOSTS`: optional comma-separated hostnames if using a custom
  domain. Vercel preview and production domains ending in `.vercel.app` are
  allowed by default.

Generate a key locally with `python -c "import secrets; print(secrets.token_urlsafe(50))"`
and add its output as the Vercel environment variable. Do not commit secrets or
paste credentials into chat.

After adding the Neon and Cloudinary settings, run `python manage.py migrate`
and `python manage.py createsuperuser` from a trusted local shell configured with
the production `DATABASE_URL` and `DJANGO_SECRET_KEY`. This creates the tables
and the first private admin account. Do not run these commands against the
development SQLite database if you intend to manage production content.

After deployment, verify the site in Google Search Console and Bing Webmaster
Tools, submit `https://<your-primary-domain>/sitemap.xml`, and use their URL
inspection tools to request crawling. Search engines choose when to index and
how to rank pages; metadata and a sitemap help discovery but cannot guarantee a
specific position.

## Project layout

```text
config/                         Django settings, URLs, and WSGI entrypoint
website/
  admin.py                      Restricted team and gallery management
  models.py                     Team members and moderated gallery photos
  migrations/                   Schema and existing-content seed data
  static/website/css/
    base.css, hero.css, navbar.css, about.css, story.css, what-we-do.css
    events.css, outreach.css, gallery.css, join.css, footer.css
    animations.css, leaders.css, team.css
    responsive-tablet.css, responsive-mobile.css, pages.css
  static/website/js/            Navigation and event-date behavior
  static/website/images/        Page images
  templates/website/
    base.html                   Shared HTML document
    home.html                   Homepage composition and previews
    story_page.html             Dedicated story page
    team_page.html              Dynamic team page
    gallery_page.html           Moderated photo gallery
    sections/                   Individual page sections
  tests.py                      Homepage and static asset tests
manage.py                       Django management commands
requirements.txt                Python dependencies
```
