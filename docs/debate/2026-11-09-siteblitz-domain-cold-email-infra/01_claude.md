You are reviewing this developer's project.

<project_context>
<file path="docs/debate/2026-11-09-siteblitz-domain-cold-email-infra/facts.md">
# Verified facts and Claude Code's draft plan (2026-11-09)

## The business
- SiteBlitz sells one-time-fee websites to small local businesses in India (Gujarat-based, serving India).
  Prices: Launch Rs 7,999 (1 page, 2 working days), Business Rs 17,999 (3 pages, 7 working days), Custom quoted.
  No GST registration yet. Founder plus one friend build sites. Founder's name and photo never appear publicly.
- Site: Next.js on Vercel Hobby (non-commercial terms - host undecided), live only at `siteblitz.vercel.app`.
  No custom domain bought yet. Site email `[REDACTED]` is hidden (`emailLive=false`) because it bounces.
- Earlier founder decisions (2026-11-01): buy the domain only, no paid mailbox, no other paid tools; WhatsApp is
  the primary channel; Rs 1,000 total ad budget for November 2026; cold email on hold "pending the domain and a
  legal review"; warm introductions first. The founder is now asking for a 1,000 emails/day plan instead.
- Lead generator (this repo): finds businesses that need a website, worldwide data (86.75 M Overture places),
  used in practice for Indian cities. Target pilot in docs/PHASES.md: one Indian city, dentists and salons,
  200 businesses.

## Code evidence (this repo)
- `backend/app/engines/enrichment/discovery.py:131-139` fabricates contacts when none are found:
  `contact_email = f"inquiry.{slug}@gmail.com"` and phone `+91 9825` + hash.
- `surat_restaurant_leads_with_contacts.csv`: 38 rows, 38 emails, 37 are `inquiry.*@gmail.com` (fabricated);
  only `[REDACTED]` looks real. 36 of 38 phones are fabricated too.
- Real email sources: Overture Places `emails` field, emails crawled from a business's own website, Hunter.io
  if a key is set (not set).
- Sending: `backend/app/engines/conversion/sender.py` is a scaffold - round-robin over fictional
  `@siteblitz.agency` mailboxes, marks messages SENT without any network call (always `simulate=True`).
  Default `daily_send_limit` 50, 60-300 s jitter, Mon-Fri 9-17 UTC, no warm-up, unsubscribe link points to
  localhost, footer uses a fake New York postal address. Phase 5 (real sending) is not started.
  docs/DECISIONS.md: WhatsApp is never automated; sending stays off until a real provider confirms delivery.
- No India / TRAI / DPDP rules in `country_rules.py` (only US, UK, EU, Canada, Australia).
- How the team sends today ("multiple normal Gmails") is NOT in any doc - it comes only from the founder's
  message. We do not know which list they used.

## Domain checks (registry RDAP / WHOIS, 2026-11-09 ~06:30 UTC)
- AVAILABLE: siteblitz.in ("Domain siteblitz.in is available for registration" - NIXI RDAP), siteblitz.co.in,
  siteblitz.net.in, siteblitz.co (whois.registry.co: DOMAIN NOT FOUND), siteblitz.io (whois.nic.io: not found),
  siteblitz.app, siteblitz.dev, siteblitz.studio, siteblitz.agency, siteblitz.site, siteblitz.tech,
  siteblitz.xyz, siteblitz.digital, siteblitz.biz, siteblitz.pro, siteblitz.store,
  siteblitzhq.com, joinsiteblitz.com, siteblitzstudio.com, siteblitzweb.com (Verisign RDAP 404).
- TAKEN: siteblitz.com (GoDaddy, since 2001-09-11, own nameservers, no website answers),
  siteblitz.net and siteblitz.org (since 2001, GoDaddy, Rackspace DNS), siteblitz.online (2026-04-07),
  siteblitz.ai (OVH, 2026-06-16, Vercel DNS) - a live French site titled
  "SiteBlitz - Le site web tout-en-un, specialise par metier" (all-in-one websites per profession),
  getsiteblitz.com and trysiteblitz.com (both 2026-06-16, Cloudflare, 301-redirect to siteblitz.ai).
