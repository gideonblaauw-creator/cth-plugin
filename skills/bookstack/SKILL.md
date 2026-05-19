---
name: bookstack
description: |
  Deploy, configure, and manage BookStack wiki instances via Docker and REST API. Use this skill whenever the user mentions BookStack, wiki deployment, wiki migration, BookStack API, BookStack shelves/books/chapters/pages, or wants to set up a knowledge base or documentation wiki. Also trigger when working with existing BookStack instances — creating content via API, managing users/roles/permissions, branding, or troubleshooting Docker-based BookStack deployments. If the user mentions "wiki.cleantechhub.net" or any BookStack URL, use this skill.
---

# BookStack Wiki — Deployment, API & Migration

This skill captures hard-won operational knowledge from deploying and managing BookStack (bookstackapp.com) via Docker with the linuxserver/bookstack image. It covers the full lifecycle: deployment, API authentication, content creation, permissions, branding, and migration from other platforms.

## Architecture Overview

A typical BookStack deployment looks like this:

```
Internet → Reverse Proxy (Caddy/Nginx, ports 443/80, auto-SSL)
         → BookStack container (internal port, e.g. 8081)
         → MariaDB container (internal only)
```

Key components:
- **Docker image**: `lscr.io/linuxserver/bookstack:latest` (LinuxServer.io)
- **Database**: MariaDB 10.11+ (separate container, named `bookstack-db`)
- **Reverse proxy**: Caddy is recommended for automatic SSL; Nginx works too
- **Data persistence**: Mount volumes for `/opt/bookstack/data/bookstack` and `/opt/bookstack/data/mysql`

## Critical Gotchas (Read These First)

These are the issues that will waste hours if you don't know about them:

### 1. The API has NO version prefix

BookStack's REST API lives at `/api/shelves`, `/api/books`, `/api/pages`, etc. There is **no** `/v1/` prefix. Many scripts and tutorials incorrectly use `/api/v1/shelves` — this returns **405 Method Not Allowed**, which is confusing because it looks like an API issue rather than a URL issue.

```
WRONG: https://wiki.example.com/api/v1/shelves  → 405
RIGHT: https://wiki.example.com/api/shelves     → 200
```

### 2. The linuxserver image does NOT auto-map Docker env vars to Laravel .env

Unlike many Docker images, setting environment variables in `docker-compose.yml` does NOT automatically configure BookStack's Laravel `.env` file. The `.env` at `/opt/bookstack/data/bookstack/www/.env` must be written or updated manually (or via script). If you recreate the container, you need to regenerate `.env` — but **preserve the APP_KEY** or you'll lose encrypted data.

Also note the naming mismatch: Docker uses `DB_USER`/`DB_PASS`, but Laravel expects `DB_USERNAME`/`DB_PASSWORD`.

### 3. API token creation via artisan tinker is unreliable

The `php artisan tinker` approach inside the container often creates tokens with empty `token_id` or `user_id=0`, which silently fail on auth. The reliable approach is to use a PHP script with PDO inside the container (see the API Authentication section below).

### 4. Content permissions default to admin-only

When you create shelves/books/pages via the API (authenticated as admin), other users — even logged-in ones — cannot see them by default. You must either assign users the Admin role, or configure role-based permissions on each shelf. This catches everyone off guard after a migration: "I created 50 pages but users see nothing."

### 5. Books must be explicitly assigned to shelves

Creating a book does NOT automatically place it on a shelf, even if you set shelf metadata during creation. You must make a separate `PUT /api/shelves/{id}` call with a `{"books": [book_id]}` payload to assign books to shelves.

## Deployment

### Docker Compose Template

