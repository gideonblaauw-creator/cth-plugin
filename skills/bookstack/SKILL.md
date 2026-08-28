---
name: bookstack
description: >
  Deploys and manages BookStack wiki via Docker and REST API. Use when:
  BookStack, wiki deployment, wiki.cleantechhub.net, knowledge base,
  shelves/books/chapters/pages.
license: MIT
metadata:
  version: "2.1.0"
  category: "operations"
---

# BookStack Operations

Manage the CleantechHUB BookStack wiki instance — deploy containers, maintain infrastructure, migrate content, and interact with the REST API for programmatic content management.

## CTH Instance

- URL: wiki.cleantechhub.net
- Deployment: Docker container on OVH VPS
- Database: MariaDB container (shared Docker network)
- Reverse proxy: Caddy (auto-TLS)

## Content Hierarchy

BookStack organizes content as: Shelves > Books > Chapters > Pages.

- **Shelves**: top-level categories (e.g., "Programs", "Infrastructure", "Clients"). Use shelves to group related books under a single organizational umbrella.
- **Books**: projects or topics within a shelf. Each book represents a coherent subject area with its own table of contents.
- **Chapters**: logical groupings within a book. Use chapters to break large books into navigable sections.
- **Pages**: individual content documents. Pages hold the actual written content, images, and attachments.

Always respect this hierarchy when creating content. Never create orphan pages — every page belongs to either a book directly or a chapter within a book.

## API Usage

Base URL: `https://wiki.cleantechhub.net/api/`

Authentication: Token-based. Include both the Token ID and Token Secret in the Authorization header as `Token {id}:{secret}`.

### Common Read Operations

- List all shelves: `GET /api/shelves`
- Get a shelf and its books: `GET /api/shelves/{id}`
- List all books: `GET /api/books`
- Get a book and its contents: `GET /api/books/{id}`
- List all pages: `GET /api/pages`
- Get a page with HTML content: `GET /api/pages/{id}`
- Search across all content: `GET /api/search?query={term}`

### Common Write Operations

- Create a page in a book: `POST /api/pages` with `book_id`, `name`, and `html` or `markdown`
- Create a page in a chapter: `POST /api/pages` with `chapter_id`, `name`, and `html` or `markdown`
- Update a page: `PUT /api/pages/{id}` with updated `name` and/or `html`/`markdown`
- Create a book: `POST /api/books` with `name` and optional `description`
- Create a chapter: `POST /api/chapters` with `book_id`, `name`, and optional `description`
- Create a shelf: `POST /api/shelves` with `name` and optional `description`

### Search Best Practices

Use the search endpoint with targeted queries. BookStack search supports:
- Plain text search across all content
- Filters: `{type:page}`, `{type:chapter}`, `{type:book}`
- Tag filters: `[tagname=value]`

Prefer search over listing all items and filtering client-side — it is faster and respects permissions.

## Docker Management

The BookStack container runs alongside other CTH services on the OVH VPS. All containers share a Docker network for inter-service communication.

### Routine Maintenance

- View logs: `docker logs bookstack` (add `--tail 100` for recent entries)
- Restart the service: `docker restart bookstack`
- Check container health: `docker ps --filter name=bookstack`
- View resource usage: `docker stats bookstack --no-stream`

### Backup Procedure

1. Dump the MariaDB database: `docker exec bookstack-db mysqldump -u bookstack -p bookstack > backup.sql`
2. Copy uploaded files from the container: `docker cp bookstack:/config/www/uploads/ ./uploads-backup/`
3. Copy environment configuration: back up the `.env` file and `docker-compose.yml`
4. Store backups off-server (use rsync or scp to a secondary location)

### Recovery Procedure

1. Deploy fresh containers using the saved `docker-compose.yml`
2. Import the database dump: pipe `backup.sql` into the MariaDB container
3. Restore uploads to `/config/www/uploads/`
4. Verify the instance loads correctly and content is intact

## Content Migration

When migrating content into BookStack from other sources (Notion, Google Docs, Confluence):

1. Map the source structure to BookStack hierarchy (Shelves/Books/Chapters/Pages)
2. Convert content to HTML or Markdown
3. Use the API to create the hierarchy top-down: shelves first, then books, then chapters, then pages
4. Upload images and attachments separately via the attachments API
5. Verify links and cross-references after migration

## Troubleshooting

- **502 Bad Gateway**: Check if the BookStack container is running. Restart if needed. Verify Caddy is proxying to the correct internal port.
- **Authentication errors on API**: Verify the token ID and secret are correct. Check that the token has not been revoked in the BookStack admin panel.
- **Missing images after backup restore**: Ensure the `/config/www/uploads/` directory was fully restored with correct file permissions.
- **Slow performance**: Check MariaDB container resources. Consider adding indexes or increasing container memory limits.

## User and Permission Management

BookStack has a built-in roles and permissions system:

- **Roles**: define what actions a user can perform (view, create, edit, delete) at the system level
- **Entity permissions**: override role-level permissions on individual shelves, books, chapters, or pages
- **API tokens**: each user can create API tokens for programmatic access — tokens inherit the user's permissions

When creating content via the API, the content is owned by the user whose API token is used. Plan token usage accordingly — use an admin token for system-level operations and user-specific tokens when content ownership matters.

### Common Permission Patterns

- Public wiki (read-only for guests): enable the Guest role with view permissions
- Team wiki (authenticated access): disable the Guest role, assign users to appropriate roles
- Restricted sections: set entity-level permissions on sensitive books or shelves to limit access to specific roles

## Integration Points

BookStack integrates with the broader CTH infrastructure:
- Caddy handles TLS termination and reverse proxying
- MariaDB provides the database backend on a shared Docker network
- Backups feed into the CTH disaster recovery process
- Content can be cross-referenced with Notion pages and Google Drive documents

## Attachment and Image Management

BookStack handles file attachments and images through dedicated API endpoints:

- **Image uploads**: `POST /api/image-gallery` to upload images for use in page content
- **Attachments**: `POST /api/attachments` to attach files to pages (PDFs, spreadsheets, etc.)
- **Linked images**: reference external image URLs directly in page HTML content

When migrating content with images, upload images first via the image gallery API, then reference the returned URLs in the page HTML. This ensures images are stored within BookStack rather than depending on external sources.

For API reference details and Docker compose configuration, see references/.
