# HANDOFF — SiteBlitz Lead Generator — Phase 14 (email finder) — 2026-11-10

Branch: `phase-01-pipeline-repair`. Full run report: `docs/outreach/email-finder-run-2026-11-10.md`.

## Done
- **The email finder ran on all 2,162 Navsari + Surat leads** (spec row 9): 19:31 to 19:46 IST, 5,713 requests.
  - 69 leads skipped by rule 9 (colleges and schools).
  - 79 leads have an empty website field.
  - 2,014 leads visited (1,860 URLs on 1,230 hosts).
- **Emails:** 499 leads have at least one email: 619 unique addresses in 839 lead-email rows.
  - 0 rows have no source URL, and 0 come from a page off the business's own host. Checked independently from
    the CSVs.
  - 15 random rows fetched live again: 15/15 addresses are still on their page.
- **Totals:**
  - Down on this check: 701.
  - NO_VIEWPORT: 37.
  - NO_HTTPS: 63.
  - robots-blocked: 70.
  - Also ok 1,063, listing 102, protected 70, SSRF-blocked 6, social 2.
- **QA-038 fixed:** coaching classes (`specialty_school`) and preschools are prospects. Schools are skipped by exact
  category. Before the fix, 89 coaching leads in this selection were skipped.
- **QA-040 fixed:** the crawler respects robots.txt (RFC 9309 parser). It allows 12 s per GET, reads at most 2 MB
  and follows at most 5 redirects. It takes emails only from mailto links, visible text and Cloudflare-encoded
  addresses.
  - Before the fix, the probe extracted `you@example.com`, a Sentry key and an address inside an HTML comment, and
    ignored `Disallow: /`.
- **Tests:** backend 338/338, up from 325. New: 12 site-visit tests and the QA-038 rule test.

## Files changed
- `backend/app/engines/intelligence/rules.py`: exact school categories instead of the "school" fragment (QA-038).
- `backend/app/engines/enrichment/site_visit.py` (new): the polite visit.
  - robots.txt, homepage + `/contact`, `/contact-us`, `/contactus`, `/about`.
  - 12 s / 2 MB / 5 redirects, SSRF guard.
  - Records site down / HTTPS / viewport, and `no_address` for an empty website.
- `backend/app/engines/enrichment/discovery.py`:
  - `_extract_from_html` reads only mailto, visible text and Cloudflare. It drops scripts, comments and
    placeholders.
  - `_crawl_contact_pages` now calls `visit_site`.
- `scripts/email_finder.py` (new): the 2,162-lead selection, rule-9 skips, 10 hosts in parallel, resumable
  `visits.jsonl`, and `sites.csv` / `emails.csv` / `summary.json`.
- Tests:
  - `backend/tests/test_enrichment/test_site_visit.py` (new).
  - `test_phase3_deep.py`: JSON-LD is now ignored.
  - `test_discovery.py`: the fallback test stubs the crawl. It used to call the real hotelalpha.ch.
  - `test_intelligence/test_rules.py`: QA-038 test.
- `docs/outreach/email-finder-run-2026-11-10.md` (new): the totals and what they mean.
- `docs/DECISIONS.md`: phase-14 section.
- `docs/PHASES.md`: 14 ✅, new row 14b, Now / Next 3.
- `docs/spec/outreach-engine.md`: the phase-14 box is ticked.
- `docs/qa/ISSUES.csv`: QA-038 and QA-040 FIXED.
  - Rewriting the file removed redundant quotes on 28 other rows. Their content is unchanged; checked by parsing
    both versions.
- `CLAUDE.md`: 3 traps (below).

## Decisions made
- All are in `docs/DECISIONS.md` under "2026-11-10 - Phase 14 email finder". In short:
  - Own RFC 9309 robots parser.
  - "5 GET" counts page GETs; robots.txt is fetched on top.
  - The visit stops at the first page that shows an email.
  - JSON-LD is no longer read.
  - An email is kept only from the listed or redirected host.
  - Listing and social addresses are not fetched.
  - "Down" means one failed check.
  - The output stays outside the repo and is not imported into the app DB yet.

## Known broken / deliberately skipped
- **Not pushed.** The Claude OS guard blocked `git push` again: "the check itself failed (… git log …
  --not --remotes=origin)". The branch is about 29 commits ahead of origin.
- **The guard also blocked `git checkout -- docs/qa/ISSUES.csv`**, which I wanted to use to undo my own re-quoting.
  The re-quoted file was kept instead (content verified identical).
- **Chain stores are in the results.**
  - 115 hosts carry 797 leads, for example `stores.amaron.in`. 136 of the 499 email leads are on such hosts.
  - Brand head-office addresses repeat across many leads.
  - Not filtered: that is row 14b.
- **"Down" is not confirmed.** SITE_DOWN_CONFIRMED needs a second failure at least 6 h later (row 14b). 124 of the
  701 are deep links that return 404/410, so the domain may still work.
- **No email ladder status yet** (CONFIRMED / VALID / RISKY).
- **Nothing is imported into the app DB.** Phase 15 cannot list these leads until 14b does that.
- **Some old tests still reach real websites** through `discover_contacts()` (`test_merge_with_audit_emails`).
  Removing that function is phase 5.
- **Leftover files:**
  - `E:\tmp\_p14\` (probe, smoke run, logs).
  - The earlier session's `E:\tmp\_qa_scratch\`.
  - `visits.jsonl` keeps one stale `https://` record from the first run. It is unused.

## Next session starts here
- **Phase 14b:** re-check the 701 failed sites (now more than 6 h after the run), filter out chain store-locator
  hosts and head-office addresses, and import the kept rows into the app DB for phase 15.
- **First command:** push by hand in your own terminal: `git push origin phase-01-pipeline-repair`. Then in a new
  session: `/boot`, then `go`.
- **Watch out for:** never call `ContactDiscoveryEngine.discover_contacts()` (it invents addresses). Re-running
  `scripts/email_finder.py` with the same `--out` skips URLs that are already in `visits.jsonl`, so a re-check needs a
  new output folder.