```yaml
version: "3.8"
services:
  bookstack:
    image: lscr.io/linuxserver/bookstack:latest
    container_name: bookstack
    restart: unless-stopped
    environment:
      - PUID=1000
      - PGID=1000
      - TZ=America/Bogota
      - APP_URL=https://wiki.example.com
      - DB_HOST=bookstack-db
      - DB_PORT=3306
      - DB_USER=bookstack
      - DB_PASS=${DB_PASS}
      - DB_DATABASE=bookstack
    volumes:
      - ./data/bookstack:/config
    ports:
      - "127.0.0.1:8081:80"
    depends_on:
      - bookstack-db

  bookstack-db:
    image: mariadb:10.11
    container_name: bookstack-db
    restart: unless-stopped
    environment:
      - MYSQL_ROOT_PASSWORD=${DB_ROOT_PASS}
      - MYSQL_DATABASE=bookstack
      - MYSQL_USER=bookstack
      - MYSQL_PASSWORD=${DB_PASS}
    volumes:
      - ./data/mysql:/var/lib/mysql
```

### Caddy Reverse Proxy

Add to `/etc/caddy/Caddyfile`:

```
wiki.example.com {
    reverse_proxy 127.0.0.1:8081
}
```

Then `sudo systemctl reload caddy`. Caddy handles SSL automatically.

### Post-Deploy Checklist

1. Wait for containers to be healthy: `docker ps --filter "name=bookstack"`
2. Access the URL and login with `admin@admin.com` / `password`
3. **Change the admin password immediately**
4. Create an API token (see next section)
5. Configure branding, language, and registration settings

## API Authentication

This is the most reliable method for creating API tokens — using a PHP script executed inside the BookStack container. The artisan tinker approach is prone to creating broken tokens.

### Creating a Working API Token

```bash
# Step 1: Write a PHP script that generates the bcrypt hash AND inserts the token
cat > /tmp/create_token.php << 'PHPEOF'
<?php
$token_id = 'my_api_token_01';
$secret = 'MySecretPassword123';
$hash = password_hash($secret, PASSWORD_BCRYPT);
$pdo = new PDO(
    'mysql:host=bookstack-db;dbname=bookstack',
    'bookstack',
    getenv('DB_PASS')
);
$pdo->exec("DELETE FROM api_tokens WHERE token_id='$token_id'");
$stmt = $pdo->prepare(
    "INSERT INTO api_tokens (name, token_id, secret, user_id, expires_at, created_at, updated_at)
     VALUES ('api-migration', ?, ?, 1, '2027-01-01', NOW(), NOW())"
);
$stmt->execute([$token_id, $hash]);
echo "Token created successfully!\n";
echo "Use: Token $token_id:$secret\n";
PHPEOF

# Step 2: Copy into the container and execute with the DB password
docker cp /tmp/create_token.php bookstack:/tmp/create_token.php

# Get the DB password from docker-compose.yml
DB_PASS=$(grep 'MYSQL_PASSWORD=' /opt/bookstack/docker-compose.yml | grep -v ROOT | head -1 | cut -d'=' -f2)

docker exec -e DB_PASS="$DB_PASS" bookstack php /tmp/create_token.php
```

### Testing the Token

```bash
curl -s -H 'Authorization: Token my_api_token_01:MySecretPassword123' \
  https://wiki.example.com/api/shelves
# Should return: {"data":[],"total":0}
```

If you get `401 Unauthorized` with "No se ha encontrado un token API que corresponda", the token wasn't inserted correctly — check that `user_id=1` exists and the bcrypt hash was generated by PHP's `password_hash()`.

### Authentication Header Format

All API requests use this header:
```
Authorization: Token {token_id}:{plain_text_secret}
```

## REST API Reference

Base URL: `https://wiki.example.com/api`

### Content Hierarchy

BookStack organizes content as: **Shelves → Books → Chapters → Pages**

- Shelves are the top-level containers (like categories)
- Books sit inside shelves
- Chapters are optional groupings inside books
- Pages hold the actual content (HTML)

### Key Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/api/shelves` | List all shelves |
| POST | `/api/shelves` | Create a shelf |
| PUT | `/api/shelves/{id}` | Update shelf (including book assignment!) |
| GET | `/api/books` | List all books |
| POST | `/api/books` | Create a book |
| POST | `/api/chapters` | Create a chapter |
| POST | `/api/pages` | Create a page |
| GET | `/api/users` | List all users |
| PUT | `/api/users/{id}` | Update user (including role assignment) |
| GET | `/api/roles` | List all roles |

