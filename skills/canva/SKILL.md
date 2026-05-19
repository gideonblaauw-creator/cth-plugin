---
name: canva
description: >
  Use this skill whenever Canva is involved in any way — exporting designs, getting thumbnails,
  preparing images for use in other tools (Buffer, social media schedulers, email platforms,
  Notion, Google Slides, etc.), or any workflow that touches a Canva design. Trigger immediately
  when the user mentions Canva, design export, social media visuals from Canva, or posting
  Canva images anywhere. Do NOT attempt Canva MCP calls without first reading this skill —
  critical sequencing and URL-handling rules apply that will prevent hard-to-debug failures.
---

# Canva Skill

This skill encodes everything learned from a real production session using the Canva MCP to
export social media assets. Follow these rules exactly — every one of them was discovered
through an actual failure.

---

## 1. NEVER make Canva MCP calls in parallel

The Canva MCP uses a stateful session. If you fire two or more Canva tool calls at the same
time (i.e. in the same message), all but the first will fail with:

> "Session state unavailable; cannot verify tool permissions."

**Rule:** Every Canva MCP call must be its own sequential step. Wait for a result before
making the next call. This applies to `export-design`, `get-design-thumbnail`,
`start-editing-transaction`, `cancel-editing-transaction`, and every other Canva tool.

---

## 2. Canva export URLs are NOT publicly accessible

When you call `export-design` or `get-design-thumbnail`, Canva returns an AWS pre-signed S3
URL. These URLs include an `x-amz-expected-bucket-owner` header requirement that ties the
request to Canva's own AWS account.

**Consequence:** You cannot use these URLs directly in:
- Buffer (`create_post` → "Failed to fetch image dimensions: Not Found")
- Any external image hosting check
- `curl` from the sandbox (also blocked by network, see §5)
- Any third-party service that doesn't know Canva's AWS account ID

**Rule:** Never pass a raw Canva export/thumbnail URL to Buffer or any external service.
You must re-host the image first (see §4).

---

## 3. Getting thumbnails requires an editing transaction

`get-design-thumbnail` does not work standalone. You must first call
`start-editing-transaction` and then pass the `transaction_id` to the thumbnail call.

**Correct flow:**
```
1. start-editing-transaction  → returns transaction_id (e.g. "4345347249581065398")
2. get-design-thumbnail        → pass transaction_id + page_index (1-based, NOT 0-based)
3. cancel-editing-transaction  → always cancel when done to release the lock
```

**Important:** `page_index` is 1-based. Page 1 = index 1, page 4 = index 4.

**Thumbnail resolution:** Canva thumbnails are approximately 600×600 px. If you need
full-resolution (e.g. 1080×1080 for Instagram), use `export-design` instead, which
returns full-res images — but those are also subject to the AWS URL restriction in §2.

---

## 4. Re-hosting Canva images: the Imgur workaround via Chrome

Because the sandbox has no outbound network (curl exits with code 56) and Canva URLs are
signed for Canva's AWS account only, the only reliable way to get a publicly accessible
URL for a Canva image is to use the **user's browser** (which is authenticated to Canva)
plus the **Imgur anonymous upload API**.

### Why it works
- The browser is logged into canva.com, so it can load signed Canva URLs
- `<img crossOrigin='anonymous'>` lets the browser load the image into a `<canvas>` element
- The canvas can be exported as base64
- Imgur's anonymous API accepts a base64 image and returns a permanent public URL that any
  server (Buffer, Notion, email, etc.) can access

### Step-by-step

**Step 1:** Get the Canva image URLs (via `export-design` or `get-design-thumbnail` — see §3).

**Step 2:** Navigate the browser to a Canva tab (the user must be logged in). Use the
Claude-in-Chrome MCP `navigate` tool to open canva.com if not already there.

**Step 3:** Run the following JavaScript via `javascript_tool` or `execute_javascript`:

```javascript
(async () => {
  const images = [
    { id: 'post2', url: 'PASTE_CANVA_URL_HERE' },
    { id: 'post3', url: 'PASTE_CANVA_URL_HERE' },
    // add more as needed
  ];

  const uploadToImgur = async ({ id, url }) => {
    const b64 = await new Promise((resolve, reject) => {
      const img = new Image();
      img.crossOrigin = 'anonymous';
      img.onload = () => {
        const canvas = document.createElement('canvas');
        canvas.width = img.width;
        canvas.height = img.height;
        canvas.getContext('2d').drawImage(img, 0, 0);
        resolve(canvas.toDataURL('image/png').split(',')[1]);
      };
      img.onerror = reject;
      img.src = url;
    });

    const response = await fetch('https://api.imgur.com/3/image', {
      method: 'POST',
      headers: {
        'Authorization': 'Client-ID 546c25a59c58ad7',
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ image: b64, type: 'base64' })
    });
    const json = await response.json();
    return { id, link: json?.data?.link, status: response.status };
  };

  // Upload all images in parallel (Imgur can handle this; only Canva MCP cannot)
  const results = await Promise.all(images.map(uploadToImgur));
  return JSON.stringify(results);
})();
```

