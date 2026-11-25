# Weekly token audit report

- **Source CSV:** staged slice `usage-events.csv` (Nov 19–25 UTC, 16k events; not committed to repo)
- **Events parsed:** 16,000 (skipped 0 of 16,000 rows)
- **Window (UTC):** 2026-11-19 20:54:40.337000+00:00 → 2026-11-25 12:48:11.595000+00:00
- **Duration:** 5.66 days

## Baseline statement

Reproduces the **staged Nov 19–25 UTC slice** (`usage-events.csv`, 16k events, ~1.54B tokens). This is **not** the full Nov 1–25 corpus behind plan §0 (6.13B tokens, 65.7% / 76.9% Grok shares).

## Product share (whole window)

| Product | Tokens | Share |
| :--- | ---: | ---: |
| grok-bot | 864,988,379 | 56.15% |
| cursor | 675,394,610 | 43.85% |
| **Total** | **1,540,382,989** | 100% |

## Daily Grok vs Cursor share (UTC date)

| Date | Total tokens | Grok % | Cursor % |
| :--- | ---: | ---: | ---: |
| 2026-11-19 | 25,507,176 | 100.00% | 0.00% |
| 2026-11-20 | 342,258,384 | 65.50% | 34.50% |
| 2026-11-21 | 288,166,804 | 22.98% | 77.02% |
| 2026-11-22 | 196,346,716 | 55.98% | 44.02% |
| 2026-11-23 | 410,921,756 | 63.83% | 36.17% |
| 2026-11-24 | 273,241,279 | 63.28% | 36.72% |
| 2026-11-25 | 3,940,874 | 100.00% | 0.00% |

## Grok model mix (share of Grok tokens)

| Bucket | Tokens | Share of Grok |
| :--- | ---: | ---: |
| default | 689,359,989 | 79.70% |
| automation | 121,217,674 | 14.01% |
| other | 34,024,545 | 3.93% |
| cua | 20,386,171 | 2.36% |

## Cached prompt

- Cached prompt tokens: **1,407,793,462**
- Share of all tokens: **91.39%**
- Share of prompt + cached: **94.14%**

## Hour-of-day heatmap (America/Bogota)

```
Hour (America/Bogota) | bar (token share)
00:00    312,654
01:00    934,052
02:00    521,075
03:00  █  6,656,938
04:00    309,144
05:00    616,671
06:00  █  10,065,499
07:00  ████  24,549,884
08:00  █  8,085,889
09:00  ██████████████  74,943,130
10:00  ███████████████████  104,131,100
11:00  █████████  52,026,302
12:00  ███████  40,958,412
13:00  ████████████  65,127,849
14:00  ███████████████  84,135,787
15:00  ██████████████████  100,680,179
16:00  ████████████████████████  131,004,076
17:00  ██████████████████  98,927,671
18:00  ███████████████████████████  149,156,947
19:00  ████████████████████████████████████████  213,211,355
20:00  ███████████████████████████████████  191,470,534
21:00  ███████████████████  101,349,958
22:00  ██████████████  79,710,682
23:00    1,497,201
```

## Rapid-fire intervals

Plan §0 KPI uses **grok-bot-only** consecutive call pairs. The all-product metric is included for context but is not the governance threshold.

### Grok-bot only (plan §0 KPI — baseline ~82.1% under 15s)

- Consecutive pairs: 8,983
- Gap &lt;15s: 7,378 (82.13%)
- Gap &lt;5m: 8,819 (98.17%)

### All products in CSV time order (informational)

- Consecutive pairs: 15,999
- Gap &lt;15s: 14,150 (88.44%)
- Gap &lt;5m: 15,849 (99.06%)

## Top events by tokens

| UTC time | Product | Model | Total tokens |
| :--- | :--- | :--- | ---: |
| 2026-11-22T15:03:24.747000+00:00 | grok-bot | grok-bot-default | 321,545 |
| 2026-11-22T15:03:16.193000+00:00 | grok-bot | grok-bot-default | 320,111 |
| 2026-11-22T15:02:59.237000+00:00 | grok-bot | grok-bot-default | 316,982 |
| 2026-11-22T15:02:50.595000+00:00 | grok-bot | grok-bot-default | 316,297 |
| 2026-11-22T15:02:36.328000+00:00 | grok-bot | grok-bot-default | 315,097 |
| 2026-11-22T15:01:59.146000+00:00 | grok-bot | grok-bot-default | 310,394 |
| 2026-11-21T23:56:05.883000+00:00 | cursor | composer-2.5 | 309,350 |
| 2026-11-22T15:01:51.184000+00:00 | grok-bot | grok-bot-default | 308,670 |
| 2026-11-22T15:01:48.043000+00:00 | grok-bot | grok-bot-default | 307,722 |
| 2026-11-24T01:04:32.073000+00:00 | grok-bot | grok-bot-knowledge-work | 307,667 |

## KPI comparison (plan §0)

| KPI | Observed | Threshold | Status |
| :--- | ---: | ---: | :--- |
| grok_share_of_spend | 56.15% | 33.0% | fail |
| cursor_share_of_spend | 43.85% | 67.0% | fail |
| cached_prompt_share_of_total_tokens | 91.39% | 92.6% | info |
| rapid_fire_grok_only_under_15s_share | 82.13% | 20.0% | fail |
| rapid_fire_grok_only_under_5m_share | 98.17% | — | info |
| rapid_fire_all_products_under_15s_share | 88.44% | — | info |
| rapid_fire_all_products_under_5m_share | 99.06% | — | info |
| grok_cua_share_of_total | 1.32% | 2.0% | pass |
| grok_turns_over_80k | 5388 | 80000events | fail |

## Plan vs this CSV

The fleet redesign plan (25 Nov 2026) cites **6.13B tokens**, **65.7% Grok (monthly)**, **76.9% Grok (weekly active)**, and **92.6% cached reads** from the **full Nov 1–25** usage corpus. The staged `usage-events.csv` slice is **~5.7 days** and **~1.54B tokens**; it **cannot reproduce** the plan’s monthly/weekly headline percentages without the missing rows.

_Enforcement actions (tighten max_context, PROTOCOLS.md PR, circuit breaker, auto-pause) are disabled unless `--enforce` and `ENFORCE_APPROVED` are set (Gideon GO required)._