### Creating Content — Full Workflow

Here's the correct order for creating a complete content structure:

```python
import requests

BASE = "https://wiki.example.com/api"
HEADERS = {
    "Authorization": "Token my_token:my_secret",
    "Content-Type": "application/json"
}

# 1. Create the shelf
shelf = requests.post(f"{BASE}/shelves", headers=HEADERS, json={
    "name": "Mi Estante",
    "description": "Descripcion del estante"
}).json()

# 2. Create the book
book = requests.post(f"{BASE}/books", headers=HEADERS, json={
    "name": "Mi Libro",
    "description": "Descripcion del libro"
}).json()

# 3. CRITICAL: Assign the book to the shelf (separate call!)
requests.put(f"{BASE}/shelves/{shelf['id']}", headers=HEADERS, json={
    "books": [book["id"]]
})

# 4. Optionally create chapters
chapter = requests.post(f"{BASE}/chapters", headers=HEADERS, json={
    "book_id": book["id"],
    "name": "Mi Capitulo"
}).json()

# 5. Create pages (can go in a book directly or in a chapter)
# Page in a book:
requests.post(f"{BASE}/pages", headers=HEADERS, json={
    "book_id": book["id"],
    "name": "Mi Pagina",
    "html": "<h1>Titulo</h1><p>Contenido aqui</p>"
})

# Page in a chapter:
requests.post(f"{BASE}/pages", headers=HEADERS, json={
    "chapter_id": chapter["id"],
    "name": "Pagina en Capitulo",
    "html": "<p>Contenido del capitulo</p>"
})
```

### Page Content Format

Pages accept `html` (rendered HTML) or `markdown` (converted to HTML on save). HTML is recommended for migration scripts because you have full control over formatting. Use standard HTML — BookStack renders it inside its content area.

## User & Permission Management

### Default Roles

BookStack ships with these roles (IDs may vary):
- **Admin** (ID: 1) — Full access to everything
- **Editor** (ID: 2) — Can create/edit content
- **Viewer** (ID: 3) — Read-only access
- **Public** (ID: 4) — What logged-out visitors see

### Assigning a User to a Role via API

```bash
# Make user ID 3 an admin
curl -s -X PUT \
  -H 'Authorization: Token my_token:my_secret' \
  -H 'Content-Type: application/json' \
  -d '{"roles":[1]}' \
  'https://wiki.example.com/api/users/3'
```

### Making Content Visible

If you created content as admin and other users can't see it, you have two options:

1. **Give users the Admin role** (quick but overpowered)
2. **Set shelf-level permissions** via the BookStack UI: go to each shelf → Permissions → enable "View" for the appropriate roles

For public-facing content, ensure the **Public** role has View permission on the relevant shelves.

## Branding & Customization

### Custom CSS (injected via Settings → Customization → Custom HTML Head)

```html
<style>
  /* Navbar color */
  header, .tri-layout-left-contents, .breadcrumb-listing {
    background-color: #0C498A !important;
  }
  /* Font */
  body, h1, h2, h3, p { font-family: 'Open Sans', sans-serif !important; }
  /* Link color */
  a { color: #0C498A; }
</style>
<link href="https://fonts.googleapis.com/css2?family=Open+Sans:wght@400;600;700&display=swap" rel="stylesheet">
```

### Language

Set the application language in Settings → Features → Default Language. Individual users can override this in their profile settings.

### Google SSO

Add to docker-compose.yml environment:
```yaml
- GOOGLE_APP_ID=your_client_id.apps.googleusercontent.com
- GOOGLE_APP_SECRET=your_client_secret
- GOOGLE_AUTO_REGISTER=true
- GOOGLE_AUTO_CONFIRM_EMAIL=true
```

