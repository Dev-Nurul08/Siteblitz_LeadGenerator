# Claude Code research - outreach law, platform rules, payments (2026-11-10)

Research by a Claude Code agent; not legal advice. "Law/policy" = regulator, statute or platform docs;
"vendor/blog" = secondary. Confidence in brackets.

## 1. WhatsApp
- Policy: you may contact people only if they gave you their number AND opted in. A number from a public map
  listing fails both. Spamming / messaging "at scale in an unauthorized manner" -> limits or permanent ban.
  https://whatsappbusiness.com/policy/ (updated 2026-09-23) [high]
- Pricing per delivered message since 2025-07-01; marketing rate increases India 2026-01-01, UK 2026-07-01, UAE
  2026-10-01; Click-to-WhatsApp ad replies free up to 7 days; first 1,000 service messages/number/month free.
  https://developers.facebook.com/documentation/business-messaging/whatsapp/pricing [high]. India marketing
  ~Rs 0.8631/message + GST (msg91, vendor) [medium].
- Marketing templates are not delivered to US (+1) numbers; per-user engagement cap (error 131049).
  https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/marketing-templates/per-user-limits [high]
- New portfolio: 250 unique users / 24 h outside the window; 2,000 after verification. [high]
- Template headers: TEXT, IMAGE, VIDEO, GIF, DOCUMENT, LOCATION - no audio. A voice note can only be sent inside a
  24-hour window the customer opened. https://developers.facebook.com/documentation/business-messaging/whatsapp/templates/components [high]
- WhatsApp Business app: bulk or automated messaging breaks the Terms; bans "millions"; legal action since
  2019-12-07. https://faq.whatsapp.com/5957850900902049 [high]

## 2. India
- TRAI TCCCPR second amendment (2025-02-12): first violation -> all the sender's numbers barred 15 days; repeat ->
  all numbers disconnected 1 year across operators + blacklisted; 5 complaints in 10 days trigger action;
  promotional calls from 140 series, service from 1600; ordinary 10-digit numbers barred for telemarketing;
  customers have 7 days to complain. TRAI PR 11/2025 (via JSA law-firm copy) [medium-high]. IndiaMART challenges
  Regulation 25's B2B application in Delhi HC (pending).
- No anti-spam statute for email in India [medium-high].
- DPDP Act s.3(c)(ii) excludes data "made or caused to be made publicly available" by the data principal, but MeitY
  told the Lok Sabha (2025) scrapers must still comply; scope contested (IAPP) [medium]. DPDP Rules notified
  2025-11-13/14; core duties from ~2027-05-13/14 (AZB) [medium-high].

## 3. Cold B2B email by country
| Country | Rule | Conf. |
|---|---|---|
| US | CAN-SPAM opt-out, includes B2B; honest headers/subject, ad disclosure, postal address, opt-out within 10 business days; up to USD 53,088 per email (FTC guide) | high |
| Canada | CASL implied consent: conspicuously published, no "no unsolicited messages" note, role-relevant; identity + mailing address; unsubscribe valid 60 days, honoured in 10 business days | high |
| UK | Ltd companies / LLPs: no consent, identify + address. **Sole traders and ordinary partnerships = individuals -> consent needed.** Fines up to GBP 17.5 m / 4 % from 2026-02-05 (ICO; DUAA SI 2026/82) | high / med-high |
| Germany | UWG §7(2) Nr. 2: prior express consent even B2B | high |
| France | B2B email allowed without prior consent if related to the recipient's profession, with information + free opt-out; generic info@/contact@ addresses treated separately (CNIL 2026-06-10) | high |
| Netherlands | Opt-in also covers legal persons (Tw 11.7, ACM) | medium |
| Spain | LSSI art. 21: prior request or express authorisation, businesses included | medium-high |
| Australia | Inferred consent: conspicuous publication, no refusal note, role-relevant; identity; unsubscribe in 5 working days | high |
| UAE | TDRA: marketing messages need opt-in (secondary) | low-medium |
| Singapore | Spam Control Act for bulk (>100 similar / 24 h ...): `<ADV>` subject prefix, unsubscribe, accurate headers | medium |
| Brazil | No anti-spam law; LGPD legitimate interest with documented balancing test (ANPD 2024-02-02) | medium |
| South Africa | POPIA s.69: consent or existing customer; may ask for consent once; juristic persons protected | medium-high |

## 4. Mailbox providers
- Google (2024-02-01): all senders SPF or DKIM, PTR, TLS, spam < 0.3 %; bulk (~5,000+/day to Gmail) also DMARC,
  alignment, one-click unsubscribe for marketing; target < 0.1 %; bulk status never expires; rejections ramped
  from 2025-11. https://support.google.com/a/answer/81126 [high]
- Yahoo: same 0.3 %; unsubscribe honoured within 2 days. Microsoft Outlook.com (2025-05-05): >5,000/day need
  SPF + DKIM + DMARC; non-compliant to Junk, then 550 5.7.515. [high]

## 5. AI voice
- FCC 24-17 (2024-02-08): AI/cloned voices in calls = "artificial voice" under TCPA; consent needed (calls only). [high]
- EU AI Act Art. 50(4) from 2026-08-02: deployers of deep-fake audio must disclose; Art. 2(1)(c) reaches non-EU
  senders whose output is used in the EU. [medium-high]
- ElevenLabs use policy (2026-10-09): cloning a living person needs explicit consent (own voice fine); spam and
  unlawful automated messaging banned; disclose AI where the law requires or hiding would mislead; no watermark removal. [high]

## 6. Getting paid from abroad
- Stripe India: invite-only for new accounts since 2024-05; video KYC from 2026-01-01. [high]
- Razorpay: unregistered businesses/freelancers "must integrate PayPal" for international; export account needs
  PAN + GST certificate + business bank account. [medium-high]
- PayPal India: purpose code needed to withdraw; ~4.4 % + fixed fee (vendor). [medium]
- Wise / Payoneer for Indian businesses: reported, check directly. [low]
- GST: export of services zero-rated (IGST s.16) under LUT (RFD-11), which needs a GSTIN; payment in convertible
  foreign exchange; registration threshold Rs 20 lakh (exporter-below-threshold question disputed). [high / medium]

## Gaps
Dutch statute text, official TRAI PDF (connection refused), PayPal India user agreement, UAE official texts, Italy not read.
