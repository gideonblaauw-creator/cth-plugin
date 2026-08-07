---
name: canva
description: >
  Export designs, get thumbnails, prepare images for other tools (Buffer, social
  media, email, Notion), or work with Canva designs in any way. Trigger on Canva,
  design export, social media visuals from Canva, or posting Canva images
  anywhere. Critical sequencing and URL-handling rules apply.
metadata:
  version: "2.0.0"
  category: operations
---

# Canva Operations

Work with Canva designs — search, read, export, edit, and prepare images for downstream use in Buffer, email campaigns, Notion, Google Slides, and other tools.

## Critical Rule: Export Before Use

Canva editor URLs (`canva.com/design/...`) are NOT usable as image URLs in other tools. They point to the Canva editor, not to an image file. Passing an editor URL to Buffer, an email platform, or any other tool will silently fail or produce broken images.

Always export the design first to obtain a public, downloadable image URL.

## Standard Export Workflow

Follow this sequence every time you need a usable image from a Canva design:

1. **Identify the design**: Search by name using `search-designs`, or use the design ID if already known.
2. **Read the design**: Call `read-design` with the design ID to inspect its current state — pages, dimensions, and content.
3. **Export the design**: Call `export-design` with:
   - `designId`: the design's ID
   - `format`: PNG (for social media, web), PDF (for print, documents), or other supported formats
   - `pages`: specify page numbers if the design has multiple pages and you only need specific ones
4. **Poll for completion**: Export is asynchronous. The initial response returns a job ID or status. Poll until the export is complete.
5. **Retrieve the download URL**: Once complete, the response contains a temporary download URL.
6. **Use the URL promptly**: Export URLs are temporary (typically valid for a few hours). Download the file or pass it to the downstream tool immediately.

## Common Integration Patterns

### Canva to Buffer (Social Media Post)

1. Export the design as PNG at the appropriate dimensions for the target platform
2. Confirm the export URL is accessible
3. Pass the export URL to Buffer's `create_post` as the media attachment
4. Create the post with the accompanying text and schedule

Do not skip the export step. Do not pass the Canva editor URL to Buffer.

### Canva to Notion (Content Database)

1. Export the design as PNG
2. Download the exported file or use the temporary URL
3. Attach to the Notion page or database record
4. If the URL will be stored long-term, download and re-upload to a persistent location first

### Canva to Email / HTML

1. Export as PNG for inline images or PDF for attachments
2. Download the file to ensure persistence (export URLs expire)
3. Upload to a permanent hosting location if embedding in HTML
4. Reference the permanent URL in the email template or HTML artifact

### Brand Template to New Design

1. Search brand templates: call `search-brand-templates` with keywords matching the campaign or content type
2. Create from template: call `create-design-from-brand-template` with the template ID
3. Edit the new design: call `edit-design` to update text, images, or colors
4. Export the final version using the standard export workflow above

## Design Search and Discovery

### Search by Name
Use `search-designs` with descriptive keywords. Canva searches across design titles and descriptions.

### Search Brand Templates
Use `search-brand-templates` to find organization templates. These are pre-approved designs that maintain brand consistency.

### Browse Folders
Use `list-folder-items` to browse designs organized in Canva folders. Use `search-folders` to find specific folders by name.

## Editing Designs

Use `edit-design` to modify existing designs programmatically:
- Update text elements (headlines, body copy, captions)
- Replace images with new ones
- Adjust colors to match campaign themes

For complex edits, consider creating a new design from a brand template rather than modifying an existing one — this preserves the original as a reference.

## Multi-Page Designs

Some designs (presentations, multi-post carousels) have multiple pages:
- Use `read-design` to see all pages and their content
- Export specific pages by specifying page numbers in `export-design`
- For carousels, export each page separately as individual images

## Known Issues and Limitations

- **Temporary export URLs**: Export download URLs expire after a few hours. Download files immediately or pass them to the downstream tool right away. Never store export URLs for later use.
- **Async export timing**: Large designs or high-resolution exports take longer. Allow adequate time for the export to complete before polling aggressively.
- **Rate limits**: Canva enforces API rate limits. Space out bulk export operations (e.g., exporting 20+ designs) with 2-3 second delays between calls.
- **Format support**: Not all export formats are available for all design types. Use `get-export-formats` to check supported formats before exporting.
- **Design permissions**: The API can only access designs the authenticated user owns or has been shared on. Verify access before attempting operations.

## Troubleshooting

- **Broken images in downstream tools**: Almost always caused by using the Canva editor URL instead of an exported URL. Re-export the design.
- **Export fails or hangs**: Check the design for unsupported elements. Try exporting as a different format.
- **Design not found in search**: Try broader search terms, or browse folders directly. The design may have been renamed or moved.

For Canva template IDs and export format reference, see references/.
