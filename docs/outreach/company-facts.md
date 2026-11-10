# COMPANY_FACTS - SiteBlitz (attach to every writer request)

Status: approved 2026-11-10 (founder `go`). Fields marked `TO FILL` are blanks the founder fills in `.env`; the
writer puts the `.env` values into this file's text before sending it to the model.
While any `TO FILL` field that a channel needs is empty, the writer returns `HOLD` for that channel.

Sources: `E:\Temp\SiteBlitz\src\lib\offer.ts` (prices, payments, delivery, inclusions, exclusions),
`src\lib\site.ts` (location line, phone, site URL), `src\lib\demos.ts` (demo pages). If any of these files changes,
update this file the same day. `offer.ts` wins on any conflict.

## Identity
| Field | Value |
|---|---|
| Studio name | SiteBlitz |
| Who we are, in one line | A small web studio based in Gujarat that builds websites for businesses across India |
| Location wording | "based in Gujarat". Never name another city or claim an office (FD-22, truthful location) |
| Sender name used in signatures | `TO FILL` (set `SITEBLITZ_SENDER_NAME` in `.env`; founder decision: first name only, or full name. The site shows no founder name, per FD-28/29) |
| Reply email address | `TO FILL` (set `SITEBLITZ_REPLY_EMAIL` in `.env`: the sending domain's mailbox. hello@siteblitz.in is NOT live, so mail to it bounces, see site.ts) |
| Postal address for email and letter footers | `TO FILL` (set `SITEBLITZ_POSTAL_ADDRESS` in `.env`; kept out of git because it is personal) |
| WhatsApp / phone (public on the site) | +91 92744 90242 |
| Website | https://siteblitz.vercel.app |
| GST | Not GST-registered, so prices are final and no GST is added |
| Clients, reviews, case studies | None yet. Never mention clients, results, reviews, awards, team size or years of experience |

## Packages (India, INR)
| Package | Price | Pages | Paid as | Delivery | Includes |
|---|---|---|---|---|---|
| Launch | ₹7,999 | 1 page | ₹4,000 deposit + ₹3,999 balance | 2 working days after ready-to-build | One responsive page; services and business information; WhatsApp and call buttons; basic technical SEO setup; one consolidated revision round |
| Business | ₹17,999 | 3 pages | ₹9,000 deposit + ₹8,999 balance | 7 working days after ready-to-build | Three agreed pages; mobile-first design; service information and enquiry journey; WhatsApp, call and enquiry options; basic technical SEO setup; one consolidated revision round |
| Custom | Quoted | Quoted | Milestones in the quotation | Written schedule in the quotation | E-commerce, larger catalogues, bookings, more pages or integrations |

Short price line for first messages: "starting at ₹7,999 (domain and hosting are separate)".
Outside India: no price in the first message. Say a written quotation is sent on request.

## Qualifying questions (asked one per message, in this order, after a positive reply)
1. Are you the person who decides on the website?
2. Does the ₹7,999-₹17,999 range work for you?
3. Would you like it live within 60 days?

## Not included in any package
Domain registration and yearly renewal · third-party hosting or subscription charges · paid plugins, premium fonts,
stock photos or software licences · e-commerce, online payments or advanced booking systems · new pages or features
beyond the agreed scope · advertising spend or ongoing marketing · guaranteed Google rankings, traffic, enquiries or
sales · unlimited redesigns, content writing or ongoing edits.

## Ready-to-build (the delivery clock starts only when all five are true)
1. The pages and features are confirmed in writing.
2. The client's content, images and business details are with us.
3. Any access we need (domain, accounts) is shared.
4. The first payment is received.
5. A start date is agreed.

## Payment moments
1. Written scope accepted -> deposit invoice (₹4,000 or ₹9,000). No design or build starts before it is received.
2. Staging site + one consolidated revision approved in writing -> balance invoice (₹3,999 or ₹8,999).
3. Balance received -> site goes live; logins and the domain are handed over in the client's name.
Payment status comes only from the bank / UPI record.

## Demo pages (sample sites with invented brands, shown as examples, never as client work)
| Vertical | Demo URL | Customer word | What the page gives their customers (from demos.ts) |
|---|---|---|---|
| salon_beauty | `TO FILL` (route /demo/salon exists only on branch v2-redesign) | clients | Services with prices, an appointment request and timings |
| coaching_tuition | `TO FILL` (route /demo/coaching, same) | parents and students | Courses, batch timings and fees, and an admission enquiry without a phone call |
| retail_showroom | `TO FILL` (route /demo/showroom, same) | customers | A catalogue with sizes, materials and price ranges, and a one-tap WhatsApp enquiry per product |
| other | none | customers | Services, location and contact details on one page |

The demo pages are NOT live: siteblitz.vercel.app/demo/salon, /coaching and /showroom returned HTTP 404 on 2026-11-10,
because the redesign (branch v2-redesign of E:TempSiteBlitz) is not deployed. Fill the URLs only after deploying.
Demo links are allowed only in email touch 2, WhatsApp replies and letters. Never in email touch 1 or a social message request.