- .in rules: NIXI e-KYC mandatory within 7 days of registration (registrar bulletins; start date given as
  27 Jan 2026 or 31 Mar 2026), privacy/proxy banned, SERVERHOLD if not verified. Public WHOIS output is
  redacted ("The WHOIS information provided in this page has been redacted").
- Prices: Hostinger India list price .in Rs 899/yr (renewal Rs 899), .co.in Rs 799 (Rs 469 first year),
  .com Rs 1,499 (renewal Rs 1,499); GST not stated on page. Porkbun API (USD): .com 11.81, .in 7.83,
  .co.in 5.80, .co 15.76 then 31.20 renewal, .io 28.12 then 51.80.
- FX used: Rs 94.5 per USD (PTI close 94.46 on 2026-11-05).

## Email facts
- Google Workspace India page (workspace.google.com/intl/en_in/pricing.html): Base Rs 99/user/month
  (custom-domain Gmail, 20 GB, max 20 users; intro 50% off from 22 Nov 2026), Starter Rs 270 (30 GB,
  up to 300 users, Gemini), Standard Rs 1,080. Prices under "Annual (save 16% with one-year commitment)",
  excluding tax.
- Workspace limits (Google doc): 2,000 messages/user/day, 2,000 external unique recipients/day, trial 500.
  Up to 30 aliases per user at no extra cost.
- Google sender FAQ: keep spam rate under 0.1%, never reach 0.3%; bulk senders need a DMARC record.
  Bulk-sender threshold of 5,000/day to Gmail comes from third-party explainers.
- Workspace Acceptable Use Policy bans generating or distributing "large volumes of unwanted emails" and
  promotional content.