**Step 4:** The script returns an array like:
```json
[
  { "id": "post2", "link": "https://i.imgur.com/AbCdEfG.png", "status": 200 },
  { "id": "post3", "link": "https://i.imgur.com/XyZaBcD.png", "status": 200 }
]
```

These `https://i.imgur.com/...` URLs are publicly accessible and can be passed directly
to Buffer, Notion, emails, or any other service.

### Notes on the Imgur API
- **Client ID:** `546c25a59c58ad7` (CleantechHUB anonymous uploads)
- **No authentication required** for anonymous image hosting
- **Rate limits:** generous for typical social media batches (4–20 images)
- **URL format:** `https://i.imgur.com/<hash>.png` — permanent, no expiry for active links
- Uploads are parallel-safe (only Canva MCP calls must be sequential — see §1)

---

## 5. Sandbox has no outbound network

Do not attempt to download Canva images, upload to image hosts, or make any external HTTP
requests from the sandbox (Bash tool or Python scripts). These will fail with exit code 56
or similar network errors.

**Rule:** All network calls to external services involving image data must go through the
Chrome browser (Claude-in-Chrome MCP), where the user's network context applies.

---

## 6. Buffer: always use public image URLs

When creating Buffer posts with images:
- Always use Imgur URLs (from §4) or other truly public CDN URLs
- Never use Canva export URLs, pre-signed S3 URLs, or any URL with expiry/signature
- For Instagram: an image is mandatory. Buffer will reject IG posts without at least one image.
- For Facebook: images are optional but strongly recommended for engagement

---

## 7. Watch out for "shareNow" silent success

When using Buffer's `create_post` with `mode: shareNow` and the call seems to time out or
return slowly, the post may have actually been published server-side. Do NOT retry
immediately — check Buffer's dashboard or `list_posts` first to confirm whether the post
was created. Retrying a "shareNow" can result in a duplicate post that cannot be deleted.

---

## 8. Quick reference: common errors and fixes

| Error | Root Cause | Fix |
|---|---|---|
| "Session state unavailable; cannot verify tool permissions" | Parallel Canva MCP calls | Make all Canva calls sequential |
| Buffer "Failed to fetch image dimensions: Not Found" | Passing Canva S3 signed URL to Buffer | Re-host via Imgur first (§4) |
| curl exit code 56 | Sandbox has no outbound internet | Use Chrome browser JS instead |
| `get-design-thumbnail` failure | No editing transaction open | Call `start-editing-transaction` first |
| Instagram post rejected | Missing image | Imgur workaround required before IG posts |
| Buffer duplicate post | Retry of silent-success shareNow | Check `list_posts` before retrying |

---

## 9. Typical end-to-end workflow

For posting Canva designs to social media (e.g. Buffer → Instagram + Facebook):

```
1. [Sequential] Export each page from Canva using export-design OR
   [Sequential] start-editing-transaction → get-design-thumbnail (per page) → cancel-editing-transaction

2. [Chrome] Open canva.com tab in user's browser

3. [Chrome JS] Run Imgur upload script with all image URLs in parallel
   → collect https://i.imgur.com/... URLs

4. [Buffer] create_post for each channel using Imgur URLs as media
   → use mode: customScheduled or saveToDraft (not shareNow unless truly ready to publish)

5. Confirm post IDs and share a summary with the user
```

---

## 10. Design ID and page references

When the user refers to "slides", "pages", or "visuals" from a Canva design:
- The design ID is typically in the Canva URL: `https://www.canva.com/design/<DESIGN_ID>/...`
- Pages are 1-indexed in `get-design-thumbnail` (page_index: 1 = first slide)
- Confirm page numbers with the user or check the handoff document before exporting — 
  page numbers in a brief may refer to specific numbered slides in the design

---

## 11. Related skills

- `buffer` — the destination for most Canva exports; enforces the public-image-URL rule that drives §4
- `social-media-campaign` — orchestrates the full Canva → Imgur → Buffer pipeline for campaigns
- `claude-in-chrome` — the browser runtime that executes the Imgur rehost JavaScript in §4
- `cleantechhub-brand` / `clp26-brand` — brand rules for what Canva designs should contain before export
