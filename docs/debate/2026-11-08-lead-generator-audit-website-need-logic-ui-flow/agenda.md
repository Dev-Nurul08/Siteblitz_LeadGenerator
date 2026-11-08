# Agenda — SiteBlitz Lead Generator audit (2026-11-08)

1. Data sources: replace the broken OSM-only discovery with Google Places API (New) as the primary "Google Maps" source, OSM as free fallback, CSV as manual import — and NO direct scraping of Google Maps HTML or logged-in social platforms (Instagram, Facebook, LinkedIn, TikTok).
2. Social presence: detect a business's Instagram / Facebook / LinkedIn / TikTok links only from lawful signals (Places websiteUri pointing to a social profile, OSM contact:* tags, links on the business's own site) — is that enough, or is there a lawful source we are missing?
3. "Does this business need a website?" — replace the current rule (no website field => CRITICAL) with a verified Website-Need verdict: verify the website is really missing (Places websiteUri, OSM tags, domain-guess DNS check, dead/parked/link-in-bio detection), exclude chains / government / religious / ATMs, require the business to be operating and active.
4. Scoring + tiers: an explainable 0–100 Website Need Score with HOT / WARM / COLD / SKIP tiers and fixed thresholds; every point traced to evidence; no fake confidence.
5. Pipeline order: no-website leads have no email, so today they can never reach "qualified". Make phone / WhatsApp a first-class outreach channel and stop fabricating info@domain contacts.
6. Reliability: long network work runs inside HTTP requests today; move discovery + evaluation to background jobs with progress polling; SQLite as zero-setup default, Postgres optional.
7. UI flow + deletions: replace the 8 engine-named pages with a 4-step workflow (Find → Review → Hot leads → Outreach); delete or hide the parts that pretend (simulated sending, fake sender identity, fabricated pitch claims, Wikidata source, auto "Mobile App" opportunities).
