# Project rules - SiteBlitz Lead Generator

- The founder lives in Navsari, South Gujarat. SiteBlitz's public identity is "based in Gujarat" (SiteBlitz FD-22,
  truthful location). Never write Mumbai, Thane or any other city as the studio's location. Pilot and field areas
  default to Navsari + Surat. (Corrected twice on 2026-11-10.)
- `ContactDiscoveryEngine.discover_contacts()` was deleted on 2026-11-12 (commit 619ff24) because it fabricated emails
  and phones; a regression test scans for guessed-address patterns. Never reintroduce pattern-made addresses. Emails
  come only from `_crawl_contact_pages` / `_extract_from_html` (with source URL + excerpt) or a founder confirmation.
- Email engine v2 (`docs/spec/email-engine-v2.md`): no email is sent from Gmail/Workspace/Vercel; the suppression
  list on the website is authoritative and is checked fresh before every SMTP submission.
- Outreach copy rules, languages and limits live in `docs/outreach/` and `docs/spec/outreach-engine.md`.
- On this PC Smart App Control blocks the jiter 0.19 DLL that `anthropic` installs, which breaks `import anthropic`.
  Fix: `.venv/Scripts/python.exe -m pip install --force-reinstall --no-deps jiter==0.8.2`. SQLAlchemy needs its
  pure-Python reinstall too (see README / memory). fontTools' compiled `.pyd` files are blocked too (PDF export):
  they were renamed to `*.pyd.blocked-by-sac` in `.venv` on 2026-11-12 so the pure-Python fallback loads.
- Crawls: keep `--min-free-mb` (default 500) on `scripts/pool_e1.py`; this PC often has < 1 GB free RAM and a crawl
  died with MemoryError on 2026-11-12. Store times in UTC (SQLite drops the offset).
- Writer tests build `Settings(_env_file=None, ...)` so a real `.env` (API key, sender facts) can never make them
  call the API or change their result. Keep it that way.
- UI / API QA without new installs:
  - Playwright 1.62 is in the npx cache. Pass `PW_PATH=%LOCALAPPDATA%/npm-cache/_npx/e41f203b7505f1fb/node_modules/playwright`
    to `docs/qa/tools/ui_sweep.cjs`.
  - Run the backend on a copy of `dev_preview.db` through the `DATABASE_URL` / `DATABASE_URL_SYNC` environment
    variables, never on the original file.
  - The issue register is `docs/qa/ISSUES.csv`. Keep adding to it; do not start a new one. Edit only the target
    lines: rewriting it with `csv.writer` re-quotes every row (and the guard blocks `git checkout --` to undo it).
- Email finder (`scripts/email_finder.py`): output holds business emails, so it lives under
  `E:\SiteBlitz-World-Business-Data\_work\email_finder\<date>\`, never in the repo. The same `--out` resumes from
  `visits.jsonl`, so a re-check needs a new folder. Overture rows can list an empty string as their website.
- New tests that touch `ContactDiscoveryEngine` must stub `_crawl_contact_pages`: it fetches real websites.
- Parallel workers: the Agent tool's `isolation: "worktree"` refuses this repo (path case `e:` vs `E:`). Create the
  worktree by hand (`git worktree add E:/tmp/_lg_<name> -b <branch> <base>`) and run tests there with the main
  checkout's `.venv` (the backend package is not installed, so imports resolve to the worktree).
- Push: the Claude OS guard blocks a `git push` that carries a redirect or pipe (`2>&1`, `| tail`). Use the bare
  `git push origin phase-01-pipeline-repair`. Vercel production changes (env vars, `--prod`) are denied to Claude by
  the safety classifier: give the founders the commands (`docs/outreach/email-engine-setup.md`).
