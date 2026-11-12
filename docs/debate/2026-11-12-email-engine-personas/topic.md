# Topic - SiteBlitz email engine v2: personas, content that gets read, a creative layer, worldwide sending from the admin panel, and an AI-run daily conversation loop - 2026-11-12

## The founders' words (translated from Roman Hindi)
"The agency idea is very good, but focus mainly on this. From the data we extracted - the whole world, 248
countries - we mail X people every day, from the admin panel, in a single click; we will set up whatever SMTP is
needed. The main point is the content: what a mail needs so it does not go to spam, and so that when the client or
their assistant reads it, it feels worth it and they understand immediately. Think of creative ways - an audio
message that reads the mail, or a summary - so it feels unique and interactive and people read it at least once. I
guarantee nothing; you and ChatGPT analyse everything: how every kind of person thinks after receiving a mail; test
with multiple different personas. Then set up the mailing system (WhatsApp later). My motive: I open my laptop and
say 'start today's day'; you check yesterday, read the replies, tell ChatGPT, decide who is interested and what to
reply - complete flows. You and ChatGPT handle clients and conversations; my friend and I deliver the sites. If you
cannot send daily yourself, add scheduling through the admin panel."

## Agenda
1. Personas: how 8-10 different recipients of a cold website email actually read it (who opens it - owner, receptionist, assistant, manager; device; first 3 seconds; what makes them delete, mark as spam, forward or reply), with evidence where it exists. Test the three sample emails in claude-position.md against each persona.
2. Email anatomy that both survives spam filters (Gmail / Yahoo / Outlook rules in force in 2026) and is understood in 5 seconds by the owner or an assistant: subject, preview text, first line, a one-line "in short" summary, the observation, offer, price, call to action, sender, opt-out, plain text vs HTML, links, images, attachments, length - per touch (1 / 2 / 3).
3. The creative / interactive layer the founders asked for (an audio message that reads the mail, a summary, an "interactive UI"): judge each option - audio file, audio link, a personalised one-page "Opportunity Snapshot" per business (their observations, a labelled concept preview, a 30-60 s audio summary, price, one-tap reply / WhatsApp), AMP email, GIF - on deliverability, trust, law (AI-voice disclosure) and effort. Which touch gets which element.
4. Worldwide: which countries can receive this email now (tiers by law and by language), how the daily number X is chosen and ramped (inboxes, domains, warm-up, verification, gates), and which leads out of 86.75 M qualify.
5. Sending from the admin panel: one click to approve the day's batch, a scheduler that sends inside each recipient's local window, where it runs (founders' laptop + Task Scheduler, a small server, GitHub Actions), sending infrastructure that the provider's terms allow (the founders say "we will set up SMTP"), bounces, suppression, automatic stop rules.
6. The daily loop "start my day": what Claude Code does each morning (yesterday's numbers, read replies, classify, draft replies), what ChatGPT does, what the founders must still do, whether any reply may go out without a human click, and which metrics are honest ("how many read" without tracking pixels).
7. Build order, gates and pre-send tests (including a synthetic persona test of every template before real sending), and what the public website must show before the first email (it currently shows invented testimonials).

Attached: claude-position.md (Claude Code's view, written before your reply, with three sample emails to test),
docs/spec/outreach-engine.md (the spec approved on 2026-11-10), research-deliverability.md (a Claude Code research pass, 2026-11-12).

Answer each agenda point by number: agree / disagree because ... / need data: ... . For point 1, give a table:
persona x (who reads, device, first 3 seconds, delete trigger, reply trigger, verdict on samples A / B / C). End with
the list of points still open.
