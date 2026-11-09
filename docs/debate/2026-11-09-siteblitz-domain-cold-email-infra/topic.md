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
