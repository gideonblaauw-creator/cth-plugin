# Ticket — /diagnostico consent box loads checked

```
desk: Infrastructure
folder: WordPress on cleantechhub.net (live site). This ticket file lives at artifacts/diagnostico-consent-checkbox-ticket.md in the cth-plugin repo. Do not treat the repo file as the site change.
cursor_project: CTH-Infrastructure
cursor_workspace: cth-plugin
done-when: On https://cleantechhub.net/diagnostico the green-finance checkbox loads unchecked, and contact_consent is sent only after the person checks it.
model: composer-2.5 (fast=true)
files: The WordPress custom HTML or JS that emits id="newsletter-consent" and LEAD_ENDPOINT. Likely Elementor custom code, a footer script, or an HTML widget. Do not edit WPForms form 104.
read-budget: That one snippet, plus this ticket. Do not crawl the VPS.
lane: github-pr
tier: 0
hitl: Do not edit the live site until Gideon approves. Nothing posted, and nothing deployed, by writing this file.
reviewer: Infrastructure Desk
context: Remove the checked attribute so authorization is the person’s own act. Exclusive write path is the WordPress snippet that contains newsletter-consent. Do not change the privacy-policy text in this repo as part of the fix.
```

## What is wrong

Checked on 22 October 2026, from the public homepage HTML, without wp-admin.

A site-wide script returns early unless the path is `/diagnostico`. On that path it injects a checkbox.

- Element id: `newsletter-consent`.
- The input is emitted with the `checked` attribute.
- Label: `Quiero recibir tips de financiamiento verde (max 1/semana)`.
- The script posts JSON to `https://agents.cleantechhub.net/diagnostico/lead`, including `contact_consent`.

The public privacy policy says the person checks that box. The live box currently loads checked, so the sentence is not true until this ticket lands.

## What to change

1. In wp-admin, find the custom HTML or JS that contains `newsletter-consent` and `LEAD_ENDPOINT`. Search Elementor custom code, the footer, and HTML widgets.
2. Remove the `checked` attribute from the input whose id is `newsletter-consent`.
3. Leave the label text as it is.
4. Leave the endpoint as it is.
5. Send `contact_consent` as true only when the box is checked at submit time.

## What not to change

WPForms form 104 is a different form. It is the footer widget “Stay up to date”. It has one email field and no checkbox. Do not add a checkbox there, and do not clear a default on that form.

Do not deploy this from the cth-plugin repo. The change is on the WordPress site.

## How to check

1. Open `https://cleantechhub.net/diagnostico` in a private window.
2. Confirm the green-finance box is empty.
3. Submit with the box empty and confirm the request does not claim consent.
4. Check the box, submit, and confirm `contact_consent` is true.
5. Open the homepage and confirm the footer form is still email only.
