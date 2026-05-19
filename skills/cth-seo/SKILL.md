---
name: cth-seo
description: >
  CleantechHUB SEO Command Center — operational skill for all SEO, AEO, and content strategy across cleantechhub.net subdomains. Use EVERY TIME the user mentions SEO, keywords, rankings, Google Search Console, Google Ads, Ad Grant, meta tags, schema markup, JSON-LD, sitemap, robots.txt, Core Web Vitals, keyword clustering, content decay, cannibalization, internal linking, E-E-A-T, information gain, AI Overviews, AEO, llms.txt, blog strategy, competitor analysis, or technical SEO audit. Also trigger on "audit this page", "optimize for search", "write a blog post", "keyword research", "content brief", "schema for this page", or references to Semrush, Screaming Frog, Ahrefs, or Claude SEO tool. If in doubt whether a task has an SEO dimension — use this skill.
---

# CleantechHUB SEO Command Center Skill

This skill turns every Claude session into an SEO-aware workspace for CleantechHUB. It encodes the full methodology from the "Mastering SEO with Claude Code" playbook, adapted to CTH's specific web properties, data-first strategy, and LATAM climate data positioning.

---

## 1. CTH Web Properties & SEO Roles

| Property | URL | SEO Role | Index? |
|---|---|---|---|
| **Main site** | www.cleantechhub.net | Authority hub, service pages, blog, landing pages | Yes — full index |
| **Climate Intel Platform** | data.cleantechhub.net | Product demo, gated app | Selective — public pages only |
| **BookStack Wiki** | wiki.cleantechhub.net | Educational content, topical authority builder | Yes — public-facing pages |
| **Nexus** | nexus.cleantechhub.net | Community/marketing layer, stories | Yes — content marketing |
| **Apps** | *.apps.cleantechhub.net | SaaS tools (HubPluma, ESG, etc.) | No — login-gated apps |
| **API** | api.cleantechhub.net | Backend | No — noindex, disallow |

### Subdomain Strategy

The main domain (www.cleantechhub.net) is the SEO authority anchor. All high-value content should live under the main domain as subdirectories when possible (/blog, /services, /resources, /about). Subdomains are for application layers only. Wiki content that has strong SEO value should be cross-linked from the main site, or mirrored as blog posts under /blog.

---

## 2. Strategic SEO Alignment (2026 Strategy)

CTH is pivoting to a **data-compounding model** — Climate Data First (AI-Powered). SEO serves the Acquire tier of the GTM funnel:

```
Nexus Content → Organic Search / AI Citations → Free Briefing (T1) → Platform Trial (T2) → Advisory (T3)
```

**SEO's job in the funnel:**
- **Top of funnel (Acquire):** Blog posts, sector snapshots, ecosystem reports rank for informational queries and attract Corporates, Investors, Multilaterals, and Public Sector visitors.
- **Mid-funnel (Expand):** Service pages and case studies rank for commercial queries. Platform landing pages convert organic traffic into trials.
- **AEO layer:** Structured content earns citations in AI Overviews, ChatGPT, Perplexity — positioning CTH as the authoritative LATAM climate data source.

### Target Keywords by Client Segment

| Segment | Keyword Themes | Intent |
|---|---|---|
| **Corporates** | "climate risk assessment LATAM", "cleantech supplier discovery", "corporate sustainability Colombia" | Commercial |
| **Investors** | "climate tech deal flow", "cleantech startups Latin America", "impact investment pipeline" | Commercial |
| **Multilaterals** | "NDC compliance tracker", "climate policy Colombia", "green economy LATAM" | Informational/Commercial |
| **Public Sector** | "green workforce development", "climate innovation ecosystem", "sustainability data platform" | Informational |

---

## 3. The Hybrid Blueprint (AI + Human)

All CTH content follows the hybrid approach. AI drafts, humans refine.

### Why Hybrid Matters

Pure AI content ranks well initially (+35%) but declines 48% over time due to high bounce rates (68%). The hybrid approach combines AI scalability with human originality for sustained rankings.

### Content Production Workflow

```
1. Keyword Research (Semrush/GSC data → Claude clustering)
2. Content Brief (Claude generates outline with claim-evidence structure)
3. AI Draft (Claude writes, following CTH brand voice + SEO checklist)
4. Human Refinement (add proprietary data, counter-narratives, anecdotes)
5. Technical Optimization (schema, meta tags, internal links)
6. Publish + Monitor (GSC tracking, content decay alerts)
```

### CTH Information Inventory (What Makes Our Content Unique)

Draw from these three pillars to achieve information gain:

