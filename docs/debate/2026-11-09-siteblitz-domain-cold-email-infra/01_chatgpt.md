# SiteBlitz: Domain, Email Infrastructure & 12-Month Budget Review

Independent review of Claude Code's proposal | 9 November 2026

Overall verdict: I disagree with purchasing the proposed 30-mailbox, 10-domain cold-email infrastructure immediately. The project's biggest problems are unreliable lead data, an unverified brand name, unfinished sending infrastructure, and the absence of evidence that 1,000 daily emails would generate profitable customers.

I would prioritize fixing these problems, establishing one professional business email account, and proving customer acquisition through a smaller pilot.

## 1. Best domain for SiteBlitz

Verdict: Conditional agreement with `siteblitz.in`; serious reservation about the brand itself.

### Domain comparison

The following availability information comes from the registry checks documented in `facts.md`, dated 9 November 2026. It is not a guaranteed live registrar checkout result.

| Domain                | Reported status  | Assessment                                            |
| --------------------- | ---------------- | ----------------------------------------------------- |
| `siteblitz.in`        | Available        | Best India-focused option if the brand is cleared     |
| `siteblitz.co.in`     | Available        | Optional defensive registration                       |
| `siteblitz.com`       | Taken since 2001 | Unavailable                                           |
| `siteblitzstudio.com` | Available        | Longer, but still contains the conflicting brand name |
| `siteblitzhq.com`     | Available        | Less intuitive for a local web-development service    |
| `siteblitz.ai`        | Taken            | Potentially competing website business                |

Availability source: supplied registry/WHOIS research. Final purchase availability remains unverified.

### Brand conflict

The project reports a French website at `siteblitz.ai` offering a similar website-building service. Independent access to that website was unsuccessful, so its current business activity and trademark rights remain unverified.

This is more important than which domain extension is cheapest.

- The French business does not automatically prevent Indian use of the name.
- The identical name and similar service create a potential trademark and customer-confusion issue.
- Registering `siteblitzstudio.com` does not eliminate that risk.
- An available domain is not proof that the brand is legally safe to use.

My decision: Before purchasing any SiteBlitz domain, conduct an Indian trademark search, including Classes 35 and 42, and review potentially relevant international registrations. The official [IP India trademark search guidance](https://ipindia.gov.in/trade-marks-before-you-apply-search-existing-trademarks?utm_source=chatgpt.com) is the starting point.

If the legal review finds a material conflict, I would favor a distinctive new brand rather than spending money protecting multiple SiteBlitz variants.

### `.in` requirements and cost

NIXI's registrar agreement requires accurate registrant identification and e-KYC acknowledgement within seven days. It also prohibits anonymous or proxy registration. This does not necessarily mean personal details are publicly visible in WHOIS results.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://web.nixiregistry.in\&sz=32)

web.nixiregistry.in



Hostinger currently lists these standard reference prices:

| Extension | Annual reference price | With illustrative 18% GST |
| --------- | ---------------------- | ------------------------- |
| `.in`     | ₹899                   | ₹1,061                    |
| `.co.in`  | ₹799                   | ₹943                      |
| `.com`    | ₹1,499                 | ₹1,769                    |

Promotional prices may require multi-year purchases. The actual checkout price and applicable tax must be confirmed.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.hostinger.com\&sz=32)

Register Your Domain From $0.01



Recommended domain budget: ₹1,061 for the `.in` reference price, conditional on brand clearance. Do not buy ten additional domains now.

## 2. Why multiple free Gmail accounts are landing in spam

Verdict: Strong disagreement with the idea that the main problem is simply using free Gmail instead of business Gmail.

The lead-generation system has a much more serious data-quality defect.

Sample contacts

# 38

Fabricated email addresses

# 37

97.37% of emails in the supplied 38-row export are fabricated, according to the project audit.

The `discovery.py` implementation generates addresses such as `inquiry.<business-slug>@gmail.com` when it cannot find an authentic email address. The supplied audit also reports 36 fabricated phone numbers.

An address that looks realistic is not necessarily real. A generated Gmail address could belong to somebody completely unrelated to the business.

