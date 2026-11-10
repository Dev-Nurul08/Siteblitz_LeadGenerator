# Email finder run (phase 14) - 2026-11-10

Script: `scripts/email_finder.py`, run from 19:31 to 19:46 IST on this PC. It made 5,713 requests: 10 hosts in
parallel, one request at a time per host.

Output (business contact data, outside the repository): `E:\SiteBlitz-World-Business-Data\_work\email_finder\2026-11-10\`
- `sites.csv`: one row per lead, with its outcome, site checks and the number of emails kept.
- `emails.csv`: one row per lead and email, with its source URL and method.
- `summary.json`: the totals below.
- `visits.jsonl`: the raw visits. A re-run skips URLs that are already in this file.

## Coverage: all 2,162 leads have an outcome
| | Leads |
|---|---|
| Selected (spec row 9: Surat coaching 271 / retail 1,704 / salon 74; Navsari 10 / 98 / 5) | 2,162 |
| Skipped by website-intelligence rule 9: colleges 45, high schools 13, elementary schools 11 | 69 |
| Website field is an empty string, so there is nothing to visit | 79 |
| Visited: 1,860 distinct URLs on 1,230 hosts | 2,014 |

## Totals asked for by the acceptance criterion
| Measure | Count | Notes |
|---|---|---|
| Emails found | 619 unique addresses, 839 lead-email rows, **499 leads** with at least one | mailto 483, visible text 210, Cloudflare 145, "[at] [dot]" 1 |
| Emails without a source URL | **0** | Every email row has the URL of the page it was read from |
| Emails whose source page is not on the business's own host | **0** | 1 more was dropped during the run because its contact page redirected to another host |
| Sites down on this check | 701 leads (669 URLs) | No DNS 363, connection failed 128, homepage 404/410 124, timeout 72, parked 6, HTTP 500 4, other 4 |
| NO_VIEWPORT | 37 | Reachable HTML homepages with no viewport meta tag |
| NO_HTTPS | 63 | Reachable sites (ok or protected) that ended on `http://` |
| robots-blocked | 70 | Includes 10 sites whose robots.txt answered 5xx or 429, which means "disallow everything" |

The other outcomes of the 2,014 visited leads: ok 1,063, listing pages (Google / directories, not fetched) 102,
protected (401/403/429, the site exists) 70, SSRF-blocked (DNS points at 127.0.0.1 or a private address) 6,
social 2.

## Checks run
- `email_rows_without_source_url` = 0, and an independent check of `emails.csv` against `sites.csv` found 0
  source pages off the business's host.
- 15 random email rows were fetched live again: 15/15 addresses are still on their source page.
- `backend/tests`: 338 passed, including 12 site-visit tests (robots, 2 MB, 5 redirects, timeout, placeholders).

## What the numbers mean for the pilot
- **Many of these "no brand" leads are chain stores.** Their Overture row has no `brand`, but the listed website is
  a chain store locator:
  - 115 hosts carry 3 or more leads each, 797 leads in all, for example `stores.amaron.in` and
    `cakeshops.monginis.net`.
  - 136 of the 499 leads with an email are on such hosts.
  - The most repeated addresses belong to national brands: one address on 18 leads, another on 12.
  - On the other hosts: 363 leads with an email, 555 unique addresses. Brand sites with only 1-2 Surat stores
    are still in that number.
- **"Down" is one failed check.** `SITE_DOWN_CONFIRMED` needs a second failure at least 6 h later
  (website-intelligence row 6). Until then, these 701 sites cannot carry a SITE_DOWN observation in a message (spec
  row 12).
- 124 "down" leads list a deep link that now returns 404 or 410. The domain itself may still work.
- `summary.json` counts `failed_notes` per URL; the breakdown above is per lead.
- No email has a ladder status yet (CONFIRMED / VALID / RISKY): the run only finds addresses. The spec's fallback
  (fewer than 100 VALID emails, then use the 9,176 leads that already have an email) can only be judged after that
  check.

## Not done here (board row 14b)
- Second site check, at least 6 h later, for the 701 failed sites.
- Filter out chain store-locator hosts and head-office addresses.
- Import the kept rows into the app database (businesses, `website_checks`, contacts) for phase 15.
