# World coverage - every country, state and main city - 2026-11-09 - 19 ChatGPT messages

Goal (user, 2026-11-08 night): every country A-Z, every state, every city, as much contact data as possible,
compressed, in one shareable folder on E: (34 GB free).

Done: `E:\SiteBlitz-World-Business-Data\` - 86,751,626 businesses from Overture Places 2026-10-21.0 in 249
country folders (ZIP of Excel-sized CSV parts + state/city index + category index), 7.5 GB.
Phone 82 %, email 36 %, own website 54 %, social-but-no-website 38 %.

Verification: ChatGPT reference lists (all 249 countries; 4,249 state capitals + largest cities = 5,090 places).
5,048 (99.2 %) have business data; 42 remote places have none in the source. Details:
`E:\SiteBlitz-World-Business-Data\verification\README.md`, per-message checks `verify_NN.txt`.

Why not one app search per city: 40-150 s each x tens of thousands of cities = weeks; the bulk read of the
whole source took ~1 h 50 min end to end and contains every city the source knows.

Problems hit and fixed during the run: non-ISO country values (158, incl. a quote character) -> mapped / ZZ;
single partitioned COPY out of memory -> one raw file at a time; state codes vs names -> ISO 3166-2 names.