### Likely causes, ranked

| Priority | Issue                                                      | Assessment                                       |
| -------- | ---------------------------------------------------------- | ------------------------------------------------ |
| 1        | Unverified or fabricated recipients                        | Critical if the team actually used these exports |
| 2        | Unwanted promotional messages                              | High risk of spam complaints                     |
| 3        | Repetitive, low-relevance content                          | Likely deliverability problem                    |
| 4        | Multiple new or low-reputation accounts                    | Additional account-reputation risk               |
| 5        | Authentication, sending practices and domain configuration | Must be audited, not assumed                     |
| 6        | Free Gmail rather than paid Workspace                      | Not, by itself, the root cause                   |

Important qualification: The audit establishes that 37 addresses were fabricated in one CSV. It does not establish that those exact addresses were used in the team's historical Gmail campaigns. Therefore, fabricated-address bounces are a major suspected cause, not yet a proven cause.

Google explicitly identifies invalid addresses, delivery failures and spam complaints as reasons for Gmail delivery restrictions. Google also prohibits distributing unsolicited commercial mail through consumer Gmail.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://support.google.com\&sz=32)

Gmail Help+1



### Immediate correction

The lead generator should never generate an email address merely because a business contact is missing.

The project should classify contacts as verified, unverified, absent, or invalid; maintain a suppression list; and retain the actual source of each address.

There is a second defect in `sender.py`: the current scaffold marks messages `SENT` without transmitting anything. Sending is still simulated. The status must reflect an actual provider event rather than a successful Python function call.

Conclusion: Buying paid inboxes before correcting these two defects would spend money without addressing the underlying problem.

## 3. How many email accounts are needed for 1,000 emails/day?

Verdict: Agree with the arithmetic, disagree with treating 30 inboxes and 10 domains as a proven delivery strategy.

### The actual mailbox mathematics

Assuming 1,000 individual messages per day:

| Assumed emails per inbox/day | Accounts needed |
| ---------------------------- | --------------- |
| 10                           | 100             |
| 20                           | 50              |
| 30                           | 34              |
| 33                           | 31              |
| 40                           | 25              |
| 50                           | 20              |

These are mathematical scenarios, not recommended cold-email limits or guaranteed safe sending capacities.

Claude's suggested 30 accounts × 33 emails produces only 990 emails/day. To reach 1,000, ten accounts would have to send one additional message.

The more important distinction is between a technical quota and permission to send promotional messages.

Google Workspace documents a standard maximum of 2,000 messages per user per rolling 24 hours. However, trial restrictions apply, and Google warns that new paid accounts may not receive their increased sending limits until cumulative payments reach US$100, with activation potentially taking up to 75 days after that threshold.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://knowledge.workspace.google.com\&sz=32)

Google Workspace Help



Those technical limits are not a promise that 1,000 unsolicited promotional messages will be accepted or delivered.

### Monthly lead requirement

Target volume

22 working days/month

# 22,000

Unique businesses/month

30 calendar days/month

# 30,000

Unique businesses/month

Assumes one initial message to each business and no repeat contacts. Follow-ups increase message volume, not the number of new businesses reached.

### My disagreement with 10 sending domains

There is no independent evidence in the project that ten domains with three accounts each is the optimum configuration for reaching Indian small businesses.

A fresh domain does not automatically have a trusted reputation. Additional domains create more administrative burden and can make the business's identity less clear. Splitting unwanted mail among domains or accounts does not make it acceptable to recipients or providers.

Google's requirements also apply to personal Gmail recipients, who appear particularly important in this market. The guidelines call for authentication, low complaint rates and appropriate unsubscribe mechanisms. Google recommends spam complaint rates below 0.1% and avoiding 0.3% or higher.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://support.google.com\&sz=32)

Gmail Help+1



Need data: Actual historical sent volume, recipient-provider mix, hard-bounce rates, spam complaints, replies and positive responses. None of these are provided in the project evidence.

My decision: Do not approve a 30-inbox deployment or rely on a three-to-five-week warm-up assumption. For permission-based promotional email at scale, evaluate a suitable bulk-email provider instead of multiplying employee mailboxes.

