# Third-party facts checked by Claude Code (subagent, 2026-11-10)

| # | Fact | Source | Confidence |
|---|---|---|---|
| 1 | Vercel Hobby = non-commercial personal use only; a paid classes site needs Pro at USD 20 / month per developer seat (+ tax) | vercel.com/docs/plans/hobby (updated 2026-09-14), vercel.com/pricing | high |
| 2 | MongoDB Atlas M0 free: 0.5 GB storage, 500 connections, 100 ops/s, paused after 30 days with no connections; Mumbai free-tier availability unconfirmed | mongodb.com/docs/atlas/reference/free-shared-limitations/ | high / low (Mumbai) |
| 3 | Razorpay: "Individual" accounts must use PayPal for international payments; registered businesses (sole proprietorship with 2 business proofs e.g. Udyam + one more, PAN, address proof, bank) can enable international cards after KYC + website pages (Terms, Privacy, Refund/Cancellation, Shipping) | razorpay.com/docs/payments/business-types-kyc-documents/, /docs/payments/international-payments/ | medium - confirm with Razorpay support |
| 4 | Razorpay Payment Links support international cards; webhooks payment_link.paid / .cancelled / .expired; fee up to 3% + 18% GST on fee; settlement in INR | razorpay.com/docs/webhooks/payloads/payment-links/, razorpay.com/pricing/ | high |
| 5 | Stripe India: invite-only for new accounts since May 2024 | support.stripe.com/questions/stripe-accounts-are-invite-only-in-india | high |
| 6 | PayPal India: receive-only; commercial international fee 4.40% + fixed fee | paypal.com/in/business/paypal-business-fees (snippet) | medium |
| 7 | Cashfree international gateway: 2.99% per international card payment, INR settlement T+2, FIRS per payment | cashfree.com/international-payment-gateway | medium-high |
| 8 | Meta Marketing API reading own ad account insights: Standard access (ads_read), no App Review; Limited tier rate limits fine for a daily pull. Conversions API for own pixel: no App Review | developers.facebook.com/docs/marketing-api/get-started/authorization; conversions-api/get-started | medium-high / high |
| 9 | **Zoom free: 40-minute limit on every meeting** (classes are 45 min -> needs paid Zoom or another tool). Google Meet free: 60 minutes for 3+ participants on a computer. Google Workspace Business Starter Rs 270 / user / month (annual) | zoom.com free video conferencing page; support.google.com/meet/answer/7317473; workspace.google.com/intl/en_in/pricing | high |
| 10 | Resend free: 3,000 emails / month, 100 / day, 1 domain on free? (3 custom domains listed), 1 webhook. Brevo free: 300 emails / day | resend.com/pricing; brevo.com | high / medium |
| 11 | WhatsApp click-to-chat: https://wa.me/<number-without-plus>?text=<urlencoded>. Cloud API charges per delivered template message; service messages charged after 1,000 free per number per month from 1 Oct 2026 | faq.whatsapp.com/5913398998672934; developers.facebook.com WhatsApp pricing | high |
| 12 | UAE PDPL (Decree-Law 45/2021) applies to controllers outside the UAE processing UAE residents' data; executive regulations reportedly still not issued (mid-2026). UAE Child Digital Safety Law (Decree-Law 26/2025) in force 1 Jan 2026, 1-year transition | uaelegislation.gov.ae; Clyde & Co Jan 2026 | high / medium |
| 13 | US COPPA covers data collected online from children; parent-only collection generally outside, but child-facing trackers/pixels or child input re-trigger it. Amended rule compliance date 22 Apr 2026 | ftc.gov COPPA FAQ and final rule | high |
| 14 | GST: online classes to an overseas recipient paid in foreign exchange = export of services, zero-rated; LUT (RFD-11) needs GSTIN; registration threshold for a Gujarat service provider Rs 20 lakh, aggregate turnover includes exports | IGST Act s.2(6), s.13(2), s.16; CBIC LUT circular; CGST s.22 | high / medium-high |

