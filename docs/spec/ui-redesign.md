# SPEC LOCK — UI redesign (4-step workflow)

Status: **DRAFT — waiting for the founder's `go`** (spec-lock rule).
Sources: design-taste-frontend (`system.md`, `layout-v4.md` §5, `motion.md`, `icons.md`, `copy.md`,
`library/type.json`, `library/palettes.json`), ui-contract, the agreed flow (`docs/flow/siteblitz-flow.mmd`).
All contrast ratios computed with the WCAG 2.x formula and re-checked on 2026-11-08.
Marketing-page parts of the taste skill (hero, moments, photos, shader grounds, section-per-screen)
are deliberately **not** applied: this is an all-day internal data tool.

## Decision table
| # | Ambiguity | Locked value | Why |
|---|---|---|---|
| 1 | Theme | Light only, no theme switch | Status tints stay distinct on white; one theme halves QA (system.md Colour) |
| 2 | Neutrals | bg `#f4f4f1` · surface `#ffffff` · hover `#f7f7f4` · inset `#efefeb` · line `#dededa` · line-strong `#8a8b8e` (3.41:1) · skeleton `#e8e8e4` | system.md Colour; UI borders ≥ 3:1 |
| 3 | Text | ink `#17181a` (17.77:1) · ink-2 `#45474b` (9.31:1) · ink-3 `#66686c` (5.58:1, meta only) | system.md Type |
| 4 | Accent (one) | `#1a4be0` (6.72:1) · hover `#163fba` · tint `#ecf1fd`; only primary button, links, focus, current step, selected row. Old violet `#6366f1` removed (banned hue band) | system.md, SKILL §6, palette `white-link-blue` |
| 5 | Website verdict chips | Lead = green `#15603a` on `#e1f3e7` (6.57): "No website found", "Social media only", "Website down" · Not a lead = rose `#a1182f` on `#fce6e9` (6.56): "Has own website" · Needs you = amber `#7a4f00` on `#fbf0d2` (6.28): "Needs review" · Skip = `#5c5f64` outline `#8a8b8e`. Always label + lucide icon, raw code shown in the drawer | ui-contract (colour never alone) |
| 6 | Tier chips | Hot: filled `#b8360f`, white text (5.88), Flame icon — the only filled chip · Warm `#9a3f05` on `#fdeedd` (5.98) · Cold `#33526e` on `#e7eef5` (6.98) · Review = amber of row 5 · Skip = outline. Sentence case labels | copy.md (no all-caps) |
| 7 | Job status | Queued (outline) · Running (accent tint + spinner) · Done (green) · Partial (amber) · Failed (rose) · Cancelled (outline). Error text `#b42318` (6.57) | one system, three tints reused |
| 8 | Fonts | IBM Plex Sans 400/500/600 + IBM Plex Mono 400/500 (Google Fonts, `display=swap`); stack `"IBM Plex Sans","Segoe UI",system-ui,sans-serif`; `tabular-nums` on every number; no Inter | layout-v4 §5, `type.json` "plex" |
| 9 | Type scale | h1 28/36 500 (24/32 < 768) · h2 20/28 500 · h3 16/24 500 · body 16/24 · table + controls 14/20 · labels/chips/meta 13/18 500 · mono 13/20 · stat 28/36. Nothing under 13 px. Paragraphs ≤ 72ch | system.md Type |
| 10 | Spacing | 4, 8, 12, 16, 24, 32, 48, 64 only | system.md spacing scale |
| 11 | Radius | chips 4 · buttons/inputs 6 · panels/tables/dialogs 8 · drawer 0 · no pills | system.md `sharp` |
| 12 | Shadow | only `0 8px 24px rgba(23,24,26,.12)` on drawer/menus/dialogs; panels use 1 px line | system.md |
| 13 | Header + stepper | fixed 56 px white header, 1 px line. Logo tile "S" + "SiteBlitz Lead Generator". Steps `1 Find › 2 Review › 3 Hot leads › 4 Outreach` with live counts; current = accent circle + 2 px accent bar + `aria-current="page"`. Settings at right. < 768: steps move to a 64 px bottom tab bar | system.md Nav |
| 14 | Routes | hash routes `#/find`, `#/review?job=&verdict=`, `#/leads?tier=`, `#/outreach?lead=`, `#/settings`; no router package; opens on Find when 0 businesses, else last step (localStorage `sb.lastStep`) | no new deps |
| 15 | Content width | max 1440 centred; side padding 32 / 24 / 16 | system.md gutters |
| 16 | Tables | rows 44 px, header 40 px sticky in its box, no zebra, hover `#f7f7f4` 120 ms, selected = accent tint, numbers right-aligned, 50 rows/page; < 768 rows become 2-line items ≥ 64 px | ui-contract |
| 17 | Evidence drawer | right, 480 px; ≥ 1024 non-modal (J/K move rows); 768–1023 modal with scrim `rgba(23,24,26,.32)`; < 768 full-screen; Esc closes, focus returns to row | system.md Access |
| 18 | Breakpoints | desktop-first at 1279 / 1023 / 767; verified at 1280×800, 390×844, overflow check at 320 | SKILL §5 |
| 19 | Icons | `lucide-react ^1.70.0`, stroke 1.75, 16 px in tables, 20 px in nav; zero emoji; real brand logos (CC0) via the skill's `icons.mjs` | icons.md |
| 20 | Motion | hover 150 ms in / 120 ms out; press 90 ms; drawer 240 ms `cubic-bezier(.22,1,.36,1)`, out 120 ms; UI ease `cubic-bezier(.2,.8,.2,1)`; spinner 16 px 1 s → check icon; jobs poll every 2000 ms while queued/running; only transform/opacity/colour animate | motion.md |
| 21 | Reduced motion | no transforms; drawer/menus fade 120 ms; static spinner + word "Running" | motion.md |
| 22 | Focus | `outline: 2px solid #1a4be0; outline-offset: 2px` (−2 px inside tables), never removed | system.md Access |
| 23 | Controls | two buttons only: primary (accent fill) and secondary (white, line-strong border); 40 px tall (44 < 768); one primary per view; inputs with visible label above; disabled shows its reason | system.md buttons |
| 24 | States | StateBlock (40 px inset icon tile, title, one sentence, one action, optional "Technical details" with raw error in mono), `aria-live="polite"`; skeleton shaped like the result, shown after 300 ms, no shimmer | ui-contract Part 3 |
| 25 | Numbers + dates | `Intl.NumberFormat('en-IN')`; scores "72/100" integers; dates "8 Nov 2026, 15:42", < 24 h "14 min ago" (absolute in title); evidence timestamps absolute with seconds; empty "—" | system.md Type |
| 26 | Copy voice | plain English, sentence case, no "Engine" names, no "Learn more", no "!" — e.g. "Start search", "See 31 businesses", "Mark correct", "Copy draft", "Log a call", "Add to do-not-contact list", "Retry search". Honest line: "Sending is off: no email provider is connected. Copy the draft, send it yourself, then log it here." | copy.md |