- Free Gmail: ~500 recipients/day (third-party sources only, not confirmed on Google's page).
- Per-inbox cold volume (vendor blogs, not independent): 10-20/day new, 30-50/day warmed after weeks;
  1,000/day needs ~20-34 inboxes; keep a domain under ~500/day.
- Instantly (third-party pages): Growth USD 47/month (1,000 uploaded contacts cap), Hypergrowth USD 97/month
  or 77.60 annual (25,000 uploaded contacts, 100k-125k emails/month); unlimited accounts + warm-up on all plans.
- MillionVerifier: USD 37 per 10k credits, USD 89 per 50k (third-party pages citing vendor pricing).
- Zoho Mail Lite: Rs 59-90/user/month per Indian resellers (official page not checked).
- DPDP Rules notified 13 Nov 2025; main obligations from ~May 2027 (18-month phase-in).

## Claude Code's draft plan (challenge this)
1. Buy `siteblitz.in` as the brand domain (+ optional `siteblitz.co.in`). Search the IP India trademark
   registry for "SITEBLITZ" first because of the French company.
2. Stop the free-Gmail sending now. Never cold-send from `siteblitz.in`.
3. 1,000/day = 30 inboxes x ~33/day on 10 separate .com sending domains (3 inboxes each), redirecting to the
   main site; SPF + DKIM + DMARC on every domain; 3-5 week ramp; Google Postmaster Tools.
4. Main org: 1 paid Workspace Base user (founder's real first name) with free aliases hello@, support@, billing@.
   Cold org: a SEPARATE Workspace account, 30 Starter users (Base caps at 20). No CEO/CTO mailboxes.
5. Every address verified before sending; one-line opt-out; suppression list; no fabricated addresses ever.
6. Costs: month 1 = .in Rs 1,061 + 10 .com Rs 11,160 + Workspace Rs 9,675 (31 users + 18% GST) +
   Instantly Growth Rs 4,442 + MillionVerifier 10k Rs 3,497 = ~Rs 29,800.
   Months 2-12 = Workspace Rs 9,675 + Instantly Hypergrowth Rs 9,167 + verification ~Rs 3,700 = ~Rs 22,500.
   Year 1 ~Rs 2.78 lakh. If phase 5 builds sending in-house, drop Instantly (~Rs 13,400/month).
7. Gate before buying the cold stack: prove ~22,000 real verified addresses/month exist.

</file>

<file path="docs/DECISIONS.md">
# Decisions — SiteBlitz Lead Generator (append-only)

## 2026-11-08 — audit + ChatGPT review round
- **OpenStreetMap is the stored discovery source; Google Places is only an optional live verification
  adapter.** Why: the Maps Platform terms allow storing only the place ID permanently, and scraping the
  Maps website breaks Google's terms. (debate RESULT row 1)
- **No automated logged-in scraping of Instagram / Facebook / LinkedIn / TikTok.** Social links come from
  listings and the business's own pages and are recorded as discovered/confirmed/rejected. Why: platform
  terms (LinkedIn explicitly) and account bans; a social profile alone never proves need. (row 2)
- **"No website field" is not evidence of "no website".** A HOT lead needs a verified website verdict
  including a search or recorded manual search. Why: OSM is incomplete; the old rule produced mostly false
  HOT leads. (rows 3, 3c)
- **Three indicators, not one score:** Website Need Score, Evidence Confidence, Outreach Readiness.
  Why: contactability and certainty were mixed into "need", and confidence was a fake constant. (row 4)
- **Claude's 45/25/15/15 formula rejected in favour of 60/20/10/10 (provisional).** Why: reviews, phone and
  category are not proof of need; calibrate on the pilot. (row 4a)
- **WhatsApp is never automated; sending stays disabled until a real provider confirms delivery.** Why:
  WhatsApp opt-in policy; the old code marked unsent messages as SENT. (row 5)
- **CSV source ids are a hash of the row's identity fields**, not the row number. Why: row ids collided
  across files and silently dropped new data. (phase 1)
- **City search in Overpass resolves an administrative relation inside the country and maps it to an
  area.** Why: city areas never carry `ISO3166-1`; the old query always returned 0. (phase 1)
- **Phase-1 bug fixes were built before spec approval** because the founder's request explicitly
  authorised fixing broken APIs and the fixes add no new values — they restore what the code already
  promised. Website-need logic and UI redesign wait for spec-lock approval.

## 2026-11-08 — second request (why 29, validation, export)
- **Overture Maps Places is the default discovery source.** Why: OSM's Udaipur data really has only 29 named
  cafés; Overture (CDLA-Permissive-2.0 / Apache-2.0, Meta + Microsoft + Foursquare) has 246, with phones for
  83 % of places and social links for 87 %. Read with DuckDB from the public S3 GeoParquet by city bounding box
  (one Nominatim lookup per job). Release folder pinned in `OVERTURE_RELEASE` (update monthly).
- **Two records are merged only at "same city" or "within 5 km" confidence (≥ 0.70)**, not "same name in the
  same country" (0.60). Why: different shops with common names were being lost.
- **Every input limit comes from the DB column size or an existing rule** (ISO alpha-2, verifier email regex);
  free-form `query_params` are an allow-list (`min_confidence`); `adapter_class` is an allow-list. Why: no
  invented numbers; arbitrary module import was possible through POST /sources.
- **CSV upload cap 15 MB** = 5,000 rows (existing max_results limit) × ~3 KB max row at DB column sizes.
- **Exports:** CSV = all stored columns, formula-prefixed cells neutralised (OWASP CSV injection); PDF via
  fpdf2 (pure Python). Exports with real business contacts are not committed to git.

## 2026-11-08 — third request ("go … complete everything")
- **Both specs approved by the founder's "go"**: website intelligence (phase 2) and the UI redesign v2
  (dark graphite + safety orange, Mona Sans + Geist Mono, motion + MapLibre + NumberFlow + Lucide).
- **Website checks run concurrently per batch** (25 businesses ≈ 35 s instead of minutes); the DB writes stay sequential.
- **Google links (g.co, google.com, business.site) and directories (Justdial, Practo, Zomato…) are listings, not
  websites** — found live: "Dr Shweta's … Clinic" was "Has own website" because its website field was a g.co link.
- **The old Dashboard / Businesses / Opportunities / Contacts / Compliance / Campaigns screens were removed**
  from the UI; their APIs remain but are not used by the app (the Contacts API still fabricates `info@` — phase 5).
- **Screenshots containing real businesses' contact data are not committed** (`.gitignore`).
- **Open (founder):** social-only + phone can never be Hot under the approved weights (max 75). Options:
  (a) keep — only no-website businesses are Hot; (b) count "its listed web address is a social profile" as the
  10-point business-problem signal (social-only + phone + confirmed open + dentist = 85 → Hot).

## 2026-11-08 — fourth request ("as much data per run as I targeted")
- **Default source = All sources (Overture + OpenStreetMap in one job).** Overlap is merged by source id,
  phone (last 10 digits, same city / ≤ 5 km) and name + place.
- **Category = whole word-parts of the category fields OR keywords in the business name** (categories.py).
  Fixes `%dent%` → student_union and `%tax%` → taxi; adds 27–54 % real matches.
- **OpenStreetMap searches the geocoded city box**, not the named boundary (the "Udaipur" boundary matched the
  whole district + same-named villages and timed out).
- **Each discovery record runs in a SAVEPOINT** (SQLite needs SQLAlchemy's BEGIN recipe, enabled in database.py).
- **Not done, needs a decision:** (1) treat "listed domain has no DNS record, confirmed by a second resolver" as
  Website down immediately instead of waiting 6 h (changes approved spec row 6); (2) widen the area beyond the
  city when it has fewer businesses than asked (measured gain small: Udaipur dentists 102 → 112 at 3× area).

## 2026-11-08 — fifth request (city test: India, Bangladesh, Afghanistan + top 50 countries, 10 ChatGPT rounds)
- **Geocoder takes the first settlement hit** (city / town / village / municipality) of 5, retries without the
  state when the state-qualified lookup only finds a landmark, and trims a city boundary larger than 1.5° to the
  1.5° square around the city's point (inside the boundary; the job and the Find screen show it). Found live:
  Beijing → a 1 × 2 km business district, Ho Chi Minh City → a TV station building, Shenzhen → rejected; all 0.
  After: Shenzhen 0 → 522 available. A state or district hit is still rejected, never trimmed.
- **A repeat search lists what it found again** (`source_job_sightings`). Before: a job whose records an earlier
  job had saved showed nothing under "View businesses", the map, export and website checks (Pimpri-Chinchwad:
  300 found, 19 listed, because its box overlaps Pune's).
- **Find screen offers all 249 ISO countries** (it had 10 — Bangladesh and Afghanistan could not be chosen).
- **Public Overpass stopped answering this machine** after three test processes ran at once (connection refused
  for 40+ cities). The test continued with Overture only. Per-process Overpass lock is a global queue only while
  one API process runs.
- **Open (founder):** production OpenStreetMap data from Geofabrik country extracts processed locally (ChatGPT R5:
  ≈ $24–96 / month, 3–5 developer days) instead of public Overpass — proposed as phase 11.
- **Open (founder + counsel):** Overture's Places guide says joining Places with OSM "may need to carry the Open
  Database License (ODbL) if it is a derivative database". "All sources" joins them. Internal use only today;
  get advice before any merged list leaves the company.
- **Overture results are limited to the chosen country** (address country). Measured in six boxes, 7,834 dentist
  places: none lacks an address country, so the filter is complete there. Shenzhen 522 → 43 CN; Tijuana −377 US.
- **Geocoder uses a settlement only when it carries the requested name** (any language, old or alternative name);
  a city beats a same-named village (Nanded); a name that only matches a building is "not found"; a province-only
  name (Tokyo) is rejected — ChatGPT R6 and Claude agreed not to search a province's admin centre automatically
  (Buenos Aires province → La Plata). Ward names work (Shinjuku 485).
- **Open (founder):** Foursquare Open Source Places (Apache 2.0; names, phone, email, website, socials) as a third
  source for countries where Overture is thin (Iran, China). Needs a free Places Portal account + access token
  created by the founder; the paid Foursquare API terms forbid lead generation, the open dataset does not.
  Proposed as phase 12 (incremental-coverage test first: keep it only if it adds ≥ 20 % verified unique businesses).

</file>

<file path="docs/PHASES.md">
# Phases — SiteBlitz Lead Generator

Legend: ✅ done · 🔨 in progress · ⛔ blocked · ⬜ not started · 🔒 waiting for spec approval

| # | Phase | Status | Owner session | Depends on | Demo criterion |
|---|-------|--------|---------------|------------|----------------|
| 1 | Pipeline repair (install, OSM city search, CSV ids, async crashes, unsubscribe GET) | ✅ | 2026-11-08 audit session | — | `docs/spec/phase-01-pipeline-repair.md` all boxes; 138/138 tests; live Pune/Hyderabad/Munich discovery returns businesses |
| 1b | Overture Places source (lifts the 29-row OSM ceiling), location-aware dedup, job error reasons + definitions | ✅ | 2026-11-08 session, 2nd request | 1 | Udaipur cafés: OSM 29 → Overture 246 found / 225 new; 146 tests |
| 1c | Validate + sanitize every request body, query param and CSV upload; adapter import allow-list | ✅ | same | 1 | 29 new 422/400 tests; 175 tests |
| 1d | SSRF guard on every server-side website fetch (incl. redirects) | ✅ | same | 1 | internal/metadata addresses blocked; 183 tests |
| 1e | Export CSV / PDF (filters + per job), "View businesses" per job | ✅ | same | 1 | CSV + PDF downloaded through the UI for job #9; 185 tests |
| 1f | Data volume + reliability: all-sources search, name + whole-word category matching, phone dedup, shared geocoder, Overpass retries, per-record savepoints, up to 5,000 per search, re-check Needs review | ✅ | 2026-11-08, 4th request | 1b | Udaipur dentists 70→100 new, cafés 225→370, Pune salons 4,065 new / 0 errors; 208 tests |
| 2 | Website Intelligence Engine (verdicts, evidence table, SKIP rules — use Overture `brand` too —, need score, tiers) | ✅ | 2026-11-08, 3rd request | 1 | `docs/spec/website-intelligence.md` acceptance list |
| 3 | Background jobs + SSRF guard + Alembic for all tables + SQLite WAL default | ⬜ | — | 1 | Start a discovery, restart the API mid-run, job resumes with no duplicate businesses |
| 4a | UI contract (verdicts, checks, labels, tiers, 3 indicators, map points, contact log, source health in the API) | ✅ | same | 2 | Every field the new screens read exists in an API response |
| 4b | UI-1: design tokens + app shell/stepper + Find screen with live map (taste skill, spec v2) | ✅ | same | 4a | `docs/spec/ui-redesign.md` criteria for Find + shell, 5 states screenshotted |
| 4c | UI-2: Review screen + evidence drawer + founder labels | ✅ | same | 4b | Review criteria + drawer screenshots |
| 4d | UI-3: Hot leads + Outreach + Settings (honest outreach: no sending, contact log, do-not-contact) | ✅ | same | 4c | Remaining criteria; all 5 screens × 5 states at 1280 + 390 |
| 5 | Honest outreach backend: remove the old fabricated `info@` contacts, template pitches and fake SENT (old Contacts/Campaigns APIs, no longer in the UI); unsubscribe confirmation page | ⬜ | — | 2 | Zero generated addresses; no message marked SENT without a provider event |
| 6 | Pilot: one Indian city, dentists + salons, 200 businesses, 100 calibration / 100 holdout labels | ⬜ | founder | 2, 4 | HOT precision ≥ 90 % on ≥ 30 holdout HOT predictions |
| 7 | Google Places live verification adapter (place ID only stored) | ⬜ | — | 2, API key + counsel | Live `businessStatus` shown on a lead, nothing but place ID persisted |
| 8 | Search verification via API (replaces manual search step) | ⬜ | — | 2, founder picks provider | HOT without manual search, search result stored as a check |
| 10 | Calibration: social-only + phone tops out at 75 (Warm) under the approved weights — founder decision needed | ⛔ | founder | 6 | Decision recorded in DECISIONS.md |
| 11 | OpenStreetMap from Geofabrik country extracts processed locally (no public Overpass); per-country refresh ≤ 7 days | ⬜ | — | 3, founder approves cost | 10 tested cities: 0 public Overpass requests, OSM adds measurable unique businesses over Overture |
| 12 | Foursquare Open Source Places as a third source (Apache 2.0) — incremental-coverage test in 7 thin countries first | ⬜ | — | founder creates a Places Portal token | Same city boxes: ≥ 20 % more verified unique businesses than Overture, or ≥ 20 in a near-empty city |
| 9 | Later: moment-of-need triggers, evidence-based micro-proposals, outcome learning | ⬜ | — | 6 | Defined after pilot results |

## Now
Phases 1, 1b–1e, 2, 4a–4d done on branch `phase-01-pipeline-repair` (2026-11-08), not pushed.

## Next 3
Phase 3 (background jobs, SSRF/size limits already partly done), phase 5 (remove old fabricated-contact APIs), phase 10 (calibration decision), then the pilot (6).

</file>

<file path="backend/app/engines/conversion/sender.py">
"""
Multi-Mailbox Sender & Token Resolver (Phase 5).

Rotates across verified agency mailboxes to balance sender reputation,
replaces dynamic opt-out and address tokens, and logs dispatch audits.
"""

from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import List, Optional
import urllib.parse

from backend.app.models.campaign import MessageStatus, OutreachMessage
from backend.app.models.contact import RoleLevel


@dataclass
class DeliveryReport:
    """Outcome of message dispatch."""

    success: bool
    sender_used: str
    recipient: str
    message_id: int
    sent_at: datetime
    error: Optional[str] = None


class MultiMailboxSender:
    """
    Manages agency sender identity rotation and dynamic token resolution.
    """

    DEFAULT_MAILBOXES = [
        "[REDACTED]",
        "[REDACTED]",
        "[REDACTED]",
        "[REDACTED]",
    ]

    PHYSICAL_POSTAL_ADDRESS = "100 Innovation Way, Suite 400, New York, NY 10001"
    COMPANY_NAME = "SiteBlitz Intelligence"
    BASE_UNSUBSCRIBE_URL = "http://localhost:8000/api/v1/qualification/unsubscribe"

    def __init__(self, mailboxes: Optional[List[str]] = None):
        self.mailboxes = mailboxes or list(self.DEFAULT_MAILBOXES)
        self._rotation_index = 0

    def get_next_mailbox(self, role_level: Optional[RoleLevel] = None) -> str:
        """
        Select next sender mailbox using round-robin rotation.
        """
        if not self.mailboxes:
            return "[REDACTED]"

        chosen = self.mailboxes[self._rotation_index % len(self.mailboxes)]
        self._rotation_index += 1
        return chosen

    def resolve_message_tokens(
        self,
        body_text: str,
        recipient_email: str,
        sender_mailbox: str,
    ) -> str:
        """
        Replace compliance and identity tokens with concrete values.
        """
        encoded_email = urllib.parse.quote_plus(recipient_email)
        opt_out_link = f"{self.BASE_UNSUBSCRIBE_URL}?email={encoded_email}"

        resolved = body_text.replace("{{UNSUBSCRIBE_LINK}}", opt_out_link)
        resolved = resolved.replace("{{PHYSICAL_ADDRESS}}", self.PHYSICAL_POSTAL_ADDRESS)
        resolved = resolved.replace("{{SENDER_COMPANY}}", self.COMPANY_NAME)
        resolved = resolved.replace("{{SENDER_MAILBOX}}", sender_mailbox)

        return resolved

    def dispatch(
        self,
        message: OutreachMessage,
        role_level: Optional[RoleLevel] = None,
        simulate: bool = True,
    ) -> DeliveryReport:
        """
        Dispatch outbound message with sender rotation and token resolution.
        """
        sender = self.get_next_mailbox(role_level)
        message.sender_mailbox = sender

        # Resolve tokens
        message.body_text = self.resolve_message_tokens(
            body_text=message.body_text,
            recipient_email=message.recipient_email,
            sender_mailbox=sender,
        )

        now = datetime.now(timezone.utc)
        message.status = MessageStatus.SENT
        message.sent_at = now

        return DeliveryReport(
            success=True,
            sender_used=sender,
            recipient=message.recipient_email,
            message_id=message.id,
            sent_at=now,
        )

</file>
</project_context>

<topic>
# Topic

The founder's words (Hinglish, verbatim):

> yeh ek project hai isse analyze kijiye and ab me chata hun ki aap reserach kijiye for site blizt ke liye best
> domain kya hoga [eg. .in , .com] yeh bhi verify kijiye ki konse avalable hai.. and hume emails send karne hai
> daily basis pe atleast 1k daily busniess ko toh atoleast kitne gmails chaiye honnge, abhi hum multiple normal
> gmails se karte hai toh spam em jatya hai iska reason analyze karke muje bataye that kyun aesa hota hai..
> busniess gmails banane padege kya ???? busniess gmail kya hota haia??? kitne paise lagege and multiple
> bussniess gmails ho toh kitne paise lagege??? and agar busniess mails lene hai toh multiple roles ke liye lenge
> like ceo , cto ya bjo bhi roles hote hai yeh aapko desicde karna haia nd aagara required ho to hi and aapke
> according next 1 year ke liye kitna paisa kkagega and 1 month abhi setup ke kitne lagege maintance ke kiten
> lagege??

In English: pick and verify the best domain for SiteBlitz; the team wants to email at least 1,000 businesses a
day - how many mailboxes; why their current multiple free Gmail accounts land in spam; do they need business
email (Google Workspace), what it is and what it costs for one and for many; which role mailboxes (CEO, CTO...)
only if really needed; 1-month setup cost, monthly maintenance and 12-month total.

Claude Code has already researched this (see `facts.md` - every number there has a source or a registry check).
Your job is to challenge that plan, not to repeat it.

## Agenda

1. Main domain: `siteblitz.in` (available; .in needs NIXI e-KYC, no privacy proxy) vs a .com variant such as
   `siteblitzstudio.com` - and does the French company "SiteBlitz" (siteblitz.ai, same business, registered
   2026-06-16) mean the founder should rename before spending on the brand?
2. Why cold mail from several free @gmail.com accounts lands in spam - ranked causes. Is the fabricated-address
   bounce problem (37 of 38 exported emails are generated) the main one?
3. Inbox math for 1,000 cold emails/day: 30 inboxes x ~33/day, 10 sending domains x 3 inboxes, 3-5 week ramp.
   Right numbers for Indian small-business recipients (mostly @gmail.com addresses)?
4. Provider for the cold inboxes: Google Workspace in a separate org (Starter Rs 270/user/month) vs Base
   (Rs 99, 20-user cap) vs Zoho / Microsoft 365 / dedicated cold-inbox resellers - and the AUP suspension risk.
5. Roles: 1 paid founder mailbox + free aliases (hello@, support@, billing@), no CEO/CTO mailboxes; how to name
   the cold inboxes honestly when the founder stays anonymous on the site.
6. Costs: month 1 ~Rs 29.8k, then ~Rs 22.5k/month, year 1 ~Rs 2.78 lakh. Paid sender/warm-up tool (Instantly)
   vs building sending into the lead generator (phase 5). What is missing, wrong or overpriced?
7. Go / no-go gates and staging: verified-address supply (~22k real addresses/month), India DPDP + recipient
   rules, and whether 1,000 emails/day is even the right channel for Indian local businesses vs WhatsApp /
   warm channels. What staged plan would you commit to?

Answer each agenda point by number: agree / disagree because ... / need data: ... . End with the list of points
still open.

Rules for your answer: give exact numbers (INR, counts, days), say where each number comes from, and mark
anything you are not sure of as "unverified". Claude Code will check every claim against the web and the code
before accepting it.
</topic>
