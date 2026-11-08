# SiteBlitz Lead Generator — Poora Use Karne Ka Tareeka (Roman Hindi)

> Ye guide har button, har shabd aur har number ko step-by-step samjhaati hai.
> App ke andar jo English shabd dikhte hain, woh yahan **"quotes"** mein bilkul waise hi likhe hain,
> taaki aap screen par turant dhoondh sakein.

---

## Bhaag 0 — Ye tool karta kya hai? (2 line mein)

1. Aap ek **city** aur ek **kaam ka type** (jaise dentist, salon, cafe) chunte ho → tool us city ke
   saare matching businesses nikaal kar laata hai (naam, phone, email, address, Facebook/Instagram link, map location).
2. Phir tool **har business ki website check** karta hai aur batata hai ki kis business ko sach mein website
   ki zaroorat hai. Jinko sabse zyada zaroorat hai aur jinse contact ho sakta hai, woh **"Hot"** lead bante hain.

Data kahan se aata hai:
- **Overture Places** — Meta (Facebook pages), Microsoft, Foursquare jaise providers ka open data. Free aur legal.
- **OpenStreetMap** — volunteers ka banaya hua free map data.
- **CSV file** — aapki apni list.
- Google Maps ko scrape **nahi** kiya jaata (Google ki terms ke khilaf hai). Instagram / Facebook / LinkedIn /
  TikTok mein login karke scraping **nahi** hoti. Social links sirf business ki listing aur uski apni website se milte hain.

---

## Bhaag 1 — Tool ko start kaise karein

Do PowerShell windows chahiye. Dono mein pehle project folder mein jaayein:
```powershell
cd E:\tmp\Siteblitz_LeadGenerator
```

### Window 1 — Backend (data wala hissa)
```powershell
$env:DATABASE_URL = "sqlite+aiosqlite:///./dev_preview.db"
.venv\Scripts\python -m uvicorn backend.app.main:app --port 8000
```
- `dev_preview.db` = aapka abhi tak ka saara data (searches, businesses, checks). Naya khaali database
  chahiye to iski jagah `dev.db` likh dein.
- Jab tak ye window khuli hai, backend chal raha hai. Band karne ke liye `Ctrl + C`.

### Window 2 — Frontend (screen wala hissa)
```powershell
cd frontend
npm run dev
```
Ab browser mein kholein: **http://localhost:5173**

### Pehli baar naye computer par (sirf ek baar)
```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -e ".[dev]"
cd frontend; npm install; cd ..
```
Is PC par Windows "Smart App Control" ek library ko block karta hai, isliye ye bhi ek baar chalayein:
```powershell
$env:DISABLE_SQLALCHEMY_CEXT="1"
.venv\Scripts\python -m pip install --force-reinstall --no-deps --no-binary sqlalchemy sqlalchemy
```

---

## Bhaag 2 — Screen ka naksha (sabse upar wali patti)

Upar ek patti hai jismein 4 steps hain — isi order mein kaam karna hai:

| Patti par likha | Matlab | Uske aage ka number |
|---|---|---|
| **"01 Find"** | Businesses dhoondhna | Kitni searches ho chuki hain |
| **"02 Review"** | Har business ki website ka faisla dekhna aur sahi/galat batana | Kitne business abhi check / review hone baaki hain |
| **"03 Hot leads"** | Sabse achhe leads, score ke saath | Kitne Hot leads hain |
| **"04 Outreach"** | Lead ko khud contact karna aur log likhna | Kitne businesses ko contact kiya |
| **"Settings"** (right side) | Data sources ki health, "do-not-contact" list | — |

- Jis step par aap ho, uske neeche **orange line** hoti hai.
- Do steps ke beech ki line tab orange ho jaati hai jab pehle step ka kaam ho chuka ho (jaise pehli search ho gayi).
- Phone par ye 4 steps screen ke **neeche** aa jaate hain.

---

## Bhaag 3 — Step 01 "Find" (data nikaalna)

### 3.1 "New search" box — har field ka matlab

