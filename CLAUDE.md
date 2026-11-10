# Project rules - SiteBlitz Lead Generator

- The founder lives in Navsari, South Gujarat. SiteBlitz's public identity is "based in Gujarat" (SiteBlitz FD-22,
  truthful location). Never write Mumbai, Thane or any other city as the studio's location. Pilot and field areas
  default to Navsari + Surat. (Corrected twice on 2026-11-10.)
- Never call `ContactDiscoveryEngine.discover_contacts()` for real outreach until phase 5 lands: it fabricates email
  addresses and phone numbers. Use `_crawl_contact_pages` / `_extract_from_html` only.
- Outreach copy rules, languages and limits live in `docs/outreach/` and `docs/spec/outreach-engine.md`.
- On this PC Smart App Control blocks the jiter 0.19 DLL that `anthropic` installs, which breaks `import anthropic`.
  Fix: `.venv/Scripts/python.exe -m pip install --force-reinstall --no-deps jiter==0.8.2`. SQLAlchemy needs its
  pure-Python reinstall too (see README / memory).
- Writer tests build `Settings(_env_file=None, ...)` so a real `.env` (API key, sender facts) can never make them
  call the API or change their result. Keep it that way.
- UI / API QA without new installs:
  - Playwright 1.62 is in the npx cache. Pass `PW_PATH=%LOCALAPPDATA%/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright`
    to `docs/qa/tools/ui_sweep.cjs`.
  - Run the backend on a copy of `dev_preview.db` through the `DATABASE_URL` / `DATABASE_URL_SYNC` environment
    variables, never on the original file.
  - The issue register is `docs/qa/ISSUES.csv`. Keep adding to it; do not start a new one.
