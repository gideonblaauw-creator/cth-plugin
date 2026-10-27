# Jobs privacy page — deploy note

Published 22 October 2026 from the OVH VPS. The live page is https://jobs.cleantechhub.net/privacidad/.

Checked the same day, without a login: that URL returns HTTP 200, and the body is the CleantechHUB privacy policy. The effective date on the page is 22 de octubre de 2026 / 22 October 2026. `https://jobs.cleantechhub.net/privacy` and `https://jobs.cleantechhub.net/privacy/` redirect to it. TLS is valid. There is no login wall.

## Where it lives

- Page file: `/opt/cth-jobs-board/privacidad/index.html`
- Redirect: `/etc/caddy/Caddyfile.d/jobs.cleantechhub.net.caddy`
- Host: `jobs.cleantechhub.net` on `51.195.45.77` (Caddy). The organization website stays `https://cleantechhub.net`.

The repo copy is `artifacts/cleantechhub-privacy-policy.html`.

## Warning

A jobs-board `rsync --delete` would remove `/opt/cth-jobs-board/privacidad/index.html`, because that file was added on the server and is not yet part of the jobs build output.

Add `privacidad/index.html` to the jobs build source before the next deploy that syncs the board with `--delete`. Keep the Caddy redirect in `jobs.cleantechhub.net.caddy`.

The `/diagnostico` checkbox on cleantechhub.net is a separate open item. This deploy did not change it.
