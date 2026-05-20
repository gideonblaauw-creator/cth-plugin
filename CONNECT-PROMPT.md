# Connect this plugin to a Cowork session

Paste one of the prompts below into any new Cowork session to mount this folder
so Claude can read and edit the skills at source.

After mounting, Claude should read `CLAUDE.md` at the root for the editing rules.
Never edit the cached copy under `~/Library/Application Support/Claude/` — only this
source folder.

---

## Standard prompt

Connect my CleantechHUB plugin folder so you can read and edit the skills at source. Request access to this exact path:

`/Users/gideonblaauw/Documents/Claude/Projects/cth-plugin`

This is the source of truth for the `cleantechhub` plugin (16 skills under `skills/`). Once it's mounted, read `CLAUDE.md` at the root for the editing rules before changing anything. Don't edit the cached copy under `~/Library/Application Support/Claude/` — only the source folder above.

---

## Short version

Connect my folder `/Users/gideonblaauw/Documents/Claude/Projects/cth-plugin` — it's my cleantechhub plugin source. Read its CLAUDE.md before editing.