## 4. Business Gmail: What it is, which provider to choose, and cost

Verdict: Agree that SiteBlitz needs a professional email address. Disagree that it currently needs 30 Google Workspace users.

A business Gmail account means Gmail running on a domain owned by the business—for example, `hello@siteblitz.in` instead of `siteblitz2026@gmail.com`.

It normally provides an administrator, custom-domain email, account management and Gmail integration. It does not automatically improve the quality of a lead list or prevent spam classification.

### Verified provider comparison

Indian reference pricing, annual-commitment rates where stated. GST illustrated at 18%. USD conversion uses the project's ₹94.50/USD planning assumption.

| Provider                           | One user/month, before tax | With estimated GST |
| ---------------------------------- | -------------------------- | ------------------ |
| Google Workspace Base              | ₹99                        | ₹117               |
| Google Workspace Starter           | ₹270                       | ₹319               |
| Microsoft 365 Business Basic       | ₹170                       | ₹201               |
| Microsoft 365 Basic, without Teams | ₹130                       | ₹153               |
| Zoho Mail Lite, 5 GB               | Approx. ₹95 (US$1)         | Approx. ₹112       |

Sources: Google Workspace's [India plans](https://workspace.google.com/intl/en_in/?utm_source=chatgpt.com), Microsoft's [business plans](https://www.microsoft.com/en-in/microsoft-365/business/compare-all-microsoft-365-business-products-b?utm_source=chatgpt.com), and [Zoho Mail pricing](https://www.zoho.com/en-in/mail/zohomail-pricing.html?utm_source=chatgpt.com). Currency conversion is illustrative, and the final Indian Zoho checkout price is unverified.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://workspace.google.com\&sz=32)

Business apps and collaboration tools+2



For Google Workspace specifically:

- Base allows up to 20 users per organization and provides custom-domain Gmail.
- Starter supports up to 300 users and adds features that SiteBlitz does not presently need.
- Both options are paid mailbox services, not cold-email sending licenses.

### If Claude's 30-account plan were purchased

| Configuration            | Monthly including 18% GST |
| ------------------------ | ------------------------- |
| 1 Google Base user       | ₹116.82                   |
| 10 Google Starter users  | ₹3,186                    |
| 20 Google Starter users  | ₹6,372                    |
| 30 Google Starter users  | ₹9,558                    |
| 30 Starter + 1 Base user | ₹9,674.82                 |

These calculations use the published annual-commitment prices. Actual billing offers and tax treatment may vary.

Critical provider risk: Google's Acceptable Use Policy prohibits unsolicited mass email, and its Gmail policies warn about accounts that distribute unwanted commercial email. Buying 30 paid accounts does not remove suspension risk.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://workspace.google.com\&sz=32)

Google Workspace+1



I would not purchase accounts from dedicated cold-inbox resellers without clear written provider authorization, account ownership terms and security protections.

Need data: Whether SiteBlitz genuinely requires separate users, a shared inbox, or merely different public email addresses.

My provider choice: Google Workspace Base at ₹99 per user/month before tax, initially for one user. Add a second seat only when the founder and developer need separate, independent logins.

## 5. Which email roles should SiteBlitz create?

Verdict: Agree that CEO and CTO addresses are unnecessary. Disagree that the founder must use their personal name in the email address.

Because the founder wishes to remain anonymous publicly, I would use a genuine company identity rather than inventing senior executives.

### Recommended email structure

| Address                 | Purpose                                 | Paid account? |
| ----------------------- | --------------------------------------- | ------------- |
| `hello@siteblitz.in`    | Main inbox, enquiries and introductions | Yes — 1       |
| `projects@siteblitz.in` | Project discussions                     | No — alias    |
| `support@siteblitz.in`  | Customer assistance                     | No — alias    |
| `billing@siteblitz.in`  | Invoices and payments                   | No — alias    |

One Google Workspace user can have up to 30 aliases at no extra cost. Aliases share the primary inbox and do not provide independent logins or extra sending quotas.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://knowledge.workspace.google.com\&sz=32)

Google Workspace Help



The sender could truthfully appear as:

SiteBlitz Team\
Web Design & Development\
`hello@siteblitz.in`

The founder's real details can remain private from the public website while being provided accurately to the registrar, email provider and other parties where legally required.

Do not create imaginary people or misleading CEO/CTO identities.

Need data: Whether the founder and developer both require separate email access. If they do, use two licensed accounts instead of sharing a password.

Cost decision: One Base user costs approximately ₹117/month including GST; two users cost approximately ₹234/month.

## 6. Month-one setup, monthly maintenance and 12-month costs

Verdict: Claude's ₹2.78 lakh calculation is broadly arithmetically consistent with its assumptions, but the proposed configuration cannot reliably deliver the stated volume within its purchased plan limits.

### Errors in the original budget

Instantly Growth is insufficient

The US$47/month plan includes 1,000 uploaded contacts and only 5,000 emails per month. That cannot support 1,000 emails per working day.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://instantly.ai\&sz=32)

Instantly



Instantly Hypergrowth has a fixed contact cap

It supports 25,000 uploaded contacts, but this is a total active account limit rather than a fresh monthly allowance. At 22,000 new businesses each month, the capacity issue appears almost immediately.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://help.instantly.ai\&sz=32)

Instantly Help Center



Verification pricing is outdated

MillionVerifier's official page currently lists US$39 for 10,000 credits—not US$37—and US$89 for 50,000 credits.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.millionverifier.com\&sz=32)

MillionVerifier



Other infrastructure costs are missing

The cost of compliant commercial hosting, engineering, monitoring, legal review, potential foreign-service taxes and payment fees has not been adequately incorporated.

Instantly's official pages also disagree about Hypergrowth pricing: the public pricing page shows US$97/month, while one help article shows US$107/month. The applicable checkout price is unverified.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://instantly.ai\&sz=32)

Instantly+1



### Scenario A: Recommended lean setup

This buys only the professional infrastructure currently justified.

| Expense                                 | First month | Recurring/month |
| --------------------------------------- | ----------- | --------------- |
| One `.in` domain (standard annual rate) | ₹1,061      | —               |
| Google Workspace Base, one user         | ₹117        | ₹117            |
| Ten additional domains                  | ₹0          | ₹0              |
| Instantly subscription                  | ₹0          | ₹0              |
| Bulk verification subscription          | ₹0          | ₹0              |
| Total, excluding hosting                | ₹1,178      | ₹117            |

Estimates include illustrative 18% GST on the domain and Workspace. No promotional pricing assumed.

Estimated first-year email and domain cost

# ₹2,463

One domain purchase + 12 months of Google Workspace Base; excludes hosting, professional services and operating labor.

### Important hosting correction

SiteBlitz currently runs on Vercel Hobby. Vercel's official terms reserve Hobby for personal, non-commercial use. A commercial website needs appropriate hosting.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://vercel.com\&sz=32)

Vercel



Vercel Pro is advertised at US$20/month. Using the project's ₹94.50/USD planning exchange rate:

- Monthly hosting: approximately ₹1,890 before tax.
- Monthly hosting with illustrative 18% tax: approximately ₹2,230.
- First month including domain, one email account and this hosting estimate: approximately ₹3,408.
- First-year total for those three items: approximately ₹29,225.

These are planning estimates, not a verified checkout invoice. Additional usage or team seats may change the Vercel bill.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://vercel.com\&sz=32)

Vercel



### Scenario B: Corrected estimate for Claude's large infrastructure

This is a cost comparison, not approval to deploy.

Using the same 10 `.com` domains, 30 Starter mailboxes, one Base mailbox and original exchange rate, but substituting a Hypergrowth subscription and a 50,000-credit verification pack:

| Expense                     | Month-one estimate |
| --------------------------- | ------------------ |
| Main `.in` domain           | ₹1,061             |
| Ten `.com` domains          | ₹11,160            |
| 30 Starter + 1 Base mailbox | ₹9,675             |
| Instantly Hypergrowth       | ₹9,167–₹10,112     |
| 50,000 verification credits | ₹8,411             |
| Month-one total             | ₹39,473–₹40,418    |

For the 12-month calculation, assume 22,000 distinct emails verified monthly, or 264,000 in one year. Six 50,000-credit purchases would cover that quantity at a total of approximately ₹50,463, leaving unused credits.

Illustrative full-stack first-year cost

# ₹2.89–3.00 lakh

Before commercial hosting, staff time, legal review, foreign-service taxes and any upgrades needed to manage more than 25,000 uploaded contacts.

The monthly equivalent is approximately ₹24,100–₹25,000 across the first year, but actual cash payments will be uneven because domain and verification purchases occur at different times.

The arithmetic is based on project domain quotes, Google Workspace India pricing, Instantly's published plan prices and MillionVerifier's published credit packages. Some vendor limits and prices remain subject to checkout verification.

### Should SiteBlitz build the sender itself?

Agree with developing Phase 5's honest outreach backend, but not as a shortcut to free bulk email.

The project already needs to:

- Remove fabricated `info@` and `inquiry.*@gmail.com` contacts.
- Record provider-confirmed delivery rather than fabricated SENT statuses.
- Implement functional unsubscribe and suppression handling.
- Replace the fictional New York postal address with accurate company information.
- Correct the current localhost unsubscribe link.

The current code also puts recipient email addresses directly into unsubscribe URLs. An opaque, signed unsubscribe token would be a better design.

Building those features improves accuracy and accountability. It does not eliminate provider charges, operational labor, spam enforcement or compliance requirements.

The draft's claimed ₹13,400/month saving from removing Instantly is not supported by its own cost table: Instantly Hypergrowth was budgeted at approximately ₹9,167/month, and email verification remains a separate requirement.

### Financial viability

The project reports selling prices of ₹7,999 for Launch and ₹17,999 for Business.

At the corrected illustrative ₹2.89 lakh annual infrastructure cost, SiteBlitz would need approximately:

| Product           | Sales to recover ₹2.89 lakh |
| ----------------- | --------------------------- |
| Launch, ₹7,999    | 37                          |
| Business, ₹17,999 | 17                          |

Those are revenue-only break-even figures. They ignore website-production costs, support, taxes, refunds and founder time. Actual profitable break-even would require more sales.

My decision: Approve the lean infrastructure budget, subject to brand clearance and hosting. Do not authorize the large campaign expenditure until actual acquisition economics are demonstrated.

## 7. Go/no-go gates, Indian regulations and staged implementation

Verdict: Strong agreement with staged validation. I would make it more rigorous and treat 1,000 daily emails as a proposed business target, not an infrastructure requirement.

### Legal and platform requirements

The project's India-specific compliance coverage is incomplete.

India's Digital Personal Data Protection Rules were notified on 13 November 2025. The Gazette provides phased commencement: Rule 4 after one year and numerous principal operational rules after 18 months, corresponding to 13 November 2026 and 13 May 2027 respectively. That timeline does not make earlier unrestricted contact-data processing automatically lawful.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.meity.gov.in\&sz=32)

MeitY



There should be legal review of business-contact collection, personal data, notices, consent or other lawful grounds, retention and marketing practices. Do not assume a publicly visible personal email address is automatically available for unlimited promotional use.

TRAI's unsolicited-commercial-communications rules primarily concern telecom messaging and calls, rather than being a complete regulatory framework for email.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://trai.gov.in\&sz=32)

Government of India



WhatsApp is not an unrestricted alternative. Its Business Messaging Policy requires recipient opt-in before business-initiated contact, and the project has already decided not to automate WhatsApp outreach.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://whatsappbusiness.com\&sz=32)

WhatsApp for Business



### My proposed rollout

Stage 1 — Days 1–7: Fix the foundation

Complete brand clearance, remove generated contacts, audit prior Gmail campaigns and correct message status handling. Establish a reliable public contact method, compliant hosting and a usable opt-out process. Sending remains disabled.

Stage 2 — Days 8–21: Validate 200 businesses

Follow the existing pilot: one Indian city, dentists and salons, 100 calibration labels and 100 holdout labels.

The documented quality gate is at least 90% HOT precision on at least 30 holdout HOT predictions. Also measure the proportion with genuine, usable contact channels, preserving their source and permission status.

Stage 3 — Days 22–42: Validate customer acquisition

Use permission-based communications, warm introductions, direct enquiries from prospects, referrals and local partnerships.

Track qualified conversations, proposals, paid orders, cost per customer and fulfillment capacity. Compare results against the existing ₹1,000 advertising budget.

Stage 4 — After Day 42: Decide whether to scale

Increase spending only when legal and provider permissions, real contact supply, delivery data, conversion and unit economics support the proposed channel.

The 1,000/day objective requires proof of approximately 22,000 genuinely contactable new businesses each 22-day working month if the target refers to unique initial contacts.

### The biggest supply problem

The project contains a huge business-discovery dataset, but business records are not equivalent to valid marketing email addresses.

Here is the underlying volume requirement:

| Genuine email availability among discovered businesses | Business records needed for 22,000 verified emails |
| ------------------------------------------------------ | -------------------------------------------------- |
| 10%                                                    | 220,000                                            |
| 20%                                                    | 110,000                                            |
| 50%                                                    | 44,000                                             |

These are mathematical scenarios. The project's actual verified-email yield is unverified.

Even if this supply exists, lawful permission to contact recipients, provider acceptance, consumer interest and business economics remain separate requirements.

### Additional website consistency issue

A web-indexed version of SiteBlitz's current public site shows pricing of ₹14,999 for Growth and ₹24,999 for Scale, while the supplied project facts describe ₹17,999 for Business. It also displays an email address that the project documentation says is hidden because it bounces.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://siteblitz.vercel.app\&sz=32)

SiteBlitz+1



These may be differences between deployed and documented versions, but they should be reconciled before outreach. An inconsistent website or non-working business address damages trust independently of email deliverability.

## Final recommendation

| Decision                                                        | Recommendation                       |
| --------------------------------------------------------------- | ------------------------------------ |
| Purchase `siteblitz.in`                                         | Conditional on legal brand clearance |
| Change the SiteBlitz name                                       | Seriously evaluate before spending   |
| Keep using multiple free Gmails for cold campaigns              | No                                   |
| Establish a professional business email                         | Yes                                  |
| Buy 30 paid business mailboxes                                  | Not justified now                    |
| Buy 10 sending domains                                          | No                                   |
| Purchase Instantly immediately                                  | No                                   |
| Fix lead-data fabrication                                       | Mandatory                            |
| Finish honest outreach backend                                  | Yes                                  |
| Scale to 1,000 cold emails/day                                  | Not approved on current evidence     |
| Prioritize website pilot and warm, permission-based acquisition | Yes                                  |

## Points still open

1. Trademark: Is SITEBLITZ legally clear for the intended services in India and relevant future markets?
2. Domain: Can a registrar complete the purchase of `siteblitz.in` at the quoted price today?
3. Historical email evidence: Which lists were actually sent through the free Gmail accounts, and what were the bounce and complaint rates?
4. Real contact yield: What percentage of the lead generator's discovered businesses have authentic, verified email addresses and a permissible basis for marketing contact?
5. Provider authorization: Will the proposed email provider explicitly permit the intended communications?
6. Plan pricing: Is Instantly Hypergrowth US$97 or US$107 at checkout, and what are the full applicable taxes?
7. Commercial hosting: Will SiteBlitz move to Vercel Pro or an alternative compliant production host?
8. Offer consistency: Which pricing packages and business details are final and publicly accurate?
9. Unit economics: How much does it really cost to acquire and fulfill one ₹7,999 or ₹17,999 order?
10. Legal review: What contact-data collection and promotional communication practices are permissible for this specific Indian business?

The order I would commit to is: brand clearance → fix fabricated data → working professional website and email → 200-business validation → demonstrate paid conversions → evaluate scaling.

Until those gates pass, a ₹2.89–3.00 lakh annual email stack is a speculative expense rather than a justified growth investment.
