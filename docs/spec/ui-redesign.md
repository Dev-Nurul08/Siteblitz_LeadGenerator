# SPEC LOCK — UI redesign v2 (motion-led, award-reference direction)

Status: **APPROVED** — founder replied "go … complete everything" on 2026-11-08 after asking for an
extraordinary, award-reference, motion-based redesign (v1, a restrained light theme, was superseded).
Sources: design-taste-frontend (`system.md`, `layout-v4.md` §5, `motion.md`, `moments.md`,
`effects-usage.md`, `effects-creative.md` fx-map/fx-progress, `diagrams.md`, `icons.md`, `copy.md`,
`library/palettes.json` "graphite-safety-orange", `library/type.json` "mona"), ui-contract.
External facts checked 2026-11-08: npm `motion` 14.10.1, `@number-flow/react` 0.6.2, `maplibre-gl`
6.17.0, `lucide-react` 1.70.0; OpenFreeMap (free, no key, commercial OK, attribution required, as-is).

| # | Item | Locked value |
|---|---|---|
| 1 | Theme | Dark graphite; light "paper" sheet only for the outreach draft |
| 2 | Neutrals | bg `#18191b` · surface `#222427` · surface-2 `#2a2c30` · surface-3 `#33363a` · line `#34373b` · line-strong `#6b6e74` · map-land `#1d1f22` · paper `#eff0f1` / paper-ink `#18191b` / paper-muted `#55585d` |
| 3 | Text | ink `#eff0f1` (15.42:1) · ink-2 `#c4c6ca` · ink-3 `#9c9ea3` (labels/meta only) |
| 4 | Accent | `#ff4a1f` (label on it `#18191b`), hover `#ff6a45`, accent text `#ff8a6a`, tint `#3a2420`; only primary button, focus, current step, Hot tier, map arrival ring, selected-row bar |
| 5 | Verdict chips | Lead = green `#7ee2a8` on `#183324` (No website found / Social media only / Website down) · Needs review = yellow `#f5c451` on `#352b10` · Has own website = grey `#c4c6ca` on `#2e3034` · Skipped = outline `#9c9ea3` / `#6b6e74`; always label + lucide icon |
| 6 | Tier chips | Hot filled `#ff4a1f` + `#18191b` (only filled chip, Flame) · Warm `#ffb27a` on `#3a2719` · Cold `#9ec3e6` on `#1d2a36` · Review = yellow · Skip = outline |
| 7 | States / map dots | Errors rose `#ff8a9b` on `#3d1d24`; confidence low rose / medium yellow / high green; map dots lead `#4fd18b`, review `#f5b83d`, not a lead `#8d9097`, unchecked `#c4c6ca`, arrival ring `#ff4a1f` |
| 8 | Fonts | Mona Sans (wdth 75–125, wght 400–600) + Geist Mono 400/500 for every number/URL/time; `https://fonts.googleapis.com/css2?family=Geist+Mono:wght@400;500&family=Mona+Sans:wdth,wght@75..125,400..600&display=swap` |
| 9 | Type scale | title 44/48 wdth 125 w500 −0.035em (30/34 < 768) · h2 22/28 wdth 112 · h3 16/24 · body 16/24 · table 14/20 · labels 13/18 w500 · mono 13/20 · stats Geist Mono 500 36/40 (28/32 phone) · step index "01–04" mono 13 |
| 10 | Spacing / radius | 4 8 12 16 24 32 48 64 · radius chips 4, controls 6, panels 8, drawer/header 0, no pills |
| 11 | Shadow | only overlays: `0 16px 48px rgba(0,0,0,.5)` + 1 px line-strong edge |
| 12 | Header / stepper | 56 px, 3 px accent bar on top edge, `01 Find — 02 Review — 03 Hot leads — 04 Outreach`, live counts (NumberFlow), current = ink + 2 px accent bar + `aria-current`, Settings right; < 768 → 64 px bottom bar |
| 13 | Routes | `#/find` `#/review` `#/leads` `#/outreach` `#/settings`; first visit Find, then last step used; max width 1440, padding 32/24/16 |
| 14 | Table | rows 44 px, hover surface-2, selected surface-3 + 2 px accent left bar, sticky header 13/500 ink-3, mono numbers right-aligned, 50/page |
| 15 | Drawer | 480 px, non-modal ≥ 1024, modal 768–1023, full sheet < 768, Esc closes, focus returns |
| 16 | Breakpoints | 1279 / 1023 / 767; verify 1280×800, 390×844, 320; Find map ≥ 560 px desktop, 320 px phone |
| 17 | Icons | `lucide-react ^1.70.0`, stroke 1.75, 16/20 px, no emoji |
| 18 | Motion | `motion ^14.10.1`, `@number-flow/react ^0.6.2`, `maplibre-gl ^6.17.0`; hover 150/120, press 90, menu 200, indicator 240, route 120 out + 240 in, drawer 320; springs bounce 0; UI ease `cubic-bezier(.2,.8,.2,1)`, entrance `(.22,1,.36,1)`, camera `(.65,0,.35,1)`; nothing > 1200 ms; loops only spinner 1 s + diagram 3.2 s; animate transform/opacity/colour/stroke-dashoffset only; never bounce/parallax/glow/custom cursor |
| 19 | Reduced motion | `MotionConfig reducedMotion="user"` + CSS query; map `jumpTo`; route = 120 ms fade |
| 20 | Focus | `outline: 2px solid #ff4a1f; outline-offset: 2px` (−2 px in tables) |
| 21 | Controls | primary accent + dark label; secondary transparent + line-strong border; 40 px (44 phone); one primary per view; disabled shows its reason |
| 22 | States | StateBlock (glyph, title, sentence, one action, `<details>` raw error); skeleton static surface-3 after 300 ms; Find first run = lanes diagram |
| 23 | Numbers / dates | Geist Mono, NumberFlow `en-IN`; coordinates 5 decimals in drawer; "8 Nov 2026, 15:42" |
| 24 | Copy | plain English, sentence case, no "Engine", no "!", e.g. "Start search", "View businesses", "Export CSV", "Mark correct", "Copy draft", "Sending is off: no email provider is connected. Copy the draft, send it yourself, then log it here." |
| 25 | Map | MapLibre, style `https://tiles.openfreemap.org/styles/dark`, land `#1d1f22`, no rotation/pitch, clusters < zoom 13, attribution always on, one map at a time, lazy-loaded |

