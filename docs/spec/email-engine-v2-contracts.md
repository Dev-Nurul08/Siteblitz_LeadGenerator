# Email engine v2 - contract between the lead generator and the SiteBlitz website (2026-11-12)

Approved spec: `docs/spec/email-engine-v2.md` (founder `go` 2026-11-12). This file fixes the shapes both repos use.
Copy kept in `E:\Temp\SiteBlitz\docs\spec\outreach-contract.md`; if one changes, change both the same day.

Why two repos: the always-on parts (unsubscribe, suppression list, snapshot pages) must answer while the founders'
laptop is off (spec rows 12, 13, 18). They live on the website stack (Next.js + MongoDB Atlas). Sending, scheduling,
replies and the batch screen live in the lead generator on the laptop. Nothing is ever sent from the website.

## Shared values
| Name | Where | Value |
|---|---|---|
| `OUTREACH_API_KEY` | website env + lead-generator `.env` | random 32+ byte secret; lead generator sends `Authorization: Bearer <key>` |
| `OUTREACH_SIGNING_SECRET` | website env + lead-generator `.env` | random 32+ byte secret for HMAC tokens |
| `OUTREACH_PUBLIC_BASE_URL` | website env + lead-generator `.env` | public origin that serves `/u/` and `/s/` (today `https://siteblitz.vercel.app`; later the sending domain) |
| Email hash | both | `sha256_hex(email.strip().lower())` - the website never stores a plain address |
| Token | both | `base64url(payload) + "." + base64url(HMAC_SHA256(secret, base64url(payload)))`, no padding; payload = compact JSON with sorted keys `{"h":"<email hash>","m":"<send record id>","v":1}` |

## Website endpoints
| Method + path | Auth | Request | Response | Rules |
|---|---|---|---|---|
| `GET /u/{token}` | none | - | HTML page: "Stop emails from SiteBlitz to this address?" + one button (form POST to the same URL) | Never unsubscribes on GET (link scanners). Bad token -> 400 page. `noindex` |
| `POST /u/{token}` | none | RFC 8058 body `List-Unsubscribe=One-Click` (form-encoded) or the page's form | 200 (HTML confirmation for the form; plain `ok` for one-click) | Verify HMAC; upsert suppression (reason `unsubscribe_one_click` or `unsubscribe_link`); return 200 only after the write succeeds; idempotent; no redirect, no login, no cookie, no CAPTCHA |
| `POST /api/outreach/suppressions/check` | Bearer | `{"hashes": ["<hex>", ...]}` (max 500) | `{"suppressed": ["<hex>", ...], "checked_at": "<ISO>"}` | `Cache-Control: no-store`; 401 without the key; 503 if the DB is unavailable (the lead generator then sends nothing) |
| `POST /api/outreach/suppressions` | Bearer | `{"hash": "<hex>", "reason": "reply_stop" \| "hard_bounce" \| "complaint" \| "manual", "source": "<text, max 200>"}` | `{"ok": true}` | Upsert; the first reason and time are kept, later ones appended to a history array |
| `GET /api/outreach/suppressions?since=<ISO>` | Bearer | - | `{"items": [{"hash", "reason", "created_at"}], "next": "<ISO or null>"}` | Max 1,000 per page |
| `POST /api/outreach/snapshots` | Bearer | see Snapshot below | `{"slug": "...", "url": "<base>/s/<slug>", "expires_at": "<ISO>"}` | Slug = business-name words (ASCII, max 40 chars) + "-" + 10 random base32 chars |
| `GET /s/{slug}` | none | - | the 3-layer snapshot page | `noindex, nofollow`; after `expires_at` or removal -> 410 page with no business data |
| `POST /s/{slug}/remove` | none | form button on the page | 200 "removed" page | Sets `removed_at`; removal is final |

## Snapshot (request body of `POST /api/outreach/snapshots`)
```json
{
  "business_name": "string, max 120",
  "city": "string, max 80",
  "vertical": "salon_beauty | coaching_tuition | retail_showroom | other",
  "observation": {"type": "SOCIAL_ONLY | NO_VIEWPORT | SITE_DOWN", "text": "one dated, bounded sentence, max 300", "checked_at": "ISO"},
  "evidence_image_base64": "optional PNG/JPEG, max 400 KB after decoding",
  "concept_demo": "salon | coaching | showroom",
  "offer": {"price_inr": 7999, "scope_lines": ["max 6 lines, each max 120"], "yearly_costs_note": "max 200"},
  "recording": {"url": "optional https URL of the founder's recorded overview", "transcript": "required if url is set, max 2,000"},
  "reply_email": "the sender mailbox address",
  "expires_in_days": 30
}
```
Page layers (spec row 7): (1) business name, the observation, a one-line offer; (2) date checked, the evidence image,
the concept preview built from the matching demo with the business name and city only (no copied photos), the label
"Illustrative concept prepared by SiteBlitz. Not your current website and not an existing client project."; (3)
scope, one-time price, yearly costs note, the recorded overview (no autoplay, transcript shown) if present, a
"Reply by email" mailto button to `reply_email`, the removal button. No analytics scripts, no third-party trackers on
`/s/` and `/u/`. Page requests are logged server-side as raw counts only (spec row 16: raw, not "viewed").

## Lead-generator side
- Builds `List-Unsubscribe: <{base}/u/{token}>, <mailto:{mailbox}?subject=unsubscribe>` and
  `List-Unsubscribe-Post: List-Unsubscribe=One-Click` on every campaign message, and the body line
  `Reply "stop" or unsubscribe here: {base}/u/{token}`.
- Before every SMTP submission: `POST /suppressions/check` for that hash; any non-200 = do not send and pause
  (spec row 11). A local copy is for display only and never authorises a send.
- "stop" replies, hard bounces and complaints are written to `POST /suppressions` first, then locally.
- Creates a snapshot only after a reply labelled `sample_requested` or `interested`, and puts the returned URL in the
  AI-drafted reply, which waits for the founder's approval.

## Byte rules and known-answer vector (added 2026-11-12 from the website implementation, commit 35fdc03)
- The secret is the env value with surrounding whitespace removed, used as UTF-8 bytes; a secret shorter than 32
  characters counts as missing (the website answers 503).
- The HMAC message is the base64url payload string (ASCII), not the raw JSON.
- base64url without `=` padding on both parts.

| Input / output | Value |
|---|---|
| email (before strip + lower) | `"  Owner@Example.com "` |
| h | `c8cd3c6427301eaf6665bccacd65ddb614527acc843a15463e3faba57124c351` |
| m | `"send-0001"` |
| secret | `kat-secret-not-for-production-0123456789` |
| payload | `{"h":"c8cd3c6427301eaf6665bccacd65ddb614527acc843a15463e3faba57124c351","m":"send-0001","v":1}` |
| token | `eyJoIjoiYzhjZDNjNjQyNzMwMWVhZjY2NjViY2NhY2Q2NWRkYjYxNDUyN2FjYzg0M2ExNTQ2M2UzZmFiYTU3MTI0YzM1MSIsIm0iOiJzZW5kLTAwMDEiLCJ2IjoxfQ.CyQyXv0246O-c9S4tTeSF4c3xo-pCWu4M_Uj6ituq3Y` |

Website limits chosen where this contract was silent (website D19): suppression history capped at 100 events per
address; `since` paging includes the boundary item (the caller removes duplicates); snapshot life 1-30 days; scope
1-6 lines; recording URL must be https; image checked by PNG/JPEG header, max 409,600 bytes; every API answer also
carries `ok: true/false`. `/u/{token}/` with a trailing slash gets a 308 to the URL without it - never generate one.
