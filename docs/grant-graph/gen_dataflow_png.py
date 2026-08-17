"""Generate grant-dataflow.png — CTH Grant Data Flow (TNS VerdeXcelerate example)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

# ── palette ──────────────────────────────────────────────────────────────────
C_BG        = "#F8F9FA"
C_DARK      = "#1B4332"
C_GREEN     = "#2D6A4F"
C_MID       = "#40916C"
C_LIME      = "#95D5B2"
C_PALE      = "#D8F3DC"
C_CODED     = "#B7E4C7"
C_ABSENT    = "#FDECEA"
C_WARN      = "#B5450B"
C_ARROW     = "#40916C"
C_STAGE_TXT = "#FFFFFF"
C_NOTE      = "#555555"
C_LIVE      = "#52B788"

fig, ax = plt.subplots(figsize=(22, 16))
ax.set_xlim(0, 22)
ax.set_ylim(0, 16)
ax.axis("off")
fig.patch.set_facecolor(C_BG)
ax.set_facecolor(C_BG)

# ── helpers ───────────────────────────────────────────────────────────────────
def box(ax, x, y, w, h, label, sublabel="", bg=C_MID, tc=C_STAGE_TXT,
        edge=C_DARK, lw=1.2, fontsize=8.2, subfontsize=6.5, bold=True):
    r = FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.1",
                       linewidth=lw, edgecolor=edge, facecolor=bg, zorder=3)
    ax.add_patch(r)
    yc = y + h/2 + (0.13 if sublabel else 0)
    ax.text(x + w/2, yc, label, ha="center", va="center",
            fontsize=fontsize, color=tc,
            fontweight="bold" if bold else "normal", zorder=4)
    if sublabel:
        ax.text(x + w/2, y + h/2 - 0.22, sublabel, ha="center",
                va="center", fontsize=subfontsize, color=tc,
                alpha=0.88, zorder=4, linespacing=1.35)

def arrow_h(ax, x1, x2, y, color=C_ARROW, lw=1.6, label=""):
    ax.annotate("", xy=(x2, y), xytext=(x1, y),
                arrowprops=dict(arrowstyle="-|>", color=color,
                                lw=lw, mutation_scale=14), zorder=5)
    if label:
        ax.text((x1+x2)/2, y + 0.14, label, ha="center",
                fontsize=6.2, color=color, zorder=6)

def arrow_v(ax, x, y1, y2, color=C_ARROW, lw=1.2, label="", ls="-"):
    ax.annotate("", xy=(x, y2), xytext=(x, y1),
                arrowprops=dict(arrowstyle="-|>", color=color,
                                lw=lw, mutation_scale=11,
                                linestyle=ls), zorder=5)
    if label:
        ax.text(x + 0.1, (y1+y2)/2, label, fontsize=6.0,
                color=color, va="center", zorder=6)

def tag(ax, x, y, text, color=C_GREEN, bg="white", fontsize=6.2):
    ax.text(x, y, text, fontsize=fontsize, color=color, ha="center",
            va="center", zorder=6,
            bbox=dict(boxstyle="round,pad=0.18", facecolor=bg,
                      edgecolor=color, linewidth=0.8))

def note(ax, x, y, text, color=C_NOTE, fontsize=6.0, ha="left"):
    ax.text(x, y, text, fontsize=fontsize, color=color,
            ha=ha, va="center", zorder=4, style="italic",
            linespacing=1.4)

# ── stage column headers ──────────────────────────────────────────────────────
stages = [
    (0.3,  4.2, "1  INPUT",          "raw notes / docs"),
    (5.8,  4.2, "2  ORGANIZE",       "graph layer"),
    (11.2, 4.2, "3  RETRIEVE /\nANALYZE", "CTH memory"),
    (16.8, 4.2, "4  OUTPUT",         "Hands → Drive Lane B"),
]
for x, w, title, sub in stages:
    box(ax, x, 13.5, w, 0.88, title, sub, bg=C_DARK, tc=C_LIME,
        fontsize=10, subfontsize=7.5)

# ── spine marker ─────────────────────────────────────────────────────────────
ax.text(11.0, 15.60,
        "Spine N1–N9 unchanged  ·  Data flow maps onto existing stages (ingest-before-N4)  ·  No new N-nodes",
        ha="center", fontsize=8, color=C_DARK, fontweight="bold",
        bbox=dict(facecolor=C_PALE, edgecolor=C_MID, linewidth=0.8,
                  boxstyle="round,pad=0.22"))

# ── STAGE 1 — INPUT ───────────────────────────────────────────────────────────
s1_x = 0.35
box(ax, s1_x, 11.2, 4.0, 0.80, "JP Diaz notes /\njoint-work points",
    "raw text, bullets,\nverbal commitments", bg=C_MID, tc="white", fontsize=7.5)
box(ax, s1_x, 9.9, 4.0, 0.80, "Gmail Call  (N1)",
    "RFP email · deadline\nfunder contact", bg=C_MID, tc="white", fontsize=7.5)
box(ax, s1_x, 8.6, 4.0, 0.80, "Supporting docs\nalready in Drive",
    "partner CVs · budgets\nprior CTH work", bg=C_MID, tc="white", fontsize=7.5)

# Drive landing box
box(ax, s1_x, 6.8, 4.0, 1.30,
    "TNS grant Drive folder",
    "https://drive.google.com/…/1saTASGx9VPyG7auRjNu5SkzAP3e34vEA\nHands writes  ·  Desks do not write Drive",
    bg=C_GREEN, tc="white", fontsize=7.8, subfontsize=5.8)

# arrows into Drive folder
for y in [11.60, 10.30, 9.00]:
    arrow_v(ax, s1_x + 2.0, y, 8.10, color=C_ARROW)
tag(ax, s1_x + 2.0, 7.80, "bc-id required", color=C_WARN, bg="#FFF3EE")

# ── inter-stage arrows ────────────────────────────────────────────────────────
arrow_h(ax, 4.35, 5.80, 9.60, label="raw docs")
arrow_h(ax, 4.35, 5.80, 7.45, label="Drive read")

# ── STAGE 2 — ORGANIZE ───────────────────────────────────────────────────────
s2_x = 5.85
box(ax, s2_x, 11.0, 4.2, 0.95,
    "FalkorDB + Graphiti",
    "fact store: funder · requirement · deliverable\npartner · deadline · budget-line",
    bg=C_CODED, tc=C_DARK, fontsize=7.5, subfontsize=6.0)
tag(ax, s2_x + 2.1, 10.75, "EMPTY — 0 nodes today", color=C_WARN, bg="#FFF3EE")
note(ax, s2_x + 0.15, 10.45,
     "Graphiti temporal layer tracks when facts stated / updated.\nPath drawn. Do not claim live grant facts.")

box(ax, s2_x, 8.90, 4.2, 0.80,
    "Neo4j",
    "Graphify can emit Cypher · no container",
    bg=C_ABSENT, tc=C_WARN, fontsize=7.5, subfontsize=6.2,
    edge=C_WARN, lw=1.5)
tag(ax, s2_x + 2.1, 8.65, "ABSENT — Falkor is graph DB", color=C_WARN, bg="#FFF3EE")

box(ax, s2_x, 7.10, 4.2, 1.30,
    "Hands organize ticket",
    "lane: haiku / flash\ninput = raw Drive docs\noutput = Falkor write + bc-id",
    bg=C_GREEN, tc="white", fontsize=7.5, subfontsize=6.2)

arrow_v(ax, s2_x + 2.1, 11.95, 11.0, color=C_ARROW)
arrow_v(ax, s2_x + 2.1, 9.70, 8.90, color="#ccc", lw=0.9, ls="--")  # neo4j (greyed)
arrow_v(ax, s2_x + 2.1, 8.40, 8.40, color=C_ARROW)

arrow_h(ax, 10.05, 11.20, 9.50, label="structured facts")
arrow_h(ax, 10.05, 11.20, 7.75, label="organize ticket")

# ── STAGE 3 — RETRIEVE / ANALYZE ─────────────────────────────────────────────
s3_x = 11.25
row_ys = [11.80, 10.70, 9.60, 8.50, 7.40]
sources = [
    ("Nexus / idea-browser\n(Chroma RAG)",
     "startup matches for the call",
     C_LIVE, "white", "live analog"),
    ("Drive / Archive\n(prior CTH packs)",
     "UNDP · P4G/MubOn · other proposals",
     C_LIVE, "white", "live"),
    ("Cognee\n(Sustenttia analog)",
     "9-dataset pattern — NOT grant SoT",
     C_CODED, C_DARK, "live analog"),
    ("R2R",
     "retrieval — crash-loop",
     C_ABSENT, C_WARN, "ABSENT"),
    ("FalkorDB query\n(Stage 2 output)",
     "structured grant facts — EMPTY today",
     C_CODED, C_DARK, "EMPTY"),
]
for (y, (lbl, sub, bg, tc, status)) in zip(row_ys, sources):
    box(ax, s3_x, y - 0.42, 4.6, 0.82, lbl, sub,
        bg=bg, tc=tc, fontsize=7.2, subfontsize=5.8)
    color = C_WARN if status in ("ABSENT", "EMPTY") else C_MID
    tag(ax, s3_x + 4.88, y + 0.00, status,
        color=color, bg="#FFF3EE" if color == C_WARN else C_PALE,
        fontsize=5.8)

# analysis note
box(ax, s3_x, 6.20, 4.6, 0.95,
    "Isolated analysis ticket  (Grants Desk reviews)",
    "maker ≠ checker  ·  feeds N3/N4 context\nnot a new Gideon stage",
    bg=C_DARK, tc=C_LIME, fontsize=7.2, subfontsize=6.0)

arrow_v(ax, s3_x + 2.3, 7.98, 7.15, color=C_ARROW)

arrow_h(ax, 15.85, 16.80, 8.50, label="analysis + context")

# ── STAGE 4 — OUTPUT ─────────────────────────────────────────────────────────
s4_x = 16.85
outputs = [
    (11.50, "Draft narrative  (N3 / N4)",  ".docx  unformatted"),
    (10.30, "Structured proposal  (N4)",   "donor template  .docx"),
    (9.10,  "Budget  (N5)",                ".xlsx"),
    (7.90,  "Annexes / CVs  (N6)",         "various formats"),
]
for y, lbl, sub in outputs:
    box(ax, s4_x, y - 0.38, 4.85, 0.75, lbl, sub,
        bg=C_MID, tc="white", fontsize=7.2, subfontsize=6.0)

# Drive output landing
box(ax, s4_x, 6.20, 4.85, 1.20,
    "Hands writes → TNS Drive folder",
    "Always include Drive URL in bc-id report\nVerify (N7) reads Drive only  ·  HITL (N8) before send",
    bg=C_GREEN, tc="white", fontsize=7.5, subfontsize=6.0)

for y in [11.12, 9.92, 8.72, 7.52]:
    arrow_v(ax, s4_x + 2.42, y, 7.40, color=C_ARROW)

tag(ax, s4_x + 2.42, 7.10, "bc-id + Drive URL required", color=C_WARN, bg="#FFF3EE")

# HITL / N8 flag
ax.text(s4_x + 2.42, 5.80,
        "▲  HITL — N8 — nothing sent to TechnoServe\n    without Gideon's yes in the owning chat",
        ha="center", fontsize=7.0, color=C_WARN, fontweight="bold",
        bbox=dict(facecolor="#FFF3EE", edgecolor=C_WARN,
                  linewidth=1.0, boxstyle="round,pad=0.22"), zorder=6)

# ── spine reference bar ───────────────────────────────────────────────────────
spine_nodes = ["N1 Call", "N2 RFP", "N3 SOI", "N4 Full\nProposal",
               "N5 Budget", "N6 Support\nDocs", "N7 Verify", "N8 HITL"]
xs = [1.35, 3.35, 5.45, 7.55, 9.65, 11.55, 14.45, 18.0]
for x, lbl in zip(xs, spine_nodes):
    box(ax, x - 0.85, 4.50, 1.70, 0.65, lbl,
        bg=C_DARK, tc=C_LIME, fontsize=6.5, lw=1.0)
for i in range(len(xs) - 1):
    ax.annotate("", xy=(xs[i+1] - 0.85, 4.825),
                xytext=(xs[i] + 0.85, 4.825),
                arrowprops=dict(arrowstyle="-|>", color=C_LIME,
                                lw=1.0, mutation_scale=9), zorder=5)
ax.text(11.0, 4.20, "Spine N1–N9 (reference — unchanged)",
        ha="center", fontsize=7, color=C_DARK, style="italic")

# ── legend ────────────────────────────────────────────────────────────────────
legend_items = [
    mpatches.Patch(color=C_LIVE,   label="live / live analog"),
    mpatches.Patch(color=C_CODED,  label="coded-analog"),
    mpatches.Patch(color=C_ABSENT, label="absent / crash-loop"),
    mpatches.Patch(color=C_GREEN,  label="Hands action (Drive write / ticket)"),
    mpatches.Patch(color=C_DARK,   label="Spine / gate"),
]
ax.legend(handles=legend_items, loc="lower left", fontsize=7,
          framealpha=0.92, edgecolor=C_MID, bbox_to_anchor=(0.01, 0.01))

# ── title ─────────────────────────────────────────────────────────────────────
ax.text(11.0, 15.28,
        "CTH Grant Data Flow — TNS VerdeXcelerate (CANOA) example",
        ha="center", fontsize=13, fontweight="bold", color=C_DARK)
ax.text(11.0, 14.95,
        "2026-08-17  ·  Falkor EMPTY today — path drawn, no live grant facts  ·"
        "  analog ≠ live  ·  Hands writes Drive (bc-id required)",
        ha="center", fontsize=7.5, color="#555")

plt.tight_layout(pad=0.3)
plt.savefig("/workspace/docs/grant-graph/grant-dataflow.png",
            dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print("saved grant-dataflow.png")