**Source (data kahan se aaye)** — chaar card dikhte hain, ek chunein:
| Card | Kab chunein |
|---|---|
| **"All sources (default)"** | Hamesha yahi. Overture + OpenStreetMap dono ek saath chalte hain, duplicate apne aap merge. Sabse zyada data. |
| **"Overture Places"** | Sirf Overture chahiye ho (thoda tez). |
| **"OpenStreetMap"** | Sirf OSM. Chhote shehron mein bahut kam data hota hai. |
| **"Google Places"** | Abhi band hai ("Not available yet") — API key aur licensing check chahiye. |
| **"CSV file"** | Aapke paas apni list hai. |

**"Country"** — desh chunein (default "India (IN)").

**"City"** — shehar ka naam English mein, jaise `Udaipur`, `Pune`. Spelling sahi honi chahiye.
State ka naam (jaise "Rajasthan") mat likhein — area bahut bada ho jaata hai aur search ruk jaati hai.

**"Kind of business"** — kaam ka type. Neeche suggestions aate hain: `dentist`, `salon`, `hairdresser`,
`cafe`, `restaurant`, `gym`, `clinic`, `hotel`, `school`, `lawyer`, `accountant`, `estate_agent`, `car_repair`,
`plumber`, `electrician`, `bakery`, `shop`. Inke alawa koi bhi shabd likh sakte ho.
Tool do tareeke se match karta hai:
1. business ki **category** se (jaise "dental_clinic"),
2. business ke **naam** se (jaise "Smile **Dental** Care" — category "doctor" ho tab bhi mil jaata hai).

**"Max results"** — zyada se zyada kitne businesses chahiye: 50, 100, 200, 500, 1000, 2000, 5000.
Bade shehar (Pune, Mumbai) ke liye 2000 ya 5000 rakhein.

