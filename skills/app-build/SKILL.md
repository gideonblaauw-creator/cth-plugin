---
name: app-build
description: >
  Blaauw app-build protocol — rulebook for building, promoting, or putting a
  live tree on GitHub. Trigger on "app-build", "promote to GitHub", "create a
  repo", "new repo", "build an app", "Infrastructure classifies", or any request
  to create or push a service, app, or pipeline to GitHub. Cloud Hands must read
  this before opening a branch, creating a repo, or promoting a VPS/Archive tree.
metadata:
  version: "1.0.0"
  category: operations
  owner: Infrastructure
  adopted: "2026-08-16"
---

# App-build protocol

**Owner:** Infrastructure
**Date:** 2026-08-16
**SSOT:** GitHub. Mac is never SoT. Archive is notes + working copy.

This is the rulebook for building or promoting an app. Orchestrator routes. Desks ticket. Infrastructure classifies. Gideon locks. Cloud Hands writes on a GitHub branch. Gideon merges and deploys.

Do not grind apps. Do not create a GitHub repo until Gideon marks the row.

## 1. When this applies

Use this when Gideon or a Desk wants to build, promote, or put on GitHub a live tree (VPS /opt, Archive, or Mac leftover).

Do not use this for notes, one-off HTML, or a tree Hands will never touch again.

## 2. Classify (three buckets)

A new private GitHub repo is allowed only if all three are true:

1. Hands will write it again (not a one-shot dump).
2. It can run or deploy (service, app, pipeline, not a notes folder).
3. More than one desk will touch it.

Otherwise: Archive (/opt/claude-files / /mnt/data/claude-files).

If a GitHub repo already exists: existing repo. Do not open a second one. Uncommitted VPS work (example: Sustenttia v5 dirty tree on sustenttia-v2) is a commit/PR on the existing repo, not a new repo.

Mac copies are never a reason to create a repo. No cloud VM for Mac-only trees. No Air commit as SoT.

Grant application outputs that live in Google Drive are Archive/Tool work. Drive is a Tool (Composio / GDrive connector). Do not open a GitHub repo for a donor pack unless Gideon marks a repo row. A Desk that needs a donor pack on Drive does not launch Hands.

## 3. Path

1. Desk or Orchestrator writes a Ticket.
2. Infrastructure classifies: Archive / existing repo / new repo.
3. Gideon locks the classify. No Hands until that yes.
4. Cloud Hands opens a branch (existing repo) or, only if Gideon marked new-repo, creates the empty private repo then a branch.
5. Desk reviews.
6. Gideon merges.
7. Gideon deploys. Hands does not deploy.

Nothing sent, posted, paid, merged, published, or deployed without Gideon in the owning chat.

## 4. Ticket fields

```
desk:
folder:
done-when:
lane: sonnet | haiku | flash | opencode
hitl: no merge, no publish, no deploy, no new repo unless Gideon marked the row
reviewer:
context:
```

No files only in chat. The ticket and the output live in the repo or Archive.

## 5. Hands rules

- GitHub is SSOT. Change via PR.
- No secrets in the repo (.env, PATs, credentials.txt).
- No Grok Bot UUIDs.
- Do not clone Archive onto a cloud VM.
- Do not treat the Mac as SoT.
- Archive writes stay BLOCKED until a Cursor worker exists on the VPS.
- Sustenttia trees stay Sustenttia. Bravo Bridge / AIC stay isolated. Do not mix CTH lime into Sustenttia.
- Do not create repos until Gideon marks the row.
- Desks ticket Hands. They do not first-draft or write files.
