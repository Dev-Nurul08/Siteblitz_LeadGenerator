# Topic — SiteBlitz Lead Generator: audit findings, scraping + website-need logic, UI flow

## The founder's words (translated from Hinglish)
"This is my lead generator engine. Analyse everything word by word. It has many problems — UI logic,
output not coming properly, not reliable, not efficient, not effective. The data is not extracted /
scraped properly. It should scrape Google Maps, and Instagram, Facebook, LinkedIn, TikTok or other
social platforms of a particular country, for a particular business. The main motive is not just to
scrape businesses but to UNDERSTAND them: find out which businesses actually need a website. Only if
yes should they come into HOT. The UI is very bad — I can't understand where to start, how the flow
goes. Backend APIs may be broken. ChatGPT is my assistant who knows many things; Claude knows the real
development."

The founder runs SiteBlitz, a small web studio in India that sells websites (domestic and
international clients). The tool is internal: find small businesses that truly need a website and
contact them.

## Important difference from your system prompt
This round Claude Code HAS read every file of the repository and RAN the code (unit tests + a live
end-to-end probe against the real API on SQLite + live Overpass calls). The evidence file below is
verified, not README claims. File:line references point to the repo.

## Agenda
1. Data sources: replace the broken OSM-only discovery with Google Places API (New) as the primary "Google Maps" source, OSM as free fallback, CSV as manual import — and NO direct scraping of Google Maps HTML or logged-in social platforms (Instagram, Facebook, LinkedIn, TikTok).
2. Social presence: detect a business's Instagram / Facebook / LinkedIn / TikTok links only from lawful signals (Places websiteUri pointing to a social profile, OSM contact:* tags, links on the business's own site) — is that enough, or is there a lawful source we are missing?
3. "Does this business need a website?" — replace the current rule (no website field => CRITICAL) with a verified Website-Need verdict: verify the website is really missing (Places websiteUri, OSM tags, domain-guess DNS check, dead/parked/link-in-bio detection), exclude chains / government / religious / ATMs, require the business to be operating and active.
4. Scoring + tiers: an explainable 0–100 Website Need Score with HOT / WARM / COLD / SKIP tiers and fixed thresholds; every point traced to evidence; no fake confidence.
5. Pipeline order: no-website leads have no email, so today they can never reach "qualified". Make phone / WhatsApp a first-class outreach channel and stop fabricating info@domain contacts.
6. Reliability: long network work runs inside HTTP requests today; move discovery + evaluation to background jobs with progress polling; SQLite as zero-setup default, Postgres optional.
7. UI flow + deletions: replace the 8 engine-named pages with a 4-step workflow (Find → Review → Hot leads → Outreach); delete or hide the parts that pretend (simulated sending, fake sender identity, fabricated pitch claims, Wikidata source, auto "Mobile App" opportunities).

## What Claude Code proposes for point 3–4 (challenge it)
Website Need Score (0–100), computed only from stored evidence:
- Presence evidence (max 45): no website anywhere after verification 45; website field is a social
  profile / link-in-bio (instagram, facebook, linktr.ee, wa.me) 40; listed website dead (DNS fail /
  connection refused / 5xx / parked / "coming soon") 38; old Google "business.site" URL 40; website
  works but not mobile-friendly or no HTTPS 20; works and modern 0.
- Business is real and active (max 25): operational status confirmed 10; review count >= 10 → 10,
  >= 3 → 6; rating present 5.
- Reachable (max 15): phone 10; email 3; any social link 2.
- Category website-ROI (max 15): high (clinics, dentists, salons, restaurants, hotels, gyms, coaching,
  lawyers, CAs, real estate, interior designers, trades) 15; medium (retail shops) 9; low 4.
- SKIP (score forced to 0, never shown as a lead): chain/brand (OSM brand / brand:wikidata tag, or the
  same name in >= 3 places in the run), ATM / fuel / bank branch / place of worship / government /
  school-university-hospital, permanently closed.
- Tiers: HOT >= 75, WARM 55–74, COLD < 55, SKIP. HOT additionally REQUIRES presence evidence >= 38
  (i.e. verified no real website) AND a phone number.

Answer each agenda point by number: agree / disagree because ... / need data: ... . End with the list
of points still open.