1. **Proprietary Data:** Startup profiles from 8+ Academy cohorts. 73+ startups ingested. Sector distributions, TRL levels, funding stages across LATAM. No one else has this.
2. **First-Hand Experience:** 5 years operating in LATAM cleantech. REIN Programs across Colombia, Peru, El Salvador, Guatemala, Costa Rica. Use phrases like "In our experience working with 70+ cleantech startups..." or "When we analyzed our cohort data..."
3. **Counter-Narratives:** Challenge the "climate tech is only a developed-world story" narrative. Push the LATAM innovation angle. Challenge generic ESG frameworks with LATAM-specific compliance realities (Colombian Taxonomia Verde, CSRD for LATAM exporters).

---

## 4. On-Page SEO Checklist

Apply to EVERY page or blog post:

### Structure
- Exactly one H1 tag per page (contains primary keyword)
- Primary keyword in the first 100 words
- H2 headings framed as questions (for AI Overview extraction)
- H3 subheadings using claim-evidence pattern
- Short paragraphs (2-3 sentences max)
- Varied sentence lengths (no robotic rhythm)

### Meta Tags
- Title tag: Under 60 characters, primary keyword + CTH brand hook
- Meta description: Under 155 characters, includes CTA and keyword
- OG tags: Title, description, image (1200x630px branded visual)

### Links
- 3-5 internal links per post (to service pages, related blog posts, wiki)
- 2-3 external links (to authoritative sources — IPCC, World Bank, government data)
- Natural anchor text — never forced or keyword-stuffed

### Content Quality (Anti-Slop Rules)
- **FORBID:** "In today's world," "It's important to note," "In conclusion"
- **FORBID:** "delve," "tapestry," "pivotal," "showcase," "underscore," "landscape"
- **FORBID:** Em dashes
- **REQUIRE:** Experience-signaling phrases ("In our testing...", "When we implemented...")
- **REQUIRE:** At least one proprietary data point or first-hand observation per post
- **REQUIRE:** Claim-evidence pattern for key insights (H3 question → 40-60 word answer → evidence)

---

## 5. Technical SEO Standards

### Schema Markup (JSON-LD)

Every page must have appropriate schema. Generate clean JSON-LD — no conversational filler.

| Page Type | Required Schema |
|---|---|
| Homepage | Organization + WebSite + BreadcrumbList |
| Service pages | Service + Organization + BreadcrumbList + FAQPage |
| Blog posts | Article + FAQPage + BreadcrumbList |
| About page | Organization + Person (Gideon) + AboutPage |
| Wiki pages | Article + BreadcrumbList |
| Platform pages | SoftwareApplication + Organization |

**Entity Anchoring:** The /about page must have Organization and Person schema to help AI models associate CTH content with a credible source.

### robots.txt Strategy

```
# www.cleantechhub.net
User-agent: *
Allow: /
Sitemap: https://www.cleantechhub.net/sitemap.xml

# Allow AI crawlers explicitly
User-agent: GPTBot
Allow: /
User-agent: ClaudeBot
Allow: /
User-agent: PerplexityBot
Allow: /
User-agent: Google-Extended
Allow: /

# data.cleantechhub.net — selective
User-agent: *
Disallow: /dashboard/
Disallow: /api/
Allow: /

# api.cleantechhub.net — block all
User-agent: *
Disallow: /

# *.apps.cleantechhub.net — block all
User-agent: *
Disallow: /
```

### llms.txt

Create an llms.txt at the root of www.cleantechhub.net:

```
# CleantechHUB
> LATAM's climate innovation and data intelligence hub.
> We connect cleantech startups with corporates, investors, multilaterals, and government through AI-powered climate data products.

## Key Pages
- /about — Who we are, team, methodology
- /services — Climate data platform, Academy programs, advisory
- /blog — Climate tech insights, sector analysis, startup ecosystems
- /resources — Reports, frameworks, tools

## Data & APIs
- data.cleantechhub.net — Climate Intel Platform (requires subscription)
- api.cleantechhub.net — Climate data API (authenticated access)
- wiki.cleantechhub.net — Public knowledge base on climate innovation
```

### Core Web Vitals Targets

| Metric | Target |
|---|---|
| LCP | < 2.5s (aim for < 1.0s) |
| CLS | < 0.1 |
| FID/INP | < 200ms |
| Performance Score | > 90 (aim for 97+) |

---

## 6. Keyword Research & Clustering

### Process

1. **Source keywords:** Export from Semrush or GSC
2. **Apply winning filters:** KD <= 30, Volume >= 100, Intent = Informational (blog) or Commercial (service pages)
3. **Feed to Claude for clustering:** Group by semantic relevance and search intent
4. **Identify money keywords:** "Service + City" combinations, high CPC terms
5. **Map clusters to content:** Each cluster = one comprehensive page targeting 50-100 keywords

### Clustering Prompt Template

