# View HITL Lab — PR footer snippet (major Lane A)

Paste at the **end** of every **major** Lane A draft PR body. Replace placeholders before opening the PR.

Hands: plant Notion HITL Lab beats first if missing. Infra: also post **View HITL Lab** as a prominent chat link beside the cloud-agent card — do not rely on PR body alone.

See `skills/notion/SKILL.md` § View HITL Lab delivery and `skills/harness/SKILL.md` § View HITL Lab — major Lane A.

---

```markdown
## View HITL Lab
- **Notion lab Home:** https://app.notion.com/p/3d5dfee50be98174a045febce0fc4b3d
- **Interactive HTML (stable host):** HITL_HTML_STABLE_URL
- **Interactive HTML (local fallback):** `http://127.0.0.1:8080/hitl/microworld/` or `/review/<job_id>` when Flask is up
- **Decisions DB:** https://app.notion.com/p/bb52cfa45b6744e59983528480fbab4b

**Gate:** Draft only. Infra reviews. Gideon merges after ≤10 min HITL pass (Explainer → Microworld → Decisions).
```

**Stable host:** Replace `HITL_HTML_STABLE_URL` with the value Infra plants in harness after Vercel/Tailscale deploy. Do not invent a fake URL.

**Ticket field (optional):** `major: yes|no` — when omitted, infer from scope per harness major vs tiny table.
