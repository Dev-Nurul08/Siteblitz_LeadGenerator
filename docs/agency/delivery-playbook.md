# Delivery playbook - so "management was not right" never happens again

Source: RESULT row 4 (01_chatgpt.md section 3). One founder is the **delivery owner** for each agency: the only
person who sends dates, prices and promises to that agency. The other founder never sends a competing estimate.

## Project record (one per project, in the tracker or a shared doc)
Quote number · agency · approver · scope (sections) · stack · price · advance received (date, amount, reference) ·
ready-to-build date · staging target · handover target · inputs still missing · feedback received · change requests
(each with a price) · balance received · handover date · hours spent (log every session) · notes.

## Step by step
| Step | What happens | Message |
|---|---|---|
| 1. Quote accepted | Send the advance details; list missing inputs | "Thank you. Advance details are below. We still need: [list]. Dates start when these are in." |
| 2. Ready-to-build | All 6 items true (`offer-and-scope.md`) | "Everything is in. Staging on [date], handover on [date]." |
| 3. Build | Written update at least every second working day, and the same day anything blocks | Update format below |
| 4. Staging | Staging link + checklist of what to review; ask for ONE consolidated list of changes | "Staging is ready: [link]. Please send all changes in one list by [date]. Anything outside the scope we'll quote first." |
| 5. Changes | Sort each item: in scope (do it) / defect (fix free) / change request (quote first) | "Done: [items]. These two are new features; quote: [amount]. Shall we add them?" |
| 6. Balance | Ask for the balance after the agency approves staging in writing | "Thanks for approving. Balance ₹[amount] is due now; handover follows on receipt." |
| 7. Handover | Send the handover pack (below) | "Handover pack attached. Defect fixes are free until [date + 14 days]." |
| 8. Close | Day 7 after handover: ask for the next brief and permission to mention the work privately | "Is there another brief we can quote? And may we show this build privately to other agencies, without your client's name?" |

## Written update (always this shape)
> Completed: [...]
> Next: [...]
> Blocked / decision needed: [... or "nothing"]
> Delivery date: unchanged / revised to [date] because [reason]

Reply to every agency message within one business day. Not round-the-clock.

## Handover pack (checklist)
- [ ] Source code (zip or repository transfer) and how to run it
- [ ] Deployment: where it runs, how to redeploy, DNS records changed
- [ ] Access and ownership list: every account, who owns it, what was transferred
- [ ] Third-party costs and licences (fonts, images, services), who pays
- [ ] Form: where enquiries go, tested on [date] with a test entry
- [ ] Tested on: phone (width 390) and desktop (width 1280), [browsers]
- [ ] Known limitations
- [ ] Defect-fix window end date

## Change request vs defect
- **Defect:** the site does not do what the accepted scope says (broken link, form not delivering, layout breaks on
  phone). Free, within 14 days.
- **In-scope change:** part of the one consolidated round. Free once.
- **Change request:** anything new (page, section, feature, new design direction). Written price first.

## Time tracking
Log hours per project. Allowances: landing 14 h, three-page 28 h (RESULT row 5). If a package overruns twice, stop
selling it unchanged: fix the scope or the price (RESULT row 15 stop rule).