```xml
<role>Senior SEO strategist specializing in semantic search and intent mapping for climate tech</role>
<context>
CleantechHUB is a LATAM climate data and innovation hub. Target audiences: corporates needing sustainability compliance, investors seeking climate deal flow, multilaterals tracking NDC progress, public sector building green workforce.
</context>
<task>
Analyze the keywords in <data>. Cluster into logical groups based on semantic relevance and search intent. Each cluster should be targetable by a single comprehensive page. For each cluster, specify: cluster name, primary keyword, supporting keywords, search intent, recommended page type, and priority.
</task>
<data>[Paste CSV keyword data here]</data>
```

### CTH-Specific Keyword Pillars

| Pillar | Root Keywords | Content Type |
|---|---|---|
| Climate Data & Intelligence | climate data platform, sustainability analytics, ESG data | Service pages |
| LATAM Cleantech Ecosystem | cleantech startups Latin America, climate innovation Colombia | Blog + reports |
| Corporate Sustainability | sustainability compliance, green taxonomy, CSRD for exporters | Blog + service |
| Climate Investment | climate tech investment, impact fund pipeline, cleantech deal flow | Blog + landing |
| Green Workforce | green jobs LATAM, sustainability training, climate careers | Blog + Academy pages |

---

## 7. AEO — Answer Engine Optimization

CTH must be the source AI Overviews cite, not just a page that ranks.

### AEO Infrastructure Checklist

- Every H2 heading framed as a question
- FAQ schema on every blog post and service page
- /about page with Organization + Person + AboutPage schema (entity anchor)
- robots.txt allowing GPTBot, ClaudeBot, PerplexityBot, Google-Extended
- llms.txt at site root
- Claim-evidence pattern on all key insights
- Short direct answers (40-60 words) after each H3 question header
- Internal links creating topical cluster authority

---

## 8. Google Ad Grant Strategy

CTH has a Google for Nonprofits account with ~$10,000/month in unused Ad Grant credits.

### Ad Grant Compliance Rules
- 5% minimum CTR requirement
- No single-word keywords
- No overly generic keywords
- Must use Maximize Conversions bidding
- Must have valid conversion tracking
- Quality Score >= 3 on all keywords

### Campaign Structure

| Campaign | Objective | Budget % |
|---|---|---|
| Climate Intel Platform | Drive platform signups | 30% |
| Academy / REIN Programs | Drive applications | 25% |
| Blog Content | Drive traffic to pillar pages | 20% |
| Brand Awareness | Branded terms | 10% |
| Reports & Resources | Drive downloads / leads | 15% |

---

## 9. Content Decay & Audit Workflows

### Six-Step Monthly Audit

1. Quick Win Identification (positions 4-10, CTR < 3%)
2. Competitor Gap Analysis
3. Keyword Clustering (new data → content plan)
4. On-Page Optimization (PASS/WARN/FAIL audit)
5. Technical SEO + Schema validation
6. Internal Linking Audit (orphan pages, new opportunities)

---

## 10. Bilingual SEO (English + Spanish)

- **Spanish-first** for LATAM-facing content
- **English** for international audience
- **Hreflang tags** for dual-language content
- **Separate keyword research** per language
- URL structure: /es/blog/[slug], /en/blog/[slug], default /blog/[slug] = Spanish

---

## 11. Topical Authority Architecture

Organize by semantic topic clusters, not chronological:

```
/blog/
  climate-data/          <- Pillar: Climate intelligence
  cleantech-ecosystem/   <- Pillar: LATAM ecosystem
  corporate-sustainability/  <- Pillar: Compliance & ESG
  investment/            <- Pillar: Climate finance
```

Every informational post links to at least one commercial service page.

---

## 12. Available MCP Integrations

| Tool | MCP | What It Provides |
|---|---|---|
| Google Search Console | Windsor.ai | Query performance, CTR, positions |
| Google Analytics (GA4) | Windsor.ai | Traffic by channel |
| Google Ads (Ad Grant) | Windsor.ai | Campaign performance |
| Canva | Canva MCP | OG images, blog visuals |
| Notion | Notion MCP | Content calendar |
| Monday.com | Monday MCP | SEO task tracking |
| Slack | Slack MCP | SEO notifications |
| Buffer | Buffer MCP | Social amplification |
| BookStack | BookStack API | Wiki content inventory |

---

## Related Skills

- `cleantechhub-brand` — Brand voice, colors, visual identity (always co-trigger)
- `social-media-campaign` — Blog content amplification via Buffer
- `canva` — OG image and blog visual generation
- `bookstack` — Wiki content for topical authority
- `google-drive` — Past SEO docs and reports
- `windsor-ai` — GA4, GSC, and Google Ads data
- `notion` — Editorial calendar and content planning

---

*Based on "Mastering SEO with Claude Code and AI Strategy" (May 2026) adapted for CleantechHUB's Climate Data First strategy.*
