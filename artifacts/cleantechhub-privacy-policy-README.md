# Privacy policy — repo notes

**Awaiting Gideon's approval** before this page is published on cleantechhub.net. Nothing in this folder is deployed.

The public text is `artifacts/cleantechhub-privacy-policy.md` and `artifacts/cleantechhub-privacy-policy.html`. It starts at “Política de privacidad”. This README is not pasted onto the site.

## Token list

One set. The values below are already written into the public text. They stay here so a later edit can see what was filled.

| Token | Value in the public text |
| --- | --- |
| LEGAL_NAME | FUNDACIÓN CLEANTECH HUB, entidad sin ánimo de lucro (ESAL), régimen tributario especial. Do not add a simplified-stock-company suffix. |
| CONTACT_EMAIL | admin@cleantechhub.net |
| CONTACT_PHONE | +57 313 715 5965 |
| RESPONSIBLE_AREA | Representante Legal de la Fundación CleantechHUB |
| EFFECTIVE_DATE | `Vigente desde: 22 de octubre de 2026` / `Effective from: 22 October 2026`. This matches the live page. |
| ADS_TAG_KEEP | yes. Section 9 discloses Google Ads `AW-10974720045` as advertising measurement. Opt-out is Google Ads settings (https://adssettings.google.com) and the browser’s cookie controls. |
| N8N_HOST_COUNTRY | Germany. The website and the n8n workflow are both hosted by OVH in Germany. OVH’s data processing terms cover both. The page makes no SIC adequacy claim. |
| RNBD_NUMBER | Omitted from the public text. |
| RETENTION_APPLICATIONS | Six months after the hiring process closes, then deleted, unless the applicant authorizes a longer period. |
| RETENTION_ACCOUNTING_EMPLOYMENT | The periods required by commercial, tax, and labour law. No year count. |

Also fixed in sections 1 and 16, and not left as tokens:

- NIT 901.523.941-9.
- Address: Calle 90 No. 19-41 Of. 801, Bogotá D.C., Colombia.

Vigencia, in section 10 of both languages: the databases stay in force while the purpose lasts, plus the periods the law requires.

If `ADS_TAG_KEEP` is later set to no, delete the Google Ads paragraphs in section 9 of both languages. Leave Google Analytics.

## What the public text does not contain

- Placeholders other than `[fecha de publicación]` and `[publication date]`.
- A draft banner, or a note that the wording comes from an internal policy.
- The mailboxes `ofcumplimiento@solucionesjv.co` and `info@cleantechhub.net`.
- A database-registry number.
- Article numbers. Consultations stay at ten business days, with an extension of up to five, because that timeline is in the 2022 PDF. Complaint day counts are not stated. Law 1581 of 2012 and Decree 1377 of 2013 are named. Decree 886 of 2014 is not named in the public text.
- The sentence that the `/diagnostico` checkbox loads already checked. The live bug is `artifacts/diagnostico-consent-checkbox-ticket.md`. Land that ticket before publish, so the public line “the person checks a box” matches the form.

## How the site is built, and where it lives

Checked on 22 October 2026, without opening wp-admin or the server.

- WordPress. `https://cleantechhub.net/` sends `Link: <https://cleantechhub.net/wp-json/>`. The front page is page 347.
- `Server: Apache`.
- Theme Astra. The public stylesheet is version 4.14.0.
- Pages are built with Elementor. The Governance page uses the `page-builder` layout.
- Polylang. Spanish is the default language, at `https://cleantechhub.net/`. English is under `https://cleantechhub.net/en/`. The English front page is `/en/home-english/`.
- Rank Math SEO. The public API includes the redirections route.
- Also visible: GTranslate, WPForms Lite, ElementsKit, and Essential Addons.
- DNS name servers `ns10.ovh.ca` and `dns10.ovh.ca`. A record `51.195.42.49`.
- That address is in the RIPE block `VPS-DE2` (`51.195.40.0`–`51.195.43.255`). The block holder is OVH GmbH, in Germany.
- Nothing was published from this repo.

## Where to publish

WordPress is not the publish path. There is no WordPress admin access.

The live page is `https://jobs.cleantechhub.net/privacidad/`. `/privacy` redirects there. The VPS paths are in `artifacts/jobs-privacidad-deploy.md`. A jobs-board `rsync --delete` can remove the file unless the jobs build source includes it.

The WordPress steps below are kept only as a record of the earlier plan. Do not follow them.

Final URL, if WordPress were used: `https://cleantechhub.net/politica-de-privacidad/`.

`/privacy` and `/privacy/` should 301 to that URL.

On 22 October 2026 those routes returned 404. The page sitemap had no privacy page. The footer had no privacy link.

## Publish steps

Gideon, or whoever administers WordPress, publishes. This draft does not deploy itself.

1. On the day of publication, replace `[fecha de publicación]` and `[publication date]`. Confirm no other bracket is left.
2. Open `https://cleantechhub.net/wp-admin/` with your own account.
3. Go to Pages → Add New.
4. Title: `Política de privacidad`.
5. Slug: `politica-de-privacidad`. The site already uses slugs such as `/governance/`, so the URL is `https://cleantechhub.net/politica-de-privacidad/`.
6. In Polylang, set the language to Spanish. The page must not sit under `/en/`. English stays inside the same page, after the Spanish text.
7. Edit with Elementor. Add an HTML widget. Paste the whole `<main>` from `artifacts/cleantechhub-privacy-policy.html`, including the `<style>` inside it. Do not paste the header comment. The style is scoped to `.cth-privacy`.
8. If the new page opens in the block editor, use a Custom HTML block and paste the same `<main>`.
9. Publish. Open the URL in a private window. It must load without a login.
10. In Rank Math → Redirections, add a 301 from `/privacy` to `https://cleantechhub.net/politica-de-privacidad/`. Repeat the 301 for `/privacy/`.
11. Add the link in the footer. The footer is an Astra widget area. Today it shows contact details only.
12. GTranslate is installed. If it translates the whole site, exclude this page. Otherwise it can translate the English half again.
13. Land `artifacts/diagnostico-consent-checkbox-ticket.md` so the green-finance box loads unchecked.
14. When the URL returns 200, paste it into the LinkedIn access form. Until then that form field stays open.

## What was reused from the 2022 policy

Source: the PDF “Política y tratamiento de datos”, linked from `https://cleantechhub.net/governance/`. In force from 1 December 2022.

The public page keeps the NIT, the Bogotá address, the Law 1581 rights, the consultation timeline, the ban on selling databases, and the purposes for donors, beneficiaries, employees, and suppliers.

That PDF is an internal text. It is not hosted as a page on cleantechhub.net. This public page does not say that it replaces the PDF. Gideon decides that when he approves publication.

The PDF has no national database-registry number. That number stays out of the public text.

The PDF contact line was not clean, and its complaint mailbox is not the public channel. The public channel is admin@cleantechhub.net and +57 313 715 5965.

## Site facts the public text covers

- Footer form WPForms 104, title “Stay up to date”. The visible field is the email.
- On `/diagnostico`, a script can ask for an email for green-finance tips, at most one a week. It posts to `https://agents.cleantechhub.net/diagnostico/lead`. The checkbox bug is the separate ticket, not a sentence on the public page.
- The homepage loads Google Analytics `G-5Q0N5VB7KZ` and Google Ads `AW-10974720045`.
- Polylang sets the cookie `pll_language` for one year.
- No public jobs form was found in the page sitemap or the page search on 22 October 2026. The public text does not say that. It says applications arrive through the channel named on the job post.