## Screens (states to screenshot: default · loading · empty · error · populated)
- **Find** `#/find` — "New search" panel (country default India, city, category, include-franchises switch off, max results default 500, source: OpenStreetMap / Google Places disabled with reason until a key exists / CSV dropzone) + "Current search" panel (Queued → Running → Finished, Found / New / Duplicates / Errors, "See N businesses" → Review) + "Past searches" table. A 0-result or failed job shows the backend `error_message` verbatim and "Retry search".
- **Review** `#/review` — filters (name, job, verdict with counts), legend line, pilot strip ("Your labels: 46 of 200 …"), table (Business, Category, City, verdict chip, Checked, Your label), evidence drawer with every check (icon, name, result, timestamp with seconds, raw details) and footer "Is this verdict right?" Mark correct / Mark wrong (+ what was wrong) / Mark not sure; keys 1 2 3, J K, Esc.
- **Hot leads** `#/leads?tier=hot` — tier tabs with counts, table (Rank, Business, Category, Tier, Need 0–100 + bar, Confidence, contact-route icons, Next action), lead drawer with the three indicators shown separately, "Why Hot" reasons each with points and "See evidence", contact routes, "Start outreach".
- **Outreach** `#/outreach` — "Sending is off" notice, lead queue, contact-route checklist, draft built from listed facts + "I checked every fact" checkbox before "Copy draft", "Send email" disabled with reason, contact log, "Add to do-not-contact list" with confirm.
- **Settings** `#/settings` — data-source status (keys live in backend `.env`, never in the browser), do-not-contact list.

## OUT OF SCOPE
Dark mode · router/UI libraries other than lucide-react · real sending · old CRM board, simulated replies, funnel dashboard · entering API keys in the UI · auth/multi-user · non-English UI · taste-skill hero/moments/photos/effects · backend changes (separate phase + `docs/contracts/ui-api.md`).

## Delivery split (8-file rule)
UI-1 tokens + shell + Find · UI-2 Review + evidence drawer · UI-3 Hot leads + Outreach + Settings.
Depends on phase 2 (verdicts, checks, tiers in the API); write `docs/contracts/ui-api.md` first.

## ACCEPTANCE CRITERIA (binary)
- [ ] At 1280×800 the header, and at 390×844 the bottom bar, list exactly Find, Review, Hot leads, Outreach; current step has `aria-current="page"`; Settings reachable at both widths.
- [ ] 0 emoji code points (U+1F300–1FAFF, U+2600–27BF) in `frontend/src`.
- [ ] No hex colour in `frontend/src` outside `:root` in `index.css`; every hex there is in rows 2–7.
- [ ] Tab walk on all 5 screens shows the 2 px `#1a4be0` focus ring on every focused element.
- [ ] Lighthouse accessibility ≥ 95 on all 5 screens at 1280; axe-core 0 contrast violations.
- [ ] `scrollWidth <= innerWidth` on all 5 screens at 1280, 390 and 320.
- [ ] A 0-result search shows the backend `error_message` verbatim and "Retry search".
- [ ] Every evidence row shows name, result and a timestamp with seconds; a label survives reload.
- [ ] With no provider, "Send email" has `aria-disabled="true"`, "Sending is off" visible within 24 px, click sends no request.
- [ ] Screenshots: 5 screens × 5 states at 1280 + populated at 390 for each + both drawers open, in `docs/screenshots/ui/`.
- [ ] Reduced motion: drawer transform `none` while opening, spinner `animation-name: none`.
- [ ] Only IBM Plex fonts load (≤ 4 files); `lucide-react` is the only new dependency; `api.js` only gains lines.

## RISKS
- The API does not yet expose verdicts, checks, labels, tiers or the three indicators → phase 2 first; without it screens can only show empty states.
- Green = "no website found" (a lead) and rose = "has own website" reverses the usual meaning → legend line on Review; confirm on the first screenshots.
- The taste skill's own gate scripts fail any app (no hero/moments) by design → verify with the criteria above instead.

Reply `go` to build all of it, or `change 4,8` with your values.
