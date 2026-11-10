# UAE laws - what applies and what the product must do (subagent research, 2026-11-10)

Research to brief a lawyer and a tax adviser, not legal advice. Official texts read in full: Decree-Law
14/2023, Cabinet Resolutions 56/2024 and 66/2023, TDRA spam policy v1.1. PDPL, Decree-Law 26/2025 and Cabinet
Resolution 106/2026 come from law-firm notes and u.ae (uaelegislation.gov.ae blocks automated fetch).

| # | Law | Applies to an India-based seller? | Product obligations | Dates / penalties |
|---|---|---|---|---|
| 1 | PDPL, Federal Decree-Law 45/2021 | Yes - Art 2(1)(c) covers controllers outside the UAE processing data of people in the UAE | Consent default, provable, withdrawable as easily as given; notice (purposes, recipients, retention, transfer, rights, contact); rights: access, portability, correction / erasure, restriction, objection, stop marketing; security; processor contracts; records of processing; transfer to India: no adequacy list - use contract necessity + express consent (Art 23) | In force 2 Jan 2022; executive regulations still not issued (9 Nov 2026); no penalties set yet |
| 2 | Child Digital Safety, Federal Decree-Law 26/2025 | Likely for the under-13 data rule (all learners are 7-12) | No collecting / processing / sharing a child's data without explicit, documented, verifiable parental consent; quick withdrawal; purpose disclosed; access limited to authorised staff; no commercial use, targeted ads or tracking beyond the stated purpose; reporting route for harmful content / abuse | In force 1 Jan 2026, compliance about 1 Jan 2027; penalty rulebook unpublished. Res. 106/2026 (under-15 social media) does not apply unless a child social feature is built |
| 3 | Consumer Protection Law 15/2020 + Res. 66/2023 | No (excludes e-commerce providers outside the UAE) - use as a standard | Price in AED, refund for undelivered service, no "no refund" clause | - |
| 4 | E-commerce law, Decree-Law 14/2023 | Yes - Art 2(1)(b) covers trading received from outside the UAE | Publish prices, fees, T&Cs (Art 5(5)); seller registration, address, phone, website (Art 6(8)-(9)); complaint channels with tracking (Art 6(6)-(7)); public rating box (Art 6(5)); customer chooses marketing channel (Art 6(4)); electronic detailed invoice per purchase (Art 5(8)); no misleading claims; secure checkout; no unannounced fees (Art 15(3)); refund / exchange if service not as described, defective, too late or T&C breach (Art 7); no arbitration clause under AED 50,000 (Art 9(2)(b)); no sharing consumer data without consent (Art 10) | In force 16 Sep 2023; Res. 200/2025 penalties up to AED 100,000 + closure |
| 5 | Media law 55/2023 + Advertiser Permit | Permit: No for own-page ads; Yes for any paid UAE influencer. Content standards: likely in practice | Target adults only; no identifiable child in creatives without written parental consent; never claim KHDA / ADEK approval | Res. 42/2025 from AED 10,000 |
| 6 | KHDA / ADEK / Private Teacher Work Permit | KHDA / ADEK unclear - ask in writing; work permit No for tutors living in India | Any UAE-resident tutor needs the permit | - |
| 7 | TDRA anti-spam, Res. 56/2024 telemarketing | Not binding on WhatsApp from India as written - use as the standard | Message only parents who asked / opted in; identify the business; stop after a decline; calls 09:00-18:00, SMS 07:00-21:00 UAE time; opt-out within 24 h; keep consent records; never buy lists | Res. 57/2024 AED 10,000-150,000 |
| 8 | UAE VAT | Live human-taught classes: unclear, leaning no (place of supply where performed). Recorded / self-paced content: yes, register from first sale | Sell live classes only until a UAE tax adviser confirms | FTA Education Guide VATGED1 (Jun 2026) |
| - | Cybercrime Law 34/2021 Art 44 | Yes in practice | Never record / publish a person's image or voice without consent | AED 150,000-500,000 |

## Build checklist (implemented by the product unless marked "founder" or "lawyer")
Website
- Imprint page: legal name, Indian registration (Udyam / GSTIN when available), physical address, phone, WhatsApp, email.
- Prices shown in AED (and charge currency), all fees disclosed.
- Terms: format, sessions, schedule + time zone, teacher absence + make-up, refunds per Art 7, no "no refund", no arbitration, governing law reviewed by a lawyer.
- Privacy notice (PDPL + children + India DPDP): controller, purposes, legal bases, processors, transfer to India, retention, rights, withdrawal, complaint contact.
- Cookie / consent banner with equal Reject; Meta Pixel / CAPI only after consent; no pixel on pages that collect child details; never send child data to Meta.
- Complaint form with ticket ID and a status-tracking page; a public rating / feedback box.
- No "accredited", "KHDA", "ADEK" claims; no testimonials or child images until real and consented.

Enrolment (the parent is the account holder; children get no accounts)
- Collect only: parent name, WhatsApp, email, country, time zone; child first name and age (or age band).
- Separate unticked consents, stored with timestamp, wording version, IP and channel: (a) child data for classes, (b) transfer to India, (c) marketing per channel (WhatsApp / email / phone), (d) recording (default off), (e) testimonials / photos.
- Parent verification: OTP to email (or WhatsApp later) + payment in the parent's name.
- Self-service withdraw-consent link in every email.

Admin
- Consent ledger; withdrawals take effect immediately.
- Rights inbox: access, export (CSV / JSON), correction, erasure / anonymisation, restriction, marketing stop, internal deadline.
- Marketing suppression list checked before any send; UAE send-window guard (calls 09:00-18:00, messages 07:00-21:00 Asia/Dubai).
- Retention settings per data category (founder + CA approve periods).
- Role-based access; teachers see only their batch's children (first name, age band, level); audit log; encryption in transit and at rest.
- Breach register + notification templates.
- Electronic receipt / invoice per payment.
- Complaints module: ticket ID, status, assignee, parent-visible tracker.

Classes (founder operating rules, recorded in admin)
- Unique private meeting links, waiting room / host admission, recording off, no private teacher-child contact, parent-only communication, teacher code of conduct.

Lawyer / tax adviser must confirm (founder)
1. PDPL transfer ground; 2. whether "Gujarati heritage" data is sensitive (ethnic origin); 3. whether the site is a platform "directed at UAE users" under 26/2025 and the educational exemption; 4. what licence a foreign seller shows under Art 6(9); 5. KHDA / ADEK / SPEA position; 6. UAE VAT place of supply; 7. telemarketing rules for WhatsApp; 8. governing-law clause.
