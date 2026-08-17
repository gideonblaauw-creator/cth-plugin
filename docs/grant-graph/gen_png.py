"""Generate grant-graph.png — CTH Grant Graph with NEW BAND."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

fig, ax = plt.subplots(figsize=(20, 13))
ax.set_xlim(0, 20)
ax.set_ylim(0, 13)
ax.axis("off")
fig.patch.set_facecolor("#F8F9FA")

# ── colour palette ──────────────────────────────────────────────────────────
C_SPINE_BG   = "#2D6A4F"   # CTH Green — spine nodes
C_SPINE_TXT  = "#FFFFFF"
C_TOOL_BG    = "#1B4332"   # CTH Dark — tools
C_TOOL_TXT   = "#95D5B2"
C_REPO_BG    = "#40916C"   # mid green — repos
C_REPO_TXT   = "#FFFFFF"
C_BACK_LIVE  = "#52B788"   # live backend
C_BACK_CODED = "#95D5B2"   # coded-analog
C_BACK_ABS   = "#D8E8D8"   # absent
C_BACK_TXT   = "#1B4332"
C_BAND_BG    = "#EDF7F1"
C_ARROW      = "#40916C"
C_WARN       = "#B5450B"   # absent label colour

BAND_H = 2.6   # height of each horizontal band

def band_box(ax, y_bottom, label, color="#EDF7F1"):
    rect = FancyBboxPatch((0.15, y_bottom), 19.7, BAND_H - 0.15,
                          boxstyle="round,pad=0.05", linewidth=1,
                          edgecolor="#AECDBF", facecolor=color, zorder=0)
    ax.add_patch(rect)
    ax.text(0.38, y_bottom + BAND_H / 2, label,
            fontsize=9, color="#2D6A4F", fontweight="bold",
            va="center", rotation=90, zorder=1)

def node(ax, x, y, label, sub="", bg=C_SPINE_BG, tc=C_SPINE_TXT, w=1.75, h=0.80):
    rect = FancyBboxPatch((x - w/2, y - h/2), w, h,
                          boxstyle="round,pad=0.08", linewidth=1.2,
                          edgecolor="#1B4332", facecolor=bg, zorder=3)
    ax.add_patch(rect)
    ax.text(x, y + (0.12 if sub else 0), label,
            ha="center", va="center", fontsize=7.8, fontweight="bold",
            color=tc, zorder=4)
    if sub:
        ax.text(x, y - 0.18, sub,
                ha="center", va="center", fontsize=6.2,
                color=tc, alpha=0.85, zorder=4)

def arrow(ax, x1, x2, y, color=C_ARROW):
    ax.annotate("", xy=(x2 - 0.88, y), xytext=(x1 + 0.88, y),
                arrowprops=dict(arrowstyle="-|>", color=color,
                                lw=1.4, mutation_scale=12), zorder=5)

def connector(ax, x, y_from, y_to, label="", color=C_ARROW, ls="-"):
    ax.plot([x, x], [y_from, y_to], color=color, lw=1.2,
            linestyle=ls, zorder=2)
    if label:
        ax.text(x + 0.08, (y_from + y_to) / 2, label,
                fontsize=5.8, color=color, va="center", zorder=4)

# ── band backgrounds ─────────────────────────────────────────────────────────
band_box(ax,  9.9, "SPINE",    "#E6F4ED")
band_box(ax,  7.1, "TOOLS",    "#D4EDE2")
band_box(ax,  4.3, "REPOS",    "#EAF3EF")
band_box(ax,  1.2, "BACKENDS", "#F4F9F6")

# ── band labels (right margin) ───────────────────────────────────────────────
for txt, yc in [("N1–N9 unchanged", 11.25),
                ("NEW BAND  ▼", 8.50),
                ("NEW BAND  ▼", 5.70),
                ("NEW BAND  ▼", 2.65)]:
    ax.text(19.7, yc, txt, fontsize=7, color="#2D6A4F",
            ha="right", va="center", style="italic")

# ── SPINE nodes ──────────────────────────────────────────────────────────────
spine_y = 11.1
spine = [
    (1.35, "N1", "Call"),
    (3.2,  "N2", "RFP"),
    (5.05, "N3", "SOI"),
    (6.9,  "N4", "Full\nProposal"),
    (8.75, "N5", "Budget"),
    (10.6, "N6", "Supporting\nDocs"),
    (12.45,"N7", "Verify"),
    (14.3, "N8", "HITL"),
    (15.9, "N9", "Park"),
]
for x, nid, lbl in spine:
    node(ax, x, spine_y, f"{nid}  {lbl}", bg=C_SPINE_BG, tc=C_SPINE_TXT)

for i in range(len(spine) - 2):   # N1→N8 sequential; N9 branches off
    arrow(ax, spine[i][0], spine[i+1][0], spine_y)
# N8 → N9 (dashed — park branch)
ax.annotate("", xy=(spine[8][0] - 0.88, spine_y),
            xytext=(spine[7][0] + 0.88, spine_y),
            arrowprops=dict(arrowstyle="-|>", color="#888", lw=1.2,
                            linestyle="dashed", mutation_scale=10), zorder=5)

# ── TOOLS band ───────────────────────────────────────────────────────────────
tools_y = 8.45
tool_data = [
    (1.35,  "Gmail",    "N1 ingest only\ndo not send"),
    (3.55,  "Calendar", "N1 deadline\nparallel"),
    (6.9,   "Drive",    "N3–N6 write\nN7 read  (SoT)"),
    (14.3,  "Box",      "scratch only\nnever SoT"),
]
for x, lbl, sub in tool_data:
    node(ax, x, tools_y, lbl, sub=sub, bg=C_TOOL_BG, tc=C_TOOL_TXT,
         w=2.1, h=0.90)

# connectors spine → tools
connector(ax, 1.35, spine_y - 0.40, tools_y + 0.45, color=C_ARROW)   # Gmail→N1
connector(ax, 3.55, spine_y - 0.40, tools_y + 0.45, color=C_ARROW)   # Cal→N1
# Drive spans N3-N6 (use N4 midpoint x)
for nx in [spine[2][0], spine[3][0], spine[4][0], spine[5][0]]:
    connector(ax, nx, spine_y - 0.40, tools_y + 0.45,
              color="#40916C", ls="--")
# N7 reads Drive
ax.annotate("", xy=(spine[5][0] + 0.88, tools_y + 0.12),
            xytext=(spine[6][0] - 0.88, tools_y + 0.12),
            arrowprops=dict(arrowstyle="<|-", color="#888",
                            lw=1.0, mutation_scale=10), zorder=5)
ax.text((spine[5][0]+spine[6][0])/2, tools_y + 0.28,
        "read", fontsize=6, color="#555", ha="center")

# Hands-writes label
ax.text(6.9, tools_y - 0.65,
        "★  All Drive writes via Hands  (bc-id required)  — Desks do not write Drive",
        fontsize=6.8, color=C_WARN, ha="center", fontweight="bold")

# ── REPOS band ───────────────────────────────────────────────────────────────
repos_y = 5.65
repo_data = [
    (4.2,  "cth-plugin",          "Lane A  •  harness + graph\nHands PR only"),
    (12.0, "sustenttia-v2\n@ 1fc2dfb", "analog pattern\ningest + enrich\nNOT grant pack"),
]
for x, lbl, sub in repo_data:
    node(ax, x, repos_y, lbl, sub=sub, bg=C_REPO_BG, tc=C_REPO_TXT,
         w=3.0, h=1.0)

connector(ax, 4.2,  tools_y - 0.45, repos_y + 0.50, color=C_ARROW, ls="--")
connector(ax, 12.0, tools_y - 0.45, repos_y + 0.50, color="#888",  ls=":")

ax.text(12.0, repos_y - 0.72,
        "pattern ref only — no new repo for grant packs",
        fontsize=6.2, color="#888", ha="center", style="italic")

# ── BACKENDS band ────────────────────────────────────────────────────────────
backends_y = 2.55
be_data = [
    (1.6,  "Cognee",              "live analog\n9 datasets\nKùzu inside",         C_BACK_LIVE,  C_BACK_TXT),
    (4.4,  "FalkorDB\n+Graphiti", "coded-analog\ncontainer up\n0 nodes",          C_BACK_CODED, C_BACK_TXT),
    (7.2,  "R2R",                 "absent\ncrash-loop\ndo not claim hits",        C_BACK_ABS,   C_WARN),
    (9.8,  "Gold LanceDB",        "coded-analog\nvector store",                   C_BACK_CODED, C_BACK_TXT),
    (12.6, "Chroma",              "coded-analog\nleftover gate\ndon't replicate", C_BACK_CODED, C_BACK_TXT),
    (15.6, "Neo4j",               "ABSENT\nno container\nFalkor = graph DB",      C_BACK_ABS,   C_WARN),
]
for x, lbl, sub, bg, tc in be_data:
    node(ax, x, backends_y, lbl, sub=sub, bg=bg, tc=tc, w=2.3, h=1.05)

connector(ax, 4.4, repos_y - 0.50, backends_y + 0.53, color=C_ARROW, ls="--")

# ── legend ────────────────────────────────────────────────────────────────────
legend_items = [
    mpatches.Patch(color=C_SPINE_BG,  label="Spine node (N1–N9)"),
    mpatches.Patch(color=C_TOOL_BG,   label="Tool"),
    mpatches.Patch(color=C_REPO_BG,   label="Repo"),
    mpatches.Patch(color=C_BACK_LIVE, label="Backend — live analog"),
    mpatches.Patch(color=C_BACK_CODED,label="Backend — coded analog"),
    mpatches.Patch(color=C_BACK_ABS,  label="Backend — absent"),
]
ax.legend(handles=legend_items, loc="lower right", fontsize=7,
          framealpha=0.9, edgecolor="#AECDBF")

# ── title + footer ────────────────────────────────────────────────────────────
ax.text(10, 12.85,
        "CTH Grant Graph — Spine N1–N9 + Tools / Repos / Backends band",
        ha="center", va="center", fontsize=13, fontweight="bold",
        color="#1B4332")
ax.text(10, 12.55,
        "2026-08-17  •  NEW BAND added  •  analog only — do not upgrade to live until gates A–C clear",
        ha="center", va="center", fontsize=8, color="#555")

plt.tight_layout(pad=0.3)
plt.savefig("/workspace/docs/grant-graph/grant-graph.png",
            dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
print("saved grant-graph.png")