**"Include franchises and chains"** — tick NAHI karoge to chains (Domino's, Lakmé jaise brands), ATM, bank,
petrol pump, school, hospital, mandir/masjid/church, band dukaanein — sab **"Skipped"** ho jaate hain
(inko website bechna bekaar hai). Tick karoge to chains bhi score honge.

**"Start search"** button dabayein. Button par "Searching…" aa jaata hai. 20 second se 2 minute lag sakte hain.

### 3.2 "Current search" box — har shabd ka matlab
- **"Queued — Running — Finished"**: search kis stage par hai (orange dot = ho gaya).
- Hara chip **"Done"** = bina error ke poori hui. Peela **"Partial"** = poori hui par kisi source ne error diya
  (wajah laal rang mein likhi hoti hai). Laal **"Failed"** = search toot gayi.
- Ye line sabse zaroori hai:
  - **"The sources have 426 matching businesses here; this search took 426 — all of them."**
    = us shehar mein jitne mile, saare aa gaye.
  - **"… — raise Max results to get more."** = aur bhi hain, "Max results" badha kar dobara search karein.
- Chaar dabbe:
  | Dabba | Matlab |
  |---|---|
  | **"Found"** | Sources ne kitne businesses diye |
  | **"New"** | Pehli baar save hue — yahi naye leads hain |
  | **"Duplicates"** | Pehle se save the (same source record, same phone number, ya same naam same jagah) — dobara nahi jode, par is search ki list mein dikhenge |
  | **"Errors"** | Source ki taraf se aayi dikkat (wajah laal mein) |
- **"Website checks: 100 done · 293 left"** — search ke turant baad tool har business ki website apne aap
  check karta hai, ek baar mein 100 (har 100 par lagbhag 25–40 second). Map ke dots ka rang badalta rehta hai.
  - **"Stop checking"** = checking rok do. Baad mein Review screen se aage badha sakte ho.
  - Dhyan dein: checking ke beech "Find" screen chhodoge to checking ruk jaati hai.
- **"View businesses"** = is search ke saare businesses Review screen par khul jaate hain.
- **"Export CSV"** / **"Export PDF"** = is search ka data download (Bhaag 8 dekhein).

### 3.3 Map (right side)
- Search poori hote hi businesses map par **girte** hain, har ek ke saath chhota orange ring — ye animation hai.
- Dots ke rang (neeche legend mein likha hai):
  | Rang | Matlab |
  |---|---|
  | Hara — **"Possible lead"** | Website nahi hai / sirf social media / website band |
  | Peela — **"Needs review"** | Tool pakka nahi keh sakta, aap dekhein |
  | Grey — **"Not a lead"** | Apni website hai, ya skip kiya gaya |
  | Halka safed — **"Not checked yet"** | Abhi website check nahi hui |
- Gol number wale circle = paas-paas ke kai businesses ka jhund. Click karo to zoom hota hai.
- Kisi dot par click = woh business Review screen mein khul jaata hai.
- Map na khule to **"Map tiles did not load"** + **"Retry map"** — list phir bhi kaam karti hai.

### 3.4 "Past searches" table
Har purani search ek line mein: **"Started"** (kab), **"Search"** (category · city · country),
**"Source"**, **"Status"**, **"Found"** (agar kam liya to neeche "of 3,780" — kitne available the),
**"New"**, **"Duplicates"**, **"Errors"**, aur **"Data"** column mein teen button:
"View businesses", "Export CSV", "Export PDF". Line par click = uske businesses Review mein.

Pehli baar (koi search nahi hui) right side par ek chalta hua diagram aata hai — tool kaise kaam karta hai —
aur neeche **"No searches yet"** + **"Start your first search"**.

### 3.5 CSV file se data daalna
1. Source mein **"CSV file"** chunein.
2. **"Choose a CSV file (name column required)"** par click karke file chunein.
3. Zaroori: file **UTF-8 CSV** ho (Excel: *Save As → CSV UTF-8*), max **15 MB**, max **5,000 rows**,
   extension `.csv` ya `.txt`, aur ek column ka naam `name` (ya business_name / company) ho.
4. Baaki columns jo pehchaane jaate hain: address, city, state, postal_code/zip, country, phone, email,
   website/url, category/industry.
5. Same file dobara upload karoge to rows "Duplicates" mein jaayengi — data double nahi hoga.

---

## Bhaag 4 — Step 02 "Review" (website ka faisla dekhna)

### 4.1 Upar ke controls
- **"Search by name"** — naam se dhoondhein.
- **"Table" / "Map"** — list ya map view.
- **"Your labels: 46 of 200 · 41 correct · 3 wrong · 2 not sure"** — aapne kitne faislon ko sahi/galat bataya
  (200 ka pilot target).
- **"Check websites for 100 businesses"** — jinki website abhi check nahi hui, unmein se 100 check karo.
- Jab filter **"Needs review"** chuna ho, yahi button **"Check these again"** ban jaata hai (Bhaag 4.5).
- Upar **"Search #9 ×"** dikhe to list sirf us search ki hai; **×** dabao to saari list.

### 4.2 Faisle (verdict) ke filters — har shabd ka matlab
| Filter / chip | Matlab | Lead hai? |
|---|---|---|
| **"No website found"** (hara) | Kisi source mein website nahi, naam se bane domain (jaise smiledental.com / .in / .co.in) exist nahi karte ya kisi aur ke hain | Haan |
| **"Social media only"** (hara) | Sirf Facebook / Instagram / WhatsApp / Linktree mila, apni website nahi | Haan |
| **"Website down"** (hara) | Listed website do baar, kam se kam 6 ghante ke gap par, nahi khuli | Haan |
| **"Needs review"** (peela) | Check pakka nahi (jaise website ek baar fail hui) — aapka faisla chahiye | Aap decide karo |
| **"Has own website"** (grey) | Apni website khulti hai (Google Maps link ya Justdial/Practo page **website nahi** maana jaata) | Nahi |
| **"Skipped"** (outline) | Chain/brand, bank, ATM, petrol pump, school, hospital, dharmik sthal, band dukaan | Kabhi nahi |
| **"Not checked yet"** | Abhi check hi nahi hua | — |

Table ke columns: **"Business"**, **"Category"**, **"City"**, **"Website verdict"**, **"Checked"** (kitni der
pehle), **"Your label"**.

### 4.3 Business kholna (right side drawer)
Kisi line par click karo (ya line chun kar **Enter**). Drawer khulta hai:

**Sabse upar:** business ka naam, faisla (chip), **"Confidence"**:
- **"High"** = saare checks + aapki khud ki search ho chuki (30 din ke andar).
- **"Medium"** = checks ho gaye par aapki search record nahi hui → abhi Hot nahi ban sakta.
- **"Low"** = check ruk gaya ya ulta-pulta result.
Neeche ek line mein faisle ki wajah, jaise *"No independent website after all checks incl. a search."*

**"Checks, in the order they ran"** — tool ne jo-jo check kiya, time (seconds tak) ke saath:
| Check ka naam | Kya dekha |
|---|---|
| **"Exclusion rules (chains, ATMs, closed…)"** | Skip karna hai ya nahi |
| **"Website field in the source data"** | Kisi source mein website likhi hai? ("Listed" / "No website listed in any source") |
| **"Social profile"** | Facebook/Instagram link mila |
| **"Link-in-bio page"** | Linktree jaise page khol kar bahar ke links dekhe. Facebook/Instagram pages **nahi** khole jaate (login wall + unki terms) — wahan likha aayega "not fetched" |
| **"Open the website"** | Website khol kar dekhi: "Opened (HTTP 200)" = chalti hai; "HTTP 403 … not counted as down" = website hai par robots ko rokti hai; "Domain has no DNS record — the listed website is gone" = domain hi khatam |
| **"Domain guess"** | Naam se domain bana kar check: "Domain does not exist" / "Exists, but it is another business" / "This business's site" |
| **"Your web search"** | Aapne khud jo search record ki |
| **"Open / closed"** | Aapne call karke jo bataya |
Icon: hara ✓ = check ka result positive, laal ✗ = negative (jaise domain nahi mila), dotted gola = check nahi
chala, peela tikona = check mein error. **"Check again"** = saare checks dobara chalao.

**"What the sources say"** — Category, Address, Phone, Email, Website, social links, Coordinates aur
**"Show on map"**.

**"Your checks"** — yahin se lead pakki hoti hai:
1. **"Search “naam”"** — Google par us business ka naam + city search khulta hai (naye tab mein).
2. Website nahi mili → **"I found no website"** dabao.
3. Website mil gayi → **"Website you found"** box mein URL daal kar **"Save website"** (business "Has own website" ho jaayega).
4. Phone karke confirm kiya ki dukaan chalu hai → **"Confirmed open (call)"**. Band hai → **"It is closed"** (business Skipped ho jaata hai).

**Sabse neeche — "Is this verdict right?"**
- **"Correct"** (key **1**), **"Wrong"** (key **2**), **"Not sure"** (key **3**).
- "Wrong" se pehle dropdown **"If wrong: what?"** mein galti chunein: "Website ownership", "Open or closed",
  "Wrong business", "Should (not) be skipped", "Need / score".
- Label lagte hi agla bina-label wala business apne aap khul jaata hai.
- Shortcut: **J** = agla, **K** = pichhla, **Esc** = band.

Business abhi check nahi hua ho to drawer mein **"Not checked yet"** + **"Check this business"** aata hai.

### 4.4 Ek lead ko Hot banane ka seedha raasta
1. Filter **"No website found"** (ya "Social media only") chuno.
2. Business kholo → **"Search “naam”"** se Google dekho → kuch nahi mila to **"I found no website"**.
3. Number par call karo → chalu hai to **"Confirmed open (call)"**.
4. Agar business dentist/salon hai aur phone ya email hai → woh **Hot** ban jaata hai (Bhaag 6).

### 4.5 "Needs review" wale businesses
Zyaadatar ka matlab: listed website ek baar nahi khuli. Test mein 39 mein se 32 ka domain hi exist nahi karta
tha (website khatam). Niyam: do baar fail ho, kam se kam 6 ghante ke gap par, tabhi "Website down".
Isliye: 6 ghante baad filter **"Needs review"** → **"Check these again"** dabao.

---

## Bhaag 5 — Step 03 "Hot leads" (sabse achhe leads)

Upar tabs: **"Hot"**, **"Warm"**, **"Cold"**, **"Review"**, **"Skip"** — har ek ke saath ginti.
| Tier | Matlab |
|---|---|
| **Hot** (bhara hua orange) | Score 80+ **aur** confidence High **aur** aapne confirm kiya ki chalu hai **aur** phone/email hai |
| **Warm** | Score 60–79, ya 80+ par upar ki koi shart baaki |
| **Cold** | Score 60 se kam (zyaadatar jinki achhi website hai) |
| **Review** | Faisla pakka nahi — score nahi diya |
| **Skip** | Kabhi lead nahi |

Table: **"#"** (rank), **"Business"**, **"Category"**, **"Tier"**, **"Need"** (0–100 + patti),
**"Confidence"**, **"Routes"** (phone / email / social ke icon — gehre = mila, halke = nahi mila),
**"Website verdict"**.

Line par click → drawer:
- Teen alag dabbe (kabhi jode nahi jaate): **"Website need"** (score/100), **"Evidence confidence"**,
  **"Outreach readiness"** ("Can be contacted" / "Find a phone or email first" / "Do not contact").
- **"Why it scores"** — score tukdon mein banta dikhta hai (animation), har tukde ke saath points aur
  **"See evidence"** (Review mein woh check khulta hai).
- **"Contact routes"** — phone (click = call), email, social links.
- **"Before it can be Hot"** — kya baaki hai: "Record a search for its name + city", "Confirm it is open
  (call or visit)", "Find a phone number or email" + button **"Check in Review"**.
- **"Start outreach"** — Outreach screen par yahi lead khulti hai.

Koi Hot nahi hai to: **"No hot leads yet"** + **"Review N warm leads"**.

---

## Bhaag 6 — Score kaise banta hai (har number)

**Website Need Score = 4 hisson ka jod (max 100):**

| Hissa | Kab kitne points |
|---|---|
| **Website gap** (max 60) | Website nahi mili = **60** · Sirf social media = **55** · Website down = **50** · Apni website hai par mobile-friendly nahi + HTTPS nahi = **35** · sirf mobile-friendly nahi = **30** · sirf HTTPS nahi = **20** · achhi website = **0** |
| **Business problem** (max 20, sirf ek sabse mazboot) | Sirf social media aur phone/email bhi nahi (log sirf DM/WhatsApp se pahunch sakte hain) = **10** · Inka web page sirf Zomato/Swiggy/Justdial/Practo par hai = **8** · Sirf category ke basis par = **0** |
| **Activity** (max 10) | Aapne call/visit se confirm kiya "chalu hai" = **10** · OpenStreetMap ne 180 din ke andar check kiya = **2** |
| **Service fit** (max 10) | Dentist / salon / hair / beauty = **10** · clinic, gym, restaurant, cafe, hotel, lawyer, CA, real estate, school/coaching = **7** · baaki = **4** |

Example: website nahi + aapne search record ki + call karke confirm + dentist + phone hai
= 60 + 0 + 10 + 10 = **80 → Hot**.

**Dhyan dein (abhi ka niyam):** sirf-social-media wala business jiske paas phone hai, max 55 + 0 + 10 + 10 =
**75 → Warm** tak hi jaata hai. Isko badalna hai ya nahi, ye aapka faisla baaki hai (docs/DECISIONS.md).

---

## Bhaag 7 — Step 04 "Outreach" (contact karna)

Upar notice: **"Sending is off: no email provider is connected. Copy the draft, send it yourself, then log it
here."** — matlab app khud email/message nahi bhejta. Aap khud bhejte ho, phir yahan likhte ho.

Left side = queue: pehle Hot, phir Warm leads. Click karo.

**Contact routes (upar wala dabba):**
- **"Call"** — phone dial.
- **"Open chat"** — WhatsApp chat khulta hai, message **aap khud** likhoge. (WhatsApp ki policy: business
  message ke liye saamne wale ki permission chahiye; isliye automatic kabhi nahi.)
- **"Copy email"**, **"Open profile"** (Facebook/Instagram).

**"Draft" (beech wala dabba):**
- Left mein **"Facts used"** — draft mein jo bhi baat likhi hai uska saboot (check ka time ke saath).
- Kisi fact par mouse le jaao → draft ka woh vakya underline hota hai aur ek patli orange line fact se vakya tak
  banti hai. Matlab har baat ka saboot dikh jaata hai.
- **"N sentences have no linked fact"** — namaste, offer, sawaal, sign-off jaise vakya, jinka koi saboot nahi chahiye.
- Draft mein **"[your name]"** ki jagah apna naam likhna.
- **"I checked every fact in this draft"** par tick → tabhi **"Copy draft"** chalega ("Copied" dikhega).
- **"Send email"** hamesha band hai + likha "Sending is off".

**"Log contact" (neeche):**
- **Channel**: "Phone", "Email", "Social message", "Contact form", "Visit".
- **Outcome**: "Interested", "Not now", "No reply", "Other".
- **"Note"** mein jo hua woh likho → **"Save log"**. Neeche history aati hai ("Not contacted yet." = abhi tak kuch nahi).
- **"Add to do-not-contact list"** → "Never contact … again?" → **"Yes, add"**. Iske baad us business par saare
  button band, laal patti: "On the do-not-contact list — every action is off."

---

## Bhaag 8 — Data download (Export)

Kahan se:
- **Find → "Current search"** box mein, ya **"Past searches"** ki har line par: **"Export CSV"** / **"Export PDF"**.

File ka naam jaisa: `siteblitz-businesses-job9-20261108-1048.csv` (job9 = search number, phir date-time).

**CSV** (Excel mein khulta hai, Hindi/special characters sahi rehte hain) — columns:
id, name, category, industry, address, city, state, postal_code, country, phone, email, website_url,
website_status, facebook, instagram, linkedin, tiktok, youtube, twitter, whatsapp, linktree, latitude,
longitude, status, discovered_at.
- Phone number ke aage `'` dikhe to ghabraayein nahi — isse Excel number ko formula/scientific number nahi
  banata. Excel mein woh chhupa rehta hai.

**PDF** — A4 landscape table: Name, Category, City, Phone, Email, Website / social, Website status.

Dhyan dein: in files mein businesses ke phone/email hain — inhe private rakhein.

---

## Bhaag 9 — "Settings"

**"Data sources"** table — har source ke saamne live status:
| Status | Matlab |
|---|---|
| **"Ready"** (hara) | Kaam kar raha hai |
| **"Not reachable"** (laal) | Internet / server ki dikkat (wajah saath mein) |
| **"Not set up"** (peela) | Kuch install/setting baaki |
| "Google Places — Not built yet" | Abhi tool mein nahi |
| "Email provider — Not connected" | Isliye app se sending band hai |

API keys browser mein kabhi nahi dikhti — woh backend ki `.env` file mein hoti hain.

**"Do-not-contact list"** — email daalo (+ wajah) → **"Add to list"**. Jo email yahan hai uspar outreach band.
Sirf phone wale business ko Outreach screen ke "Add to do-not-contact list" se block karo.

---

## Bhaag 10 — Rozana ka poora flow (copy kar lo)

1. Backend + frontend start karo (Bhaag 1).
2. **01 Find** → "All sources" → Country → City → Kind of business → Max results → **Start search**.
3. "The sources have … all of them" padho. Kam aaye to Max results badhao.
4. Website checks khatam hone do ("… 0 left"). Beech mein band kiya to Review se "Check websites for 100 businesses".
5. **02 Review** → filter "No website found" / "Social media only" → har business: Google search →
   "I found no website" ya "Save website" → call → "Confirmed open (call)" → label "Correct/Wrong/Not sure".
6. 6 ghante baad: filter "Needs review" → **"Check these again"**.
7. **03 Hot leads** → Hot tab → lead kholo → **"Start outreach"**.
8. **04 Outreach** → call / WhatsApp chat khud → draft copy (tick ke baad) → **"Save log"**.
9. Zaroorat ho to **Export CSV / PDF**.

---

## Bhaag 11 — Problem aaye to (troubleshooting)

| Screen par dikhe | Matlab | Kya karein |
|---|---|---|
| "City '…' was not found" | Shehar ka naam galat / us desh mein nahi | Spelling theek karo, sahi country chuno |
| "… matched an area of …° × …° (a district or state)" | State/district ka naam likh diya | Shehar ka naam likho |
| Bahut bada shehar (Beijing, Shenzhen, Ho Chi Minh City) — sirf beech ka hissa aaya | Shehar ki seema 1.5° (≈ 165 km) se badi hai, isliye shehar ke centre ke aas-paas 1.5° ka square search hota hai (job par `trimmed_from_km` likha hota hai) | Baaki hisse ke liye us area ke chhote shehar / district ke shehar alag se search karo |
| "Overpass API request timed out" / "Overpass API error: 502" | OpenStreetMap ka free server busy | Thodi der baad "Retry search". "All sources" mein Overture ka data phir bhi aa jaata hai |
| "OpenStreetMap: … All connection attempts failed" (ghanton tak) | OpenStreetMap ke free server ne is computer ka IP kuch der ke liye block kiya (ek saath bahut search chale) | Ek time par ek hi search chalao; tab tak "Overture Places" source se search karo |
| "Overture read failed … update OVERTURE_RELEASE" | Overture ne purana data release hata diya | `backend/app/config.py` mein `OVERTURE_RELEASE` naye release se badlo (docs.overturemaps.org/blog) |
| "Could not load …" + "Retry" | Backend band hai | Window 1 check karo |
| "Map tiles did not load" | Map ka free server nahi mila | "Retry map"; list kaam karti rahegi |
| "CSV must be UTF-8 encoded" | File ka format galat | Excel: Save As → CSV UTF-8 |
| "CSV file is larger than 15 MB" | File badi | File ko chhote hisson mein todo |
| Hot leads khaali | Warm leads par search + call confirm nahi hua | Bhaag 4.4 follow karo |
| Found, Max results se kam | Us shehar mein utne hi hain | Panel "all of them" bole to yahi poora data hai |

---

## Bhaag 12 — Aksar pooche jaane wale sawaal

**Q: Max results 1000 rakha, aaye sirf 426 — kyon?**
Us shehar mein sources ke paas utne hi matching businesses hain. Panel likhta hai "all of them". Isse zyada
chahiye to bada area ya paid data source chahiye.

**Q: Pehle sirf 29 aate the, ab zyada kyon?**
29 sirf OpenStreetMap ke Udaipur cafés the (wahan bas utne hi the). Ab "All sources" + naam se matching:
Udaipur cafés 418, dentists 108, salons 426, Pune salons 4,557.

**Q: Business ka Instagram dikh raha hai par tool kehta "No website found" — sahi hai?**
Haan, agar Instagram ke alawa apni website nahi mili. Instagram/Facebook website nahi maane jaate.

**Q: Kya tool Instagram / Facebook / Google Maps scrape karta hai?**
Nahi. Social links sirf open data aur business ki apni website se aate hain. Google Maps aur logged-in social
scraping unki terms ke khilaf hai.

**Q: Data kahan save hota hai?**
Project folder ki database file mein (`dev_preview.db` ya `dev.db`). Isko delete kiya to data chala jaayega.

**Q: Ek hi business do baar aa gaya?**
Same phone + same shehar, ya same naam + paas-paas → apne aap merge hota hai. Phir bhi dikhe to dono ka naam
alag-alag ho aur phone alag ho — tab tool unhe alag business maanta hai.

**Q: Kya app khud email bhejta hai?**
Nahi. "Sending is off" — aap khud bhejte ho aur "Log contact" mein likhte ho.
