# LinkedIn Community Management API access request

Prepared 22 October 2026 for Gideon Blaauw. He submits this himself, from his own device, at [developer.linkedin.com](https://developer.linkedin.com). This pack does not log in to LinkedIn, and it does not click any LinkedIn screen.

The existing app was supplied as **n8n-li CleantechHUB**, app id **266511324**, Client ID **782xlcklyvbakg**. Its current scopes were supplied as `email`, `openid`, `profile`, and `w_member_social`. Those facts were not re-checked inside LinkedIn.

LinkedIn does not publish the live survey’s exact question labels. A survey is generated in the Developer Portal after you request the product. The paste blocks below cover every item the current docs say the form must contain. Resolved fields are filled below. Anything only Gideon knows stays as `[GIDEON TO FILL]`. Do not guess.

Internal working draft. Gideon reviews every paste block before it leaves his device.

## Stop before you submit

**Privacy-policy URL: not live.** There is no URL to paste yet. Do not submit the access form until a private window returns 200 on a page that is this privacy policy, with valid TLS, and without a login. LinkedIn’s rejection for a missing page is **Invalid Privacy Policy**. A Development-tier rejection cannot be retried on the same app.

Checked on 22 October 2026, without a login:

- `https://cleantechhub.net/politica-de-privacidad/` returns 404. WordPress is not the publish path. There is no WordPress admin access.
- `https://jobs.cleantechhub.net/privacidad/` and `https://jobs.cleantechhub.net/privacy` return 200, but the body is the jobs homepage, not this policy. Do not paste those URLs.
- `https://agents.cleantechhub.net/privacidad/` and `https://agents.cleantechhub.net/privacy` return 200 with an empty body. Do not paste those URLs.

The approved draft is `artifacts/cleantechhub-privacy-policy.html`. It was not deployed. Both candidate hostnames resolve to the OVH VPS `51.195.45.77` and answer with Caddy. Writing a file there needs a secret from Infisical. This environment has no Infisical CLI, no Infisical identity variables, and no Infisical config file. Vercel is connected, but neither hostname points at Vercel, and a new DNS record was not allowed.

The `/diagnostico` green-finance checkbox is still an open item. A fresh fetch of `https://cleantechhub.net/diagnostico/` still contains `<input type="checkbox" id="newsletter-consent" checked>`. It was not changed. Fixing it needs WordPress admin, which is not available.

Do not paste the Google Drive policy PDF into the privacy-policy field. That file is not a page on cleantechhub.net.

The worker authorization PDF is also the wrong document. Do not use `https://cleantechhub.net/wp-content/uploads/2026/07/Autorizacion-Tratamiento-Datos-Trabajadores.pdf`. It is a consent form for workers and contractors. Its street line also disagrees with the website and with the data policy.

## 1. Paste-ready form answers

### 1.1 Which app

**Paste if the new app is the one in front of you:**

This request is for a new CleantechHUB developer app. Its only product is the Community Management API. The existing app is n8n-li CleantechHUB, Client ID 782xlcklyvbakg. That app already has Sign In with LinkedIn and member posting. Leave that app in place for personal-profile posting.

**Why:** Community Management must be the only product on the app. If Share, Sign In, or any other product is already on the app, Request access stays grayed out. Source: [LinkedIn API Partner Support](https://learn.microsoft.com/en-us/linkedin/shared/linkedin-api-partner-support-guide).

### 1.2 App name

**Paste:**

CleantechHUB n8n

**Do not use** a name that contains Linked, In, LinkedIn, Microsoft, or the abbreviation li. **Invalid App Name** is a published rejection. The examples in the docs are “Linked” and “In”. The current name n8n-li contains “li”. The docs do not say whether reviewers treat those two letters as a portion of LinkedIn. Use the clean name on the new app so a rejection is not spent on the name.

### 1.3 Company and legal entity

**Paste:**

FUNDACIÓN CLEANTECH HUB

Entidad sin ánimo de lucro (ESAL), régimen tributario especial.

NIT (Número de Identificación Tributaria) 901.523.941-9.

Bogotá D.C., Colombia.

Legal representative: Gideon Blaauw, Representante Legal de la Fundación CleantechHUB.

Phone: +57 313 715 5965.

**Where this comes from:** Gideon confirmed this legal name, this non-profit form, and this tax number on 22 October 2026 for the public privacy policy. The NIT matches the public “Política y tratamiento de datos” PDF linked from [the governance page](https://cleantechhub.net/governance/). That page also says “Fundación”. The PDF contact block names Gideon Blaauw, cargo Representante legal.

**Paste this name.** Do not add a simplified-stock-company suffix. The 2022 PDF used a commercial company form. Do not copy that form into this field. A name that does not match the registry is a known cause of **Fail Organization Verification**.

### 1.4 Registered address

**Paste:**

Calle 90 No. 19-41 Of. 801, Bogotá D.C., Colombia.

**Where this comes from:** Gideon confirmed this address on 22 October 2026. It matches the public data policy (CALLE 90 No. 19-41 OF 801, Bogotá) and the site footer at `https://cleantechhub.net/`, which prints “Cll 90 #19 - 41 Office 801”.

Do not paste Calle 45 #9-42 from the worker authorization PDF.

### 1.5 Business email

**Paste:**

admin@cleantechhub.net

**Where this comes from:** Gideon set this as the public contact on 22 October 2026. It is the address in the privacy policy.

**Rules from the docs:** the address must be a business email. A personal mailbox will not pass. LinkedIn sends a verification message to this address. Check spam, junk, the social tab, and the promotions tab. He must be able to open admin@cleantechhub.net.

### 1.6 Website

**Paste:**

https://cleantechhub.net

The organization website and the domain must match this site. Review checks a verified organization website and domain.

### 1.7 Privacy policy URL

**Status: not live. Do not paste a URL yet.**

The approved page is `artifacts/cleantechhub-privacy-policy.html`. It is not on a public URL. See the stop notice. Paste the URL only after it returns 200 without a login and the body is this policy.

### 1.8 LinkedIn Page

**Paste:**

LinkedIn Page name: CleantechHUB.

LinkedIn Page URL: [GIDEON TO FILL].

Organization ID: [GIDEON TO FILL].

The public pages checked on cleantechhub.net do not print the company Page URL or the organization id. The Page must belong to the same organization as the legal entity. A Page for a different organization is **Invalid Company Page**.

### 1.9 Page admin

**Paste:**

Page super admin who will approve the app verification URL: [GIDEON TO FILL].

LinkedIn member who will sign in and grant the token: [GIDEON TO FILL].

That member’s company Page role: ADMINISTRATOR.

Verification is done by a Page super admin. Posting can be done by an ADMINISTRATOR, a DIRECT_SPONSORED_CONTENT_POSTER, or a CONTENT_ADMIN. Page analytics under `rw_organization_admin` is limited to the ADMINISTRATOR role. Gideon is named as legal representative in the data policy. That sentence does not prove his LinkedIn Page role. `[GIDEON TO FILL]` both names, even if they are Gideon.

The super admin has 30 days to open the verification URL. Approval is permanent. The app cannot later move to another Page.

### 1.10 Use case description

**Paste:**

CleantechHUB will use the Community Management API for its own LinkedIn Page only.

The use cases are Page Management and Page Analytics.

A private n8n workflow, run by CleantechHUB, will publish CleantechHUB jobs, program news, and newsletters as that Page.

The same workflow will read that Page’s own posts and comments.

It will read aggregate analytics for those posts. The counts are impressions, clicks, reactions, comments, shares, and engagement.

It will read aggregate follower counts and page view counts for that same Page.

The workflow serves no other organization.

It does not scrape member profiles.

It does not use LinkedIn data for ads, sales, recruiting, lead lists, or audience building.

It does not place a LinkedIn feed on cleantechhub.net or on an intranet.

It does not combine member data with a CRM (customer relationship management) system or any other database.

### 1.11 Company and product overview

**Paste:**

CleantechHUB is a climate innovation organization in Latin America. Its public site is https://cleantechhub.net.

This application is not sold to other companies. It is CleantechHUB’s own publishing workflow.

The workflow posts CleantechHUB content to the CleantechHUB Page, then reads that Page’s results.

No third-party Pages are connected. No ads account is connected.

### 1.12 How the data is used

**Paste:**

We use organization posts we created so the Page can show CleantechHUB jobs, programs, and newsletters.

We use our own post ids so the workflow can avoid duplicate posts and can fetch analytics for those posts.

We use aggregate Page analytics so CleantechHUB staff can see how our own posts performed. The figures are impressions, clicks, reactions, comments, shares, follower counts, and page views.

We display comments on our own posts only to CleantechHUB people who manage that Page.

We request only the member data required to show that a comment exists. We do not export member data. We do not build member profiles. We do not enrich any other database.

### 1.13 How the data is stored

**Paste:**

Data stays inside CleantechHUB’s own n8n workflow. OVH hosts that workflow in Germany, the same host and country as https://cleantechhub.net. OVH’s data processing terms cover that hosting. Deletion follows the periods below.

Storage follows the LinkedIn Marketing API data storage requirements.

Posts and other social activity by our own Page may be stored for up to six months, because the Page authenticates into this app. The shorter public cap, where the organization has not authenticated, is six weeks.

Aggregate Page admin and reporting data, with no individual member record, may be stored for up to one year. This includes follower counts and summaries of social actions.

Our Page’s name and logo URL may be stored for up to eight weeks while the Page is authenticated.

Ids for the organization, our posts, and social actions may be kept with no LinkedIn time cap.

The signed-in Page admin’s person id and basic profile may be kept with no LinkedIn time cap. We keep them only to hold that admin’s authorization.

Content of member comments, reactions, and other member social activity is kept for no more than 48 hours, then deleted.

Profile fields of members who did not sign in are cached for no more than 24 hours. Examples are a commenter’s name, photo, or headline. They are not stored.

We delete stored member data when the admin asks, and when LinkedIn asks. On termination of the Marketing API terms, member data is deleted immediately, except lead-form and Page-messaging data, which this app does not collect.

### 1.14 Scopes and why

Request the **Community Management API** product. Approval grants a bundle of scopes to the app. In the OAuth (Open Authorization) consent call, ask only for the three scopes below. Marketing permissions are three-legged. A member must sign in. Client-credentials access is not available.

**Paste:**

We need three scopes, and we will request only these three in the member consent screen.

w_organization_social. This scope posts, comments, and likes as the organization. We use it to publish CleantechHUB jobs, programs, and newsletters as the Page. The signed-in member must be an ADMINISTRATOR, a DIRECT_SPONSORED_CONTENT_POSTER, or a CONTENT_ADMIN. Source: Posts API.

r_organization_social. This scope reads the organization’s posts, comments, and likes. We use it to read our own Page’s posts and comments. The same Page roles apply. Source: Posts API.

rw_organization_admin. This scope manages organization pages and retrieves reporting data. We use it for aggregate post analytics, follower statistics, and page statistics. The signed-in member must be an ADMINISTRATOR. Sources: Organization Share Statistics, Organization Follower Statistics, Organization Page Statistics, and Organization Lookup. Total follower count uses networkSizes on the Organization Lookup page, under this same permission.

We do not need r_organization_followers for analytics. The docs describe that scope as follower data so an organization can mention followers in posts. We will not mention followers. We will not request that scope.

We do not need r_organization_admin. That scope is listed on the Advertising API and the Lead Sync API. It is not in the Community Management permission list. Page analytics on Community Management uses rw_organization_admin. We are not applying for the Advertising API.

The Community Management product also makes other scopes available on the app. We will not request them in OAuth, and we will not call them.

- `r_1st_connections_size`
- `r_basicprofile`
- `r_organization_social_feed`
- `w_member_social`
- `w_member_social_feed`
- `w_organization_social_feed`
- `r_member_profileAnalytics`
- `r_member_postAnalytics`

Member post analytics describes the member’s own posts, not the company Page. Personal-profile posting stays on the existing app, which already has `w_member_social`.

### 1.15 Expected volume

**Paste:**

This app calls the API for one LinkedIn Page only.

Expected organization posts per month: [GIDEON TO FILL].

Expected API calls per day, for publishing and for reading our own posts, comments, and aggregate analytics: [GIDEON TO FILL].

The plan stays inside the Development tier cap of 500 calls per app per 24 hours, and 100 calls per member per 24 hours.

We will not call BATCH_GET. Those calls are not allowed on the Development tier.

We will not use social-action webhooks. Push notifications are disabled on the Development tier.

**Example only. Paste these numbers only if they are true.** Thirty posts in a month, and fewer than 50 calls in a day, fits this use. That covers a jobs board, program news, a newsletter, and a daily analytics read. That example is not a measured CleantechHUB volume.

### 1.16 Use-case choices, if the form lists them

**Paste:**

Page Management: yes. We publish as our Page and read our Page’s posts and comments.

Page Analytics: yes. We read aggregate performance of our Page’s posts, plus follower and page statistics.

Brand engagement and mention monitoring: no.

Executive management and posting as a personal profile: no, not on this app.

Employee advocacy: no.

Advertising, Lead Sync, Matched Audiences, and Conversions: no.

### 1.17 Fields that appear later, at Standard tier

Do not send these with the first Development request. They are required only when you upgrade.

**Company and product overview:** use section 1.11.

**Use case:** use section 1.10.

**Test credentials:** `[GIDEON TO FILL]`. Give the reviewer a way to sign in to the n8n workflow, or a recorded path that does not need a shared password. Do not put a live password in email.

**Screencast:** a high-resolution, downloadable recording of this app only. Close other windows. Narration helps. For Page Management, show the full OAuth consent. Show a post to the Page. Show a member comment in the app. Show which personal fields from that commenter are visible. For Page Analytics, show OAuth if the earlier clip did not. Show post performance, such as reaction counts. If a test case does not exist in the app, say so in the recording. State that member profile fields are not kept. State that no LinkedIn feed is shown on the website.

## 2. Prerequisites

1. **A registered legal organization, for a commercial use case.** Community Management is not open to personal projects. Paste FUNDACIÓN CLEANTECH HUB, a non-profit (ESAL) under the régimen tributario especial, NIT 901.523.941-9. Gideon confirmed that name on 22 October 2026. Do not add a simplified-stock-company suffix.
2. **A business email on the organization domain.** Personal mail fails vetting. Use section 1.5.
3. **Verify the app with the CleantechHUB Page super admin before you submit.** The Page’s organization must be the same organization as the legal entity.
4. **A separate app, because this one already has other products.** The supplied scopes `email`, `openid`, and `profile` are Sign In with LinkedIn using OpenID Connect. `w_member_social` is Share on LinkedIn, which posts as a member. Partner Support says Community Management must be the only product on the app, for legal and security reasons. Share is one of the examples that grays out the button. Create a new app with no other product. Keep it. n8n will use that new Client ID for the Page.
5. **Do not discard the new app.** The “discard the new app” line in the docs belongs to a different path. That path starts with an app that already has the Advertising API. Community Management is vetted on a clean app. Standard access is then added back onto the Advertising app. CleantechHUB is not requesting the Advertising API. The new app is the Page app.
6. **A public privacy-policy URL.** Not live. See the stop notice. Do not submit while the only responses are a WordPress 404, the jobs homepage, or an empty agents response.
7. **The signed-in member is an ADMINISTRATOR of the Page** if you want analytics. A content-admin token can post. It cannot call the reporting endpoints that require `rw_organization_admin`.
8. **Read these before you submit.**
   - [LinkedIn Marketing API terms](https://www.linkedin.com/legal/l/marketing-api-terms)
   - [LinkedIn API Terms of Use](https://www.linkedin.com/legal/l/api-terms-of-use)
   - [Restricted use cases](https://learn.microsoft.com/en-us/linkedin/marketing/restricted-use-cases?view=li-lms-2026-09)
   - [Data storage requirements](https://learn.microsoft.com/en-us/linkedin/marketing/data-storage-requirements?view=li-lms-2026-09)
   - [Community Management app review](https://learn.microsoft.com/en-us/linkedin/marketing/community-management-app-review?view=li-lms-2026-09)
9. **When you later build the calls, do not pin Marketing version 202511.** That version sunsets on 16 November 2026. Use a supported version from the [migrations documentation](https://learn.microsoft.com/en-us/linkedin/marketing/integrations/recent-changes?view=li-lms-2026-09). This request does not need the version header.

## 3. Steps on developer.linkedin.com

Do these on Gideon’s own device. Nobody else signs in.

1. Publish the cleantechhub.net privacy page, and confirm it loads in a private window. Stop here if it does not.
2. Read the five documents in prerequisite 8.
3. Open https://www.linkedin.com/developers/apps and sign in with Gideon’s own LinkedIn account. Source for the portal path: [LinkedIn API Partner Support](https://learn.microsoft.com/en-us/linkedin/shared/linkedin-api-partner-support-guide), section “Request API access”.
4. Click **My Apps**. Open **n8n-li CleantechHUB** only to look. If Community Management shows as grayed out, leave this app unchanged. It can keep personal-profile posting.
5. Click **Create App**. Name it **CleantechHUB n8n**. Select the CleantechHUB LinkedIn Page as the publisher. Enter the new privacy-policy URL. Add no other product. Source: Partner Support, “Create App”, and [Community Management overview](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/community-management-overview?view=li-lms-2026-09), FAQ on the grayed-out request.
6. Open the new app. Click the **Settings** tab. Click **Verify**. In the Verify company dialog, click **Generate URL**. Click **Copy URL**. Send that URL to the Page super admin by email or LinkedIn message. Click **I’m done**. Source: [Send an app verification request](https://www.linkedin.com/help/linkedin/answer/a1665329).
7. The super admin opens the URL within 30 days, signs in, and approves. The screen shows the Page, the app, and the requestor’s name. Approval cannot be undone. A denied or expired link means you generate a new URL. Source: [Approve or deny an app verification request](https://www.linkedin.com/help/linkedin/answer/a1669245). The Page association is permanent and cannot move to another Page. Source: [Associate an app with a LinkedIn Page](https://www.linkedin.com/help/linkedin/answer/a548360).
8. Return to **Settings** and confirm the Page shows as verified. The docs require this before the access form is reviewed. Source: [Community Management app review](https://learn.microsoft.com/en-us/linkedin/marketing/community-management-app-review?view=li-lms-2026-09).
9. Click the **Products** tab. Under **Additional available products**, choose **Request access** for the **Community Management API**. Source: [Migration guide, How to Apply](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/community-management-api-migration-guide?view=li-lms-2026-09).
10. Complete the survey within 21 days of the day it appears. Paste section 1. Use the business email. Check spam, junk, social, and promotions for the verification message. Source: [Partner Support, vetting survey](https://learn.microsoft.com/en-us/linkedin/shared/linkedin-api-partner-support-guide).
11. Submit the form. Write down the new app’s Client ID. That id is the one n8n will use. `[GIDEON TO FILL]` it into the n8n credential after approval. Do not put the client secret in this document, in git, or in email.
12. Watch status under **Review in progress**. The published messages are **Access Form Review**, then **Identity Vetting**. **App Review** is the screencast stage. Source: [Developer application review status definitions](https://www.linkedin.com/help/linkedin/answer/a1449586).
13. If LinkedIn writes to the business email, answer within 21 days. Silence marks the request **Insufficient Details**.
14. After Development approval, build and test within 12 months. Then apply for Standard tier under **My Apps**, then **Products**, and attach the screencast from section 1.17. If you do not reach Standard tier within 12 months, LinkedIn removes the access for inactivity. Source: [Marketing API FAQ](https://learn.microsoft.com/en-us/linkedin/marketing/lms-faq?view=li-lms-2026-09) and [Increasing access](https://learn.microsoft.com/en-us/linkedin/marketing/increasing-access?view=li-lms-2026-09).

## 4. Expected review time

LinkedIn does not publish a number of days for a Community Management decision.

The Marketing API terms say LinkedIn will make reasonable efforts to respond, and that LinkedIn is not committing to any timeframe. Source: [Marketing API terms](https://www.linkedin.com/legal/l/marketing-api-terms), in the vetting paragraph.

Partner Support says the review team works through requests in a timely manner. Extra questions, sent to the business email, can add delay. Source: [Partner Support](https://learn.microsoft.com/en-us/linkedin/shared/linkedin-api-partner-support-guide).

Clocks that do have numbers:

- Finish the survey within **21 days**, or the request can be closed as incomplete.
- Answer a request for more documents within **21 days**, or the status becomes **Insufficient Details**, and **Reapply** appears on the same app.
- The Page super admin has **30 days** to open the verification URL.
- Build the integration and apply for Standard tier within **12 months** of Development access, or the access is removed.
- On the Development tier, the call caps are **500** per app per 24 hours and **100** per member per 24 hours. `BATCH_GET` is not allowed. Social-action webhooks are off.

The partner-support page also says an Advertising API Standard-tier ticket can take up to 30 business days. That sentence is about the Advertising API. It is not the Community Management clock.

## 5. Common rejection reasons

The list below is the published rejection table. Source: [Developer application review status definitions](https://www.linkedin.com/help/linkedin/answer/a1449586).

| Rejection message | What it means here |
| --- | --- |
| Incomplete Access Request Form | A required answer was thin or blank. Paste section 1 in full, and replace every `[GIDEON TO FILL]` that the live form requires. |
| Unapproved Use Case | Social feeds, ads, sales, recruiting, lead lists, and member scraping are refused. This request stays on Page Management and Page Analytics for CleantechHUB’s own Page. |
| Fail Email Verification | A personal mailbox, or a business mailbox nobody opened. Use section 1.5 and check spam. |
| Fail Organization Verification | The legal name or address does not match a registered, active entity. Paste section 1.3 and section 1.4. |
| Invalid Company Website | The website or domain could not be verified. Use https://cleantechhub.net. |
| Invalid Company Page | The Page on the app belongs to a different organization. Verify the CleantechHUB Page only. |
| Organization doesn’t meet our access requirements | LinkedIn could not verify that the organization qualifies. Community Management is for registered legal organizations in commercial use. |
| Invalid Privacy Policy | The current blocker. There is no cleantechhub.net privacy URL today. |
| Invalid Screencast | Standard tier only. Follow section 1.17. |
| Invalid App Name | The name includes a portion of LinkedIn or Microsoft. Name the new app CleantechHUB n8n. |
| Not in Compliance with Data Restrictions | Storage or use breaks the terms. Follow section 1.13. |

A refused Development-tier application cannot request Development access again on that same app. You create a new app and start over. Source: [Community Management app review](https://learn.microsoft.com/en-us/linkedin/marketing/community-management-app-review?view=li-lms-2026-09).

**Insufficient Details** is a different outcome. It is for a survey that was never submitted, or for a follow-up that got no reply within 21 days. In that case, **Reapply** is offered on the same app. Source: [Partner Support](https://learn.microsoft.com/en-us/linkedin/shared/linkedin-api-partner-support-guide).

## 6. Sources checked

All of these were public pages, read on 22 October 2026.

- [Community Management overview](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/community-management-overview?view=li-lms-2026-09)
- [Community Management app review](https://learn.microsoft.com/en-us/linkedin/marketing/community-management-app-review?view=li-lms-2026-09)
- [Migration guide](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/community-management-api-migration-guide?view=li-lms-2026-09)
- [Increasing access](https://learn.microsoft.com/en-us/linkedin/marketing/increasing-access?view=li-lms-2026-09)
- [Posts API](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api?view=li-lms-2026-09)
- [Organization Share Statistics](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/organizations/share-statistics?view=li-lms-2026-09)
- [Organization Follower Statistics](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/organizations/follower-statistics?view=li-lms-2026-09)
- [Organization Page Statistics](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/organizations/page-statistics?view=li-lms-2026-09)
- [Organization Lookup](https://learn.microsoft.com/en-us/linkedin/marketing/community-management/organizations/organization-lookup-api?view=li-lms-2026-09)
- [Restricted use cases](https://learn.microsoft.com/en-us/linkedin/marketing/restricted-use-cases?view=li-lms-2026-09)
- [Data storage requirements](https://learn.microsoft.com/en-us/linkedin/marketing/data-storage-requirements?view=li-lms-2026-09)
- [Marketing API FAQ](https://learn.microsoft.com/en-us/linkedin/marketing/lms-faq?view=li-lms-2026-09)
- [LinkedIn API Partner Support](https://learn.microsoft.com/en-us/linkedin/shared/linkedin-api-partner-support-guide)
- [Marketing API terms](https://www.linkedin.com/legal/l/marketing-api-terms)
- [API Terms of Use](https://www.linkedin.com/legal/l/api-terms-of-use)
- [Review status definitions](https://www.linkedin.com/help/linkedin/answer/a1449586)
- [Send an app verification request](https://www.linkedin.com/help/linkedin/answer/a1665329)
- [Approve or deny verification](https://www.linkedin.com/help/linkedin/answer/a1669245)
- [Associate an app with a Page](https://www.linkedin.com/help/linkedin/answer/a548360)
- [cleantechhub.net](https://cleantechhub.net/), [About](https://cleantechhub.net/about/), [Governance](https://cleantechhub.net/governance/), and the data-policy PDF linked there

## 7. Still only Gideon knows

These stay as `[GIDEON TO FILL]`. They are not on the public site, and they were not in the approval of 22 October 2026.

- LinkedIn Page URL.
- LinkedIn organization id.
- Page super admin who will open the verification URL.
- LinkedIn member who will sign in and grant the token, if that person is not the super admin. The legal-representative title does not prove the Page role.
- Posts per month, and API calls per day.
- The new app’s Client ID, after he creates **CleantechHUB n8n**.
- Standard-tier test credentials, later. Do not put a live password in this file.

Already filled, so no longer blank: legal name FUNDACIÓN CLEANTECH HUB (ESAL), NIT 901.523.941-9, Calle 90 No. 19-41 Of. 801, Bogotá D.C., admin@cleantechhub.net, +57 313 715 5965, and website https://cleantechhub.net. n8n host country is Germany, on OVH. The privacy URL is not filled, because no page is live.

Open item, not fixed: the `/diagnostico` checkbox still loads checked. That change needs WordPress admin.

## 8. Final submit steps

Do these on Gideon’s own device. Do not submit until the privacy URL returns 200 without a login and the body is this policy.

1. Publish the approved HTML on an existing host (`jobs.cleantechhub.net` or `agents.cleantechhub.net`) at `/privacidad/`, with `/privacy` redirecting there. That publish did not happen from this run. It needs an Infisical secret that can write to the Caddy host `51.195.45.77`. Set the effective date on the day it actually goes live.
2. Open the live URL in a private window. Confirm HTTP 200, valid TLS, and no login wall.
3. Open https://www.linkedin.com/developers/apps and sign in with Gideon’s own LinkedIn account.
4. Create the app **CleantechHUB n8n**. Select the CleantechHUB Page. Paste the live privacy URL. Add no other product.
5. Settings → Verify → Generate URL → send it to the Page super admin. The super admin approves within 30 days.
6. Products → Request access for the Community Management API. Paste section 1. Use admin@cleantechhub.net. Fill only the blanks in section 7.
7. Finish the survey within 21 days. Watch Access Form Review, then Identity Vetting.
8. After Development approval, build within 12 months, then apply for Standard tier with the screencast in section 1.17.

The numbered portal detail, with the doc links, is section 3.