## Signature moment per screen
- **Session entrance** (once per browser session, ≤ 1100 ms): top bar draws 600 ms, steps fade up 12 px (520 ms, 60 ms apart), title rises from a mask 700 ms.
- **Shell — progress line:** connector to the next step fills orange (scaleX 0→1, 480 ms) when a step first produces output; current-step bar slides with `layoutId` 240 ms; counts roll 600 ms.
- **01 Find — businesses land on the map:** `fitBounds` 1200 ms; each new dot fades in 200 ms with an orange ring 18→5 px, .9→0 over 420 ms, stagger min(24 ms, 1200 ms ÷ batch).
- **02 Review — the row becomes its evidence:** name + verdict chip move into the drawer header via `layoutId` (320 ms); checks list fades up 6 px, 240 ms, 50 ms apart, ≤ 700 ms; label "stamp" 90 ms fill + tag 1.08→1 scale 180 ms, then auto-advance after 240 ms.
- **03 Hot leads — the score builds from its reasons:** Need total rolls ≤ 900 ms; stacked 0–100 bar fills one reason segment at a time; tier switch indicator 240 ms, rows FLIP 280 ms.
- **04 Outreach — evidence threads:** hovering a fact underlines its sentence (scaleX 240 ms, `#c2381a` on paper) and draws a 1 px orange connector; unlinked sentences are counted on screen; "Copy draft" icon → check for 1.6 s.
- **Settings — live source check:** each source row spinner → status chip 150 ms, in real response order.

## References (no awards claimed)
Linear (J/K triage + side panel), GitHub homepage globe (live points with contracting ring), Vercel deployments (one status line with live counts), NumberFlow (locale digit rolls), Teenage Engineering (graphite + safety orange, mono numerals).

## Out of scope
Light theme (token swap later to `steel-orange`), shader grounds/glows/grain/scroll scenes/photos/globe/3D maps/sound/custom cursor, self-hosted tiles, ⌘K palette, real sending, old CRM board/funnel, API keys in the UI, multi-user, non-English UI, Devanagari webfont.

## Acceptance criteria (binary)
1. Header at 1280 and bottom bar at 390 show 01 Find, 02 Review, 03 Hot leads, 04 Outreach; Settings reachable; `aria-current="page"` on the current step.
2. No emoji and no hex outside `:root` in `frontend/src`.
3. Tab walk on all 5 screens shows `outline: 2px solid rgb(255, 74, 31)`.
4. axe-core: 0 colour-contrast violations on all 5 screens.
5. `scrollWidth <= innerWidth` on all 5 screens at 1280, 390 and 320.
6. Initial JS ≤ 200 KB gzip with maplibre in a lazy chunk.
7. Every non-loop animation ends within 1200 ms; tokens in one `src/motion.js`.
8. Reduced motion emulated: no running transform animation; map camera jumps; numbers final at once.
9. Screenshots: each screen's states at 1280 + populated at 390 + start/middle/end of the Find signature.
10. OpenFreeMap attribution visible on every map; at most one `canvas.maplibregl-canvas`.
11. "Send email" `aria-disabled="true"` with "Sending is off" next to it; no send request on click; unlinked draft sentences counted; zero-result search shows `error_message`; exports download files named with the job id.
12. Only Mona Sans + Geist Mono load; new deps only `motion`, `@number-flow/react`, `maplibre-gl`, `lucide-react`; `api.js` only gains lines.

## Delivery split
UI-1 tokens + shell + motion system · UI-2 Find + map · UI-3 Review + drawer · UI-4 Hot leads + Outreach + Settings. Depends on phase 2 (verdicts, checks, labels, tiers in the API).
