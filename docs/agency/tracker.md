# Agency tracker (a spreadsheet the delivery owner keeps; business data stays outside the repo)

Start file: `E:\SiteBlitz-World-Business-Data\_work\agency_list\2026-11-12\shortlist_50.csv` (built 2026-11-12).
Open it in Excel or Google Sheets and add the columns below. Status names reuse the 2026-11-10 lifecycle
(`docs/debate/2026-11-10-outreach-lifecycle-to-payment/RESULT.md` section D) where one exists.

## Columns
id · agency · city · country · website · route (form / email / linkedin) · contact used · source URL of that contact ·
observation used · status · first contact date · follow-up 1 date · follow-up 2 date · reply date · reply summary ·
objection (no need / has developers / budget / stack / trust / timing / other) · brief received (Y/N) · quote number ·
quote amount · advance received (date, amount) · balance received (date, amount) · hours spent · next action ·
next action date · do-not-contact (Y/N)

## Statuses
| Status | Meaning |
|---|---|
| `NEW` | On the list, not checked yet |
| `QUALIFIED` | Founder looked at the site: real client work, stack fits, one recipient chosen |
| `TOUCH_1` / `TOUCH_2` / `TOUCH_3` | First message / follow-up 1 / follow-up 2 sent |
| `QUALIFYING` | They replied with interest or a question |
| `BRIEF_RECEIVED` | A brief arrived (form or email) |
| `AWAITING_DEPOSIT` | Quote sent |
| `READY_TO_BUILD` | Advance received and all inputs in |
| `STAGING` | Staging link sent |
| `AWAITING_BALANCE` | Staging approved, balance invoice sent |
| `DELIVERED_PAID` | Balance received, handover sent |
| `PAUSED_OOO` | Out of office; resume 2 business days after return |
| `CLOSED_NO_REPLY` | No reply 5 business days after `TOUCH_3` |
| `CLOSED` | Said not now / has own developers |
| `SUPPRESSED` | Said no / stop / unsubscribe, or hard bounce - never contact again on any channel |

## Weekly targets and stop rules (RESULT row 15; experimental targets, not forecasts)
| Week | New agencies contacted | Evidence to look for |
|---|---|---|
| 1 (12-18 Nov) | up to 10, after the site and mailbox work | working enquiry path, honest proof, 50 qualified |
| 2 | 40 | real replies and objections, aim for 2 briefs |
| 3 (from 26 Nov) | 40 (up to 2 a day may be US agencies) | first paid advance by 2 Dec |
| 4 | up to 40 while delivering | 1 pilot delivered and fully paid by 11 Dec |
| 5-6 | max 20 a week | 2 paying agencies, first repeat brief |
| 7-8 | best segment only | 3 paying agencies incl. 1 repeat (10 Jan 2027 review) |

Stop / change rules: a complaint, a provider warning or a suppression failure -> pause at once · about 40 qualified
contacts past their follow-up window with no positive reply -> fix targeting or offer before more · several briefs but
no accepted quote -> look at budget, scope, proof, payment terms · a package overruns its hours twice -> fix it ·
26 Dec with no advance after ~100-150 qualified contacts and two revisions -> pause the agency offer, contract work
becomes the main income.
