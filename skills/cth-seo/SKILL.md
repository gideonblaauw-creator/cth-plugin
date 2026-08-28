---
name: cth-seo
description: >
  SEO/AEO command center for cleantechhub.net subdomains. Use when: SEO,
  keywords, Search Console, schema, sitemap, Ad Grant, technical SEO audit.
license: MIT
metadata:
  version: "2.1.0"
  category: "programs"
---

# CTH SEO Command Center

## Domain Architecture

| Subdomain | Purpose | CMS |
|-----------|---------|-----|
| cleantechhub.net | Main site | WordPress |
| wiki.cleantechhub.net | Knowledge base | BookStack |
| nexus.cleantechhub.net | Startup portfolio | Static HTML |

## SEO Workflow

### Technical Audit

1. Check Core Web Vitals (LCP, FID, CLS) via PageSpeed Insights.
2. Validate sitemap.xml is current and submitted to GSC.
3. Check robots.txt for unintended blocks.
4. Verify JSON-LD structured data on key pages.
5. Check for broken links and redirect chains.
6. Validate mobile responsiveness.
7. Check llms.txt for AI Overview optimization.

### Keyword Strategy

1. Pull current rankings from Google Search Console.
2. Identify keyword clusters: cleantech acceleration, climate innovation Colombia, green business competition, sustainability consulting.
3. Map keywords to content pillars.
4. Identify content gaps and opportunities.
5. Prioritize by search volume x relevance x competition.

### Content Creation

For every new page:

1. Target 1 primary + 2–3 secondary keywords.
2. Write title tag (60 chars max) with primary keyword.
3. Write meta description (155 chars max) with CTA.
4. Use H1 for page title, H2 for sections, H3 for subsections.
5. Internal link to 3+ related pages.
6. Alt text on all images.
7. Include JSON-LD schema.
8. Ensure E-E-A-T signals: author bio, publish date, sources.

### Google Ad Grant

CTH operates a Google Ad Grant ($10k/month in-kind):
- Max CPC: $2.00.
- Minimum 5% CTR required.
- Must maintain valid conversion tracking.
- Cannot bid on single-word keywords (except brand terms).
- At least 2 ad groups per campaign with 2 ads each.

### AEO (Answer Engine Optimization)

- Maintain llms.txt at cleantechhub.net/llms.txt.
- Structure FAQ content with clear Q&A format.
- Use concise, factual language for AI extraction.
- Include entity markup (Organization, Event, Article schemas).

For keyword tracking templates, see references/.