## Hosting - Netlify (subagent, 2026-11-10)
| # | Fact | Source | Confidence |
|---|---|---|---|
| H1 | Netlify Free allows commercial use (Self-Serve Agreement s.5, updated 4 Nov 2026; AUP item 13: card data must be collected by a PCI-DSS provider - hosted checkout is fine) | netlify.com/legal/self-serve-subscription-agreement/, /legal/acceptable-use-policy/ | high |
| H2 | Free = 300 credits / month hard cap; production deploy 15 credits, bandwidth 20 / GB, 2 per 10k requests, 10 per GB-hour functions; when credits run out ALL sites pause (webhooks stop) until next cycle or upgrade | docs.netlify.com credit-based-pricing-plans (30 Oct 2026), billing FAQ (7 Oct 2026) | high |
| H3 | Custom domain + free automatic Let's Encrypt HTTPS on Free; external registrar: apex A 75.2.60.5, www CNAME <site>.netlify.app | docs.netlify.com/manage/domains/get-started-with-domains/ | high |
| H4 | Next.js App Router, route handlers, middleware, ISR supported via @netlify/plugin-nextjs (OpenNext); Next 16 supported; 3 Nov 2026 advisory: use next 16.4.5+ / 15.5.29+ with adapter 5.16.6+ | docs.netlify.com nextjs overview; netlify.com/changelog/2026-11-03-nextjs-security-vulnerabilities/ | high |
| H5 | Synchronous functions 60 s; scheduled functions 30 s; background 15 min | docs.netlify.com/build/functions/configuration/ | high |
| H6 | Personal USD 9 / month (1,000 credits, auto-recharge); Pro USD 20 / month (3,000 credits) | netlify.com/pricing | high |
| H7 | Free cannot deploy from organisation-owned private repos - keep the repo under the founder's personal GitHub account | credit-based-pricing-plans page | high |
| H8 | Cloudflare Free: ToS bars collecting card info on Free; 10 ms CPU / request - avoid | cloudflare.com/terms | high |
Recommendation: Netlify; Free for building, Personal (USD 9) before taking real payments.

## Payments for an individual in India (subagent, 2026-11-10)
| # | Fact | Source | Confidence |
|---|---|---|---|
| P1 | PayPal India Business as "Individual": PAN + Aadhaar + video KYC, no business proof; guest card checkout; invoices / Orders API + webhooks; AED NOT supported (UAE parents pay USD); fee 4.40% + USD 0.30 + 3.0% FX conversion (about 8.5-9.5% all-in on USD 25); daily auto-transfer to bank; free monthly digital FIRA; purpose code P1107 educational services; chargeback fee USD 8 | pep.paypal.com/in/webapps/mpp/merchant-fees (28 Mar 2024), /know-your-customer; developer.paypal.com/docs/invoicing/webhooks/ | high (fees, KYC) / medium (guest card) |
| P2 | Razorpay individual: international only via linked PayPal. Sole proprietor: any 2 of Udyam, GST, Shop & Establishment, IEC, postpaid bill; international cards after KYC + bank approval, reply within 5 working days, reapply after 90 days if rejected; 3% + GST; AED among 160+ currencies; e-FIRA automatic; about 2-3 weeks end to end | razorpay.com/docs/payments/business-types-kyc-documents/, international-payments | high |
| P3 | Udyam registration: free, same day, Aadhaar + PAN | udyamregistration.gov.in | high |
| P4 | Gujarat Shops & Establishments: below 20 workers (2026 amendment, effective 16 Dec 2025) file Form D intimation, receive Form E receipt on enagar.gujarat.gov.in; Razorpay acceptance of Form E unverified | Khaitan & Co note 16 Mar 2026 | medium |
| P5 | Cashfree 2.99% international, T+2; individual eligibility for international unconfirmed; Education category may ask for UGC/CBSE certificate | cashfree.com | medium / low |
| P6 | Ruled out: Payoneer (no B2C), Skydo (B2B, USD 9 min), Wise (no card acceptance for India), Lemon Squeezy / Paddle / Dodo (prohibit human services), Outschool (teachers must live in listed countries), Teachable (needs Stripe; Stripe India invite-only) | provider help pages | high |
| P7 | Gumroad: merchant of record, allows memberships; about 17% on USD 25 | gumroad.com/pricing | medium |
Recommendation: day 1 PayPal (individual) invoices in USD; long-term Razorpay as sole proprietor (Udyam + S&E Form E) with payment links + webhooks; Cashfree fallback.
