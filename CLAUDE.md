# Project rules - SiteBlitz Lead Generator

- The founder lives in Navsari, South Gujarat. SiteBlitz's public identity is "based in Gujarat" (SiteBlitz FD-22,
  truthful location). Never write Mumbai, Thane or any other city as the studio's location. Pilot and field areas
  default to Navsari + Surat. (Corrected twice on 2026-11-10.)
- Never call `ContactDiscoveryEngine.discover_contacts()` for real outreach until phase 5 lands: it fabricates email
  addresses and phone numbers. Use `_crawl_contact_pages` / `_extract_from_html` only.
- Outreach copy rules, languages and limits live in `docs/outreach/` and `docs/spec/outreach-engine.md`.
