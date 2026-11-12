# Research - deliverability rules, sending services, verification, reading behaviour, audio/video, AI-voice law - 2026-11-12

Claude Code subagent (web research). "Unverified" = secondary source only or page not opened.

## 1. Mailbox-provider rules
- Gmail (support.google.com/a/answer/81126, undated): all senders need SPF or DKIM, PTR, TLS, spam rate < 0.3 %; bulk sender ~5,000+/day to personal Gmail needs SPF + DKIM + DMARC (p=none ok), alignment, RFC 8058 one-click unsubscribe for marketing; aim < 0.10 %, never 0.30 %. Same page: "Don't send messages to people who didn't sign up", "Don't purchase email addresses", "Start with a low sending volume", "Google doesn't track open rates".
- Gmail FAQ (answer/14229414, undated): "Starting November 2025, Gmail is ramping up its enforcement"; bulk status is permanent; subdomains count to the parent domain; honour unsubscribes within 48 h.
- Yahoo (senders.yahooinc.com/best-practices, undated): no volume threshold; spam < 0.3 %; bulk needs SPF + DKIM + DMARC, one-click List-Unsubscribe + a body link, honoured within 2 days.
- Microsoft Outlook.com (techcommunity blog, 2025-04-02, upd. 04-30): > 5,000/day needs SPF + DKIM pass and DMARC p=none or stricter, aligned; since 2025-05-05 non-compliant mail goes to Junk; unsubscribe link "recommended".
- Gmail Program Policies (support.google.com/mail/answer/16734397, upd. 2026-10-20): "Don't use Gmail to distribute spam or unsolicited commercial mail."
- Google Workspace AUP (2025-10-13): bans "unsolicited mass email, promotions, advertisements or other solicitations ('spam')".

## 2. Sending services
- Instantly: Growth $47/mo ($37.60 yearly) - 5,000 emails, 1,000 contacts, unlimited mailboxes + warm-up (instantly.ai/pricing, undated). Terms (Claude Code read them directly, "Last Updated: November 10, 2026"): §1.10 Permitted Purpose includes "Subscriber's own direct business-to-business (B2B) sales"; §4.3(b) subscriber is the sole "sender" and "initiator"; §4.6(b) subscriber alone responsible for compliance incl. CAN-SPAM; §6.7 "Subscriber will only process such data: (a) with valid, informed consent of the data subject" (rest of the list not read); §6.8 Instantly obtains no consents for the subscriber. Sending Policy (2026-10-13): opt-outs need "immediate action". AirMail price: not on the pricing page (unverified).
- Smartlead: Base $39/mo - 2,000 leads, 6,000 emails; pre-warmed mailboxes $9/mo + $18/domain/yr; terms 3.4(d) prohibit "unsolicited commercial electronic messages ... as defined by the Spam Laws".
- lemlist: Email plan $69/user/mo; sending policy: scraped lists must follow local privacy rules; opt-out link required; domains at least 1 month old.
- Saleshandy: Starter $41/mo - 2,000 prospects, 6,000 emails; ready mailboxes $2.99-3.99/mo; domain $14/yr; no cold-email clause found (unverified).
- Forbid it: SendGrid (prior affirmative consent; no addresses "obtained from the Internet"), Brevo (no third-party lists), Amazon SES (no "unsolicited mass email"), Mailgun ("clear, explicit and provable consent"), Postmark (permission-based only).

## 3. Verification
Bouncer $8 / 1,000, $35 / 5,000, $60 / 10,000, unknowns free (usebouncer.com/pricing). ZeroBounce from 2,000 for $39. MillionVerifier 50,000 $89, 1 M $449. NeverBounce $8 / 1,000 (unverified). Catch-all = domain accepts any address, so acceptance does not prove the mailbox exists.

## 4. Reading behaviour
Litmus Oct 2026 (1.7 B opens): Apple 75.84 %, Gmail 17.02 %, Outlook 3.49 %; Apple MPP affects "roughly 55-60 %" of opens (no source given). Mobile share: no primary 2025-26 figure. Read time 13.4 s (Litmus 2018 data, published 2019); newer 9 s figures unverified. Apple MPP pre-loads pixels (Apple 2021). No provider statement or controlled test shows pixels hurt inbox placement. IPSOS / India SME Forum (2025-03-12): 60 % of 1,010 small businesses use WhatsApp Business for sales and marketing; no email figure.

## 5. Audio / video / personalised pages
No independent controlled evidence. Intercom own test (2018, warm leads): video emails "52 % more effective at getting a reply". Vendor: Vidyard "up to 5x more replies"; Sendspark 200-300 % (unverified). Gmail's blocked attachment list has no audio formats.

## 6. AI-voice law
EU AI Act Art. 50 applies from 2026-08-02: deployers of deep-fake audio "shall disclose that the content has been artificially generated or manipulated"; (EU) 2026/1744 gives systems on the market before 2026-08-02 until 2026-12-02 for machine marking (secondary source). India IT Amendment Rules 2026 (notified 2026-02-10, in force 2026-02-20): duties on intermediaries; AI audio needs a "prominently prefixed audio disclosure"; coverage of a studio's own email not established. US: no federal rule for AI voice in email/web found; California SB 942 only for AI providers > 1 M monthly users.
