# Email engine v2 - what the founders do to go live (2026-11-12)

Everything on Claude Code's side of phases E1-E5 is built and tested (lead generator: 795+ tests; website: 368
tests). What is left needs the founders' accounts, money or hands. Do the steps in order; each step says how to know
it worked. Spec: `docs/spec/email-engine-v2.md`. Commands are for PowerShell unless marked "Git Bash".

## 1. Push the work (Claude's push is blocked by the Claude OS guard)
```
cd E:\tmp\Siteblitz_LeadGenerator
git push origin phase-01-pipeline-repair
cd E:\Temp\SiteBlitz
git push origin v2-redesign
```
Worked if: both commands end with `-> phase-01-pipeline-repair` / `-> v2-redesign` and no error.

## 2. Website: switch on the outreach endpoints (O2)
The truthful site is live: another session deployed `v2-redesign` (aa116dc, incl. `/u/`, the suppression API and
`/s/`) with `NEXT_PUBLIC_SITE_URL` (website commit fa3cd13). Checked 2026-11-12: 0 invented reviews / results, no
"Studio Mumbai", no withdrawn prices. The outreach routes answer 503 `outreach_not_configured` until two secrets exist.
1. Make two random secrets (run twice, keep both private, never commit them):
   `node -e "console.log(require('crypto').randomBytes(32).toString('base64url'))"`
2. In `E:\Temp\SiteBlitz`: `vercel env add OUTREACH_API_KEY production` (secret 1) and
   `vercel env add OUTREACH_SIGNING_SECRET production` (secret 2). Not in Preview (shared database, `docs/DEPLOY.md`).
3. Redeploy the same build the way the website session does (its `docs/DEPLOY.md` records the release path and the
   rollback target).
4. Worked if: `curl -s -X POST https://siteblitz.vercel.app/api/outreach/suppressions/check -H "Content-Type: application/json" -d "{\"hashes\":[]}"`
   answers 401 (key required) instead of 503.
- Decision for you: Vercel's free Hobby plan is for non-commercial use only; move to a paid plan or another host.

## 3. Lead generator `.env` (in `E:\tmp\Siteblitz_LeadGenerator\.env`, never committed)
```
OUTREACH_API_KEY=<secret 1, same as Vercel>
OUTREACH_SIGNING_SECRET=<secret 2, same as Vercel>
OUTREACH_PUBLIC_BASE_URL=https://siteblitz.vercel.app
ANTHROPIC_API_KEY=<your key - the AI writer and reply labels>
SITEBLITZ_SENDER_NAME=<real first name, or full name>
SITEBLITZ_REPLY_EMAIL=<a mailbox from step 4>
SITEBLITZ_POSTAL_ADDRESS=<a postal address; a PO box or office is safer than home - it goes to strangers>
BOUNCER_API_KEY=<from usebouncer.com, about $8 per 1,000 checks>
MAILBOX_<SLUG>_PASSWORD=<one line per mailbox from step 4>
```
After installing or upgrading `anthropic`, run the jiter fix in `CLAUDE.md` (Smart App Control).

## 4. Sending domains and mailboxes (spec row 8)
1. Brand check first (`docs/agency/brand-check.md`): a French company uses "SiteBlitz" for the same service.
   Another session today planned `siteblitz.in` + Google Workspace for hello@ - fine for normal mail, never for cold
   email.
2. Buy 2 separate sending domains at a registrar you control (keep the registrar login yourself).
3. Mailforge (mailforge.ai): 10 mailbox slots ($3 each per month = $30), connect the 2 domains by DNS (do not hand
   over the registrar account), create 6 mailboxes, 3 per domain, each under a real founder name.
4. Add each mailbox to the app (password stays in `.env`, never in the request):
   ```
   curl -s -X POST http://127.0.0.1:8000/api/v1/outreach/mailboxes -H "Content-Type: application/json" -d "{\"slug\":\"FOUNDER1\",\"address\":\"<address>\",\"display_name\":\"<real name>\",\"smtp_host\":\"<from Mailforge>\",\"smtp_port\":587,\"smtp_tls\":\"starttls\",\"imap_host\":\"<from Mailforge>\",\"imap_port\":993,\"imap_tls\":\"ssl\",\"username\":\"<address>\"}"
   ```
5. Worked if: `.venv\Scripts\python.exe scripts\outreach_worker.py --check` passes.

## 5. Launch gates (spec row 17) - the log is `docs/outreach/e6-launch-gates.md`
- Seed test: approve a batch of 1 to your own Gmail, Outlook and Yahoo test addresses (add them as a fictional
  business only in a copy of the database, never in the real list) and check "Show original": SPF, DKIM, DMARC pass,
  both `List-Unsubscribe` headers present and inside the DKIM signature.
- Unsubscribe end to end: click the link in a seed email, then run `/start-day`; the address must be on the list.
  Laptop-off test: switch the laptop off, unsubscribe from a seed email on your phone, switch on - the queued
  message to that address must not go.
- Verify the 26 candidates: `curl -s -X POST http://127.0.0.1:8000/api/v1/outreach/eligibility/evaluate -H "Content-Type: application/json" -d "{\"verify\": true}"` (about $0.21).
- 10-reader test: show 10 business owners you know a pilot email on their phone for 5 seconds; at least 8 must say
  who wrote, why, what is offered and what to do next.
- Read the first 20 emails the AI writes (outreach spec row 6) before approving them.

## 6. Daily use
- Start the app: `.venv\Scripts\python.exe run_all.py`. In Claude Code type `/start-day`.
- Answers: `send` (replies + batch), `send replies`, `send batch`, `hold <n>`, `reject <n> <reason>`,
  `regenerate <n>`, `replied <business> whatsapp`, `stop <business> whatsapp`.
- Sending windows Tue-Thu 09:00-11:30 and 14:00-16:30 IST: run
  `.venv\Scripts\python.exe scripts\outreach_worker.py` with the laptop on (it stops at 16:30).
- Inbox reading at least every 24 h: `.venv\Scripts\python.exe scripts\outreach_reconcile.py`, or register the
  Task Scheduler jobs once with `powershell -ExecutionPolicy Bypass -File scripts\register_outreach_tasks.ps1`.
- Instagram-only businesses: the batch screen's "Founder checks" panel - open the profile, confirm no website link
  and the email you see (about 20-30 s each).
- Ramp: stage 0 (nothing new) until the gates pass, then one step at a time:
  `curl -s -X POST http://127.0.0.1:8000/api/v1/outreach/settings/ramp -H "Content-Type: application/json" -d "{\"stage\":1,\"changed_by\":\"founder\",\"note\":\"launch gates passed\"}"`
- Recordings: put your own 30-60 s voice overview per vertical (https URL + exact transcript) in
  `docs/outreach/recordings.json`; empty = no audio on the sample page. No AI voice.

## 7. The honest numbers to expect
- Eligible today: 0 (no verifier key). Eligible once verified: 26 (all "page does not fit a phone"; Surat 8,
  Ahmedabad 5, Rajkot 5, Vadodara 2, Valsad 2, 1 each Navsari, Bharuch, Gandhinagar, Jamnagar) - enough for about 2
  weeks of the 10-a-day start, not more. To grow the pool: the Instagram founder checks (biggest source) and a longer
  crawl at night (`scripts/pool_e1.py` with `--min-free-mb 500`), about 2-3 eligible per 1,000 websites.
- No "opened" count exists by design. Count replies, positive replies, samples, quotes, payments.
