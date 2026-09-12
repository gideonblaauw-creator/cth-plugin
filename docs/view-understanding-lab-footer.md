# View Understanding Lab — PR footer snippet (major Lane A)

Paste at the **end** of every **major** Lane A draft PR body. Replace placeholders before opening the PR.

Hands: plant Notion Understanding Lab beats first if missing (`Context → Explanation (quiz) → Playground → Shared decisions → Next cycle`). Infra: also post **View Understanding Lab** as a prominent chat link beside the cloud-agent card — do not rely on PR body alone.

**Playground (beat 3, hard):** scenarios + consequences + 2–4 option paths with tradeoffs; flow `scenario → consequences → options → choose` before Shared decisions — not scrub-only or single-suggestion override.

See `skills/notion/SKILL.md` § View Understanding Lab delivery and `skills/harness/SKILL.md` § View Understanding Lab — major Lane A.

---

```markdown
## View Understanding Lab
- **Context (Notion):** https://app.notion.com/p/3d5dfee50be98174a045febce0fc4b3d
- **Playground (stable HTML):** HITL_HTML_STABLE_URL
- **Playground (local fallback):** `http://127.0.0.1:8080/hitl/microworld/` or `/review/<job_id>` when Flask is up
- **Shared decisions:** https://app.notion.com/p/bb52cfa45b6744e59983528480fbab4b

**Gate:** Draft only. Infra reviews. Gideon merges after ≤10 min Understanding Lab pass (Explanation → Playground → Shared decisions).
```

**Stable host:** Replace `HITL_HTML_STABLE_URL` with the value Infra plants in harness after Vercel/Tailscale deploy. Do not invent a fake URL.

**Ticket field (optional):** `major: yes|no` — when omitted, infer from scope per harness major vs tiny table.
