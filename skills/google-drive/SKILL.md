---
name: google-drive
description: >
  Searches, reads, uploads, and manages Google Drive files. Use when: Drive,
  Google Docs/Sheets, find a file, upload to Drive.
license: MIT
metadata:
  version: "2.1.0"
  category: "operations"
---

# Google Drive Operations

Search, read, create, and manage files across Google Drive — find documents, read spreadsheet data, upload deliverables, and organize files within the CTH Drive structure.

## Search and Discovery

### Search by Keywords

Use `search_files` with descriptive terms. Google Drive searches across file names, content (for Google Docs, Sheets, Slides), and descriptions.

Tips for effective search:
- Use specific file names or unique phrases from the document
- Combine keywords that are likely to appear together
- Try variations of the file name if the first search returns nothing

### Filter by File Type

Use MIME type filters to narrow results:
- Google Docs: `mimeType='application/vnd.google-apps.document'`
- Google Sheets: `mimeType='application/vnd.google-apps.spreadsheet'`
- Google Slides: `mimeType='application/vnd.google-apps.presentation'`
- PDFs: `mimeType='application/pdf'`
- Folders: `mimeType='application/vnd.google-apps.folder'`

### Recent Files

Call `list_recent_files` for quick access to recently modified files. This is faster than searching when the user mentions "that document I was working on" or similar.

### Browse Folders

When you know the folder structure, navigate directly:
1. Search for the folder by name
2. List its contents to find the target file
3. Drill into subfolders as needed

## Standard Workflows

### Find and Read a Document

1. Search by name or content keywords using `search_files`
2. Review results — check file names, modification dates, and owners to identify the right file
3. Call `read_file_content` with the file ID to retrieve the content
4. For Google Docs: returns the document text
5. For Google Sheets: returns data in a structured text format
6. Present relevant excerpts or a summary to the user

### Read Spreadsheet Data

1. Search for the spreadsheet by name
2. Call `read_file_content` — returns sheet data as structured text
3. Parse the data for analysis, reporting, or transformation
4. For specific sheets within a multi-sheet workbook, specify the sheet name if the API supports it

### Upload a File

1. Prepare the file content locally (create it with Write or generate it)
2. Identify the destination folder — ask the user or search for the appropriate location
3. Call `create_file` with the file name, content, and parent folder ID
4. Confirm the upload with the user and share the file link

### Copy an Existing File

1. Locate the source file using search
2. Call `copy_file` with the source file ID and new name
3. Optionally move the copy to a different folder
4. Useful for creating new documents from templates

### Check File Metadata

Call `get_file_metadata` to inspect:
- File name and description
- Owner and last modifier
- Creation and modification dates
- File size and MIME type
- Parent folder

### Manage Permissions

Call `get_file_permissions` to see who has access to a file:
- Owner, editor, commenter, and viewer roles
- Shared with specific people, groups, or "anyone with the link"
- Domain-wide sharing settings

## File Content Formats

### Google Docs
- Content is returned as plain text or HTML
- Formatting (headings, bold, lists) may be preserved depending on the export format
- For highly formatted documents, consider downloading as PDF instead

### Google Sheets
- Data is returned in a tabular text format
- Multiple sheets may be included
- Formulas may show computed values rather than formulas themselves
- For complex data analysis, download the raw file content

### Google Slides
- Content extraction returns text from slides
- For visual content, export as PDF or PNG
- Slide notes are included in the extracted text

### PDFs and Binary Files
- Use `download_file_content` for binary files
- PDFs, images, and other non-Google formats must be downloaded rather than read inline

## Organizational Patterns

### CTH Drive Structure

Maintain consistent folder organization:
- Use descriptive folder names that reflect the project or department
- Keep active project files in their project folders
- Archive completed projects to an Archive folder
- Shared external files should be in clearly labeled shared folders

### Naming Conventions

- Use dates in file names for versioned documents: `CTH_Report_2026-08-07`
- Include the project or client name for context: `DPS_Budget_Q3_2026`
- Avoid special characters that may cause issues across platforms

## Rules

- **Verify before modifying**: Always read a file to confirm its identity before making changes. File names can be duplicated in Drive.
- **Check permissions**: Before assuming access to a shared file, verify permissions. The API user may not have the same access as the file owner.
- **Confirm uploads**: Always tell the user where a file was uploaded and provide the link.
- **Destructive operations**: Never delete or move files without explicit user confirmation.
- **Large files**: For files over 10MB, use download endpoints rather than inline read.

## Troubleshooting

- **File not found**: Try broader search terms. Check if the file is in a shared drive vs. personal drive. Verify the user has access.
- **Permission denied**: The authenticated account may not have access. Ask the user to share the file or check the sharing settings.
- **Empty content**: Some file types (images, binaries) cannot be read as text. Use `download_file_content` instead.
- **Stale search results**: Drive search indexes may take a few minutes to reflect recent changes. If a newly created file does not appear, wait and retry.

For Drive folder structure and naming conventions, see references/.