Then ensure the `.env` file also has these values (remember: linuxserver image doesn't auto-map).

## Migration from Other Platforms

When migrating content from Notion, Confluence, or other wikis:

1. **Extract content** from the source platform (API or export)
2. **Transform to HTML** — BookStack pages use HTML, so convert markdown/blocks to clean HTML
3. **Plan the hierarchy** — map source structure to Shelves → Books → Chapters → Pages
4. **Create structure top-down**: shelves first, then books, then chapters, then pages
5. **Assign books to shelves** as a separate step (this is easy to forget!)
6. **Set permissions** after migration — content defaults to admin-only visibility
7. **Translate if needed** — for multilingual wikis, translate during the migration step

### Migration Script Pattern

A reliable migration script follows this pattern:

```python
class BookStackAPI:
    def __init__(self, base_url, token_id, token_secret):
        self.base_url = base_url
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Token {token_id}:{token_secret}",
            "Content-Type": "application/json"
        })

    def _url(self, endpoint):
        # NO version prefix! Just /api/{endpoint}
        return f"{self.base_url}/api/{endpoint}"

    def create_shelf(self, name, description=""):
        return self.session.post(self._url("shelves"),
            json={"name": name, "description": description}).json()

    def assign_books_to_shelf(self, shelf_id, book_ids):
        return self.session.put(self._url(f"shelves/{shelf_id}"),
            json={"books": book_ids}).json()

    def create_book(self, name, description=""):
        return self.session.post(self._url("books"),
            json={"name": name, "description": description}).json()

    def create_chapter(self, book_id, name):
        return self.session.post(self._url("chapters"),
            json={"book_id": book_id, "name": name}).json()

    def create_page(self, name, html, book_id=None, chapter_id=None):
        data = {"name": name, "html": html}
        if chapter_id:
            data["chapter_id"] = chapter_id
        elif book_id:
            data["book_id"] = book_id
        return self.session.post(self._url("pages"), json=data).json()
```

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| 405 Method Not Allowed on POST | URL has `/v1/` prefix | Remove version prefix — use `/api/shelves` not `/api/v1/shelves` |
| 401 Unauthorized | Token not in database or bad hash | Recreate token with PHP PDO script inside container |
| Content invisible to users | Default permissions | Assign Admin role to user, or set shelf permissions in UI |
| Books not appearing in shelf | Not assigned | `PUT /api/shelves/{id}` with `{"books": [id1, id2]}` |
| .env not updating after docker-compose change | LinuxServer image quirk | Manually edit `/config/www/.env` inside the container volume |
| Container won't start | Port conflict | Check if another service uses the same port; change in docker-compose |
| Google SSO not working | .env missing SSO vars | Add GOOGLE_* vars to both docker-compose.yml AND the .env file |
| DB access denied from host | Wrong password or user | Use `docker exec` to run mysql commands inside the db container |

## Useful Commands

```bash
# View logs
cd /opt/bookstack && docker compose logs -f bookstack

# Restart BookStack
cd /opt/bookstack && docker compose restart bookstack

# Update BookStack
cd /opt/bookstack && docker compose pull && docker compose up -d

# Backup everything
tar -czf bookstack-backup-$(date +%Y%m%d).tar.gz /opt/bookstack/data/

# Check container status
docker ps --filter "name=bookstack"

# Access BookStack shell
docker exec -it bookstack bash

# Access database
docker exec -it bookstack-db mysql -u root -p bookstack

# Get DB password from docker-compose
grep 'MYSQL_PASSWORD=' /opt/bookstack/docker-compose.yml | grep -v ROOT | head -1 | cut -d'=' -f2
```

## Key Files on VPS

| Path | Purpose |
|------|---------|
| `/opt/bookstack/docker-compose.yml` | Docker Compose config |
| `/opt/bookstack/credentials.txt` | Generated DB passwords (chmod 600) |
| `/opt/bookstack/data/bookstack/www/.env` | Laravel application config |
| `/etc/caddy/Caddyfile` | Caddy reverse proxy config |
| `/opt/bookstack/data/mysql/` | MariaDB data directory |

---

## Related skills

- `notion` — when the user is deciding between BookStack and Notion for a given knowledge base, or migrating between them
- `cleantechhub-brand` — visual and tone rules for wiki.cleantechhub.net content
- `claude-code` — BookStack deployment and migration scripts are code projects; runs best from Code
- `mac-storage-hygiene` — Docker-based deployment means the `.raw` image grows; see the Docker section
