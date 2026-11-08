

---

## Claude Code - 2026-11-08 18:03 UTC - 01_claude.md - attachments: none

# World coverage - every country, every state, its main cities

Context: SiteBlitz finds small businesses (to sell websites to those without one). Its data source is
Overture Maps Places (open data, about 60-90 million places). We are extracting every place of every country
into files organised country -> state -> city. To check that no state or major city is missing, we need, for
every country in the world (A-Z, ISO 3166-1, 249 entries incl. territories), a reference list of its states
and main cities. We go alphabetically, about 13 countries per message, 19 messages in total.

## Message 1 of 19 - countries
Afghanistan (AF), Åland Islands (AX), Albania (AL), Algeria (DZ), American Samoa (AS), Andorra (AD), Angola (AO), Anguilla (AI), Antarctica (AQ), Antigua & Barbuda (AG), Argentina (AR), Armenia (AM), Aruba (AW)

For EACH country above give:
1. every first-level administrative division (state / province / region / governorate ... as it is today),
   with its capital or largest city (kind S);
2. the 10 largest cities of the country by population (kind N) - fewer if the country has fewer.
   A city can appear as both S and N; list it once with kind SN.
Uninhabited territories: one line `CC|-|-|||none`.

Output ONLY one code block, one line per city, pipe-separated, no header, no commentary inside it:
`CC|state|city|lat|lon|kind`
- CC = ISO code above; state and city in English (the name a map would show); lat / lon with 2 decimals.
After the code block: one line per country with any naming caveat (renamed divisions, disputed areas),
then the list of points still open.


---

## ChatGPT (Extra High) - 2026-11-08 18:18 UTC - saved as 01_chatgpt.md

```
AF|Badakhshan|Fayzabad|37.12|70.58|S
AF|Badghis|Qala-e-Naw|34.98|63.12|S
AF|Baghlan|Pul-e-Khumri|35.94|68.72|SN
AF|Balkh|Mazar-e-Sharif|36.71|67.11|SN
AF|Bamyan|Bamyan|34.82|67.82|S
AF|Daykundi|Nili|33.75|66.13|S
AF|Farah|Farah|32.37|62.12|S
AF|Faryab|Maymana|35.92|64.78|S
AF|Ghazni|Ghazni|33.55|68.42|S
AF|Ghor|Firozkoh|34.52|65.25|S
AF|Helmand|Lashkar Gah|31.58|64.37|S
AF|Herat|Herat|34.35|62.20|SN
AF|Jowzjan|Sheberghan|36.67|65.75|SN
AF|Kabul|Kabul|34.53|69.17|SN
AF|Kandahar|Kandahar|31.61|65.71|SN
AF|Kapisa|Mahmud-e Raqi|35.02|69.33|S
AF|Khost|Khost|33.34|69.92|S
AF|Kunar|Asadabad|34.87|71.15|S
AF|Kunduz|Kunduz|36.73|68.86|SN
AF|Laghman|Mehtarlam|34.67|70.21|S
AF|Logar|Pul-e-Alam|33.99|69.02|S
AF|Nangarhar|Jalalabad|34.43|70.45|SN
AF|Nimroz|Zaranj|30.96|61.86|S
AF|Nuristan|Parun|35.42|70.92|S
AF|Paktia|Gardez|33.60|69.23|S
AF|Paktika|Sharana|33.13|68.70|S
AF|Panjshir|Bazarak|35.31|69.52|S
AF|Parwan|Charikar|35.01|69.16|SN
AF|Samangan|Aybak|36.26|68.02|S
AF|Sar-e Pol|Sar-e Pol|36.22|65.93|S
AF|Takhar|Taloqan|36.74|69.53|SN
AF|Uruzgan|Tarinkot|32.63|65.87|S
AF|Maidan Wardak|Maidan Shahr|34.40|68.87|S
AF|Zabul|Qalat|32.11|66.91|S
AX|Brändö|Brändö|60.41|21.05|S
AX|Eckerö|Storby|60.23|19.60|SN
AX|Finström|Godby|60.23|19.99|SN
AX|Föglö|Degerby|60.03|20.38|S
AX|Geta|Vestergeta|60.37|19.85|S
AX|Hammarland|Prästgården|60.22|19.76|SN
AX|Jomala|Möckelö|60.12|19.90|SN
AX|Kökar|Karlby|59.92|20.92|S
AX|Kumlinge|Kumlinge|60.26|20.77|S
AX|Lemland|Söderby|60.08|20.08|SN
AX|Lumparland|Klemetsby|60.12|20.26|S
AX|Mariehamn|Mariehamn|60.10|19.93|SN
AX|Saltvik|Ödkarby|60.30|19.98|SN
AX|Sottunga|Sottunga|60.13|20.67|S
AX|Sund|Kastelholm|60.23|20.08|S
AX|Vårdö|Lövö|60.24|20.36|S
AX|Jomala|Vesterkalmare|60.13|19.92|N
AX|Jomala|Sviby|60.12|19.94|N
AX|Jomala|Österkalmare|60.13|19.96|N
AL|Berat|Berat|40.71|19.95|SN
AL|Dibër|Peshkopi|41.69|20.43|S
AL|Durrës|Durrës|41.32|19.45|SN
AL|Elbasan|Elbasan|41.11|20.08|SN
AL|Fier|Fier|40.73|19.56|SN
AL|Gjirokastër|Gjirokastër|40.08|20.14|S
AL|Korçë|Korçë|40.62|20.78|SN
AL|Kukës|Kukës|42.08|20.42|S
AL|Lezhë|Lezhë|41.78|19.64|S
AL|Shkodër|Shkodër|42.07|19.51|SN
AL|Tirana|Tirana|41.33|19.82|SN
AL|Vlorë|Vlorë|40.47|19.48|SN
AL|Tirana|Kashar|41.35|19.71|N
AL|Tirana|Kamëz|41.38|19.76|N
DZ|Adrar|Adrar|27.87|-0.29|S
DZ|Chlef|Chlef|36.17|1.33|S
DZ|Laghouat|Laghouat|33.80|2.86|S
DZ|Oum El Bouaghi|Oum El Bouaghi|35.88|7.11|S
DZ|Batna|Batna|35.56|6.17|SN
DZ|Béjaïa|Béjaïa|36.75|5.08|S
DZ|Biskra|Biskra|34.85|5.73|S
DZ|Béchar|Béchar|31.62|-2.22|S
DZ|Blida|Blida|36.47|2.83|SN
DZ|Bouira|Bouira|36.38|3.90|S
DZ|Tamanrasset|Tamanrasset|22.79|5.52|S
DZ|Tébessa|Tébessa|35.40|8.12|S
DZ|Tlemcen|Tlemcen|34.88|-1.32|S
DZ|Tiaret|Tiaret|35.37|1.32|S
DZ|Tizi Ouzou|Tizi Ouzou|36.72|4.05|S
DZ|Algiers|Algiers|36.73|3.09|SN
DZ|Djelfa|Djelfa|34.67|3.26|SN
DZ|Jijel|Jijel|36.82|5.77|S
DZ|Sétif|Sétif|36.19|5.41|SN
DZ|Saïda|Saïda|34.84|0.15|S
DZ|Skikda|Skikda|36.88|6.91|S
DZ|Sidi Bel Abbès|Sidi Bel Abbès|35.19|-0.63|SN
DZ|Annaba|Annaba|36.90|7.77|SN
DZ|Guelma|Guelma|36.46|7.43|S
DZ|Constantine|Constantine|36.37|6.61|SN
DZ|Médéa|Médéa|36.27|2.75|S
DZ|Mostaganem|Mostaganem|35.93|0.09|S
DZ|M'Sila|M'Sila|35.71|4.54|S
DZ|Mascara|Mascara|35.40|0.14|S
DZ|Ouargla|Ouargla|31.95|5.32|S
DZ|Oran|Oran|35.70|-0.64|SN
DZ|El Bayadh|El Bayadh|33.68|1.02|S
DZ|Illizi|Illizi|26.51|8.48|S
DZ|Bordj Bou Arreridj|Bordj Bou Arreridj|36.07|4.76|S
DZ|Boumerdès|Boumerdès|36.76|3.48|S
DZ|El Tarf|El Tarf|36.77|8.31|S
DZ|Tindouf|Tindouf|27.67|-8.15|S
DZ|Tissemsilt|Tissemsilt|35.61|1.81|S
DZ|El Oued|El Oued|33.36|6.86|S
DZ|Khenchela|Khenchela|35.44|7.14|S
DZ|Souk Ahras|Souk Ahras|36.29|7.95|S
DZ|Tipaza|Tipaza|36.59|2.45|S
DZ|Mila|Mila|36.45|6.26|S
DZ|Aïn Defla|Aïn Defla|36.26|1.97|S
DZ|Naâma|Naâma|33.27|-0.31|S
DZ|Aïn Témouchent|Aïn Témouchent|35.30|-1.14|S
DZ|Ghardaïa|Ghardaïa|32.49|3.67|S
DZ|Relizane|Relizane|35.74|0.56|S
DZ|Timimoun|Timimoun|29.26|0.23|S
DZ|Bordj Badji Mokhtar|Bordj Badji Mokhtar|21.33|0.95|S
DZ|Ouled Djellal|Ouled Djellal|34.42|5.06|S
DZ|Béni Abbès|Béni Abbès|30.13|-2.16|S
DZ|In Salah|In Salah|27.19|2.48|S
DZ|In Guezzam|In Guezzam|19.57|5.77|S
DZ|Touggourt|Touggourt|33.10|6.07|S
DZ|Djanet|Djanet|24.55|9.48|S
DZ|El M'Ghair|El M'Ghair|33.95|5.92|S
DZ|El Meniaa|El Meniaa|30.58|2.88|S
DZ|Aflou|Aflou|34.11|2.10|S
DZ|Barika|Barika|35.39|5.37|S
DZ|El Kantara|El Kantara|35.22|5.70|S
DZ|Bir El Ater|Bir El Ater|34.75|8.06|S
DZ|El Aricha|El Aricha|34.22|-1.26|S
DZ|Ksar Chellala|Ksar Chellala|35.21|2.32|S
DZ|Aïn Ouessara|Aïn Ouessara|35.45|2.91|S
DZ|Messaad|Messaad|34.15|3.50|S
DZ|Ksar El Boukhari|Ksar El Boukhari|35.89|2.75|S
DZ|Bou Saâda|Bou Saâda|35.21|4.17|S
DZ|El Abiodh Sidi Cheikh|El Abiodh Sidi Cheikh|32.89|0.55|S
DZ|Algiers|Bab Ezzouar|36.73|3.18|N
AS|Eastern District|Pago Pago|-14.28|-170.70|SN
AS|Manu'a District|Ta'u|-14.23|-169.51|S
AS|Rose Atoll|-|||S
AS|Swains Island|Taulaga|-11.06|-171.08|S
AS|Western District|Tafuna|-14.34|-170.72|SN
AS|Eastern District|Nu'uuli|-14.32|-170.70|N
AS|Western District|Ili'ili|-14.35|-170.75|N
AS|Western District|Faleniu|-14.33|-170.74|N
AS|Western District|Leone|-14.34|-170.79|N
AS|Eastern District|Aua|-14.27|-170.67|N
AS|Western District|Mapusagafou|-14.32|-170.75|N
AS|Western District|Vaitogi|-14.38|-170.73|N
AS|Western District|Pava'ia'i|-14.33|-170.75|N
AD|Andorra la Vella|Andorra la Vella|42.51|1.52|SN
AD|Canillo|Canillo|42.57|1.60|SN
AD|Encamp|Encamp|42.53|1.58|SN
AD|Escaldes-Engordany|Escaldes-Engordany|42.51|1.54|SN
AD|La Massana|La Massana|42.55|1.51|SN
AD|Ordino|Ordino|42.56|1.53|SN
AD|Sant Julià de Lòria|Sant Julià de Lòria|42.46|1.49|SN
AD|Andorra la Vella|Santa Coloma|42.50|1.50|N
AD|Encamp|El Pas de la Casa|42.54|1.73|N
AD|La Massana|Arinsal|42.57|1.49|N
AO|Bengo|Caxito|-8.58|13.66|S
AO|Benguela|Benguela|-12.58|13.40|SN
AO|Bié|Kuito|-12.38|16.94|SN
AO|Cabinda|Cabinda|-5.56|12.19|SN
AO|Cuando|Mavinga|-15.80|20.35|S
AO|Cubango|Menongue|-14.66|17.69|S
AO|Cuanza Norte|Ndalatando|-9.30|14.91|S
AO|Cuanza Sul|Sumbe|-11.21|13.84|S
AO|Cunene|Ondjiva|-17.07|15.73|S
AO|Huambo|Huambo|-12.78|15.74|SN
AO|Huíla|Lubango|-14.92|13.49|SN
AO|Icolo e Bengo|Catete|-8.82|13.56|S
AO|Luanda|Luanda|-8.84|13.23|SN
AO|Lunda Norte|Dundo|-7.38|20.83|S
AO|Lunda Sul|Saurimo|-9.66|20.39|SN
AO|Malanje|Malanje|-9.54|16.34|SN
AO|Moxico|Luena|-11.78|19.92|S
AO|Moxico Leste|Cazombo|-11.91|22.91|S
AO|Namibe|Moçâmedes|-15.20|12.15|S
AO|Uíge|Uíge|-7.61|15.06|SN
AO|Zaire|Mbanza Kongo|-6.27|14.24|S
AO|Icolo e Bengo|Zango|-9.08|13.39|N
AI|Blowing Point|Blowing Point Village|18.18|-63.09|SN
AI|East End|East End Village|18.23|-63.00|SN
AI|George Hill|George Hill|18.20|-63.07|SN
AI|Island Harbour|Island Harbour|18.26|-63.00|SN
AI|North Hill|North Hill|18.21|-63.09|S
AI|North Side|North Side|18.24|-63.05|SN
AI|Sandy Ground|Sandy Ground Village|18.20|-63.09|S
AI|Sandy Hill|Sandy Hill|18.22|-63.01|S
AI|South Hill|South Hill Village|18.19|-63.09|SN
AI|Stoney Ground|Stoney Ground|18.22|-63.05|SN
AI|The Farrington|Farrington|18.22|-63.02|S
AI|The Quarter|The Quarter|18.21|-63.04|SN
AI|The Valley|The Valley|18.22|-63.06|SN
AI|West End|West End Village|18.17|-63.14|SN
AQ|-|-|||none
AG|Saint George|Piggotts|17.12|-61.80|SN
AG|Saint John|Saint John's|17.12|-61.85|SN
AG|Saint Mary|Bolans|17.06|-61.87|SN
AG|Saint Paul|Liberta|17.04|-61.79|SN
AG|Saint Peter|Parham|17.10|-61.77|S
AG|Saint Philip|Freetown|17.05|-61.71|S
AG|Barbuda|Codrington|17.64|-61.82|S
AG|Redonda|-|||S
AG|Saint Peter|All Saints|17.07|-61.79|N
AG|Saint Mary|Jennings|17.08|-61.87|N
AG|Saint John|Clare Hall|17.13|-61.82|N
AG|Saint Paul|Swetes|17.05|-61.80|N
AG|Saint Philip|Willikies|17.09|-61.71|N
AG|Saint Mary|Old Road|17.02|-61.83|N
AR|Buenos Aires|La Plata|-34.92|-57.95|SN
AR|Catamarca|San Fernando del Valle de Catamarca|-28.47|-65.78|S
AR|Chaco|Resistencia|-27.46|-58.99|S
AR|Chubut|Rawson|-43.30|-65.10|S
AR|Autonomous City of Buenos Aires|Buenos Aires|-34.61|-58.38|SN
AR|Córdoba|Córdoba|-31.41|-64.19|SN
AR|Corrientes|Corrientes|-27.47|-58.83|S
AR|Entre Ríos|Paraná|-31.73|-60.52|S
AR|Formosa|Formosa|-26.18|-58.18|S
AR|Jujuy|San Salvador de Jujuy|-24.19|-65.29|S
AR|La Pampa|Santa Rosa|-36.62|-64.29|S
AR|La Rioja|La Rioja|-29.41|-66.86|S
AR|Mendoza|Mendoza|-32.89|-68.84|SN
AR|Misiones|Posadas|-27.39|-55.92|S
AR|Neuquén|Neuquén|-38.95|-68.06|SN
AR|Río Negro|Viedma|-40.81|-63.00|S
AR|Salta|Salta|-24.81|-65.42|SN
AR|San Juan|San Juan|-31.54|-68.53|SN
AR|San Luis|San Luis|-33.30|-66.34|S
AR|Santa Cruz|Río Gallegos|-51.62|-69.22|S
AR|Santa Fe|Santa Fe|-31.65|-60.71|S
AR|Santiago del Estero|Santiago del Estero|-27.79|-64.26|S
AR|Tierra del Fuego, Antarctica and South Atlantic Islands|Ushuaia|-54.80|-68.30|S
AR|Tucumán|San Miguel de Tucumán|-26.82|-65.21|SN
AR|Santa Fe|Rosario|-32.95|-60.64|N
AR|Buenos Aires|Mar del Plata|-38.00|-57.56|N
AM|Aragatsotn|Ashtarak|40.30|44.36|S
AM|Ararat|Artashat|39.95|44.55|SN
AM|Armavir|Armavir|40.16|44.04|SN
AM|Gegharkunik|Gavar|40.35|45.12|S
AM|Kotayk|Hrazdan|40.52|44.76|SN
AM|Lori|Vanadzor|40.81|44.50|SN
AM|Shirak|Gyumri|40.79|43.85|SN
AM|Syunik|Kapan|39.21|46.41|SN
AM|Tavush|Ijevan|40.88|45.15|S
AM|Vayots Dzor|Yeghegnadzor|39.76|45.33|S
AM|Yerevan|Yerevan|40.18|44.51|SN
AM|Kotayk|Abovyan|40.27|44.63|N
AM|Armavir|Vagharshapat|40.17|44.29|N
AM|Ararat|Masis|40.07|44.44|N
AW|Noord/Tanki Leendert|Noord|12.57|-70.03|SN
AW|Oranjestad West|Oranjestad|12.52|-70.03|SN
AW|Oranjestad East|Dakota|12.51|-70.01|S
AW|Paradera|Paradera|12.54|-70.01|SN
AW|Santa Cruz|Santa Cruz|12.51|-69.98|SN
AW|Savaneta|Savaneta|12.45|-69.94|SN
AW|San Nicolas North|Brasil|12.47|-69.93|S
AW|San Nicolas South|San Nicolas|12.44|-69.91|SN
AW|Noord/Tanki Leendert|Tanki Leendert|12.54|-70.02|N
AW|San Nicolas North|Butucu|12.47|-69.91|N
AW|Noord/Tanki Leendert|Malmok|12.60|-70.05|N
AW|Savaneta|Pos Chiquito|12.46|-69.96|N
```

AF — 34 provinces; Firozkoh was formerly called Chaghcharan. Daykundi/Daikundi, Jowzjan/Jawzjan and Sharana/Shrana have alternative spellings.

AX — 16 municipalities; Mariehamn is the only legally designated city. Other entries are villages or populated localities, using largest-village representatives.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.asub.ax\&sz=32)

Ålands statistik- och utredningsbyrå



AL — 12 counties; 2023 census locality populations are used, including Kashar and Kamëz in the greater Tirana area.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.worldometers.info\&sz=32)

Worldometer



DZ — 69 wilayas under the April 2026 territorial reorganisation, including 11 newly created wilayas. Administrative transfers to the new wilayas may continue through December 2026.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.aps.dz\&sz=32)

واج



AS — Three districts plus Swains Island and Rose Atoll are represented. Taulaga is a historical settlement; Swains had no permanent residents in the 2020 census. The ten largest villages use 2020 population figures.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.talanei.com\&sz=32)

Talanei

[image](https://www.google.com/s2/favicons?domain=https://asbar.org\&sz=32)

American Samoa Bar Association



AD — Seven parishes; Santa Coloma, El Pas de la Casa and Arinsal are populated localities within those parishes, not additional first-level divisions.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.worldometers.info\&sz=32)

Worldometer



AO — 21 provinces since January 2025. Kuito/Cuito, Ndalatando/N'dalatando and Moçâmedes/Namibe have spelling or former-name variants. Zango's population ranking includes Calumbo.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://governo.gov.ao\&sz=32)

Governo de Angola+1



AI — 14 administrative districts. Because settlement-level rankings are inconsistent, the ten `N` entries represent the centres of the ten most populous districts using the 2011 census, rather than a verified ranking of individual villages.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://unstats.un.org\&sz=32)

UNSD



AQ — Antarctica has no permanent cities or conventional first-level administrative divisions; research stations are excluded.

AG — Six parishes plus Barbuda and uninhabited Redonda. All Saints spans three parishes and is assigned once to Saint Peter. The top ten settlements use 2011 census figures.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://en.wikipedia.org\&sz=32)

Wikipedia



AR — 23 provinces plus the Autonomous City of Buenos Aires. Tierra del Fuego's legal name includes Antarctic and South Atlantic island claims; these are not treated as additional populated divisions. Major urban centres use 2022 agglomeration populations.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://mexpedia.org\&sz=32)

Mexpedia



AM — Ten provinces (marzes) plus separately administered Yerevan. Vagharshapat is also known as Echmiadzin. Nagorno-Karabakh is excluded from Armenia's administrative divisions.

AW — Aruba has no conventional first-level provinces. Its eight statistical regions are used as coverage proxies, not as formal provincial governments. San Nicolas is also written Sint Nicolaas.

Points still open:

- AX: Validate the exact ten largest non-Mariehamn villages against the complete 2025 ÅSUB locality dataset.
- AI: Obtain a comparable village-level population ranking; current `N` flags use district-population proxies.
- AW: Confirm statistical-region boundaries and representative-locality assignments against the boundaries used in Overture Maps.
- DZ: Check whether the Overture administrative hierarchy already reflects all 69 wilayas rather than the earlier 58.
- AG: Resolve All Saints' multi-parish boundary if strict point-in-polygon matching is required.
- AO: Verify the Zango/Calumbo urban boundary and its assignment to Icolo e Bengo in the current map extract.


---

## Claude Code - 2026-11-08 18:18 UTC - 02_claude.md - attachments: none

## Message 2 of 19 - countries
Australia (AU), Austria (AT), Azerbaijan (AZ), Bahamas (BS), Bahrain (BH), Bangladesh (BD), Barbados (BB), Belarus (BY), Belgium (BE), Belize (BZ), Benin (BJ), Bermuda (BM), Bhutan (BT)

For EACH country above give:
1. every first-level administrative division (state / province / region / governorate ... as it is today),
   with its capital or largest city (kind S);
2. the 10 largest cities of the country by population (kind N) - fewer if the country has fewer.
   A city can appear as both S and N; list it once with kind SN.
Uninhabited territories: one line `CC|-|-|||none`.

Output ONLY one code block, one line per city, pipe-separated, no header, no commentary inside it:
`CC|state|city|lat|lon|kind`
- CC = ISO code above; state and city in English (the name a map would show); lat / lon with 2 decimals.
After the code block: one line per country with any naming caveat (renamed divisions, disputed areas),
then the list of points still open.


---

## ChatGPT (Extra High) - 2026-11-08 18:34 UTC - saved as 02_chatgpt.md

```
AU|Australian Capital Territory|Canberra|-35.28|149.13|SN
AU|New South Wales|Sydney|-33.87|151.21|SN
AU|Northern Territory|Darwin|-12.46|130.84|S
AU|Queensland|Brisbane|-27.47|153.03|SN
AU|South Australia|Adelaide|-34.93|138.60|SN
AU|Tasmania|Hobart|-42.88|147.33|S
AU|Victoria|Melbourne|-37.81|144.96|SN
AU|Western Australia|Perth|-31.95|115.86|SN
AU|Queensland|Gold Coast|-28.02|153.43|N
AU|New South Wales|Newcastle|-32.93|151.78|N
AU|Queensland|Sunshine Coast|-26.65|153.07|N
AU|New South Wales|Central Coast|-33.43|151.34|N
AT|Burgenland|Eisenstadt|47.85|16.52|S
AT|Carinthia|Klagenfurt|46.62|14.31|SN
AT|Lower Austria|Sankt Pölten|48.20|15.63|SN
AT|Salzburg|Salzburg|47.80|13.04|SN
AT|Styria|Graz|47.07|15.44|SN
AT|Tyrol|Innsbruck|47.27|11.40|SN
AT|Upper Austria|Linz|48.31|14.29|SN
AT|Vienna|Vienna|48.21|16.37|SN
AT|Vorarlberg|Bregenz|47.50|9.75|S
AT|Carinthia|Villach|46.61|13.85|N
AT|Upper Austria|Wels|48.16|14.02|N
AT|Vorarlberg|Dornbirn|47.41|9.74|N
AZ|Absheron|Khirdalan|40.45|49.76|SN
AZ|Aghjabadi|Aghjabadi|40.05|47.46|S
AZ|Aghdam|Aghdam|39.99|46.93|S
AZ|Agdash|Agdash|40.65|47.48|S
AZ|Aghstafa|Aghstafa|41.12|45.45|S
AZ|Agsu|Agsu|40.57|48.40|S
AZ|Aghdara|Aghdara|40.22|46.81|S
AZ|Astara|Astara|38.46|48.88|S
AZ|Babek|Babek|39.17|45.44|S
AZ|Balakan|Balakan|41.73|46.40|S
AZ|Barda|Barda|40.37|47.13|S
AZ|Beylagan|Beylagan|39.77|47.62|S
AZ|Bilasuvar|Bilasuvar|39.46|48.55|S
AZ|Jabrayil|Jabrayil|39.40|47.03|S
AZ|Jalilabad|Jalilabad|39.21|48.49|S
AZ|Julfa|Julfa|38.96|45.63|S
AZ|Dashkasan|Dashkasan|40.52|46.08|S
AZ|Fuzuli|Fuzuli|39.60|47.15|S
AZ|Gadabay|Gadabay|40.57|45.82|S
AZ|Goranboy|Goranboy|40.61|46.79|S
AZ|Goychay|Goychay|40.65|47.74|S
AZ|Goygol|Goygol|40.59|46.33|S
AZ|Hajigabul|Hajigabul|40.04|48.94|S
AZ|Imishli|Imishli|39.87|48.06|S
AZ|Ismayilli|Ismayilli|40.79|48.15|S
AZ|Kalbajar|Kalbajar|40.11|46.04|S
AZ|Kangarli|Qivraq|39.37|45.17|S
AZ|Kurdamir|Kurdamir|40.34|48.15|S
AZ|Lachin|Lachin|39.64|46.55|S
AZ|Lankaran District|Liman|38.89|48.82|S
AZ|Lerik|Lerik|38.77|48.41|S
AZ|Masally|Masally|39.03|48.67|S
AZ|Neftchala|Neftchala|39.37|49.25|S
AZ|Oghuz|Oghuz|41.07|47.46|S
AZ|Ordubad|Ordubad|38.91|46.02|S
AZ|Qabala|Qabala|40.98|47.85|S
AZ|Qakh|Qakh|41.42|46.92|S
AZ|Qazax|Qazax|41.09|45.37|S
AZ|Gobustan|Gobustan|40.53|48.93|S
AZ|Quba|Quba|41.36|48.51|S
AZ|Qubadli|Qubadli|39.34|46.58|S
AZ|Qusar|Qusar|41.43|48.43|S
AZ|Saatly|Saatly|39.93|48.37|S
AZ|Sabirabad|Sabirabad|40.01|48.48|S
AZ|Sadarak|Heydarabad|39.72|44.85|S
AZ|Shahbuz|Shahbuz|39.41|45.57|S
AZ|Shaki District|Kichik Dahna|40.99|47.08|S
AZ|Salyan|Salyan|39.60|48.98|S
AZ|Shamakhi|Shamakhi|40.63|48.64|S
AZ|Shamkir|Shamkir|40.83|46.02|S
AZ|Samukh|Samukh|40.77|46.40|S
AZ|Sharur|Sharur|39.55|44.98|S
AZ|Siyazan|Siyazan|41.08|49.11|S
AZ|Shusha|Shusha|39.76|46.75|S
AZ|Tartar|Tartar|40.34|46.93|S
AZ|Tovuz|Tovuz|40.99|45.62|S
AZ|Ujar|Ujar|40.52|47.65|S
AZ|Khachmaz|Khachmaz|41.46|48.80|S
AZ|Khizi|Khizi|40.91|49.08|S
AZ|Khojaly|Khojaly|39.91|46.79|S
AZ|Khojavend|Khojavend|39.79|47.11|S
AZ|Yardimli|Yardimli|38.92|48.24|S
AZ|Yevlakh District|Aran|40.63|46.98|S
AZ|Zangilan|Zangilan|39.09|46.65|S
AZ|Zagatala|Zagatala|41.63|46.64|S
AZ|Zardab|Zardab|40.22|47.71|S
AZ|Shabran|Shabran|41.22|48.99|S
AZ|Baku City|Baku|40.38|49.89|SN
AZ|Ganja City|Ganja|40.68|46.36|SN
AZ|Sumqayit City|Sumqayit|40.59|49.67|SN
AZ|Mingachevir City|Mingachevir|40.76|47.06|SN
AZ|Naftalan City|Naftalan|40.50|46.82|S
AZ|Lankaran City|Lankaran|38.75|48.85|SN
AZ|Shaki City|Shaki|41.19|47.17|SN
AZ|Shirvan City|Shirvan|39.94|48.93|SN
AZ|Yevlakh City|Yevlakh|40.62|47.15|SN
AZ|Khankendi City|Khankendi|39.82|46.75|S
AZ|Nakhchivan Autonomous Republic|Nakhchivan|39.21|45.41|SN
BS|Acklins|Masons Bay|22.54|-73.88|S
BS|Berry Islands|Bullocks Harbour|25.75|-77.87|S
BS|Bimini|Alice Town|25.73|-79.30|S
BS|Black Point|Black Point|24.10|-76.40|S
BS|Cat Island|Arthur's Town|24.62|-75.67|S
BS|Central Abaco|Marsh Harbour|26.54|-77.06|SN
BS|Central Andros|Cargill Creek|24.50|-77.72|S
BS|Central Eleuthera|Governor's Harbour|25.19|-76.24|S
BS|City of Freeport|Freeport|26.53|-78.70|SN
BS|Crooked Island and Long Cay|Colonel Hill|22.76|-74.21|S
BS|East Grand Bahama|High Rock|26.63|-78.28|SN
BS|Exuma|George Town|23.52|-75.79|SN
BS|Grand Cay|Grand Cay|27.22|-78.33|S
BS|Harbour Island|Dunmore Town|25.50|-76.64|S
BS|Hope Town|Hope Town|26.54|-76.96|S
BS|Inagua|Matthew Town|20.95|-73.67|S
BS|Long Island|Clarence Town|23.10|-74.98|S
BS|Mangrove Cay|Moxey Town|24.15|-77.76|S
BS|Mayaguana|Abraham's Bay|22.37|-72.97|S
BS|Moore's Island|Hard Bargain|26.32|-77.58|S
BS|New Providence|Nassau|25.06|-77.34|SN
BS|North Abaco|Cooper's Town|26.87|-77.51|SN
BS|North Andros|San Andros|25.07|-78.05|SN
BS|North Eleuthera|Lower Bogue|25.46|-76.71|S
BS|Ragged Island|Duncan Town|22.19|-75.73|S
BS|Rum Cay|Port Nelson|23.64|-74.84|S
BS|San Salvador|Cockburn Town|24.05|-74.53|S
BS|South Abaco|Sandy Point|26.00|-77.40|S
BS|South Andros|Kemp's Bay|24.03|-77.53|S
BS|South Eleuthera|Rock Sound|24.89|-76.17|S
BS|Spanish Wells|Spanish Wells|25.55|-76.76|S
BS|West Grand Bahama|West End|26.69|-78.98|SN
BS|City of Freeport|Lucaya|26.53|-78.67|N
BS|New Providence|Killarney|25.05|-77.42|N
BH|Capital|Manama|26.23|50.59|SN
BH|Muharraq|Muharraq|26.26|50.61|SN
BH|Northern|Hamad Town|26.12|50.51|SN
BH|Southern|Riffa|26.13|50.56|SN
BH|Northern|A'ali|26.16|50.52|N
BH|Capital|Sitra|26.15|50.62|N
BH|Capital|Jidhafs|26.22|50.53|N
BH|Capital|Isa Town|26.17|50.55|N
BH|Northern|Budaiya|26.21|50.45|N
BH|Northern|Diraz|26.22|50.46|N
BD|Barishal|Barishal|22.70|90.37|S
BD|Chattogram|Chattogram|22.36|91.80|SN
BD|Dhaka|Dhaka|23.81|90.41|SN
BD|Khulna|Khulna|22.82|89.55|SN
BD|Mymensingh|Mymensingh|24.75|90.41|SN
BD|Rajshahi|Rajshahi|24.37|88.60|SN
BD|Rangpur|Rangpur|25.75|89.24|SN
BD|Sylhet|Sylhet|24.90|91.87|SN
BD|Dhaka|Gazipur|23.99|90.42|N
BD|Dhaka|Narayanganj|23.62|90.50|N
BD|Rajshahi|Bogura|24.85|89.37|N
BB|Christ Church|Oistins|13.07|-59.53|SN
BB|Saint Andrew|White Hill|13.21|-59.58|SN
BB|Saint George|Bulkeley|13.15|-59.54|S
BB|Saint James|Holetown|13.19|-59.64|SN
BB|Saint John|Four Cross Roads|13.18|-59.48|S
BB|Saint Joseph|Bathsheba|13.21|-59.53|SN
BB|Saint Lucy|Checker Hall|13.30|-59.61|S
BB|Saint Michael|Bridgetown|13.11|-59.62|SN
BB|Saint Peter|Speightstown|13.25|-59.64|SN
BB|Saint Philip|Crane|13.11|-59.45|SN
BB|Saint Thomas|Welchman Hall|13.19|-59.56|S
BB|Christ Church|Hastings|13.08|-59.60|N
BB|Saint Peter|Mile and a Quarter|13.27|-59.62|N
BB|Christ Church|Six Cross Roads|13.12|-59.48|N
BY|Brest Region|Brest|52.10|23.70|SN
BY|Gomel Region|Gomel|52.43|31.00|SN
BY|Grodno Region|Grodno|53.69|23.83|SN
BY|Minsk Region|Borisov|54.23|28.51|SN
BY|Mogilev Region|Mogilev|53.90|30.33|SN
BY|Vitebsk Region|Vitebsk|55.19|30.21|SN
BY|Minsk City|Minsk|53.90|27.57|SN
BY|Mogilev Region|Bobruisk|53.14|29.22|N
BY|Brest Region|Baranovichi|53.13|26.02|N
BY|Brest Region|Pinsk|52.12|26.10|N
BE|Brussels-Capital Region|Brussels|50.85|4.35|SN
BE|Flanders|Antwerp|51.22|4.40|SN
BE|Wallonia|Namur|50.47|4.87|SN
BE|Flanders|Ghent|51.05|3.72|N
BE|Wallonia|Charleroi|50.41|4.44|N
BE|Wallonia|Liège|50.63|5.57|N
BE|Brussels-Capital Region|Anderlecht|50.84|4.31|N
BE|Brussels-Capital Region|Schaerbeek|50.87|4.38|N
BE|Flanders|Bruges|51.21|3.22|N
BE|Flanders|Leuven|50.88|4.70|N
BZ|Belize|Belize City|17.50|-88.20|SN
BZ|Cayo|San Ignacio|17.16|-89.07|SN
BZ|Corozal|Corozal Town|18.39|-88.39|SN
BZ|Orange Walk|Orange Walk Town|18.08|-88.56|SN
BZ|Stann Creek|Dangriga|16.97|-88.23|SN
BZ|Toledo|Punta Gorda|16.10|-88.81|S
BZ|Cayo|Belmopan|17.25|-88.76|N
BZ|Belize|San Pedro|17.92|-87.97|N
BZ|Belize|Ladyville|17.55|-88.29|N
BZ|Cayo|Benque Viejo del Carmen|17.08|-89.14|N
BZ|Toledo|Bella Vista|16.51|-88.53|N
BJ|Alibori|Kandi|11.13|2.94|S
BJ|Atakora|Natitingou|10.30|1.38|S
BJ|Atlantique|Allada|6.67|2.15|S
BJ|Borgou|Parakou|9.34|2.63|SN
BJ|Collines|Dassa-Zoumé|7.75|2.18|S
BJ|Couffo|Aplahoué|6.93|1.68|S
BJ|Donga|Djougou|9.71|1.67|SN
BJ|Littoral|Cotonou|6.37|2.42|SN
BJ|Mono|Lokossa|6.64|1.72|S
BJ|Ouémé|Porto-Novo|6.50|2.60|SN
BJ|Plateau|Pobè|6.98|2.66|S
BJ|Zou|Abomey|7.18|1.99|SN
BJ|Atlantique|Abomey-Calavi|6.45|2.36|N
BJ|Atlantique|Godomey|6.39|2.35|N
BJ|Zou|Bohicon|7.18|2.07|N
BJ|Ouémé|Ekpé|6.39|2.54|N
BJ|Borgou|Nikki|9.94|3.21|N
BM|Devonshire|North Shore Village|32.31|-64.75|S
BM|Hamilton Parish|Flatts Village|32.32|-64.74|S
BM|Paget|Mount Pleasant|32.28|-64.78|S
BM|Pembroke|Stovel Bay|32.31|-64.81|S
BM|Sandys|Somerset Village|32.30|-64.87|S
BM|Smith's|Harrington Hundreds|32.32|-64.73|S
BM|Southampton|Cross Bay|32.25|-64.84|S
BM|Saint George's|Tucker's Town|32.33|-64.70|S
BM|Warwick|Warwick Camp|32.26|-64.81|S
BM|City of Hamilton|Hamilton|32.29|-64.78|SN
BM|Town of St. George|St. George's|32.38|-64.68|SN
BT|Bumthang|Jakar|27.55|90.75|SN
BT|Chukha|Phuentsholing|26.86|89.39|SN
BT|Dagana|Daga|27.08|89.88|S
BT|Gasa|Gasa|27.91|89.73|S
BT|Haa|Haa|27.39|89.28|S
BT|Lhuentse|Lhuentse|27.66|91.18|S
BT|Mongar|Mongar|27.27|91.24|S
BT|Paro|Paro|27.43|89.41|SN
BT|Pema Gatshel|Pema Gatshel|27.04|91.40|S
BT|Punakha|Punakha|27.59|89.88|SN
BT|Samdrup Jongkhar|Samdrup Jongkhar|26.80|91.51|SN
BT|Samtse|Samtse|26.90|89.10|SN
BT|Sarpang|Gelephu|26.87|90.49|SN
BT|Thimphu|Thimphu|27.47|89.64|SN
BT|Trashigang|Trashigang|27.33|91.55|S
BT|Trashiyangtse|Trashiyangtse|27.61|91.50|S
BT|Trongsa|Trongsa|27.50|90.51|S
BT|Tsirang|Damphu|27.04|90.12|S
BT|Wangdue Phodrang|Wangdue Phodrang|27.49|89.90|SN
BT|Zhemgang|Zhemgang|27.22|90.66|S
BT|Pema Gatshel|Nganglam|26.84|91.24|N
```

AU — Six states and two mainland territories; top ten use significant urban areas rather than metropolitan capital-city boundaries. Melbourne and Sydney rankings depend on the population-boundary definition.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.id.com.au\&sz=32)

Informed Decisions



AT — Nine federal states; Sankt Pölten is also written St. Pölten, and Klagenfurt is formally Klagenfurt am Wörthersee.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.migration.gv.at\&sz=32)

migration.gv.at



AZ — Includes 67 districts and 11 separately administered cities, with Aghdara restored in 2023. Nakhchivan is an autonomous republic containing seven districts and its separately administered capital; the latter is represented by the Nakhchivan row. Khankendi is also known as Stepanakert. Liman, Kichik Dahna and Aran represent districts whose namesake cities are separately administered.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.geonames.org\&sz=32)

GeoNames UI+2



BS — Includes 31 local-government districts and New Providence, which is administered separately. Lucaya forms part of the Freeport urban area, while Killarney is part of greater Nassau; both are retained as distinct population-list localities.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.thefactbook.org\&sz=32)

The Factbook+1



BH — Four governorates; Isa Town belongs to Capital Governorate. Riffa encompasses East Riffa and West Riffa.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.crownprince.bh\&sz=32)

crownprince.bh+1



BD — Eight divisions; Barishal was formerly Barisal, Chattogram was Chittagong, and Bogura was Bogra. City rankings use the 2022 census and combine specified urban municipal areas.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.worldometers.info\&sz=32)

Worldometer



BB — Eleven parishes, many without legally defined parish capitals; representative settlements are used. Bridgetown is within Saint Michael. Population rankings count individual settlements rather than the greater Bridgetown urban area.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.geonames.org\&sz=32)

GeoNames



BY — Six regions (oblasts) plus separately administered Minsk City. Minsk is the administrative centre of Minsk Region but lies outside the region itself, so Borisov is used as its largest city. Gomel/Homyel, Grodno/Hrodna, Mogilev/Mahilyow, Borisov/Barysaw and Bobruisk/Babruysk are spelling variants.

BE — Three first-level regions, not the ten second-level provinces. Antwerp represents Flanders because its formal regional capital, Brussels, lies outside Flemish regional territory. Anderlecht and Schaerbeek are separate municipalities within the Brussels urban area; the ranking uses 2026 municipal populations.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.worldometers.info\&sz=32)

Worldometer



BZ — Six districts; Belmopan is the national capital, while San Ignacio is the administrative centre of Cayo District. San Ignacio and Santa Elena are often grouped in population statistics.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://wm-site-staging.cloudflare-47b.workers.dev\&sz=32)

Worldometer



BJ — Twelve departments; Atlantique's administrative centre is Allada rather than the former centre Ouidah. Porto-Novo is the constitutional capital, while Cotonou is the principal government and commercial centre.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.ecolex.org\&sz=32)

ecolex.org



BM — Nine parishes plus two separately incorporated municipalities. The parishes do not have formal administrative capitals, so representative settlements are provided. Only Hamilton and St. George's are included as `N` because they are the two formally designated urban municipalities.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://en.wikipedia.org\&sz=32)

Wikipedia+1



BT — Twenty districts (dzongkhags); Chukha/Chhukha, Pema Gatshel/Pemagatshel and Trashiyangtse/Trashi Yangtse are name variants. Gelephu represents Sarpang as its largest urban centre. The population rankings use the 2017 census.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.worldometers.info\&sz=32)

Worldometer



Points still open:

- AU: Urban-area definitions differ from local-government boundaries, especially for Melbourne, Sydney, Sunshine Coast and Central Coast.

- AZ: Confirm district-level boundary matching for Nakhchivan's nested autonomy and the post-2023 Aghdara, Khojaly and Khojavend administrative areas. Population estimates can change whether Baku suburbs are counted separately.

- BS: Central Andros is represented by Cargill Creek because Fresh Creek, often described as its administrative centre, is placed in North Andros by some geographic datasets. This requires a boundary-level check.&#x20;

  [image](https://www.google.com/s2/favicons?domain=https://www.bahamas.com\&sz=32)

  Official Site+1

- BB: Confirm the representative settlement and current locality population for Saint George, Saint Andrew and other parishes without designated capitals.

- BE: Confirm whether SiteBlitz should treat Brussels's 19 municipalities as separate cities or consolidate them under one Brussels urban area.

- BJ: Confirm whether Godomey and Abomey-Calavi should remain separate populated places or be consolidated for urban-area population ranking.

- BM: Verify representative parish settlements against Overture polygons; parish and municipal boundaries overlap.

- BT: Confirm the top-ten population ranking against a newer complete urban-locality census if one is available.


---

## Claude Code - 2026-11-08 18:34 UTC - 03_claude.md - attachments: none

## Message 3 of 19 - countries
Bolivia (BO), Bosnia & Herzegovina (BA), Botswana (BW), Bouvet Island (BV), Brazil (BR), British Indian Ocean Territory (IO), British Virgin Islands (VG), Brunei (BN), Bulgaria (BG), Burkina Faso (BF), Burundi (BI), Cambodia (KH), Cameroon (CM)

For EACH country above give:
1. every first-level administrative division (state / province / region / governorate ... as it is today),
   with its capital or largest city (kind S);
2. the 10 largest cities of the country by population (kind N) - fewer if the country has fewer.
   A city can appear as both S and N; list it once with kind SN.
Uninhabited territories: one line `CC|-|-|||none`.

Output ONLY one code block, one line per city, pipe-separated, no header, no commentary inside it:
`CC|state|city|lat|lon|kind`
- CC = ISO code above; state and city in English (the name a map would show); lat / lon with 2 decimals.
After the code block: one line per country with any naming caveat (renamed divisions, disputed areas),
then the list of points still open.


---

## ChatGPT (Extra High) - 2026-11-08 18:43 UTC - saved as 03_chatgpt.md

ChatGPT said:
Plain text
BO|Beni|Trinidad|-14.83|-64.90|S
BO|Chuquisaca|Sucre|-19.04|-65.26|SN
BO|Cochabamba|Cochabamba|-17.39|-66.16|SN
BO|La Paz|La Paz|-16.50|-68.15|SN
BO|Oruro|Oruro|-17.97|-67.11|SN
BO|Pando|Cobija|-11.03|-68.77|S
BO|Potosí|Potosí|-19.57|-65.75|SN
BO|Santa Cruz|Santa Cruz de la Sierra|-17.78|-63.18|SN
BO|Tarija|Tarija|-21.53|-64.73|SN
BO|La Paz|El Alto|-16.50|-68.19|N
BO|Cochabamba|Sacaba|-17.40|-66.04|N
BO|Cochabamba|Quillacollo|-17.40|-66.28|N
BA|Federation of Bosnia and Herzegovina|Sarajevo|43.85|18.41|SN
BA|Republika Srpska|Banja Luka|44.78|17.19|SN
BA|Brčko District|Brčko|44.87|18.81|SN
BA|Federation of Bosnia and Herzegovina|Tuzla|44.54|18.68|N
BA|Federation of Bosnia and Herzegovina|Zenica|44.20|17.91|N
BA|Federation of Bosnia and Herzegovina|Mostar|43.34|17.81|N
BA|Republika Srpska|Bijeljina|44.76|19.21|N
BA|Federation of Bosnia and Herzegovina|Bihać|44.82|15.87|N
BA|Republika Srpska|Prijedor|44.98|16.71|N
BA|Republika Srpska|Doboj|44.73|18.09|N
BW|Central|Serowe|-22.38|26.72|SN
BW|Chobe|Kasane|-17.82|25.15|S
BW|Francistown|Francistown|-21.17|27.51|SN
BW|Gaborone|Gaborone|-24.66|25.91|SN
BW|Ghanzi|Ghanzi|-21.57|21.78|S
BW|Jwaneng|Jwaneng|-24.60|24.73|S
BW|Kgalagadi|Tshabong|-26.05|22.45|S
BW|Kgatleng|Mochudi|-24.42|26.15|SN
BW|Kweneng|Molepolole|-24.41|25.50|SN
BW|Lobatse|Lobatse|-25.21|25.68|S
BW|Orapa|Orapa|-21.31|25.37|S
BW|North East|Masunga|-20.62|27.45|S
BW|North West|Maun|-19.98|23.42|SN
BW|Selibe Phikwe|Selebi-Phikwe|-21.98|27.84|S
BW|South East|Ramotswa|-24.88|25.87|S
BW|Southern|Kanye|-24.97|25.33|S
BW|Sowa Town|Sowa Town|-20.56|26.22|S
BW|Kweneng|Mogoditshane|-24.63|25.86|N
BW|South East|Tlokweng|-24.67|25.98|N
BW|Central|Palapye|-22.55|27.13|N
BW|Central|Mahalapye|-23.10|26.83|N
BV|-|-|||none
BR|Acre|Rio Branco|-9.97|-67.81|S
BR|Alagoas|Maceió|-9.67|-35.74|S
BR|Amapá|Macapá|0.04|-51.07|S
BR|Amazonas|Manaus|-3.12|-60.02|SN
BR|Bahia|Salvador|-12.97|-38.50|SN
BR|Ceará|Fortaleza|-3.72|-38.54|SN
BR|Federal District|Brasília|-15.79|-47.88|SN
BR|Espírito Santo|Vitória|-20.32|-40.34|S
BR|Goiás|Goiânia|-16.68|-49.25|SN
BR|Maranhão|São Luís|-2.53|-44.30|S
BR|Mato Grosso|Cuiabá|-15.60|-56.10|S
BR|Mato Grosso do Sul|Campo Grande|-20.47|-54.62|S
BR|Minas Gerais|Belo Horizonte|-19.92|-43.94|SN
BR|Pará|Belém|-1.46|-48.50|S
BR|Paraíba|João Pessoa|-7.12|-34.86|S
BR|Paraná|Curitiba|-25.43|-49.27|SN
BR|Pernambuco|Recife|-8.05|-34.88|SN
BR|Piauí|Teresina|-5.09|-42.80|S
BR|Rio de Janeiro|Rio de Janeiro|-22.91|-43.17|SN
BR|Rio Grande do Norte|Natal|-5.79|-35.21|S
BR|Rio Grande do Sul|Porto Alegre|-30.03|-51.23|S
BR|Rondônia|Porto Velho|-8.76|-63.90|S
BR|Roraima|Boa Vista|2.82|-60.67|S
BR|Santa Catarina|Florianópolis|-27.60|-48.55|S
BR|São Paulo|São Paulo|-23.55|-46.63|SN
BR|Sergipe|Aracaju|-10.92|-37.07|S
BR|Tocantins|Palmas|-10.18|-48.33|S
IO|-|-|||none
VG|Anegada|The Settlement|18.73|-64.33|SN
VG|Jost Van Dyke|Belle Vue|18.45|-64.75|SN
VG|Other Islands|Great Harbour (Peter Island)|18.35|-64.58|S
VG|Tortola|Road Town|18.43|-64.62|SN
VG|Virgin Gorda|Spanish Town|18.45|-64.43|SN
VG|Tortola|East End-Long Look|18.44|-64.57|N
VG|Tortola|West End|18.41|-64.67|N
VG|Tortola|Cane Garden Bay|18.43|-64.66|N
VG|Tortola|Sea Cow's Bay|18.40|-64.63|N
VG|Tortola|Kingstown|18.42|-64.60|N
VG|Tortola|Long Trench|18.44|-64.58|N
BN|Belait|Kuala Belait|4.58|114.23|SN
BN|Brunei-Muara|Bandar Seri Begawan|4.89|114.94|SN
BN|Temburong|Bangar|4.71|115.07|S
BN|Tutong|Tutong|4.80|114.65|SN
BN|Brunei-Muara|Sengkurong|4.88|114.83|N
BN|Brunei-Muara|Mentiri|4.97|115.02|N
BN|Belait|Seria|4.61|114.32|N
BN|Brunei-Muara|Serasa|5.02|115.06|N
BN|Belait|Liang|4.68|114.50|N
BN|Brunei-Muara|Perumahan Negara Panchor|4.97|115.02|N
BN|Tutong|Telisai|4.74|114.56|N
BG|Blagoevgrad|Blagoevgrad|42.02|23.09|S
BG|Burgas|Burgas|42.50|27.47|SN
BG|Dobrich|Dobrich|43.57|27.83|SN
BG|Gabrovo|Gabrovo|42.87|25.32|S
BG|Haskovo|Haskovo|41.93|25.56|S
BG|Kardzhali|Kardzhali|41.65|25.37|S
BG|Kyustendil|Kyustendil|42.28|22.69|S
BG|Lovech|Lovech|43.14|24.72|S
BG|Montana|Montana|43.41|23.22|S
BG|Pazardzhik|Pazardzhik|42.19|24.33|S
BG|Pernik|Pernik|42.60|23.03|S
BG|Pleven|Pleven|43.42|24.61|SN
BG|Plovdiv|Plovdiv|42.14|24.75|SN
BG|Razgrad|Razgrad|43.53|26.52|S
BG|Ruse|Ruse|43.85|25.97|SN
BG|Shumen|Shumen|43.27|26.93|SN
BG|Silistra|Silistra|44.12|27.26|S
BG|Sliven|Sliven|42.68|26.32|SN
BG|Smolyan|Smolyan|41.58|24.70|S
BG|Sofia City|Sofia|42.70|23.32|SN
BG|Sofia Province|Samokov|42.34|23.56|S
BG|Stara Zagora|Stara Zagora|42.43|25.63|SN
BG|Targovishte|Targovishte|43.25|26.57|S
BG|Varna|Varna|43.21|27.92|SN
BG|Veliko Tarnovo|Veliko Tarnovo|43.08|25.63|S
BG|Vidin|Vidin|43.99|22.88|S
BG|Vratsa|Vratsa|43.21|23.56|S
BG|Yambol|Yambol|42.48|26.51|S
BF|Bankui|Dédougou|12.46|-3.46|S
BF|Djôrô|Gaoua|10.32|-3.18|S
BF|Goulmou|Fada N'Gourma|12.06|0.36|SN
BF|Guiriko|Bobo-Dioulasso|11.18|-4.29|SN
BF|Kadiogo|Ouagadougou|12.37|-1.53|SN
BF|Kuilsé|Kaya|13.09|-1.08|SN
BF|Liptako|Dori|14.03|-0.03|S
BF|Nando|Koudougou|12.25|-2.37|SN
BF|Nakambé|Tenkodogo|11.78|-0.37|S
BF|Nazinon|Manga|11.66|-1.07|S
BF|Oubri|Ziniaré|12.58|-1.30|S
BF|Sirba|Bogandé|12.97|-0.15|S
BF|Soum|Djibo|14.10|-1.63|S
BF|Tannounyan|Banfora|10.64|-4.75|SN
BF|Tapoa|Diapaga|12.07|1.79|S
BF|Sourou|Tougan|13.07|-3.07|S
BF|Yaadga|Ouahigouya|13.58|-2.42|SN
BF|Kadiogo|Saaba|12.37|-1.41|N
BF|Nakambé|Pouytenga|12.25|-0.43|N
BF|Guiriko|Houndé|11.50|-3.52|N
BI|Buhumuza|Cankuzo|-3.22|30.55|S
BI|Bujumbura|Bujumbura|-3.38|29.36|SN
BI|Burunga|Makamba|-4.13|29.80|S
BI|Butanyerera|Ngozi|-2.91|29.83|SN
BI|Gitega|Gitega|-3.43|29.93|SN
BI|Butanyerera|Kayanza|-2.92|29.63|N
BI|Buhumuza|Muyinga|-2.85|30.34|N
BI|Burunga|Rumonge|-3.97|29.44|N
BI|Bujumbura|Bubanza|-3.08|29.39|N
BI|Butanyerera|Kirundo|-2.58|30.10|N
BI|Bujumbura|Cibitoke|-2.89|29.12|N
BI|Buhumuza|Giteranyi|-2.55|30.45|N
KH|Banteay Meanchey|Serei Saophoan|13.58|102.98|SN
KH|Battambang|Battambang|13.10|103.20|SN
KH|Kampong Cham|Kampong Cham|12.00|105.46|SN
KH|Kampong Chhnang|Kampong Chhnang|12.25|104.67|SN
KH|Kampong Speu|Chbar Mon|11.47|104.51|S
KH|Kampong Thom|Stung Saen|12.71|104.89|S
KH|Kampot|Kampot|10.61|104.18|S
KH|Kandal|Ta Khmau|11.48|104.95|SN
KH|Kep|Kep|10.48|104.30|S
KH|Koh Kong|Khemarak Phoumin|11.62|102.98|S
KH|Kratie|Kratie|12.49|106.02|S
KH|Mondulkiri|Sen Monorom|12.45|107.20|S
KH|Oddar Meanchey|Samraong|14.18|103.52|S
KH|Pailin|Pailin|12.85|102.61|S
KH|Phnom Penh|Phnom Penh|11.56|104.93|SN
KH|Preah Sihanouk|Sihanoukville|10.63|103.50|SN
KH|Preah Vihear|Tbeng Meanchey|13.81|104.98|S
KH|Prey Veng|Prey Veng|11.49|105.33|S
KH|Pursat|Pursat|12.54|103.92|SN
KH|Ratanakiri|Banlung|13.74|107.00|S
KH|Siem Reap|Siem Reap|13.36|103.86|SN
KH|Stung Treng|Stung Treng|13.53|105.97|S
KH|Svay Rieng|Svay Rieng|11.09|105.80|S
KH|Takeo|Doun Kaev|10.99|104.78|S
KH|Tboung Khmum|Suong|11.91|105.66|S
KH|Banteay Meanchey|Poipet|13.65|102.56|N
CM|Adamawa|Ngaoundéré|7.32|13.59|SN
CM|Centre|Yaoundé|3.87|11.52|SN
CM|East|Bertoua|4.58|13.68|SN
CM|Far North|Maroua|10.59|14.32|SN
CM|Littoral|Douala|4.05|9.70|SN
CM|North|Garoua|9.30|13.39|SN
CM|Northwest|Bamenda|5.96|10.16|SN
CM|South|Ebolowa|2.90|11.15|S
CM|Southwest|Buea|4.15|9.24|S
CM|West|Bafoussam|5.48|10.42|SN
CM|Southwest|Kumba|4.64|9.45|N
CM|Far North|Kousseri|12.08|15.03|N

BO — Nine departments. Sucre is the constitutional capital, while La Paz is the seat of government. Top-ten cities follow 2024 census locality populations; El Alto is counted separately from La Paz. 
Wikipedia
+1

BA — Two entities (Federation of Bosnia and Herzegovina and Republika Srpska) plus separately administered Brčko District. The Federation's ten cantons are second-level divisions. Population rankings use the 2013 census. 
Agencija za unapređenje inozemnih investicija
+1

BW — Ten rural districts and seven urban units are represented. Orapa is included as a special mining town, although its first-level administrative status is not uniform across sources. Selibe Phikwe is also written Selebi-Phikwe. Top-ten settlements use 2022 census locality populations. 
GOV.UK Assets
+1

BV — Bouvet Island is an uninhabited Norwegian dependency with no permanent settlements or administrative subdivisions. 
The Norwegian Offshore Directorate

BR — Twenty-six states plus the Federal District. Brasília represents the Federal District; Vitória is the capital of Espírito Santo, although nearby Vila Velha and Serra are larger municipalities. Top-ten cities use 2025 IBGE municipal population estimates. 
Agência Gov

IO — No permanent civilian settlements or first-level divisions. Diego Garcia has temporary military and contractor personnel. The 2025 UK–Mauritius sovereignty treaty had not entered into force as of October 2026. 
British Indian Ocean Territory
+1

VG — Five island-based statistical groupings are used as geographic coverage proxies, not legally constituted administrative districts. Other Islands is also called Southern Islands; Great Harbour on Peter Island is a geographic representative rather than a formal town. N marks prominent settlements, but their exact population ranking is not verified. 
gadm.org
+2

BN — Four districts. Brunei-Muara is also written Brunei and Muara; the capital's expanded administrative boundary changes population comparisons. Several N entries represent populated mukims or housing settlements rather than separately incorporated cities. 
DEPS
+2

BG — Twenty-eight provinces. Sofia City and Sofia Province are separate; Sofia is the formal administrative centre of both, but Samokov is used as the largest city inside Sofia Province to prevent duplication and ensure geographic coverage. Top-ten cities use December 2025 population estimates. 
Bulgaria Beyond
+1

BF — Seventeen regions under the July 2025 reorganisation, replacing the previous thirteen-region system. New names include Kadiogo (formerly Centre), Guiriko (Hauts-Bassins), and Tannounyan (Cascades); Soum, Sirba, Tapoa and Sourou are newly created regions. Top-ten localities use the 2019 census. 
Présidence du Faso
+1

BI — Five provinces since 2025, replacing eighteen former provinces. Buhumuza has its seat at Cankuzo, Bujumbura at Bujumbura/Mukaza, Burunga at Makamba, Butanyerera at Ngozi and Gitega at Gitega. The top ten are based on recent urban-area estimates rather than the much larger 2024 commune populations. 
PNISAN
+2

KH — Twenty-four provinces plus the separately administered capital Phnom Penh. Serei Saophoan is also known as Sisophon, Sihanoukville as Kampong Som, and Stung Saen as Kampong Thom. Top-ten city populations follow the 2019 census. 
123 Toolbox
+1

CM — Ten regions; Northwest and Southwest are also written North-West and South-West. Regional capitals include Buea (Southwest) and Ebolowa (South). Top-ten population flags use 2026 urban-area estimates, which differ from the older 2005 census ranking. 
ubuea.cm
+1

Points still open:

VG: Obtain a reliable population ranking for individual settlements. Current N flags are coverage candidates, not a verified top ten; confirm whether Other Islands should be represented by an inhabited locality rather than Great Harbour.

BW: Confirm whether Orapa should remain a separate first-level unit in the exact administrative-boundary dataset used by SiteBlitz.

BN: Reconcile city, village, housing-estate and mukim populations, particularly Seria, Mentiri, Sengkurong and Panchor, to prevent overlapping population rankings.

BG: Confirm that the Sofia Province row should remain geographically within the province (Samokov), rather than point to its external administrative seat (Sofia).

BF: Verify that Overture's region boundaries and names reflect the complete July 2025 reorganisation, especially Soum, Sirba, Tapoa and Sourou.

BI: Verify that Overture uses the five-province, 42-commune structure rather than the previous eighteen provinces; reconcile urban-area estimates with the 2024 census.

KH: Confirm population treatment of Ta Khmau and other settlements within the expanding Phnom Penh metropolitan area.

CM: Reconcile the 2026 urban-area ranking with administrative city boundaries if strict city-proper population rankings are required.


---

## Claude Code - 2026-11-08 18:45 UTC - 04_claude.md - attachments: none

## Message 4 of 19 - countries
Canada (CA), Cape Verde (CV), Caribbean Netherlands (BQ), Cayman Islands (KY), Central African Republic (CF), Chad (TD), Chile (CL), China (CN), Christmas Island (CX), Cocos (Keeling) Islands (CC), Colombia (CO), Comoros (KM), Congo - Brazzaville (CG)

For EACH country above give:
1. every first-level administrative division (state / province / region / governorate ... as it is today),
   with its capital or largest city (kind S);
2. the 10 largest cities of the country by population (kind N) - fewer if the country has fewer.
   A city can appear as both S and N; list it once with kind SN.
Uninhabited territories: one line `CC|-|-|||none`.

Output ONLY one code block, one line per city, pipe-separated, no header, no commentary inside it:
`CC|state|city|lat|lon|kind`
- CC = ISO code above; state and city in English (the name a map would show); lat / lon with 2 decimals.
After the code block: one line per country with any naming caveat (renamed divisions, disputed areas),
then the list of points still open.


---

## ChatGPT (Extra High) - 2026-11-08 18:58 UTC - saved as 04_chatgpt.md

```
CA|Alberta|Edmonton|53.55|-113.49|SN
CA|British Columbia|Victoria|48.43|-123.37|S
CA|Manitoba|Winnipeg|49.90|-97.14|SN
CA|New Brunswick|Fredericton|45.96|-66.64|S
CA|Newfoundland and Labrador|St. John's|47.56|-52.71|S
CA|Northwest Territories|Yellowknife|62.45|-114.37|S
CA|Nova Scotia|Halifax|44.65|-63.57|S
CA|Nunavut|Iqaluit|63.75|-68.52|S
CA|Ontario|Toronto|43.65|-79.38|SN
CA|Prince Edward Island|Charlottetown|46.24|-63.13|S
CA|Quebec|Quebec City|46.81|-71.21|SN
CA|Saskatchewan|Regina|50.45|-104.62|S
CA|Yukon|Whitehorse|60.72|-135.06|S
CA|Alberta|Calgary|51.05|-114.07|N
CA|British Columbia|Vancouver|49.28|-123.12|N
CA|Ontario|Ottawa|45.42|-75.69|N
CA|Quebec|Montreal|45.50|-73.57|N
CA|Ontario|Hamilton|43.26|-79.87|N
CA|Ontario|Kitchener|43.45|-80.49|N
CV|Boa Vista|Sal Rei|16.18|-22.92|SN
CV|Brava|Nova Sintra|14.87|-24.70|S
CV|Maio|Vila do Maio|15.14|-23.21|S
CV|Mosteiros|Mosteiros|15.03|-24.33|S
CV|Paul|Pombas|17.15|-25.02|S
CV|Porto Novo|Porto Novo|17.02|-25.06|SN
CV|Praia|Praia|14.93|-23.51|SN
CV|Ribeira Brava|Ribeira Brava|16.62|-24.20|S
CV|Ribeira Grande|Ponta do Sol|17.20|-25.09|S
CV|Ribeira Grande de Santiago|Cidade Velha|14.92|-23.61|S
CV|Sal|Espargos|16.76|-22.94|SN
CV|Santa Catarina|Assomada|15.10|-23.68|SN
CV|Santa Catarina do Fogo|Cova Figueira|14.90|-24.34|S
CV|Santa Cruz|Pedra Badejo|15.14|-23.53|SN
CV|São Domingos|São Domingos|15.02|-23.56|S
CV|São Filipe|São Filipe|14.90|-24.50|SN
CV|São Lourenço dos Órgãos|João Teves|15.08|-23.60|S
CV|São Miguel|Calheta de São Miguel|15.19|-23.59|S
CV|São Salvador do Mundo|Picos|15.09|-23.64|S
CV|São Vicente|Mindelo|16.89|-24.98|SN
CV|Tarrafal|Tarrafal|15.28|-23.75|SN
CV|Tarrafal de São Nicolau|Tarrafal de São Nicolau|16.57|-24.36|S
CV|Sal|Santa Maria|16.60|-22.90|N
BQ|Bonaire|Kralendijk|12.15|-68.27|SN
BQ|Sint Eustatius|Oranjestad|17.48|-62.99|SN
BQ|Saba|The Bottom|17.63|-63.25|SN
BQ|Bonaire|Rincon|12.24|-68.33|N
BQ|Saba|Windwardside|17.63|-63.23|N
BQ|Saba|Zion's Hill|17.64|-63.23|N
BQ|Saba|Saint John's|17.63|-63.24|N
KY|Bodden Town|Bodden Town|19.28|-81.25|SN
KY|East End|East End|19.30|-81.12|SN
KY|George Town|George Town|19.30|-81.38|SN
KY|North Side|North Side|19.35|-81.20|SN
KY|Sister Islands|Stake Bay|19.72|-79.80|S
KY|West Bay|West Bay|19.37|-81.40|SN
KY|Bodden Town|Savannah|19.27|-81.30|N
KY|Bodden Town|Lower Valley|19.28|-81.33|N
KY|George Town|Prospect|19.29|-81.35|N
KY|George Town|Red Bay|19.30|-81.36|N
CF|Plateaux|Boali|4.80|18.13|S
CF|Équateur|Berbérati|4.26|15.79|SN
CF|Yadé|Bossangoa|6.49|17.45|SN
CF|Kagas|Sibut|5.73|19.08|S
CF|Fertit|Bria|6.54|21.99|SN
CF|Haut-Oubangui|Bangassou|4.74|22.82|SN
CF|Bas-Oubangui|Bangui|4.36|18.56|SN
CF|Kagas|Bambari|5.76|20.68|N
CF|Équateur|Bouar|5.94|15.59|N
CF|Équateur|Carnot|4.94|15.88|N
CF|Kagas|Kaga-Bandoro|6.99|19.18|N
CF|Yadé|Paoua|7.24|16.44|N
TD|Barh El Gazel|Moussoro|13.64|16.49|S
TD|Batha|Ati|13.22|18.34|S
TD|Borkou|Faya-Largeau|17.93|19.10|S
TD|Chari-Baguirmi|Massenya|11.40|16.17|S
TD|Ennedi Est|Amdjarass|16.07|22.84|S
TD|Ennedi Ouest|Fada|17.19|21.58|S
TD|Guéra|Mongo|12.18|18.69|S
TD|Hadjer-Lamis|Massakory|12.99|15.73|S
TD|Kanem|Mao|14.12|15.31|S
TD|Lac|Bol|13.46|14.71|S
TD|Logone Occidental|Moundou|8.57|16.08|SN
TD|Logone Oriental|Doba|8.66|16.85|SN
TD|Mandoul|Koumra|8.91|17.55|S
TD|Mayo-Kebbi Est|Bongor|10.28|15.37|SN
TD|Mayo-Kebbi Ouest|Pala|9.36|14.91|SN
TD|Moyen-Chari|Sarh|9.15|18.38|SN
TD|N'Djamena|N'Djamena|12.11|15.04|SN
TD|Ouaddaï|Abéché|13.83|20.83|SN
TD|Salamat|Am Timan|11.04|20.28|SN
TD|Sila|Goz Beida|12.23|21.41|SN
TD|Tandjilé|Laï|9.40|16.30|S
TD|Tibesti|Bardaï|21.35|17.00|S
TD|Wadi Fira|Biltine|14.53|20.93|S
TD|Tandjilé|Kélo|9.31|15.81|N
CL|Arica and Parinacota|Arica|-18.48|-70.31|S
CL|Tarapacá|Iquique|-20.21|-70.15|S
CL|Antofagasta|Antofagasta|-23.65|-70.40|SN
CL|Atacama|Copiapó|-27.37|-70.33|S
CL|Coquimbo|La Serena|-29.90|-71.25|S
CL|Valparaíso|Valparaíso|-33.05|-71.62|SN
CL|Santiago Metropolitan Region|Santiago|-33.45|-70.67|SN
CL|O'Higgins|Rancagua|-34.17|-70.74|S
CL|Maule|Talca|-35.43|-71.66|S
CL|Ñuble|Chillán|-36.61|-72.10|S
CL|Biobío|Concepción|-36.83|-73.05|S
CL|Araucanía|Temuco|-38.74|-72.60|SN
CL|Los Ríos|Valdivia|-39.82|-73.25|S
CL|Los Lagos|Puerto Montt|-41.47|-72.94|S
CL|Aysén|Coyhaique|-45.58|-72.07|S
CL|Magallanes and Chilean Antarctica|Punta Arenas|-53.16|-70.91|S
CL|Santiago Metropolitan Region|Puente Alto|-33.61|-70.57|N
CL|Santiago Metropolitan Region|Maipú|-33.52|-70.76|N
CL|Santiago Metropolitan Region|La Florida|-33.52|-70.60|N
CL|Valparaíso|Viña del Mar|-33.02|-71.55|N
CL|Santiago Metropolitan Region|San Bernardo|-33.59|-70.70|N
CL|Santiago Metropolitan Region|Las Condes|-33.41|-70.57|N
CN|Anhui|Hefei|31.82|117.23|S
CN|Beijing|Beijing|39.90|116.40|SN
CN|Chongqing|Chongqing|29.56|106.55|SN
CN|Fujian|Fuzhou|26.07|119.30|S
CN|Gansu|Lanzhou|36.06|103.83|S
CN|Guangdong|Guangzhou|23.13|113.27|SN
CN|Guangxi Zhuang Autonomous Region|Nanning|22.82|108.32|S
CN|Guizhou|Guiyang|26.65|106.63|S
CN|Hainan|Haikou|20.03|110.35|S
CN|Hebei|Shijiazhuang|38.04|114.52|S
CN|Heilongjiang|Harbin|45.80|126.53|S
CN|Henan|Zhengzhou|34.75|113.63|S
CN|Hong Kong SAR|Hong Kong|22.28|114.16|S
CN|Hubei|Wuhan|30.59|114.30|SN
CN|Hunan|Changsha|28.23|112.94|S
CN|Inner Mongolia|Hohhot|40.84|111.75|S
CN|Jiangsu|Nanjing|32.06|118.80|S
CN|Jiangxi|Nanchang|28.68|115.86|S
CN|Jilin|Changchun|43.82|125.32|S
CN|Liaoning|Shenyang|41.80|123.43|S
CN|Macau SAR|Macau|22.20|113.55|S
CN|Ningxia Hui Autonomous Region|Yinchuan|38.49|106.23|S
CN|Qinghai|Xining|36.62|101.78|S
CN|Shaanxi|Xi'an|34.34|108.94|SN
CN|Shandong|Jinan|36.67|117.00|S
CN|Shanghai|Shanghai|31.23|121.47|SN
CN|Shanxi|Taiyuan|37.87|112.55|S
CN|Sichuan|Chengdu|30.67|104.07|SN
CN|Tianjin|Tianjin|39.12|117.20|SN
CN|Tibet Autonomous Region|Lhasa|29.65|91.13|S
CN|Xinjiang Uygur Autonomous Region|Urumqi|43.83|87.62|S
CN|Yunnan|Kunming|25.04|102.71|S
CN|Zhejiang|Hangzhou|30.27|120.16|S
CN|Guangdong|Shenzhen|22.54|114.06|N
CN|Guangdong|Dongguan|23.02|113.75|N
CX|Christmas Island|Flying Fish Cove|-10.42|105.68|SN
CX|Christmas Island|Poon Saan|-10.43|105.68|N
CX|Christmas Island|Drumsite|-10.43|105.67|N
CX|Christmas Island|Silver City|-10.42|105.68|N
CX|Christmas Island|Kampong|-10.42|105.67|N
CC|Home Island|Bantam|-12.12|96.90|SN
CC|West Island|West Island|-12.19|96.83|SN
CO|Amazonas|Leticia|-4.21|-69.94|S
CO|Antioquia|Medellín|6.25|-75.56|SN
CO|Arauca|Arauca|7.08|-70.76|S
CO|Atlántico|Barranquilla|10.96|-74.80|SN
CO|Bogotá Capital District|Bogotá|4.71|-74.07|SN
CO|Bolívar|Cartagena|10.39|-75.48|SN
CO|Boyacá|Tunja|5.54|-73.36|S
CO|Caldas|Manizales|5.07|-75.52|S
CO|Caquetá|Florencia|1.62|-75.61|S
CO|Casanare|Yopal|5.35|-72.41|S
CO|Cauca|Popayán|2.44|-76.61|S
CO|Cesar|Valledupar|10.46|-73.25|SN
CO|Chocó|Quibdó|5.69|-76.66|S
CO|Córdoba|Montería|8.75|-75.88|S
CO|Cundinamarca|Soacha|4.58|-74.21|S
CO|Guainía|Inírida|3.87|-67.93|S
CO|Guaviare|San José del Guaviare|2.57|-72.64|S
CO|Huila|Neiva|2.93|-75.28|S
CO|La Guajira|Riohacha|11.54|-72.91|S
CO|Magdalena|Santa Marta|11.24|-74.20|S
CO|Meta|Villavicencio|4.14|-73.63|S
CO|Nariño|Pasto|1.21|-77.28|S
CO|Norte de Santander|Cúcuta|7.89|-72.51|SN
CO|Putumayo|Mocoa|1.15|-76.65|S
CO|Quindío|Armenia|4.53|-75.68|S
CO|Risaralda|Pereira|4.81|-75.69|SN
CO|San Andrés and Providencia|San Andrés|12.58|-81.70|S
CO|Santander|Bucaramanga|7.12|-73.12|SN
CO|Sucre|Sincelejo|9.30|-75.40|S
CO|Tolima|Ibagué|4.44|-75.24|SN
CO|Valle del Cauca|Cali|3.45|-76.53|SN
CO|Vaupés|Mitú|1.25|-70.23|S
CO|Vichada|Puerto Carreño|6.19|-67.48|S
KM|Grande Comore|Moroni|-11.70|43.26|SN
KM|Anjouan|Mutsamudu|-12.17|44.40|SN
KM|Mohéli|Fomboni|-12.29|43.74|SN
KM|Anjouan|Tsémbéhou|-12.21|44.46|N
KM|Anjouan|Domoni|-12.26|44.53|N
KM|Anjouan|Mirontsi|-12.16|44.41|N
KM|Anjouan|Ouani|-12.14|44.42|N
KM|Anjouan|Sima|-12.20|44.28|N
KM|Grande Comore|Iconi|-11.74|43.24|N
KM|Anjouan|Mrémani|-12.31|44.50|N
CG|Bouenza|Madingou|-4.15|13.55|S
CG|Brazzaville|Brazzaville|-4.27|15.28|SN
CG|Congo-Oubangui|Mossaka|-1.23|16.80|S
CG|Cuvette|Owando|-0.48|15.90|SN
CG|Cuvette-Ouest|Ewo|-0.87|14.82|S
CG|Djoué-Léfini|Odziba|-3.58|15.51|S
CG|Kouilou|Loango|-4.65|11.81|S
CG|Lékoumou|Sibiti|-3.68|13.35|S
CG|Likouala|Impfondo|1.63|18.06|S
CG|Nkéni-Alima|Gamboma|-1.87|15.86|SN
CG|Niari|Dolisie|-4.20|12.67|SN
CG|Plateaux|Djambala|-2.54|14.75|S
CG|Pointe-Noire|Pointe-Noire|-4.79|11.85|SN
CG|Pool|Kinkala|-4.36|14.76|S
CG|Sangha|Ouesso|1.61|16.05|SN
CG|Bouenza|Nkayi|-4.18|13.29|N
CG|Brazzaville|Kintélé|-4.14|15.35|N
CG|Cuvette|Oyo|-1.16|15.97|N
CG|Likouala|Bétou|3.05|18.52|N
```

CA — Ten provinces and three territories; top-ten cities use 2025 census metropolitan-area estimates, with Kitchener representing Kitchener–Cambridge–Waterloo and Ottawa representing Ottawa–Gatineau. Montréal/Montreal and Québec/Quebec are spelling variants.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.statista.com\&sz=32)

Statista



CV — Officially Cabo Verde; 22 municipalities (concelhos). Espargos is the municipal seat of Sal, while Ponta do Sol is the seat of Ribeira Grande. Santa Maria is retained as the tenth distinct urban locality because some geographical rankings duplicate Pedra Badejo under Santa Cruz.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.mf.gov.cv\&sz=32)

mf.gov.cv+2



BQ — Three special municipalities of the Netherlands: Bonaire, Sint Eustatius and Saba. Seven distinct settlements are listed using 2024 estimates; the Kralendijk figure incorporates Antriol, Nikiboko and other neighbourhoods rather than treating them as independent cities.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://wm-site-staging.cloudflare-47b.workers.dev\&sz=32)

Worldometer



KY — Six districts, with Sister Islands covering Cayman Brac and Little Cayman. Stake Bay represents the Cayman Brac administrative centre. Savannah, Lower Valley, Prospect and Red Bay are additional populated communities; the 2021 census supports district totals but not a verified ten-place ranking.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://statistics.caricom.org\&sz=32)

statistics.caricom.org



CF — Seven regions under the administrative reform, above 20 prefectures. Plateaux/Plateau and Kagas/Kaga are alternative regional names. The ten largest `N` localities follow the official 2024 city table, with Bangui counted as a single city rather than adding its metropolitan suburbs separately.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.minurbanisme-rca.org\&sz=32)

minurbanisme-rca.org+1



TD — Twenty-three provinces, with naming alternatives such as Ennedi-Est/Ennedi Est and Barh El Gazel/Bahr el Gazel. Lac and Mayo-Kebbi Ouest are retained under widely used administrative names; the applicability of newer naming variants requires checking against the production boundary data.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://openadmindata.org\&sz=32)

Province in Chad



CL — Sixteen regions. O'Higgins is formally Libertador General Bernardo O'Higgins; Aysén and Magallanes also have longer official names. The ten `N` flags use the 2024 census ranking of communes, which includes several independently administered municipalities within Greater Santiago.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://observatoriopublico.cl\&sz=32)

Observatorio Público



CN — Thirty-three administered provincial-level units are listed: 22 provinces, five autonomous regions, four municipalities and two special administrative regions. Taiwan, which China claims but does not administer, is excluded for separate ISO `TW` coverage; Hong Kong and Macau also have ISO entries `HK` and `MO`. Population flags follow a 2020 urban-core approach rather than entire prefecture-level administrative populations.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.mdpi.com\&sz=32)

MDPI+1



CX — Christmas Island is an inhabited Australian external territory with one local-government area, the Shire of Christmas Island, rather than separate first-level provinces. Flying Fish Cove is also known as The Settlement; other entries are residential communities, not independent incorporated cities.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.infrastructure.gov.au\&sz=32)

Infrastructure and Transport Department



CC — Only Home Island and West Island are inhabited. They are used as geographic coverage units rather than formal first-level subdivisions; Bantam is the principal settlement on Home Island, while West Island is the administrative centre.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.infrastructure.gov.au\&sz=32)

Infrastructure and Transport Department



CO — Thirty-two departments and separately administered Bogotá Capital District. Bogotá is also the administrative seat of Cundinamarca but lies outside the department, so Soacha represents the largest city within it. The ten `N` flags follow 2026 UN urban-agglomeration estimates.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://statisticstimes.com\&sz=32)

Statistics Times



KM — Three autonomous islands: Ngazidja (Grande Comore), Ndzuwani (Anjouan) and Mwali (Mohéli). The ten largest localities use the 2017 census; Tsémbéhou/Tsimbeo and Mutsamudu/Moutsamoudou are spelling variants. French-administered Mayotte is excluded for separate ISO `YT` coverage.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://inseed-comores.org\&sz=32)

INSEED Comores+1



CG — Fifteen departments following the October 2024 reform, including newly created Congo-Oubangui, Djoué-Léfini and Nkéni-Alima. Kintélé now belongs to Brazzaville Department rather than Pool. The ten `N` flags use the May 2023 census; Dolisie was formerly Loubomo and Nkayi was formerly Jacob.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.makanisi.org\&sz=32)

makanisi.org+2



Points still open:

- CA: Match metropolitan population centres to individual municipal and Overture locality boundaries, particularly Ottawa–Gatineau and Kitchener–Cambridge–Waterloo.
- CV: Confirm the tenth-largest distinct town using a single consistent 2021 census locality dataset; some GeoNames records overlap in Santa Cruz.
- KY: Obtain settlement-level populations to verify the four additional `N` communities and the overall top-ten ranking.
- CF: Check whether Overture contains the seven current regions or older prefecture-level boundaries as its highest subnational layer.
- TD: Resolve post-2024 provincial naming variants and confirm that the top-ten cities use consistent settlement boundaries.
- CL: Decide whether the final audit should use communes or continuous urban agglomerations; the current ranking uses communes.
- CN: Reconcile top-ten rankings under the 2020 census urban-core definition versus newer UN agglomeration definitions. Confirm ISO handling for Taiwan, Hong Kong and Macau to avoid duplicated place extraction.
- CX/CC: The state fields are territory-wide or island-based coverage proxies, not formal first-level administrative units. Confirm whether the extraction hierarchy permits those synthetic divisions.
- CO: Verify that Soacha is assigned to Cundinamarca while Bogotá is kept in its separate Capital District, and that metro-area city rankings do not introduce duplicate localities.
- CG: Confirm that Overture reflects the 2024 creation of three departments and the transfer of Kintélé to Brazzaville Department.


---

## Claude Code - 2026-11-08 18:59 UTC - 05_claude.md - attachments: none

## Check of your lists so far (businesses in our data within 10 km of each city, or with that city name)
Round 1: 263 reference lines, 260 cities, 259 with business data (100 %).
Round 2: 251 reference lines, 251 cities, 250 with business data (100 %).
Round 3: 192 reference lines, 190 cities, 190 with business data (100 %).
Round 4: 221 reference lines, 221 cities, 221 with business data (100 %).
Not covered: - AS: 11/12 cities covered, 4,958 businesses near them; no data at: Taulaga
Not covered: - BS: 33/34 cities covered, 13,861 businesses near them; no data at: Moxey Town

Thank you - same format again:


## Message 5 of 19 - countries
Congo - Kinshasa (CD), Cook Islands (CK), Costa Rica (CR), Côte d’Ivoire (CI), Croatia (HR), Cuba (CU), Curaçao (CW), Cyprus (CY), Czechia (CZ), Denmark (DK), Djibouti (DJ), Dominica (DM), Dominican Republic (DO)

For EACH country above give:
1. every first-level administrative division (state / province / region / governorate ... as it is today),
   with its capital or largest city (kind S);
2. the 10 largest cities of the country by population (kind N) - fewer if the country has fewer.
   A city can appear as both S and N; list it once with kind SN.
Uninhabited territories: one line `CC|-|-|||none`.

Output ONLY one code block, one line per city, pipe-separated, no header, no commentary inside it:
`CC|state|city|lat|lon|kind`
- CC = ISO code above; state and city in English (the name a map would show); lat / lon with 2 decimals.
After the code block: one line per country with any naming caveat (renamed divisions, disputed areas),
then the list of points still open.


---

## ChatGPT (Extra High) - 2026-11-08 19:13 UTC - saved as 05_chatgpt.md

```
CD|Bas-Uele|Buta|2.79|24.73|S
CD|Equateur|Mbandaka|0.05|18.26|S
CD|Haut-Katanga|Lubumbashi|-11.66|27.48|SN
CD|Haut-Lomami|Kamina|-8.74|24.99|S
CD|Haut-Uele|Isiro|2.77|27.62|S
CD|Ituri|Bunia|1.56|30.25|S
CD|Kasai|Tshikapa|-6.42|20.80|SN
CD|Kasai-Central|Kananga|-5.90|22.42|SN
CD|Kasai-Oriental|Mbuji-Mayi|-6.14|23.59|SN
CD|Kinshasa|Kinshasa|-4.32|15.31|SN
CD|Kongo Central|Matadi|-5.82|13.45|S
CD|Kwango|Kenge|-4.81|17.04|S
CD|Kwilu|Bandundu|-3.32|17.38|S
CD|Lomami|Kabinda|-6.13|24.48|S
CD|Lualaba|Kolwezi|-10.71|25.47|S
CD|Mai-Ndombe|Inongo|-1.93|18.28|S
CD|Maniema|Kindu|-2.95|25.92|S
CD|Mongala|Lisala|2.15|21.52|S
CD|North Kivu|Goma|-1.68|29.23|SN
CD|North Ubangi|Gbadolite|4.28|21.00|S
CD|Sankuru|Lusambo|-4.97|23.45|S
CD|South Kivu|Bukavu|-2.51|28.86|SN
CD|South Ubangi|Gemena|3.25|19.78|S
CD|Tanganyika|Kalemie|-5.95|29.19|SN
CD|Tshopo|Kisangani|0.52|25.20|SN
CD|Tshuapa|Boende|-0.22|20.87|S
CD|North Kivu|Beni|0.49|29.47|N
CK|Aitutaki|Arutanga|-18.87|-159.80|S
CK|Atiu|Teenui|-20.00|-158.12|S
CK|Mangaia|Oneroa|-21.92|-157.95|S
CK|Manihiki|Tauhunu|-10.42|-161.03|S
CK|Mauke|Kimiangatau|-20.14|-157.36|S
CK|Mitiaro|Takaue|-19.82|-157.72|S
CK|Palmerston|Palmerston|-18.06|-163.21|S
CK|Penrhyn|Omoka|-8.98|-158.05|S
CK|Pukapuka and Nassau|Roto|-10.88|-165.83|S
CK|Rakahanga|Rakahanga|-10.03|-161.10|S
CK|Rarotonga|Avarua|-21.21|-159.77|SN
CK|Rarotonga|Arorangi|-21.23|-159.83|N
CK|Rarotonga|Titikaveka|-21.27|-159.76|N
CK|Rarotonga|Matavera|-21.22|-159.73|N
CK|Rarotonga|Ngatangiia|-21.24|-159.73|N
CK|Aitutaki|Vaipae|-18.87|-159.78|N
CK|Aitutaki|Amuri|-18.85|-159.79|N
CK|Aitutaki|Nikaupara|-18.87|-159.80|N
CK|Mangaia|Te Makatea|-21.93|-157.95|N
CK|Aitutaki|Tautu|-18.88|-159.78|N
CR|Alajuela|Alajuela|10.02|-84.21|SN
CR|Cartago|Cartago|9.86|-83.92|S
CR|Guanacaste|Liberia|10.63|-85.44|SN
CR|Heredia|Heredia|9.99|-84.12|S
CR|Limon|Limon|9.99|-83.04|SN
CR|Puntarenas|Puntarenas|9.98|-84.84|SN
CR|San Jose|San Jose|9.93|-84.08|SN
CR|Cartago|Paraiso|9.84|-83.87|N
CR|San Jose|San Isidro de El General|9.37|-83.70|N
CR|San Jose|Curridabat|9.91|-84.04|N
CR|San Jose|San Vicente de Moravia|9.96|-84.05|N
CR|San Jose|Purral|9.96|-84.03|N
CI|Abidjan Autonomous District|Abidjan|5.35|-4.02|SN
CI|Agnéby-Tiassa|Agboville|5.93|-4.22|S
CI|Bafing|Touba|8.28|-7.68|S
CI|Bagoué|Boundiali|9.52|-6.49|S
CI|Bélier|Toumodi|6.56|-5.02|S
CI|Béré|Mankono|8.06|-6.18|S
CI|Bounkani|Bouna|9.27|-3.00|S
CI|Cavally|Guiglo|6.55|-7.50|S
CI|Folon|Minignan|9.99|-7.84|S
CI|Gbêkê|Bouaké|7.69|-5.03|SN
CI|Gbôklé|Sassandra|4.95|-6.09|S
CI|Gôh|Gagnoa|6.13|-5.95|SN
CI|Gontougo|Bondoukou|8.04|-2.80|S
CI|Grands-Ponts|Dabou|5.32|-4.38|S
CI|Guémon|Duékoué|6.74|-7.35|S
CI|Hambol|Katiola|8.14|-5.10|S
CI|Haut-Sassandra|Daloa|6.88|-6.45|SN
CI|Iffou|Daoukro|7.06|-3.97|S
CI|Indénié-Djuablin|Abengourou|6.73|-3.49|S
CI|Kabadougou|Odienné|9.50|-7.56|S
CI|La Mé|Adzopé|6.10|-3.86|S
CI|Lôh-Djiboua|Divo|5.84|-5.36|SN
CI|Marahoué|Bouaflé|6.99|-5.75|S
CI|Moronou|Bongouanou|6.65|-4.20|S
CI|Nawa|Soubré|5.79|-6.61|SN
CI|N'Zi|Dimbokro|6.65|-4.71|S
CI|Poro|Korhogo|9.46|-5.63|SN
CI|San-Pédro|San-Pédro|4.75|-6.63|SN
CI|Sud-Comoé|Aboisso|5.47|-3.21|S
CI|Tchologo|Ferkessédougou|9.59|-5.20|S
CI|Tonkpi|Man|7.41|-7.55|SN
CI|Worodougou|Séguéla|7.96|-6.67|S
CI|Yamoussoukro Autonomous District|Yamoussoukro|6.82|-5.27|SN
HR|Bjelovar-Bilogora|Bjelovar|45.90|16.84|S
HR|Brod-Posavina|Slavonski Brod|45.16|18.01|SN
HR|City of Zagreb|Zagreb|45.81|15.98|SN
HR|Dubrovnik-Neretva|Dubrovnik|42.65|18.09|S
HR|Istria|Pazin|45.24|13.94|S
HR|Karlovac|Karlovac|45.49|15.56|SN
HR|Koprivnica-Križevci|Koprivnica|46.16|16.83|S
HR|Krapina-Zagorje|Krapina|46.16|15.87|S
HR|Lika-Senj|Gospić|44.55|15.37|S
HR|Međimurje|Čakovec|46.38|16.43|S
HR|Osijek-Baranja|Osijek|45.55|18.69|SN
HR|Požega-Slavonia|Požega|45.34|17.69|S
HR|Primorje-Gorski Kotar|Rijeka|45.33|14.44|SN
HR|Šibenik-Knin|Šibenik|43.73|15.90|S
HR|Sisak-Moslavina|Sisak|45.49|16.38|S
HR|Split-Dalmatia|Split|43.51|16.44|SN
HR|Varaždin|Varaždin|46.31|16.34|SN
HR|Virovitica-Podravina|Virovitica|45.83|17.39|S
HR|Vukovar-Srijem|Vukovar|45.35|19.00|S
HR|Zadar|Zadar|44.12|15.23|SN
HR|Zagreb County|Velika Gorica|45.72|16.08|SN
HR|Istria|Pula|44.87|13.85|N
CU|Artemisa|Artemisa|22.81|-82.76|S
CU|Camagüey|Camagüey|21.38|-77.92|SN
CU|Ciego de Ávila|Ciego de Ávila|21.84|-78.76|S
CU|Cienfuegos|Cienfuegos|22.15|-80.44|SN
CU|Granma|Bayamo|20.38|-76.64|SN
CU|Guantánamo|Guantánamo|20.14|-75.21|SN
CU|Havana|Havana|23.11|-82.37|SN
CU|Holguín|Holguín|20.89|-76.26|SN
CU|Isla de la Juventud|Nueva Gerona|21.88|-82.80|S
CU|Las Tunas|Las Tunas|20.96|-76.95|SN
CU|Matanzas|Matanzas|23.04|-81.58|SN
CU|Mayabeque|San José de las Lajas|22.96|-82.15|S
CU|Pinar del Río|Pinar del Río|22.42|-83.70|S
CU|Sancti Spíritus|Sancti Spíritus|21.93|-79.44|S
CU|Santiago de Cuba|Santiago de Cuba|20.02|-75.83|SN
CU|Villa Clara|Santa Clara|22.41|-79.97|SN
CW|Curaçao|Willemstad|12.11|-68.93|SN
CY|Famagusta|Famagusta|35.12|33.94|SN
CY|Kyrenia|Kyrenia|35.34|33.32|SN
CY|Larnaca|Larnaca|34.92|33.63|SN
CY|Limassol|Limassol|34.68|33.04|SN
CY|Nicosia|Nicosia|35.17|33.36|SN
CY|Paphos|Paphos|34.78|32.42|SN
CY|Nicosia|Strovolos|35.15|33.34|N
CY|Nicosia|Lakatamia|35.12|33.30|N
CY|Limassol|Kato Polemidia|34.69|32.99|N
CY|Larnaca|Aradippou|34.95|33.59|N
CZ|Central Bohemian|Kladno|50.15|14.10|S
CZ|Hradec Králové|Hradec Králové|50.21|15.83|SN
CZ|Karlovy Vary|Karlovy Vary|50.23|12.87|S
CZ|Liberec|Liberec|50.77|15.06|SN
CZ|Moravian-Silesian|Ostrava|49.84|18.29|SN
CZ|Olomouc|Olomouc|49.59|17.25|SN
CZ|Pardubice|Pardubice|50.04|15.78|SN
CZ|Plzeň|Plzeň|49.74|13.38|SN
CZ|Prague|Prague|50.08|14.42|SN
CZ|South Bohemian|České Budějovice|48.97|14.48|SN
CZ|South Moravian|Brno|49.20|16.61|SN
CZ|Ústí nad Labem|Ústí nad Labem|50.66|14.04|SN
CZ|Vysočina|Jihlava|49.40|15.59|S
CZ|Zlín|Zlín|49.22|17.67|S
DK|Capital Region|Copenhagen|55.68|12.57|SN
DK|Central Denmark|Viborg|56.45|9.40|S
DK|North Denmark|Aalborg|57.05|9.92|SN
DK|Southern Denmark|Vejle|55.71|9.54|SN
DK|Zealand|Sorø|55.43|11.56|S
DK|Central Denmark|Aarhus|56.16|10.20|N
DK|Southern Denmark|Odense|55.40|10.39|N
DK|Southern Denmark|Esbjerg|55.47|8.45|N
DK|Central Denmark|Horsens|55.86|9.85|N
DK|Central Denmark|Randers|56.46|10.04|N
DK|Southern Denmark|Kolding|55.49|9.47|N
DK|Zealand|Roskilde|55.64|12.08|N
DJ|Ali Sabieh|Ali Sabieh|11.16|42.71|SN
DJ|Arta|Arta|11.53|42.85|SN
DJ|Dikhil|Dikhil|11.11|42.37|SN
DJ|Djibouti|Djibouti|11.59|43.15|SN
DJ|Obock|Obock|11.97|43.29|SN
DJ|Tadjourah|Tadjourah|11.79|42.89|SN
DJ|Ali Sabieh|Ali Adde|11.13|42.89|N
DJ|Arta|Cheik Farah|11.49|43.18|N
DJ|Dikhil|As Eyla|11.01|42.10|N
DJ|Arta|Damerjog|11.48|43.18|N
DM|Saint Andrew|Marigot|15.54|-61.29|SN
DM|Saint David|Castle Bruce|15.44|-61.26|S
DM|Saint George|Roseau|15.30|-61.39|SN
DM|Saint John|Portsmouth|15.58|-61.46|SN
DM|Saint Joseph|Saint Joseph|15.41|-61.43|SN
DM|Saint Luke|Pointe Michel|15.26|-61.38|SN
DM|Saint Mark|Soufrière|15.24|-61.36|S
DM|Saint Patrick|Grand Bay|15.23|-61.30|SN
DM|Saint Paul|Mahaut|15.36|-61.40|SN
DM|Saint Peter|Colihaut|15.49|-61.46|S
DM|Saint Paul|Canefield|15.34|-61.39|N
DM|Saint Joseph|Salisbury|15.44|-61.45|N
DM|Saint Paul|Massacre|15.34|-61.41|N
DO|Azua|Azua|18.45|-70.73|S
DO|Baoruco|Neiba|18.49|-71.42|S
DO|Barahona|Barahona|18.21|-71.10|S
DO|Dajabón|Dajabón|19.55|-71.71|S
DO|Distrito Nacional|Santo Domingo|18.47|-69.90|SN
DO|Duarte|San Francisco de Macorís|19.30|-70.25|SN
DO|El Seibo|El Seibo|18.77|-69.04|S
DO|Elías Piña|Comendador|18.88|-71.71|S
DO|Espaillat|Moca|19.39|-70.53|S
DO|Hato Mayor|Hato Mayor del Rey|18.76|-69.26|S
DO|Hermanas Mirabal|Salcedo|19.38|-70.42|S
DO|Independencia|Jimaní|18.49|-71.85|S
DO|La Altagracia|Higüey|18.62|-68.71|SN
DO|La Romana|La Romana|18.43|-68.97|SN
DO|La Vega|La Vega|19.22|-70.53|SN
DO|María Trinidad Sánchez|Nagua|19.38|-69.85|S
DO|Monseñor Nouel|Bonao|18.94|-70.41|S
DO|Monte Cristi|Monte Cristi|19.85|-71.65|S
DO|Monte Plata|Monte Plata|18.81|-69.78|S
DO|Pedernales|Pedernales|18.04|-71.74|S
DO|Peravia|Baní|18.28|-70.33|S
DO|Puerto Plata|Puerto Plata|19.79|-70.69|SN
DO|Samaná|Samaná|19.21|-69.34|S
DO|Sánchez Ramírez|Cotuí|19.06|-70.15|S
DO|San Cristóbal|San Cristóbal|18.42|-70.11|SN
DO|San José de Ocoa|San José de Ocoa|18.55|-70.50|S
DO|San Juan|San Juan de la Maguana|18.81|-71.23|S
DO|San Pedro de Macorís|San Pedro de Macorís|18.46|-69.31|SN
DO|Santiago|Santiago de los Caballeros|19.45|-70.70|SN
DO|Santiago Rodríguez|Sabaneta|19.47|-71.34|S
DO|Santo Domingo|Santo Domingo Este|18.49|-69.85|S
DO|Valverde|Mao|19.55|-71.08|S
DO|Santo Domingo|Los Alcarrizos|18.52|-70.02|N
```

CD — 26 provinces, including Kinshasa. Bas-Uele/Bas-Uélé, Kasai/Kasaï and North Kivu/Nord-Kivu are name variants. The ten `N` entries follow 2026 UN urban-area estimates, which differ from city-proper rankings.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://statisticstimes.com\&sz=32)

Statistics Times



CK — Ten outer-island government areas plus Rarotonga as a geographic coverage unit. Pukapuka and Nassau share an island-government arrangement. Village population data are from different census years; Arutanga, Omoka, Tauhunu and other island settlements use locality coordinates.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://geodatakit.com\&sz=32)

CSV, JSON & GeoJSON · GeoDataKit+1



CR — Seven provinces. San Jose/San José, Limon/Limón and Paraiso/Paraíso are spelling variants. The `N` entries use individual localities, including settlements within Greater San José, rather than consolidated metropolitan populations.

CI — 31 regions plus two autonomous districts, Abidjan and Yamoussoukro. Bélier has its administrative centre at Toumodi, while Yamoussoukro belongs to a separate autonomous district. Anyama is treated as part of Greater Abidjan for the population ranking.

HR — 20 counties plus the separately administered City of Zagreb. Zagreb is also the administrative seat of Zagreb County but lies outside it, so Velika Gorica is used as the largest city within the county. Top-ten `N` flags use 2021 administrative-city populations; settlement-only rankings would include Sesvete instead.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://mojahrvatska.com.hr\&sz=32)

MojaHrvatska+1



CU — 15 provinces plus the special municipality Isla de la Juventud. Havana/La Habana, Camagüey/Camaguey and Guantánamo/Guantanamo are spelling variants. Artemisa and Mayabeque were created during the 2011 administrative reorganisation.

CW — Curaçao has no conventional provincial subdivisions; the whole island is used as the state-level coverage unit. Willemstad is the principal officially designated city. Statistical neighbourhoods are not added as independent cities.

CY — Six districts are listed according to the Republic of Cyprus's de jure administrative structure. Famagusta and Kyrenia are under de facto Northern Cyprus administration. Nicosia is divided by the UN buffer zone; north/south census figures have different reference years.

CZ — 14 regions (kraje). The formal administrative seat of Central Bohemian Region is Prague, outside the region's territory, so Kladno is used as its largest internal city. The ten largest municipalities follow January 2026 figures.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.czech-profile.cz\&sz=32)

Czech-profile.cz



DK — Five regions as of November 2026. Copenhagen represents the Capital Region as its largest city, although the regional administrative seat is Hillerød. Capital Region and Zealand are scheduled to merge into Region of Eastern Denmark on January 1, 2027. Greenland and the Faroe Islands have separate ISO codes.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.retsinformation.dk\&sz=32)

Retsinformation



DJ — Five regions plus separately administered Djibouti City. The ten `N` entries follow the 2024 population census, but Cheik Farah's coordinates are approximate because the locality is associated with the Damerjog area.

DM — Ten parishes. Most parishes lack formally designated administrative capitals, so representative population centres are used. Grand Bay is also called Berekua; the top-ten settlements use 2011 census populations.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.worldometers.info\&sz=32)

Worldometer



DO — 31 provinces plus Distrito Nacional. Hermanas Mirabal was formerly Salcedo Province; Higüey is formally Salvaleón de Higüey. The ten `N` entries follow 2022 urban-locality populations, with Greater Santo Domingo aggregated for ranking purposes, while Santo Domingo Este is separately retained as the seat of Santo Domingo Province.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.worldometers.info\&sz=32)

Worldometer



Points still open:

- CD: Reconcile UN urban-area rankings with city-proper populations, particularly Beni, Kalemie, Kolwezi, Likasi and Kikwit. Confirm Overture province assignment in areas affected by territorial conflict.
- CK: Verify small-island settlement coordinates and population rankings against the same census year. Check whether Rarotonga and Nassau need synthetic state-level units in the extraction hierarchy.
- CR: Confirm whether the audit should use individual localities or consolidated urban areas around San José.
- CI: Check that Overture uses all 31 current regions and the two autonomous districts, especially the Bélier/Yamoussoukro boundary.
- HR: Keep administrative-city and individual-settlement population definitions separate when comparing top-ten rankings.
- CW: Confirm whether neighbourhood-level coverage is needed beyond the single Willemstad city entry.
- CY: Reconcile the northern and southern population datasets and check the practical division of Nicosia.
- DK: Prepare for the January 2027 regional merger; the current five-region structure will become outdated.
- DJ: Validate the precise location of Cheik Farah and its separation from Damerjog.
- DO: Decide whether Santo Domingo Este, Norte and Oeste should also receive individual `N` rankings rather than being aggregated under Greater Santo Domingo.


---

## Claude Code - 2026-11-08 19:14 UTC - 06_claude.md - attachments: none

## Check of your message-5 list (businesses within 10 km or with that city name)
Round 5: 223 reference lines, 223 cities, 219 with business data (98 %).
Not covered: - CK: 16/20 cities covered, 3,082 businesses near them; no data at: Kimiangatau, Palmerston, Roto, Rakahanga

Same format again:


## Message 6 of 19 - countries
Ecuador (EC), Egypt (EG), El Salvador (SV), Equatorial Guinea (GQ), Eritrea (ER), Estonia (EE), Eswatini (SZ), Ethiopia (ET), Falkland Islands (FK), Faroe Islands (FO), Fiji (FJ), Finland (FI), France (FR)

For EACH country above give:
1. every first-level administrative division (state / province / region / governorate ... as it is today),
   with its capital or largest city (kind S);
2. the 10 largest cities of the country by population (kind N) - fewer if the country has fewer.
   A city can appear as both S and N; list it once with kind SN.
Uninhabited territories: one line `CC|-|-|||none`.

Output ONLY one code block, one line per city, pipe-separated, no header, no commentary inside it:
`CC|state|city|lat|lon|kind`
- CC = ISO code above; state and city in English (the name a map would show); lat / lon with 2 decimals.
After the code block: one line per country with any naming caveat (renamed divisions, disputed areas),
then the list of points still open.


---

## ChatGPT (Extra High) - 2026-11-08 19:21 UTC - saved as 06_chatgpt.md

```
EC|Azuay|Cuenca|-2.90|-79.00|SN
EC|Bolívar|Guaranda|-1.59|-79.00|S
EC|Cañar|Azogues|-2.74|-78.85|S
EC|Carchi|Tulcán|0.81|-77.72|S
EC|Chimborazo|Riobamba|-1.67|-78.65|S
EC|Cotopaxi|Latacunga|-0.93|-78.62|S
EC|El Oro|Machala|-3.26|-79.96|SN
EC|Esmeraldas|Esmeraldas|0.97|-79.65|S
EC|Galápagos|Puerto Baquerizo Moreno|-0.90|-89.61|S
EC|Guayas|Guayaquil|-2.19|-79.89|SN
EC|Imbabura|Ibarra|0.35|-78.12|S
EC|Loja|Loja|-3.99|-79.20|SN
EC|Los Ríos|Babahoyo|-1.80|-79.53|S
EC|Manabí|Portoviejo|-1.06|-80.46|SN
EC|Morona Santiago|Macas|-2.31|-78.12|S
EC|Napo|Tena|-0.99|-77.81|S
EC|Orellana|Puerto Francisco de Orellana|-0.46|-76.99|S
EC|Pastaza|Puyo|-1.48|-77.99|S
EC|Pichincha|Quito|-0.18|-78.47|SN
EC|Santa Elena|Santa Elena|-2.23|-80.86|S
EC|Santo Domingo de los Tsáchilas|Santo Domingo|-0.25|-79.17|SN
EC|Sucumbíos|Nueva Loja|0.09|-76.89|S
EC|Tungurahua|Ambato|-1.25|-78.62|S
EC|Zamora Chinchipe|Zamora|-4.07|-78.95|S
EC|Guayas|Durán|-2.17|-79.83|N
EC|Manabí|Manta|-0.95|-80.73|N
EC|Los Ríos|Quevedo|-1.03|-79.46|N
EG|Alexandria|Alexandria|31.20|29.92|SN
EG|Aswan|Aswan|24.09|32.90|S
EG|Asyut|Asyut|27.18|31.18|SN
EG|Beheira|Damanhur|31.04|30.47|S
EG|Beni Suef|Beni Suef|29.07|31.10|S
EG|Cairo|Cairo|30.04|31.24|SN
EG|Dakahlia|Mansoura|31.04|31.38|SN
EG|Damietta|Damietta|31.42|31.81|S
EG|Faiyum|Faiyum|29.31|30.84|S
EG|Gharbia|Tanta|30.79|31.00|N
EG|Giza|Giza|30.01|31.21|SN
EG|Ismailia|Ismailia|30.60|32.27|S
EG|Kafr El Sheikh|Kafr El Sheikh|31.11|30.94|S
EG|Luxor|Luxor|25.69|32.64|S
EG|Matrouh|Mersa Matruh|31.35|27.24|S
EG|Minya|Minya|28.09|30.75|S
EG|Monufia|Shibin El Kom|30.55|31.01|S
EG|New Valley|Kharga|25.44|30.55|S
EG|North Sinai|Arish|31.13|33.80|S
EG|Port Said|Port Said|31.27|32.30|SN
EG|Qalyubia|Banha|30.47|31.18|S
EG|Qena|Qena|26.16|32.72|S
EG|Red Sea|Hurghada|27.26|33.81|S
EG|Sharqia|Zagazig|30.59|31.50|S
EG|Sohag|Sohag|26.56|31.69|S
EG|South Sinai|El Tor|28.24|33.62|S
EG|Suez|Suez|29.97|32.55|SN
EG|Qalyubia|Shubra El Kheima|30.13|31.24|N
EG|Gharbia|El Mahalla El Kubra|30.97|31.17|N
SV|Ahuachapán|Ahuachapán|13.92|-89.85|SN
SV|Cabañas|Sensuntepeque|13.87|-88.63|S
SV|Chalatenango|Chalatenango|14.04|-88.94|S
SV|Cuscatlán|Cojutepeque|13.72|-88.93|S
SV|La Libertad|Santa Tecla|13.68|-89.29|SN
SV|La Paz|Zacatecoluca|13.50|-88.87|S
SV|La Unión|La Unión|13.34|-87.84|S
SV|Morazán|San Francisco Gotera|13.70|-88.10|S
SV|San Miguel|San Miguel|13.48|-88.18|SN
SV|San Salvador|San Salvador|13.69|-89.19|SN
SV|San Vicente|San Vicente|13.64|-88.78|S
SV|Santa Ana|Santa Ana|13.99|-89.56|SN
SV|Sonsonate|Sonsonate|13.72|-89.72|S
SV|Usulután|Usulután|13.35|-88.45|S
SV|San Salvador|Soyapango|13.71|-89.15|N
SV|San Salvador|Mejicanos|13.72|-89.19|N
SV|La Libertad|Lourdes Colón|13.72|-89.37|N
SV|San Salvador|Apopa|13.81|-89.18|N
SV|San Salvador|Ciudad Delgado|13.72|-89.17|N
GQ|Annobón|San Antonio de Palé|-1.41|5.63|S
GQ|Bioko Norte|Malabo|3.75|8.78|SN
GQ|Bioko Sur|Luba|3.46|8.55|SN
GQ|Centro Sur|Evinayong|1.44|10.55|SN
GQ|Djibloho|Ciudad de la Paz|1.59|10.82|S
GQ|Kié-Ntem|Ebebiyin|2.15|11.33|SN
GQ|Litoral|Bata|1.86|9.77|SN
GQ|Wele-Nzas|Mongomo|1.63|11.31|SN
GQ|Wele-Nzas|Aconibe|1.30|10.94|N
GQ|Wele-Nzas|Añisok|1.87|10.77|N
GQ|Annobón|Aual|-1.45|5.63|N
GQ|Kié-Ntem|Mikomeseng|2.14|10.61|N
ER|Anseba|Keren|15.78|38.45|SN
ER|Debub|Mendefera|14.89|38.82|S
ER|Gash-Barka|Barentu|15.11|37.59|SN
ER|Maekel|Asmara|15.34|38.93|SN
ER|Northern Red Sea|Massawa|15.61|39.45|SN
ER|Southern Red Sea|Assab|13.01|42.74|SN
ER|Northern Red Sea|Ghinda|15.45|39.09|N
ER|Gash-Barka|Teseney|15.11|36.66|N
ER|Northern Red Sea|Nefasit|15.33|39.05|N
ER|Debub|Dekemhare|15.07|39.05|N
ER|Gash-Barka|Agordat|15.55|37.89|N
EE|Harju|Tallinn|59.44|24.75|SN
EE|Hiiu|Kärdla|58.99|22.75|S
EE|Ida-Viru|Jõhvi|59.36|27.42|S
EE|Jõgeva|Jõgeva|58.75|26.40|S
EE|Järva|Paide|58.89|25.56|S
EE|Lääne|Haapsalu|58.94|23.54|S
EE|Lääne-Viru|Rakvere|59.35|26.36|SN
EE|Põlva|Põlva|58.06|27.07|S
EE|Pärnu|Pärnu|58.39|24.50|SN
EE|Rapla|Rapla|59.01|24.79|S
EE|Saare|Kuressaare|58.25|22.49|SN
EE|Tartu|Tartu|58.38|26.72|SN
EE|Valga|Valga|57.78|26.05|S
EE|Viljandi|Viljandi|58.36|25.59|SN
EE|Võru|Võru|57.85|27.00|S
EE|Ida-Viru|Narva|59.38|28.19|N
EE|Ida-Viru|Kohtla-Järve|59.40|27.27|N
EE|Harju|Maardu|59.48|25.02|N
EE|Ida-Viru|Sillamäe|59.40|27.75|N
SZ|Hhohho|Mbabane|-26.32|31.13|SN
SZ|Lubombo|Siteki|-26.45|31.95|SN
SZ|Manzini|Manzini|-26.50|31.38|SN
SZ|Shiselweni|Nhlangano|-27.11|31.20|SN
SZ|Manzini|Matsapha|-26.52|31.31|N
SZ|Lubombo|Big Bend|-26.82|31.94|N
SZ|Manzini|Malkerns|-26.57|31.18|N
SZ|Hhohho|Piggs Peak|-25.97|31.25|N
SZ|Lubombo|Mhlume|-26.03|31.85|N
SZ|Lubombo|Simunye|-26.21|31.92|N
ET|Addis Ababa|Addis Ababa|9.03|38.75|SN
ET|Afar|Semera|11.79|41.01|S
ET|Amhara|Bahir Dar|11.59|37.39|SN
ET|Benishangul-Gumuz|Asosa|10.07|34.53|S
ET|Central Ethiopia|Hosaena|7.55|37.85|S
ET|Dire Dawa|Dire Dawa|9.59|41.87|SN
ET|Gambela|Gambela|8.25|34.59|S
ET|Harari|Harar|9.31|42.12|S
ET|Oromia|Adama|8.54|39.27|SN
ET|Sidama|Hawassa|7.06|38.48|SN
ET|Somali|Jijiga|9.35|42.80|S
ET|South Ethiopia|Wolaita Sodo|6.86|37.76|S
ET|Southwest Ethiopia Peoples|Bonga|7.27|36.25|S
ET|Tigray|Mekelle|13.50|39.47|SN
ET|Amhara|Gondar|12.60|37.47|N
ET|Amhara|Dessie|11.13|39.63|N
ET|Oromia|Jimma|7.67|36.83|N
ET|Oromia|Shashamane|7.20|38.60|N
FK|Falkland Islands|Stanley|-51.69|-57.86|SN
FK|Falkland Islands|Mount Pleasant|-51.82|-58.45|N
FK|Falkland Islands|Goose Green|-51.83|-58.98|N
FK|Falkland Islands|North Arm|-52.13|-59.37|N
FK|Falkland Islands|Port Howard|-51.62|-59.52|N
FK|Falkland Islands|Fox Bay|-51.95|-60.06|N
FK|Falkland Islands|Hill Cove|-51.50|-59.96|N
FK|Falkland Islands|Darwin|-51.82|-58.98|N
FO|Eiði|Eiði|62.30|-7.10|S
FO|Eystur|Leirvík|62.21|-6.71|S
FO|Fámjin|Fámjin|61.53|-6.88|S
FO|Fuglafjørður|Fuglafjørður|62.24|-6.81|SN
FO|Fugloy|Kirkja|62.32|-6.31|S
FO|Hov|Hov|61.51|-6.76|S
FO|Húsavík|Húsavík|61.81|-6.68|S
FO|Hvalba|Hvalba|61.60|-6.95|S
FO|Hvannasund|Hvannasund|62.30|-6.52|S
FO|Klaksvík|Klaksvík|62.23|-6.59|SN
FO|Kunoy|Kunoy|62.30|-6.67|S
FO|Kvívík|Kvívík|62.12|-7.07|S
FO|Nes|Toftir|62.09|-6.73|S
FO|Porkeri|Porkeri|61.48|-6.75|S
FO|Runavík|Runavík|62.11|-6.72|S
FO|Skálavík|Skálavík|61.83|-6.66|S
FO|Sandur|Sandur|61.84|-6.81|S
FO|Sjóvar|Strendur|62.10|-6.76|S
FO|Skopun|Skopun|61.91|-6.87|S
FO|Skúvoy|Skúvoy|61.77|-6.81|S
FO|Sumba|Sumba|61.41|-6.70|S
FO|Sunda|Oyrarbakki|62.20|-6.99|S
FO|Sørvágur|Sørvágur|62.07|-7.31|SN
FO|Tórshavn|Tórshavn|62.01|-6.77|SN
FO|Tvøroyri|Tvøroyri|61.55|-6.81|S
FO|Vágar|Miðvágur|62.05|-7.19|SN
FO|Vágur|Vágur|61.47|-6.81|SN
FO|Vestmanna|Vestmanna|62.16|-7.17|SN
FO|Viðareiði|Viðareiði|62.36|-6.54|S
FO|Tórshavn|Hoyvík|62.03|-6.75|N
FO|Tórshavn|Argir|61.99|-6.75|N
FO|Runavík|Saltangará|62.12|-6.73|N
FJ|Central Division|Suva|-18.14|178.44|SN
FJ|Eastern Division|Levuka|-17.68|178.83|S
FJ|Northern Division|Labasa|-16.43|179.37|SN
FJ|Rotuma|Ahau|-12.50|177.05|S
FJ|Western Division|Lautoka|-17.61|177.45|SN
FJ|Central Division|Nasinu|-18.07|178.51|N
FJ|Western Division|Nadi|-17.80|177.42|N
FJ|Central Division|Nausori|-18.02|178.54|N
FJ|Central Division|Lami|-18.11|178.41|N
FJ|Western Division|Ba|-17.53|177.67|N
FJ|Western Division|Sigatoka|-18.14|177.51|N
FJ|Western Division|Tavua|-17.44|177.86|N
FI|Central Finland|Jyväskylä|62.24|25.75|SN
FI|Central Ostrobothnia|Kokkola|63.84|23.13|S
FI|Kainuu|Kajaani|64.23|27.73|S
FI|Kanta-Häme|Hämeenlinna|60.99|24.46|S
FI|Kymenlaakso|Kouvola|60.87|26.70|S
FI|Lapland|Rovaniemi|66.50|25.73|S
FI|North Karelia|Joensuu|62.60|29.76|S
FI|North Ostrobothnia|Oulu|65.01|25.47|SN
FI|North Savo|Kuopio|62.89|27.68|SN
FI|Ostrobothnia|Vaasa|63.10|21.62|S
FI|Päijät-Häme|Lahti|60.98|25.66|SN
FI|Pirkanmaa|Tampere|61.50|23.76|SN
FI|Satakunta|Pori|61.49|21.80|SN
FI|South Karelia|Lappeenranta|61.06|28.19|S
FI|South Ostrobothnia|Seinäjoki|62.79|22.84|S
FI|South Savo|Mikkeli|61.69|27.27|S
FI|Southwest Finland|Turku|60.45|22.27|SN
FI|Uusimaa|Helsinki|60.17|24.94|SN
FI|Åland|Mariehamn|60.10|19.93|S
FI|Uusimaa|Espoo|60.21|24.66|N
FI|Uusimaa|Vantaa|60.29|25.04|N
FR|Auvergne-Rhône-Alpes|Lyon|45.76|4.84|SN
FR|Bourgogne-Franche-Comté|Dijon|47.32|5.04|S
FR|Brittany|Rennes|48.11|-1.68|S
FR|Centre-Val de Loire|Orléans|47.90|1.91|S
FR|Corsica|Ajaccio|41.92|8.74|S
FR|Grand Est|Strasbourg|48.58|7.75|SN
FR|Hauts-de-France|Lille|50.63|3.06|SN
FR|Île-de-France|Paris|48.86|2.35|SN
FR|Normandy|Rouen|49.44|1.10|S
FR|Nouvelle-Aquitaine|Bordeaux|44.84|-0.58|SN
FR|Occitanie|Toulouse|43.60|1.44|SN
FR|Pays de la Loire|Nantes|47.22|-1.55|SN
FR|Provence-Alpes-Côte d'Azur|Marseille|43.30|5.37|SN
FR|Guadeloupe|Basse-Terre|15.99|-61.73|S
FR|French Guiana|Cayenne|4.94|-52.33|S
FR|Martinique|Fort-de-France|14.60|-61.08|S
FR|Mayotte|Mamoudzou|-12.78|45.23|S
FR|Réunion|Saint-Denis|-20.88|55.45|S
FR|Provence-Alpes-Côte d'Azur|Nice|43.70|7.27|N
FR|Occitanie|Montpellier|43.61|3.88|N
```

EC — 24 provinces. Puerto Francisco de Orellana is also called Coca, and Nueva Loja is also called Lago Agrio. The ten `N` cities follow the 2025 INEC urbanised-canton ranking; Quito's satellite localities are not counted separately.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.ecuadorencifras.gob.ec\&sz=32)

Buenas cifras, mejores vidas



EG — 27 governorates. Beheira/Behera, Faiyum/Fayoum, Monufia/Menoufia, and Matrouh/Matruh are common spelling variants. The ten `N` entries use city populations, not Greater Cairo or other urban agglomerations.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://openadmindata.org\&sz=32)

Open Admin Data+1



SV — 14 departments; the 2024 restructuring created 44 municipalities containing 262 districts, without eliminating the departments. Lourdes Colón represents the populated centre of Colón district. The ten `N` flags use 2024 district populations, which are not always identical to built-up-city populations.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://oig.cepal.org\&sz=32)

Gender Equality Observatory+1



GQ — Eight provinces. Ciudad de la Paz, formerly Oyala, was designated the national capital on January 2, 2026, with government relocation planned over the following year. Malabo remains the capital of Bioko Norte. Aconibe/Akonibe and Añisok/Añisoc are spelling variants.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.guineaecuatorialpress.com\&sz=32)

Guinea Ecuatorial+1



ER — Six regions (zobas). Maekel means Central, Debub means Southern, and the two Red Sea regions have longer Tigrinya names. Dekemhare/Decemhare and Teseney/Tessenei are variants. The ten `N` flags use 2026 UN urban-area estimates rather than a recent national census.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://assets.publishing.service.gov.uk\&sz=32)

GOV.UK Assets+1



EE — 15 counties. Harju/Harjumaa, Ida-Viru/Ida-Virumaa and similar endings are alternative county naming forms. Top-ten cities use 2025 settlement populations, distinct from the populations of their surrounding municipalities.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.elvl.ee\&sz=32)

Eesti Linnade ja Valdade Liit+1



SZ — Four regions. The country is Eswatini, formerly Swaziland; ISO alpha-2 remains `SZ`. Siteki is also called Stegi, and Piggs Peak is usually written Pigg's Peak. Top-ten cities use 2017 census urban-centre counts.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://wm-site-staging.cloudflare-47b.workers.dev\&sz=32)

Worldometer



ET — Twelve regions and two chartered cities. Central Ethiopia and South Ethiopia were created in 2023; the former SNNPR should not remain a current first-level region. Oromia's formal administrative capital is Addis Ababa, which is separately administered, so Adama is used as the largest city within Oromia. The ten `N` flags use Ethiopian Statistics Service 2022 projections.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.gov.uk\&sz=32)

GOV.UK+1



FK — No conventional first-level provincial divisions; Falkland Islands is used as a territory-wide coverage unit. Seven civilian settlements are identifiable in the 2021 locality ranking, plus the separately counted Mount Pleasant Complex. The territory is also claimed by Argentina as Islas Malvinas.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://en.wikipedia.org\&sz=32)

Wikipedia+1



FO — 29 municipalities. The administrative system uses kommunur, and all municipality names are preserved in their customary Faroese form. Hoyvík and Argir are distinct statistical settlements within greater Tórshavn. Top-ten localities follow 2026 population figures.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.euraxess.fo\&sz=32)

EURAXESS+2



FJ — Four administrative divisions plus Rotuma, which is a dependency with special administration. The 14 provinces are below the division level. Ahau is Rotuma's administrative centre. Top-ten urban settlements use 2017 census-based figures.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.geonames.org\&sz=32)

GeoNames+1



FI — 19 regions (maakunnat), including autonomous Åland. Åland is also separately represented under ISO `AX`, so this row overlaps geographically with Message 1. The ten `N` cities follow official December 2025 municipal populations.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://stat.fi\&sz=32)

Statistics Finland+1



FR — 18 regions: 13 metropolitan and five overseas. Brittany/Bretagne, Normandy/Normandie and Corsica/Corse are English/French variants. The five overseas regions also have separate ISO codes (`GP`, `GF`, `MQ`, `YT`, `RE`); avoid double-counting these in geographic extraction. Top-ten cities use official municipal populations effective January 2026.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.insee.fr\&sz=32)

Insee+2



Points still open:

- EC: Confirm whether canton-based population rankings or individual urban settlements should govern the final top ten; Calderón may enter the latter ranking.
- EG: Validate the Cairo–Giza–Shubra El Kheima boundary separation to prevent double-counting businesses across adjacent governorates.
- SV: Match the 2024 department/municipality/district hierarchy and distinguish the Colón district population from the Lourdes urban locality.
- GQ: Verify Overture's handling of Djibloho's expanded 2026 boundaries, and whether Aual is a separately mapped populated locality or overlaps another Annobón settlement.
- ER: Reconcile the 2026 UN urban estimates with older census-based city populations, particularly Asmara, Massawa and Keren.
- ET: Check that Overture reflects the current 12-region structure, especially Central Ethiopia and South Ethiopia, and handles Addis Ababa separately from Oromia.
- FK: Confirm whether Mount Pleasant Complex should be retained as a populated-place target. The 2021 census does not establish ten independent civilian cities.
- FO: Validate municipality-point assignments for small villages, particularly Fámjin, Kirkja, Húsavík and Skúvoy. They may have few or no nearby commercial POIs.
- FJ: Confirm Rotuma's special administrative treatment and whether the extraction system uses the four divisions or the finer provincial hierarchy.
- FI/FR: Prevent duplicate geographic extraction across separate ISO entries, especially `FI`/`AX` and `FR`/`GP`/`GF`/`MQ`/`YT`/`RE`.


---

## Claude Code - 2026-11-08 19:21 UTC - 07_claude.md - attachments: none

## Check of your message-6 list (businesses within 10 km or with that city name)
Round 6: 238 reference lines, 238 cities, 235 with business data (99 %).
Not covered: - FI: 20/21 cities covered, 170,732 businesses near them; no data at: Mariehamn
Not covered: - FK: 6/8 cities covered, 163 businesses near them; no data at: North Arm, Port Howard

Same format again:


## Message 7 of 19 - countries
French Guiana (GF), French Polynesia (PF), French Southern Territories (TF), Gabon (GA), Gambia (GM), Georgia (GE), Germany (DE), Ghana (GH), Gibraltar (GI), Greece (GR), Greenland (GL), Grenada (GD), Guadeloupe (GP)

For EACH country above give:
1. every first-level administrative division (state / province / region / governorate ... as it is today),
   with its capital or largest city (kind S);
2. the 10 largest cities of the country by population (kind N) - fewer if the country has fewer.
   A city can appear as both S and N; list it once with kind SN.
Uninhabited territories: one line `CC|-|-|||none`.

Output ONLY one code block, one line per city, pipe-separated, no header, no commentary inside it:
`CC|state|city|lat|lon|kind`
- CC = ISO code above; state and city in English (the name a map would show); lat / lon with 2 decimals.
After the code block: one line per country with any naming caveat (renamed divisions, disputed areas),
then the list of points still open.


---

## ChatGPT (Extra High) - 2026-11-08 19:28 UTC - saved as 07_chatgpt.md

```
GF|Cayenne|Cayenne|4.92|-52.33|SN
GF|Saint-Georges|Saint-Georges|3.89|-51.80|S
GF|Saint-Laurent-du-Maroni|Saint-Laurent-du-Maroni|5.50|-54.03|SN
GF|Cayenne|Matoury|4.85|-52.33|N
GF|Cayenne|Rémire-Montjoly|4.92|-52.27|N
GF|Cayenne|Kourou|5.16|-52.65|N
GF|Cayenne|Macouria|5.02|-52.48|N
GF|Saint-Laurent-du-Maroni|Mana|5.67|-53.78|N
GF|Saint-Laurent-du-Maroni|Apatou|5.15|-54.34|N
GF|Saint-Laurent-du-Maroni|Grand-Santi|4.27|-54.38|N
GF|Saint-Laurent-du-Maroni|Maripasoula|3.64|-54.03|N
PF|Windward Islands|Papeete|-17.54|-149.57|SN
PF|Leeward Islands|Uturoa|-16.73|-151.44|S
PF|Marquesas Islands|Taiohae|-8.91|-140.10|S
PF|Austral Islands|Mataura|-23.35|-149.48|S
PF|Tuamotu-Gambier Islands|Avatoru|-14.94|-147.70|S
PF|Windward Islands|Faaa|-17.55|-149.60|N
PF|Windward Islands|Punaauia|-17.63|-149.60|N
PF|Windward Islands|Paopao|-17.51|-149.82|N
PF|Windward Islands|Mahina|-17.51|-149.48|N
PF|Windward Islands|Pirae|-17.54|-149.56|N
PF|Windward Islands|Afaahiti|-17.75|-149.29|N
PF|Windward Islands|Paea|-17.69|-149.59|N
PF|Windward Islands|Papara|-17.77|-149.50|N
PF|Windward Islands|Mataiea|-17.74|-149.43|N
TF|-|-|||none
GA|Estuaire|Libreville|0.39|9.45|SN
GA|Haut-Ogooué|Franceville|-1.64|13.58|SN
GA|Moyen-Ogooué|Lambaréné|-0.70|10.24|SN
GA|Ngounié|Mouila|-1.87|11.06|SN
GA|Nyanga|Tchibanga|-2.85|11.03|S
GA|Ogooué-Ivindo|Makokou|0.57|12.86|S
GA|Ogooué-Lolo|Koulamoutou|-1.13|12.48|S
GA|Ogooué-Maritime|Port-Gentil|-0.72|8.78|SN
GA|Woleu-Ntem|Oyem|1.60|11.58|SN
GA|Estuaire|Owendo|0.29|9.50|N
GA|Haut-Ogooué|Moanda|-1.57|13.20|N
GA|Estuaire|Ntoum|0.38|9.77|N
GA|Estuaire|Akanda|0.49|9.41|N
GM|Banjul|Banjul|13.45|-16.58|SN
GM|Kanifing|Serekunda|13.44|-16.68|SN
GM|Brikama|Brikama|13.27|-16.65|SN
GM|Kerewan|Kerewan|13.49|-16.10|S
GM|Mansakonko|Mansakonko|13.43|-15.54|S
GM|Kuntaur|Kuntaur|13.67|-14.89|S
GM|Janjanbureh|Janjanbureh|13.54|-14.76|S
GM|Basse|Basse Santa Su|13.31|-14.21|SN
GM|Kerewan|Farafenni|13.57|-15.60|N
GM|Brikama|Sukuta|13.40|-16.71|N
GM|Kanifing|Bakau|13.48|-16.68|N
GM|Brikama|Lamin|13.39|-16.65|N
GM|Kanifing|Bundung|13.43|-16.69|N
GM|Kanifing|Talinding|13.43|-16.66|N
GE|Abkhazia|Sukhumi|43.00|41.02|SN
GE|Adjara|Batumi|41.64|41.63|SN
GE|Guria|Ozurgeti|41.92|42.00|S
GE|Imereti|Kutaisi|42.27|42.70|SN
GE|Kakheti|Telavi|41.92|45.47|S
GE|Kvemo Kartli|Rustavi|41.55|44.98|SN
GE|Mtskheta-Mtianeti|Mtskheta|41.84|44.72|S
GE|Racha-Lechkhumi and Kvemo Svaneti|Ambrolauri|42.52|43.15|S
GE|Samegrelo-Zemo Svaneti|Zugdidi|42.51|41.87|SN
GE|Samtskhe-Javakheti|Akhaltsikhe|41.64|42.98|S
GE|Shida Kartli|Gori|41.98|44.11|SN
GE|Tbilisi|Tbilisi|41.69|44.83|SN
GE|Samegrelo-Zemo Svaneti|Poti|42.14|41.67|N
GE|Shida Kartli|Tskhinvali|42.23|43.97|N
GE|Shida Kartli|Khashuri|41.99|43.60|N
DE|Baden-Württemberg|Stuttgart|48.78|9.18|SN
DE|Bavaria|Munich|48.14|11.58|SN
DE|Berlin|Berlin|52.52|13.41|SN
DE|Brandenburg|Potsdam|52.40|13.06|S
DE|Bremen|Bremen|53.08|8.81|SN
DE|Hamburg|Hamburg|53.55|10.00|SN
DE|Hesse|Wiesbaden|50.08|8.24|S
DE|Lower Saxony|Hanover|52.37|9.74|S
DE|Mecklenburg-Vorpommern|Schwerin|53.63|11.41|S
DE|North Rhine-Westphalia|Düsseldorf|51.23|6.78|SN
DE|Rhineland-Palatinate|Mainz|50.00|8.27|S
DE|Saarland|Saarbrücken|49.23|7.00|S
DE|Saxony|Dresden|51.05|13.74|S
DE|Saxony-Anhalt|Magdeburg|52.13|11.63|S
DE|Schleswig-Holstein|Kiel|54.32|10.12|S
DE|Thuringia|Erfurt|50.98|11.03|S
DE|North Rhine-Westphalia|Cologne|50.94|6.96|N
DE|Hesse|Frankfurt am Main|50.11|8.68|N
DE|Saxony|Leipzig|51.34|12.37|N
DE|North Rhine-Westphalia|Dortmund|51.51|7.47|N
GH|Ahafo|Goaso|6.80|-2.52|S
GH|Ashanti|Kumasi|6.69|-1.62|SN
GH|Bono|Sunyani|7.34|-2.33|SN
GH|Bono East|Techiman|7.59|-1.94|S
GH|Central|Cape Coast|5.11|-1.25|SN
GH|Eastern|Koforidua|6.09|-0.26|S
GH|Greater Accra|Accra|5.56|-0.20|SN
GH|North East|Nalerigu|10.53|-0.37|S
GH|Northern|Tamale|9.40|-0.84|SN
GH|Oti|Dambai|8.07|0.18|S
GH|Savannah|Damongo|9.08|-1.82|S
GH|Upper East|Bolgatanga|10.79|-0.85|S
GH|Upper West|Wa|10.06|-2.50|S
GH|Volta|Ho|6.61|0.47|S
GH|Western|Sekondi-Takoradi|4.92|-1.76|SN
GH|Western North|Sefwi Wiawso|6.21|-2.49|S
GH|Greater Accra|Ashaiman|5.69|-0.04|N
GH|Ashanti|Obuasi|6.20|-1.67|N
GH|Greater Accra|Teshie|5.59|-0.11|N
GH|Greater Accra|Tema|5.67|-0.02|N
GI|Gibraltar|Gibraltar|36.14|-5.35|SN
GR|Attica|Athens|37.98|23.73|SN
GR|Central Greece|Lamia|38.90|22.43|S
GR|Central Macedonia|Thessaloniki|40.64|22.94|SN
GR|Crete|Heraklion|35.34|25.13|SN
GR|Eastern Macedonia and Thrace|Komotini|41.12|25.41|S
GR|Epirus|Ioannina|39.66|20.85|S
GR|Ionian Islands|Corfu|39.62|19.92|S
GR|Mount Athos|Karyes|40.26|24.25|S
GR|North Aegean|Mytilene|39.11|26.55|S
GR|Peloponnese|Tripoli|37.51|22.37|S
GR|South Aegean|Ermoupoli|37.44|24.94|S
GR|Thessaly|Larissa|39.64|22.42|SN
GR|Western Greece|Patras|38.25|21.74|SN
GR|Western Macedonia|Kozani|40.30|21.79|S
GR|Attica|Piraeus|37.94|23.65|N
GR|Attica|Peristeri|38.02|23.69|N
GR|Attica|Acharnes|38.08|23.74|N
GR|Attica|Kallithea|37.96|23.70|N
GR|Central Macedonia|Kalamaria|40.58|22.95|N
GL|Avannaata|Ilulissat|69.22|-51.10|SN
GL|Kujalleq|Qaqortoq|60.72|-46.03|SN
GL|Qeqertalik|Aasiaat|68.71|-52.87|SN
GL|Qeqqata|Sisimiut|66.94|-53.67|SN
GL|Sermersooq|Nuuk|64.18|-51.72|SN
GL|Qeqqata|Maniitsoq|65.42|-52.90|N
GL|Sermersooq|Tasiilaq|65.61|-37.64|N
GL|Avannaata|Uummannaq|70.68|-52.13|N
GL|Kujalleq|Narsaq|60.91|-46.05|N
GL|Sermersooq|Paamiut|61.99|-49.67|N
GD|Saint Andrew|Grenville|12.12|-61.62|SN
GD|Saint David|Saint David's|12.05|-61.67|SN
GD|Saint George|Saint George's|12.05|-61.75|SN
GD|Saint John|Gouyave|12.16|-61.73|SN
GD|Saint Mark|Victoria|12.19|-61.71|SN
GD|Saint Patrick|Sauteurs|12.22|-61.64|SN
GD|Carriacou and Petite Martinique|Hillsborough|12.48|-61.46|SN
GD|Saint John|Grand Roy|12.13|-61.75|N
GD|Saint Patrick|Upper La Taste|12.19|-61.62|N
GD|Saint George|Grand Anse|12.02|-61.76|N
GP|Basse-Terre|Basse-Terre|15.99|-61.73|S
GP|Pointe-à-Pitre|Pointe-à-Pitre|16.24|-61.53|S
GP|Pointe-à-Pitre|Les Abymes|16.27|-61.50|N
GP|Basse-Terre|Baie-Mahault|16.27|-61.59|N
GP|Pointe-à-Pitre|Le Gosier|16.21|-61.49|N
GP|Basse-Terre|Petit-Bourg|16.19|-61.59|N
GP|Pointe-à-Pitre|Sainte-Anne|16.23|-61.39|N
GP|Pointe-à-Pitre|Le Moule|16.33|-61.35|N
GP|Basse-Terre|Lamentin|16.27|-61.63|N
GP|Basse-Terre|Sainte-Rose|16.33|-61.70|N
GP|Basse-Terre|Capesterre-Belle-Eau|16.05|-61.57|N
GP|Pointe-à-Pitre|Morne-à-l'Eau|16.33|-61.46|N
```

GF — Three arrondissements as of 2026: Cayenne, Saint-Laurent-du-Maroni and Saint-Georges. The ten largest localities use 2023 INSEE commune populations; large communes can contain multiple villages. French Guiana is also included in France's regional structure.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.insee.fr\&sz=32)

Insee+1



PF — Five administrative subdivisions. The official Tuamotu-Gambier administrative seat is in Papeete, outside the subdivision, so Avatoru is used as a geographic representative. Paopao, Afaahiti and Mataiea represent populous communes with multiple settlements; these are not necessarily the ten largest individual villages.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.legifrance.gouv.fr\&sz=32)

Légifrance+1



TF — No permanent civilian population. French Southern and Antarctic Lands includes research stations and administrative districts, but none is a conventional inhabited city.

GA — Nine provinces. Estuaire includes Libreville, Owendo, Ntoum and Akanda. The 2013 census is used for the ten most populous cities; Ntoum may appear as Ntoum Nkan, and Koulamoutou as Koula-Moutou.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://interieur.gouv.ga\&sz=32)

interieur.gouv.ga+1



GM — Eight local-government areas as used in the 2024 census: Banjul, Kanifing, Brikama, Kerewan, Mansakonko, Kuntaur, Janjanbureh and Basse. They are not identical to the conventional five-region-plus-two-municipality classification. Serekunda/Serrekunda and Janjanbureh/Georgetown are common variants. Population rankings are affected by subdivisions of Greater Serekunda.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://gambia.unfpa.org\&sz=32)

UNFPA-Gambia+1



GE — Nine regions, two autonomous republics and separately administered Tbilisi. Abkhazia and South Ossetia/Tskhinvali are internationally disputed and not controlled by the Georgian government. Georgian census coverage excludes these areas, so population rankings including Sukhumi and Tskhinvali use non-comparable estimates.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://search.coe.int\&sz=32)

search.coe.int+1



DE — Sixteen federal states (Länder). Bavaria/Bayern, Hesse/Hessen and Lower Saxony/Niedersachsen are English/German variants. The ten largest cities use 2025 municipal populations; Bremen ranks tenth, ahead of Essen, under this definition.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://de.wikipedia.org\&sz=32)

Wikipedia



GH — Sixteen regions following the 2018–2019 reorganisation. The former Brong-Ahafo Region is replaced by Bono, Bono East and Ahafo. Sekondi-Takoradi is a twin-city urban area, and Teshie, Tema and Ashaiman belong to the wider Accra metropolitan zone. City populations are difficult to compare across changing municipal boundaries.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://lgs.gov.gh\&sz=32)

LOCAL GOVERNMENT SERVICE+1



GI — Gibraltar has no conventional first-level provinces or regions. The whole territory and its main urban settlement are represented by a single line.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.gibraltar.gov.gi\&sz=32)

Government of Gibraltar



GR — Thirteen administrative regions plus the separately self-governing monastic territory of Mount Athos, represented by Karyes. The ten `N` entries use 2021 census settlement populations; several belong to the Athens or Thessaloniki metropolitan areas.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.gov.gr\&sz=32)

gov.gr+2



GL — Five municipalities since 2018. Northeast Greenland National Park and Pituffik Space Base are two additional unincorporated geographic areas, not conventional municipalities. The top ten towns use January 2026 population figures.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.thefactbook.org\&sz=32)

The Factbook+1



GD — Six parishes plus Carriacou and Petite Martinique. Saint David has no formally designated parish capital; Saint David's village is used as its main settlement. Grand Anse is included as a population-ranking candidate, but the tenth position is not census-verified.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://grenadaembassyusa.com\&sz=32)

Embassy of Grenada+1



GP — Two arrondissements, Basse-Terre and Pointe-à-Pitre, below Guadeloupe's territory-wide departmental and regional status. Ten `N` flags follow 2023 INSEE commune populations. Guadeloupe is also represented under France, so avoid duplicate extraction.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.insee.fr\&sz=32)

Insee+2



Points still open:

- GF/GP: Confirm that Overture's first-level hierarchy supports arrondissements. These are internal administrative divisions of French overseas territories, not separate ISO provinces.
- PF: Verify the representative towns for Moorea-Maiao, Taiarapu-Est and Teva I Uta against individual settlement populations. Avatoru is a geographic substitute, not the official Tuamotu-Gambier administrative seat.
- TF: Decide whether research stations require a separate non-commercial geographic coverage layer.
- GA: Reconcile the 2013 urban rankings with any newer official settlement population dataset. Verify Akanda and Ntoum boundaries within Greater Libreville.
- GM: Confirm whether SiteBlitz uses eight census LGAs or seven conventional administrative areas. Resolve the ten largest independent cities without counting Serekunda neighbourhoods twice.
- GE: Verify Overture's treatment of Abkhazia and South Ossetia, including the administrative assignment of Tskhinvali. Avoid mixing official Georgian census figures with estimates for disputed territories.
- GH: Establish one consistent city-population definition before final ranking, especially for Sekondi-Takoradi, Kasoa, Ashaiman, Tema and the Greater Accra localities.
- GR: Ensure Mount Athos is not incorrectly assigned to Central Macedonia. Decide whether metropolitan suburbs should remain independent cities.
- GL: Determine whether the two unincorporated areas require separate state-level coverage units. They are deliberately excluded from the five-municipality reference list.
- GD: Verify the tenth-largest settlement against official locality-level census data, particularly Grand Anse and the smaller northern villages.
- GF/PF/GP: Check the two-decimal coordinates against Overture's actual settlement centroids, especially extensive communes and multi-island municipalities.


---

## Claude Code - 2026-11-08 19:29 UTC - 08_claude.md - attachments: none

## Check of your message-7 list (businesses within 10 km or with that city name)
Round 7: 160 reference lines, 159 cities, 159 with business data (100 %).

Same format again:


## Message 8 of 19 - countries
Guam (GU), Guatemala (GT), Guernsey (GG), Guinea (GN), Guinea-Bissau (GW), Guyana (GY), Haiti (HT), Heard & McDonald Islands (HM), Honduras (HN), Hong Kong SAR China (HK), Hungary (HU), Iceland (IS), India (IN)

For EACH country above give:
1. every first-level administrative division (state / province / region / governorate ... as it is today),
   with its capital or largest city (kind S);
2. the 10 largest cities of the country by population (kind N) - fewer if the country has fewer.
   A city can appear as both S and N; list it once with kind SN.
Uninhabited territories: one line `CC|-|-|||none`.

Output ONLY one code block, one line per city, pipe-separated, no header, no commentary inside it:
`CC|state|city|lat|lon|kind`
- CC = ISO code above; state and city in English (the name a map would show); lat / lon with 2 decimals.
After the code block: one line per country with any naming caveat (renamed divisions, disputed areas),
then the list of points still open.


---

## ChatGPT (Extra High) - 2026-11-08 19:36 UTC - saved as 08_chatgpt.md

```
GU|Agana Heights|Agana Heights|13.47|144.75|S
GU|Agat|Agat|13.39|144.66|SN
GU|Asan-Maina|Asan|13.47|144.71|S
GU|Barrigada|Barrigada|13.47|144.80|SN
GU|Chalan Pago-Ordot|Chalan Pago|13.45|144.77|SN
GU|Dededo|Dededo|13.52|144.84|SN
GU|Hagåtña|Hagåtña|13.48|144.75|S
GU|Inarajan|Inarajan|13.27|144.75|S
GU|Mangilao|Mangilao|13.45|144.80|SN
GU|Merizo|Merizo|13.27|144.67|S
GU|Mongmong-Toto-Maite|Mongmong|13.48|144.79|SN
GU|Piti|Piti|13.46|144.69|S
GU|Santa Rita|Santa Rita|13.39|144.68|SN
GU|Sinajana|Sinajana|13.46|144.75|S
GU|Talofofo|Talofofo|13.36|144.75|S
GU|Tamuning|Tamuning|13.49|144.78|SN
GU|Umatac|Umatac|13.30|144.66|S
GU|Yigo|Yigo|13.53|144.88|SN
GU|Yona|Yona|13.41|144.77|SN
GT|Alta Verapaz|Cobán|15.47|-90.37|SN
GT|Baja Verapaz|Salamá|15.10|-90.32|S
GT|Chimaltenango|Chimaltenango|14.66|-90.82|S
GT|Chiquimula|Chiquimula|14.80|-89.54|S
GT|El Progreso|Guastatoya|14.85|-90.07|S
GT|Escuintla|Escuintla|14.30|-90.79|SN
GT|Guatemala|Guatemala City|14.63|-90.51|SN
GT|Huehuetenango|Huehuetenango|15.32|-91.47|S
GT|Izabal|Puerto Barrios|15.73|-88.60|S
GT|Jalapa|Jalapa|14.63|-89.99|SN
GT|Jutiapa|Jutiapa|14.29|-89.90|SN
GT|Petén|Flores|16.93|-89.89|S
GT|Quetzaltenango|Quetzaltenango|14.84|-91.52|SN
GT|Quiché|Santa Cruz del Quiché|15.03|-91.15|S
GT|Retalhuleu|Retalhuleu|14.54|-91.68|S
GT|Sacatepéquez|Antigua Guatemala|14.56|-90.73|S
GT|San Marcos|San Marcos|14.96|-91.79|S
GT|Santa Rosa|Cuilapa|14.28|-90.30|S
GT|Sololá|Sololá|14.77|-91.18|S
GT|Suchitepéquez|Mazatenango|14.53|-91.50|S
GT|Totonicapán|Totonicapán|14.91|-91.36|S
GT|Zacapa|Zacapa|14.97|-89.53|S
GT|Guatemala|Mixco|14.63|-90.61|N
GT|Guatemala|Villa Nueva|14.53|-90.59|N
GT|Guatemala|San Juan Sacatepéquez|14.72|-90.64|N
GT|Guatemala|San Miguel Petapa|14.50|-90.56|N
GG|Alderney|Saint Anne|49.72|-2.20|SN
GG|Castel|Castel|49.47|-2.59|SN
GG|Forest|Forest|49.42|-2.59|SN
GG|Herm|Herm|49.47|-2.45|S
GG|Saint Andrew|Saint Andrew|49.45|-2.57|SN
GG|Saint Martin|Saint Martin|49.43|-2.55|SN
GG|Saint Peter Port|Saint Peter Port|49.46|-2.54|SN
GG|Saint Pierre du Bois|Saint Pierre du Bois|49.44|-2.64|SN
GG|Saint Sampson|Saint Sampson|49.48|-2.52|SN
GG|Saint Saviour|Saint Saviour|49.45|-2.61|SN
GG|Sark|Sark|49.43|-2.36|S
GG|Torteval|Torteval|49.43|-2.65|S
GG|Vale|Vale|49.49|-2.53|SN
GN|Beyla|Beyla|8.69|-8.65|S
GN|Boké|Boké|10.94|-14.29|S
GN|Conakry|Conakry|9.54|-13.68|SN
GN|Faranah|Faranah|10.04|-10.74|S
GN|Kankan|Kankan|10.39|-9.31|SN
GN|Kindia|Kindia|10.06|-12.86|SN
GN|Labé|Labé|11.32|-12.28|SN
GN|Mamou|Mamou|10.38|-12.08|S
GN|Nzérékoré|Nzérékoré|7.76|-8.82|SN
GN|Siguiri|Siguiri|11.42|-9.17|SN
GN|Kindia|Dubréka|9.79|-13.52|N
GN|Faranah|Kissidougou|9.18|-10.10|N
GN|Kindia|Coyah|9.71|-13.39|N
GN|Boké|Kamsar|10.65|-14.62|N
GW|Bafatá|Bafatá|12.17|-14.65|SN
GW|Biombo|Quinhámel|11.88|-15.86|S
GW|Bolama|Bolama|11.58|-15.48|S
GW|Cacheu|Cacheu|12.27|-16.17|S
GW|Gabú|Gabú|12.28|-14.22|SN
GW|Oio|Farim|12.48|-15.22|SN
GW|Quinara|Buba|11.59|-14.99|SN
GW|Tombali|Catió|11.28|-15.25|S
GW|Bissau Autonomous Sector|Bissau|11.86|-15.59|SN
GW|Cacheu|Canchungo|12.07|-16.04|N
GW|Oio|Bissorã|12.22|-15.45|N
GW|Cacheu|Bula|12.09|-15.98|N
GW|Oio|Mansôa|12.07|-15.32|N
GW|Cacheu|Ingoré|12.28|-15.85|N
GY|Barima-Waini|Mabaruma|8.20|-59.77|SN
GY|Pomeroon-Supenaam|Anna Regina|7.26|-58.48|SN
GY|Essequibo Islands-West Demerara|Vreed-en-Hoop|6.80|-58.18|S
GY|Demerara-Mahaica|Georgetown|6.80|-58.16|SN
GY|Mahaica-Berbice|Fort Wellington|6.37|-57.59|S
GY|East Berbice-Corentyne|New Amsterdam|6.25|-57.52|SN
GY|Cuyuni-Mazaruni|Bartica|6.40|-58.62|SN
GY|Potaro-Siparuni|Mahdia|5.27|-59.15|SN
GY|Upper Takutu-Upper Essequibo|Lethem|3.38|-59.80|SN
GY|Upper Demerara-Berbice|Linden|5.99|-58.31|SN
GY|East Berbice-Corentyne|Rose Hall|6.27|-57.35|N
GY|East Berbice-Corentyne|Corriverton|5.89|-57.14|N
HT|Artibonite|Gonaïves|19.45|-72.69|SN
HT|Centre|Hinche|19.15|-72.02|S
HT|Grand'Anse|Jérémie|18.65|-74.12|S
HT|Nippes|Miragoâne|18.44|-73.09|S
HT|Nord|Cap-Haïtien|19.76|-72.20|SN
HT|Nord-Est|Fort-Liberté|19.67|-71.84|S
HT|Nord-Ouest|Port-de-Paix|19.94|-72.83|SN
HT|Ouest|Port-au-Prince|18.54|-72.34|SN
HT|Sud|Les Cayes|18.20|-73.75|S
HT|Sud-Est|Jacmel|18.23|-72.54|S
HT|Ouest|Carrefour|18.53|-72.40|N
HT|Ouest|Delmas|18.54|-72.30|N
HT|Ouest|Pétion-Ville|18.51|-72.28|N
HT|Artibonite|Saint-Marc|19.11|-72.69|N
HT|Ouest|Cité Soleil|18.58|-72.33|N
HT|Ouest|Croix-des-Bouquets|18.58|-72.22|N
HM|-|-|||none
HN|Atlántida|La Ceiba|15.78|-86.79|SN
HN|Choluteca|Choluteca|13.30|-87.19|SN
HN|Colón|Trujillo|15.92|-85.95|S
HN|Comayagua|Comayagua|14.46|-87.64|SN
HN|Copán|Santa Rosa de Copán|14.77|-88.78|S
HN|Cortés|San Pedro Sula|15.50|-88.03|SN
HN|El Paraíso|Yuscarán|13.94|-86.85|S
HN|Francisco Morazán|Tegucigalpa|14.07|-87.19|SN
HN|Gracias a Dios|Puerto Lempira|15.26|-83.77|S
HN|Intibucá|La Esperanza|14.31|-88.18|S
HN|Islas de la Bahía|Coxen Hole|16.32|-86.54|S
HN|La Paz|La Paz|14.32|-87.68|S
HN|Lempira|Gracias|14.59|-88.58|S
HN|Ocotepeque|Nueva Ocotepeque|14.44|-89.18|S
HN|Olancho|Juticalpa|14.67|-86.22|S
HN|Santa Bárbara|Santa Bárbara|14.92|-88.24|S
HN|Valle|Nacaome|13.53|-87.49|S
HN|Yoro|Yoro|15.14|-87.13|S
HN|Cortés|Choloma|15.61|-87.95|N
HN|Yoro|El Progreso|15.40|-87.80|N
HN|Cortés|Villanueva|15.32|-87.99|N
HN|Cortés|La Lima|15.43|-87.92|N
HN|El Paraíso|Danlí|14.03|-86.59|N
HK|Central and Western|Central|22.28|114.16|S
HK|Eastern|North Point|22.29|114.20|S
HK|Islands|Tung Chung|22.29|113.94|S
HK|Kowloon City|Kowloon City|22.33|114.19|S
HK|Kwai Tsing|Kwai Chung|22.36|114.13|SN
HK|Kwun Tong|Kwun Tong|22.31|114.22|S
HK|North|Sheung Shui|22.50|114.12|SN
HK|Sai Kung|Tseung Kwan O|22.31|114.26|SN
HK|Sha Tin|Sha Tin|22.38|114.19|SN
HK|Sham Shui Po|Sham Shui Po|22.33|114.16|S
HK|Southern|Aberdeen|22.25|114.15|S
HK|Tai Po|Tai Po|22.45|114.17|SN
HK|Tsuen Wan|Tsuen Wan|22.37|114.12|SN
HK|Tuen Mun|Tuen Mun|22.39|113.97|SN
HK|Wan Chai|Wan Chai|22.28|114.18|S
HK|Wong Tai Sin|Wong Tai Sin|22.34|114.19|S
HK|Yau Tsim Mong|Mong Kok|22.32|114.17|S
HK|Yuen Long|Yuen Long|22.45|114.03|SN
HK|Yuen Long|Tin Shui Wai|22.46|114.00|N
HK|Sha Tin|Ma On Shan|22.42|114.23|N
HU|Bács-Kiskun|Kecskemét|46.91|19.69|SN
HU|Baranya|Pécs|46.07|18.23|SN
HU|Békés|Békéscsaba|46.68|21.09|S
HU|Borsod-Abaúj-Zemplén|Miskolc|48.10|20.79|SN
HU|Budapest|Budapest|47.50|19.04|SN
HU|Csongrád-Csanád|Szeged|46.25|20.15|SN
HU|Fejér|Székesfehérvár|47.19|18.41|SN
HU|Győr-Moson-Sopron|Győr|47.69|17.63|SN
HU|Hajdú-Bihar|Debrecen|47.53|21.63|SN
HU|Heves|Eger|47.90|20.38|S
HU|Jász-Nagykun-Szolnok|Szolnok|47.17|20.19|S
HU|Komárom-Esztergom|Tatabánya|47.58|18.39|S
HU|Nógrád|Salgótarján|48.10|19.80|S
HU|Pest|Érd|47.38|18.92|S
HU|Somogy|Kaposvár|46.36|17.80|S
HU|Szabolcs-Szatmár-Bereg|Nyíregyháza|47.96|21.72|SN
HU|Tolna|Szekszárd|46.35|18.71|S
HU|Vas|Szombathely|47.23|16.62|SN
HU|Veszprém|Veszprém|47.09|17.91|S
HU|Zala|Zalaegerszeg|46.84|16.84|S
IS|Capital Region|Reykjavík|64.15|-21.94|SN
IS|East|Egilsstaðir|65.27|-14.39|S
IS|Northeast|Akureyri|65.68|-18.09|SN
IS|Northwest|Sauðárkrókur|65.75|-19.64|S
IS|South|Selfoss|63.93|-20.99|SN
IS|Southern Peninsula|Keflavík|63.99|-22.56|SN
IS|West|Akranes|64.32|-22.07|SN
IS|Westfjords|Ísafjörður|66.08|-23.12|S
IS|Capital Region|Kópavogur|64.11|-21.91|N
IS|Capital Region|Hafnarfjörður|64.07|-21.96|N
IS|Capital Region|Garðabær|64.09|-21.93|N
IS|Capital Region|Mosfellsbær|64.17|-21.70|N
IS|Capital Region|Seltjarnarnes|64.16|-22.00|N
IN|Andhra Pradesh|Amaravati|16.52|80.52|S
IN|Arunachal Pradesh|Itanagar|27.09|93.62|S
IN|Assam|Guwahati|26.14|91.74|S
IN|Bihar|Patna|25.61|85.14|S
IN|Chhattisgarh|Raipur|21.25|81.63|S
IN|Goa|Panaji|15.50|73.83|S
IN|Gujarat|Gandhinagar|23.22|72.65|S
IN|Haryana|Faridabad|28.41|77.31|S
IN|Himachal Pradesh|Shimla|31.10|77.17|S
IN|Jharkhand|Ranchi|23.34|85.31|S
IN|Karnataka|Bengaluru|12.97|77.59|SN
IN|Kerala|Thiruvananthapuram|8.52|76.94|S
IN|Madhya Pradesh|Bhopal|23.26|77.41|S
IN|Maharashtra|Mumbai|19.08|72.88|SN
IN|Manipur|Imphal|24.82|93.95|S
IN|Meghalaya|Shillong|25.57|91.88|S
IN|Mizoram|Aizawl|23.73|92.72|S
IN|Nagaland|Kohima|25.67|94.11|S
IN|Odisha|Bhubaneswar|20.30|85.82|S
IN|Punjab|Ludhiana|30.90|75.85|S
IN|Rajasthan|Jaipur|26.91|75.79|SN
IN|Sikkim|Gangtok|27.33|88.61|S
IN|Tamil Nadu|Chennai|13.08|80.27|SN
IN|Telangana|Hyderabad|17.39|78.49|SN
IN|Tripura|Agartala|23.83|91.28|S
IN|Uttar Pradesh|Lucknow|26.85|80.95|S
IN|Uttarakhand|Dehradun|30.32|78.03|S
IN|West Bengal|Kolkata|22.57|88.36|SN
IN|Andaman and Nicobar Islands|Sri Vijaya Puram|11.67|92.74|S
IN|Chandigarh|Chandigarh|30.73|76.78|S
IN|Dadra and Nagar Haveli and Daman and Diu|Daman|20.41|72.83|S
IN|Delhi|Delhi|28.61|77.21|SN
IN|Jammu and Kashmir|Srinagar|34.08|74.83|S
IN|Ladakh|Leh|34.16|77.58|S
IN|Lakshadweep|Kavaratti|10.56|72.64|S
IN|Puducherry|Puducherry|11.93|79.83|S
IN|Gujarat|Ahmedabad|23.03|72.58|N
IN|Maharashtra|Pune|18.52|73.86|N
IN|Gujarat|Surat|21.17|72.83|N
```

GU — 19 municipalities. Agat/Hågat, Inarajan/Inalåhan, Merizo/Malesso', Umatac/Humåtak and Santa Rita/Sånta Rita-Sumai have traditional or updated Chamorro names. The ten `N` flags use 2020 municipality populations, not the smaller census-designated places within them.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://cdn.www.census.gov\&sz=32)

Census.gov+1



GT — 22 departments. Petén/Peten, Quiché/Quiche and Sacatepéquez/Sacatepequez have accented and unaccented forms. Flores is Petén's departmental capital; nearby Santa Elena is larger. The ten `N` entries follow 2018 census urban-locality counts, including separate Guatemala City suburbs.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://portal.segeplan.gob.gt\&sz=32)

SEGEPLAN+1



GG — The Bailiwick of Guernsey contains the three jurisdictions of Guernsey, Alderney and Sark. Ten parishes cover Guernsey proper; Alderney and Sark are separately represented, with Herm added as a geographic coverage proxy. The `N` flags use populations of parish or island areas, not verified independent-city populations.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.gfsc.gg\&sz=32)

gfsc.gg+1



GN — Ten top-level units, comprising nine administrative regions and the special zone of Conakry. Beyla and Siguiri were created on August 20, 2026, replacing the former eight-unit structure. The ten `N` entries use 2025 census urban-centre figures; Manéah and Kagbélen are included in Greater Conakry.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://guineelex.com\&sz=32)

GuinéeLex+2



GW — Eight regions plus the Autonomous Sector of Bissau. Bolama is also called Bolama-Bijagós, Gabú/Gabu and Quinhámel/Quinhamel. The ten `N` cities use 2009 census locality populations.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://unfccc.int\&sz=32)

UNFCCC+1



GY — Ten administrative regions. Vreed-en-Hoop and Fort Wellington are regional administrative centres rather than incorporated cities. The ten `N` flags follow Guyana's ten officially recognised municipal towns and cities, rather than a population ranking of all settlements.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://factpage.glsc.gov.gy\&sz=32)

GLSC Fact Page+1



HT — Ten departments. Gonaïves/Gonaives, Cap-Haïtien/Cap-Haitien, and Jérémie/Jeremie are spelling variants. The ten `N` flags use 2024 IHSI commune population estimates, including separate municipalities in metropolitan Port-au-Prince; commune boundaries extend beyond city centres.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://ihsi.gouv.ht\&sz=32)

Jeu de données démographiques+1



HM — Heard Island and McDonald Islands are uninhabited Australian external territories. No permanent settlements or first-level administrative subdivisions exist.

HN — 18 departments. The capital of Francisco Morazán is the Central District, represented by Tegucigalpa. Coxen Hole represents Roatán, the seat of Islas de la Bahía. The ten `N` cities use 2023 urban-locality population estimates; Choloma, Villanueva and La Lima are counted separately from San Pedro Sula.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.geo-ref.net\&sz=32)

geo-ref.net+1



HK — 18 District Council districts. Hong Kong is a single highly interconnected urban territory, so the ten `N` flags represent large distinct new-town or urban-locality centres, not ten formally independent cities. Sheung Shui represents the Fanling–Sheung Shui urban area. Hong Kong also appears under China's provincial-level structure in Message 4; avoid duplicate extraction.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.had.gov.hk\&sz=32)

My Districts+1



HU — 19 counties (vármegyék) plus separately administered Budapest. Csongrád-Csanád was formerly Csongrád County. Budapest is the administrative centre of Pest County but lies outside it, so Érd is used as the largest city within Pest. The ten `N` flags follow city-proper populations.

IS — Eight statistical regions are used for geographic coverage; Iceland's actual local-government units are 62 municipalities in 2026. Keflavík represents the combined Keflavík–Njarðvík urban area of Reykjanesbær. The ten `N` entries use January 2026 separate urban-nucleus populations, counting Reykjavík-area towns individually.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.iceland.org\&sz=32)

Iceland.org+1



IN — 28 states and eight union territories. Sri Vijaya Puram was formerly Port Blair, renamed in September 2024. Amaravati is Andhra Pradesh's statutory capital. Chandigarh is the shared capital of Punjab and Haryana but is itself a separate union territory, so Ludhiana and Faridabad are used as the largest cities inside those states. Assam's capital Dispur is within Guwahati; Uttarakhand and Jammu and Kashmir have seasonal capital arrangements. The ten `N` cities follow the 2011 census urban-agglomeration ranking.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.bookofexams.in\&sz=32)

BookOfExams+2



Points still open:

- GU: Match Chamorro-renamed municipalities to legacy Overture names. Confirm the use of municipality populations rather than 2020 census-designated-place populations.
- GT: Confirm how Santa Elena and Flores are separated in Petén. Preserve Guatemala City's surrounding municipalities as distinct population centres.
- GG: Verify Overture's handling of Alderney, Sark, Herm and Jethou. The `N` classification uses parish-population proxies and requires town-level validation.
- GN: Verify whether Overture reflects the August 2026 creation of Beyla and Siguiri. Newly created regional boundaries may not yet be consistently published or implemented.
- GW: Confirm the Bissau autonomous-sector boundary and whether a newer reliable settlement census supersedes the 2009 ranking.
- GY: Verify Fort Wellington and Vreed-en-Hoop point placement. Reconcile the ten incorporated municipalities with a strict largest-settlements-by-population ranking.
- HT: Resolve administrative commune versus built-up urban populations, especially for Delmas, Carrefour, Cité Soleil and Croix-des-Bouquets.
- HN: Verify Coxen Hole/Roatán naming and the separation of San Pedro Sula from adjacent urban municipalities.
- HK: Decide whether new towns, individual neighbourhoods or continuous urban agglomerations should define the final top ten. Preserve all 18 district boundaries.
- HU: Confirm that Pest County is geographically separated from Budapest when assigning Érd, and that current county naming is reflected in Overture.
- IS: Decide whether the eight statistical regions are sufficient for the extraction hierarchy or whether all 62 municipalities must be audited individually.
- IN: Resolve administrative-boundary differences for Jammu and Kashmir, Ladakh and other disputed territory; match Sri Vijaya Puram to Port Blair as an alias; preserve the separate Chandigarh UT without duplicating its businesses under Punjab or Haryana.


---

## Claude Code - 2026-11-08 19:37 UTC - 09_claude.md - attachments: none

## Check of your message-8 list (businesses within 10 km or with that city name)
Round 8: 230 reference lines, 229 cities, 229 with business data (100 %).

Same format again:


## Message 9 of 19 - countries
Indonesia (ID), Iran (IR), Iraq (IQ), Ireland (IE), Isle of Man (IM), Israel (IL), Italy (IT), Jamaica (JM), Japan (JP), Jersey (JE), Jordan (JO), Kazakhstan (KZ), Kenya (KE)

For EACH country above give:
1. every first-level administrative division (state / province / region / governorate ... as it is today),
   with its capital or largest city (kind S);
2. the 10 largest cities of the country by population (kind N) - fewer if the country has fewer.
   A city can appear as both S and N; list it once with kind SN.
Uninhabited territories: one line `CC|-|-|||none`.

Output ONLY one code block, one line per city, pipe-separated, no header, no commentary inside it:
`CC|state|city|lat|lon|kind`
- CC = ISO code above; state and city in English (the name a map would show); lat / lon with 2 decimals.
After the code block: one line per country with any naming caveat (renamed divisions, disputed areas),
then the list of points still open.


---

## ChatGPT (Extra High) - 2026-11-08 19:49 UTC - saved as 09_chatgpt.md

```
ID|Aceh|Banda Aceh|5.55|95.32|S
ID|Bali|Denpasar|-8.65|115.22|S
ID|Bangka Belitung Islands|Pangkalpinang|-2.13|106.11|S
ID|Banten|Serang|-6.12|106.15|S
ID|Bengkulu|Bengkulu|-3.79|102.26|S
ID|Central Java|Semarang|-6.97|110.42|SN
ID|Central Kalimantan|Palangka Raya|-2.21|113.92|S
ID|Central Papua|Nabire|-3.36|135.50|S
ID|Central Sulawesi|Palu|-0.90|119.87|S
ID|East Java|Surabaya|-7.26|112.75|SN
ID|East Kalimantan|Samarinda|-0.50|117.15|S
ID|East Nusa Tenggara|Kupang|-10.18|123.61|S
ID|Gorontalo|Gorontalo|0.54|123.06|S
ID|Highland Papua|Wamena|-4.10|138.95|S
ID|Jakarta|Jakarta|-6.21|106.85|SN
ID|Jambi|Jambi|-1.61|103.61|S
ID|Lampung|Bandar Lampung|-5.45|105.27|S
ID|Maluku|Ambon|-3.70|128.18|S
ID|North Kalimantan|Tanjung Selor|2.84|117.37|S
ID|North Maluku|Sofifi|0.74|127.56|S
ID|North Sulawesi|Manado|1.49|124.84|S
ID|North Sumatra|Medan|3.59|98.67|SN
ID|Papua|Jayapura|-2.53|140.72|S
ID|Riau|Pekanbaru|0.51|101.45|S
ID|Riau Islands|Tanjungpinang|0.92|104.46|S
ID|South Kalimantan|Banjarbaru|-3.44|114.83|S
ID|South Papua|Merauke|-8.49|140.40|S
ID|South Sulawesi|Makassar|-5.15|119.43|SN
ID|South Sumatra|Palembang|-2.99|104.76|SN
ID|Southeast Sulawesi|Kendari|-3.99|122.51|S
ID|Southwest Papua|Sorong|-0.88|131.25|S
ID|West Java|Bandung|-6.91|107.61|SN
ID|West Kalimantan|Pontianak|-0.03|109.34|S
ID|West Nusa Tenggara|Mataram|-8.58|116.12|S
ID|West Papua|Manokwari|-0.86|134.06|S
ID|West Sulawesi|Mamuju|-2.68|118.89|S
ID|West Sumatra|Padang|-0.95|100.35|S
ID|Yogyakarta|Yogyakarta|-7.80|110.37|S
ID|West Java|Bekasi|-6.24|106.99|N
ID|West Java|Depok|-6.40|106.82|N
ID|Banten|Tangerang|-6.18|106.63|N
IR|Alborz|Karaj|35.84|50.94|SN
IR|Ardabil|Ardabil|38.25|48.30|S
IR|Bushehr|Bushehr|28.92|50.84|S
IR|Chaharmahal and Bakhtiari|Shahrekord|32.33|50.86|S
IR|East Azerbaijan|Tabriz|38.08|46.29|SN
IR|Fars|Shiraz|29.59|52.58|SN
IR|Gilan|Rasht|37.28|49.59|S
IR|Golestan|Gorgan|36.84|54.44|S
IR|Hamadan|Hamadan|34.80|48.52|S
IR|Hormozgan|Bandar Abbas|27.19|56.27|S
IR|Ilam|Ilam|33.64|46.42|S
IR|Isfahan|Isfahan|32.65|51.67|SN
IR|Kerman|Kerman|30.28|57.08|S
IR|Kermanshah|Kermanshah|34.31|47.07|SN
IR|Khuzestan|Ahvaz|31.32|48.67|SN
IR|Kohgiluyeh and Boyer-Ahmad|Yasuj|30.67|51.59|S
IR|Kurdistan|Sanandaj|35.31|46.99|S
IR|Lorestan|Khorramabad|33.49|48.36|S
IR|Markazi|Arak|34.09|49.69|S
IR|Mazandaran|Sari|36.56|53.06|S
IR|North Khorasan|Bojnord|37.47|57.33|S
IR|Qazvin|Qazvin|36.27|50.00|S
IR|Qom|Qom|34.64|50.88|SN
IR|Razavi Khorasan|Mashhad|36.30|59.60|SN
IR|Semnan|Semnan|35.57|53.40|S
IR|Sistan and Baluchestan|Zahedan|29.50|60.86|S
IR|South Khorasan|Birjand|32.87|59.22|S
IR|Tehran|Tehran|35.69|51.39|SN
IR|West Azerbaijan|Urmia|37.55|45.07|SN
IR|Yazd|Yazd|31.90|54.37|S
IR|Zanjan|Zanjan|36.67|48.48|S
IQ|Al Anbar|Ramadi|33.42|43.30|S
IQ|Babil|Hillah|32.48|44.44|S
IQ|Baghdad|Baghdad|33.31|44.36|SN
IQ|Basra|Basra|30.51|47.81|SN
IQ|Dhi Qar|Nasiriyah|31.06|46.26|SN
IQ|Diyala|Baqubah|33.75|44.64|S
IQ|Dohuk|Duhok|36.87|42.99|S
IQ|Erbil|Erbil|36.19|44.01|SN
IQ|Halabja|Halabja|35.18|45.99|S
IQ|Karbala|Karbala|32.62|44.02|SN
IQ|Kirkuk|Kirkuk|35.47|44.39|SN
IQ|Maysan|Amarah|31.84|47.15|SN
IQ|Muthanna|Samawah|31.31|45.28|S
IQ|Najaf|Najaf|32.00|44.33|SN
IQ|Nineveh|Mosul|36.34|43.13|SN
IQ|Al-Qadisiyah|Diwaniyah|31.99|44.92|S
IQ|Salah ad Din|Tikrit|34.61|43.68|S
IQ|Sulaymaniyah|Sulaymaniyah|35.56|45.43|SN
IQ|Wasit|Kut|32.51|45.82|S
IE|Carlow|Carlow|52.84|-6.93|S
IE|Cavan|Cavan|53.99|-7.36|S
IE|Clare|Ennis|52.84|-8.98|S
IE|Cork City|Cork|51.90|-8.47|SN
IE|Cork County|Carrigaline|51.81|-8.39|S
IE|Donegal|Lifford|54.83|-7.49|S
IE|Dublin City|Dublin|53.35|-6.26|SN
IE|Dún Laoghaire-Rathdown|Dún Laoghaire|53.29|-6.14|S
IE|Fingal|Swords|53.46|-6.22|SN
IE|Galway City|Galway|53.27|-9.06|SN
IE|Galway County|Tuam|53.52|-8.85|S
IE|Kerry|Tralee|52.27|-9.70|S
IE|Kildare|Naas|53.22|-6.66|S
IE|Kilkenny|Kilkenny|52.65|-7.25|S
IE|Laois|Portlaoise|53.03|-7.30|S
IE|Leitrim|Carrick-on-Shannon|53.94|-8.09|S
IE|Limerick City and County|Limerick|52.67|-8.63|SN
IE|Longford|Longford|53.73|-7.80|S
IE|Louth|Dundalk|54.00|-6.40|SN
IE|Mayo|Castlebar|53.85|-9.30|S
IE|Meath|Navan|53.65|-6.68|SN
IE|Monaghan|Monaghan|54.25|-6.97|S
IE|Offaly|Tullamore|53.27|-7.49|S
IE|Roscommon|Roscommon|53.63|-8.19|S
IE|Sligo|Sligo|54.27|-8.47|S
IE|South Dublin|Tallaght|53.29|-6.36|S
IE|Tipperary|Clonmel|52.36|-7.70|S
IE|Waterford City and County|Waterford|52.26|-7.11|SN
IE|Westmeath|Mullingar|53.53|-7.34|S
IE|Wexford|Wexford|52.34|-6.46|S
IE|Wicklow|Wicklow|52.98|-6.05|S
IE|Louth|Drogheda|53.72|-6.35|N
IE|Wicklow|Bray|53.20|-6.11|N
IM|Andreas|Andreas|54.37|-4.44|S
IM|Arbory and Rushen|Ballabeg|54.10|-4.69|S
IM|Ballaugh|Ballaugh|54.31|-4.54|S
IM|Braddan|Union Mills|54.17|-4.52|S
IM|Bride|Bride|54.39|-4.39|S
IM|Castletown|Castletown|54.07|-4.65|SN
IM|Douglas|Douglas|54.15|-4.48|SN
IM|Garff|Laxey|54.23|-4.40|SN
IM|German|St John's|54.20|-4.64|S
IM|Jurby|Jurby|54.36|-4.51|S
IM|Lezayre|Sulby|54.31|-4.48|S
IM|Malew|Ballasalla|54.10|-4.64|S
IM|Marown|Crosby|54.18|-4.57|S
IM|Michael|Kirk Michael|54.29|-4.59|S
IM|Onchan|Onchan|54.17|-4.44|SN
IM|Patrick|Patrick|54.20|-4.70|S
IM|Peel|Peel|54.22|-4.69|SN
IM|Port Erin|Port Erin|54.08|-4.76|SN
IM|Port St Mary|Port St Mary|54.07|-4.74|SN
IM|Ramsey|Ramsey|54.32|-4.38|SN
IM|Santon|Santon|54.13|-4.59|S
IL|Central|Ramla|31.93|34.87|S
IL|Haifa|Haifa|32.82|34.99|SN
IL|Jerusalem|Jerusalem|31.78|35.22|SN
IL|Northern|Nof HaGalil|32.71|35.32|S
IL|Southern|Beersheba|31.25|34.79|SN
IL|Tel Aviv|Tel Aviv|32.09|34.78|SN
IL|Central|Petah Tikva|32.09|34.89|N
IL|Central|Rishon LeZion|31.97|34.80|N
IL|Tel Aviv|Bnei Brak|32.08|34.83|N
IL|Central|Netanya|32.33|34.86|N
IL|Southern|Ashdod|31.80|34.65|N
IL|Jerusalem|Beit Shemesh|31.75|34.99|N
IT|Abruzzo|L'Aquila|42.35|13.40|S
IT|Aosta Valley|Aosta|45.74|7.32|S
IT|Apulia|Bari|41.12|16.87|SN
IT|Basilicata|Potenza|40.64|15.81|S
IT|Calabria|Catanzaro|38.91|16.59|S
IT|Campania|Naples|40.85|14.27|SN
IT|Emilia-Romagna|Bologna|44.49|11.34|SN
IT|Friuli-Venezia Giulia|Trieste|45.65|13.77|S
IT|Lazio|Rome|41.90|12.50|SN
IT|Liguria|Genoa|44.41|8.93|SN
IT|Lombardy|Milan|45.46|9.19|SN
IT|Marche|Ancona|43.62|13.52|S
IT|Molise|Campobasso|41.56|14.66|S
IT|Piedmont|Turin|45.07|7.69|SN
IT|Sardinia|Cagliari|39.22|9.12|S
IT|Sicily|Palermo|38.12|13.36|SN
IT|Trentino-Alto Adige|Trento|46.07|11.12|S
IT|Tuscany|Florence|43.77|11.26|SN
IT|Umbria|Perugia|43.11|12.39|S
IT|Veneto|Venice|45.44|12.33|S
IT|Sicily|Catania|37.51|15.09|N
JM|Clarendon|May Pen|17.97|-77.25|SN
JM|Hanover|Lucea|18.45|-78.17|S
JM|Kingston|Kingston|17.97|-76.79|SN
JM|Manchester|Mandeville|18.04|-77.51|SN
JM|Portland|Port Antonio|18.18|-76.45|S
JM|Saint Andrew|Half Way Tree|18.01|-76.79|S
JM|Saint Ann|Saint Ann's Bay|18.43|-77.20|S
JM|Saint Catherine|Spanish Town|17.99|-76.96|SN
JM|Saint Elizabeth|Black River|18.03|-77.85|S
JM|Saint James|Montego Bay|18.47|-77.92|SN
JM|Saint Mary|Port Maria|18.37|-76.90|S
JM|Saint Thomas|Morant Bay|17.88|-76.41|S
JM|Trelawny|Falmouth|18.49|-77.66|SN
JM|Westmoreland|Savanna-la-Mar|18.22|-78.13|SN
JM|Saint Catherine|Portmore|17.95|-76.88|N
JM|Saint Catherine|Old Harbour|17.94|-77.11|N
JM|Saint Ann|Ocho Rios|18.40|-77.10|N
JP|Aichi|Nagoya|35.18|136.91|SN
JP|Akita|Akita|39.72|140.10|S
JP|Aomori|Aomori|40.82|140.75|S
JP|Chiba|Chiba|35.61|140.11|S
JP|Ehime|Matsuyama|33.84|132.77|S
JP|Fukui|Fukui|36.06|136.22|S
JP|Fukuoka|Fukuoka|33.59|130.40|SN
JP|Fukushima|Fukushima|37.76|140.47|S
JP|Gifu|Gifu|35.42|136.76|S
JP|Gunma|Maebashi|36.39|139.06|S
JP|Hiroshima|Hiroshima|34.39|132.46|S
JP|Hokkaido|Sapporo|43.06|141.35|SN
JP|Hyogo|Kobe|34.69|135.20|SN
JP|Ibaraki|Mito|36.37|140.47|S
JP|Ishikawa|Kanazawa|36.56|136.66|S
JP|Iwate|Morioka|39.70|141.15|S
JP|Kagawa|Takamatsu|34.34|134.05|S
JP|Kagoshima|Kagoshima|31.60|130.56|S
JP|Kanagawa|Yokohama|35.44|139.64|SN
JP|Kochi|Kochi|33.56|133.53|S
JP|Kumamoto|Kumamoto|32.80|130.71|S
JP|Kyoto|Kyoto|35.01|135.77|SN
JP|Mie|Tsu|34.72|136.51|S
JP|Miyagi|Sendai|38.27|140.87|S
JP|Miyazaki|Miyazaki|31.91|131.42|S
JP|Nagano|Nagano|36.65|138.19|S
JP|Nagasaki|Nagasaki|32.74|129.87|S
JP|Nara|Nara|34.69|135.80|S
JP|Niigata|Niigata|37.92|139.04|S
JP|Oita|Oita|33.24|131.61|S
JP|Okayama|Okayama|34.66|133.93|S
JP|Okinawa|Naha|26.21|127.68|S
JP|Osaka|Osaka|34.69|135.50|SN
JP|Saga|Saga|33.25|130.30|S
JP|Saitama|Saitama|35.86|139.65|SN
JP|Shiga|Otsu|35.02|135.85|S
JP|Shimane|Matsue|35.47|133.05|S
JP|Shizuoka|Shizuoka|34.98|138.38|S
JP|Tochigi|Utsunomiya|36.56|139.88|S
JP|Tokushima|Tokushima|34.07|134.56|S
JP|Tokyo|Tokyo|35.68|139.69|SN
JP|Tottori|Tottori|35.50|134.24|S
JP|Toyama|Toyama|36.70|137.21|S
JP|Wakayama|Wakayama|34.23|135.17|S
JP|Yamagata|Yamagata|38.26|140.34|S
JP|Yamaguchi|Yamaguchi|34.18|131.47|S
JP|Yamanashi|Kofu|35.66|138.57|S
JP|Kanagawa|Kawasaki|35.53|139.70|N
JE|Grouville|Grouville|49.19|-2.04|S
JE|Saint Brelade|Saint Aubin|49.19|-2.17|SN
JE|Saint Clement|Le Hocq|49.17|-2.07|S
JE|Saint Helier|Saint Helier|49.19|-2.11|SN
JE|Saint John|Saint John|49.24|-2.14|S
JE|Saint Lawrence|Saint Lawrence|49.21|-2.15|S
JE|Saint Martin|Saint Martin|49.22|-2.05|S
JE|Saint Mary|Saint Mary|49.23|-2.17|S
JE|Saint Ouen|Saint Ouen|49.23|-2.21|S
JE|Saint Peter|Saint Peter|49.21|-2.17|S
JE|Saint Saviour|Saint Saviour|49.20|-2.08|S
JE|Trinity|Trinity|49.23|-2.10|S
JE|Saint Brelade|Les Quennevais|49.19|-2.20|N
JE|Grouville|Gorey|49.20|-2.02|N
JE|Saint Clement|La Rocque|49.16|-2.05|N
JO|Ajloun|Ajloun|32.33|35.75|S
JO|Amman|Amman|31.95|35.93|SN
JO|Aqaba|Aqaba|29.53|35.01|S
JO|Balqa|Salt|32.04|35.73|S
JO|Irbid|Irbid|32.56|35.85|SN
JO|Jerash|Jerash|32.28|35.89|S
JO|Karak|Karak|31.18|35.70|S
JO|Ma'an|Ma'an|30.19|35.73|S
JO|Madaba|Madaba|31.72|35.79|S
JO|Mafraq|Mafraq|32.34|36.21|S
JO|Tafilah|Tafilah|30.83|35.61|S
JO|Zarqa|Zarqa|32.07|36.09|SN
JO|Zarqa|Russeifa|32.01|36.04|N
JO|Amman|Al Quwaysimah|31.92|35.96|N
JO|Amman|Khalda|31.98|35.84|N
JO|Amman|Wadi as-Seer|31.95|35.82|N
JO|Amman|Al Jubeiha|32.02|35.91|N
JO|Amman|Khraibet as-Souq|31.84|35.91|N
JO|Amman|Sahab|31.87|36.00|N
KZ|Abai|Semey|50.41|80.25|SN
KZ|Akmola|Kokshetau|53.28|69.38|S
KZ|Aktobe|Aktobe|50.28|57.17|SN
KZ|Almaty Region|Qonaev|43.86|77.06|S
KZ|Atyrau|Atyrau|47.12|51.88|SN
KZ|East Kazakhstan|Oskemen|49.96|82.61|SN
KZ|Jambyl|Taraz|42.90|71.37|SN
KZ|Jetisu|Taldykorgan|45.02|78.37|S
KZ|Karaganda|Karaganda|49.80|73.10|SN
KZ|Kostanay|Kostanay|53.21|63.63|S
KZ|Kyzylorda|Kyzylorda|44.85|65.51|S
KZ|Mangystau|Aktau|43.65|51.18|S
KZ|North Kazakhstan|Petropavl|54.87|69.15|S
KZ|Pavlodar|Pavlodar|52.29|76.95|SN
KZ|Turkistan|Turkistan|43.30|68.27|S
KZ|Ulytau|Zhezkazgan|47.80|67.71|S
KZ|West Kazakhstan|Oral|51.23|51.38|S
KZ|Almaty City|Almaty|43.24|76.95|SN
KZ|Astana City|Astana|51.17|71.45|SN
KZ|Shymkent City|Shymkent|42.32|69.59|SN
KE|Baringo|Kabarnet|0.49|35.74|S
KE|Bomet|Bomet|-0.78|35.34|S
KE|Bungoma|Bungoma|0.57|34.56|S
KE|Busia|Busia|0.46|34.11|S
KE|Elgeyo Marakwet|Iten|0.67|35.51|S
KE|Embu|Embu|-0.53|37.45|S
KE|Garissa|Garissa|-0.46|39.64|S
KE|Homa Bay|Homa Bay|-0.53|34.46|S
KE|Isiolo|Isiolo|0.36|37.58|S
KE|Kajiado|Kajiado|-1.85|36.78|S
KE|Kakamega|Kakamega|0.28|34.75|S
KE|Kericho|Kericho|-0.37|35.28|S
KE|Kiambu|Kiambu|-1.17|36.83|S
KE|Kilifi|Kilifi|-3.63|39.85|S
KE|Kirinyaga|Kerugoya|-0.50|37.28|S
KE|Kisii|Kisii|-0.68|34.78|S
KE|Kisumu|Kisumu|-0.10|34.76|SN
KE|Kitui|Kitui|-1.37|38.02|S
KE|Kwale|Kwale|-4.17|39.45|S
KE|Laikipia|Rumuruti|0.27|36.54|S
KE|Lamu|Lamu|-2.27|40.90|S
KE|Machakos|Machakos|-1.52|37.27|S
KE|Makueni|Wote|-1.78|37.63|S
KE|Mandera|Mandera|3.94|41.86|S
KE|Marsabit|Marsabit|2.33|37.99|S
KE|Meru|Meru|0.05|37.65|S
KE|Migori|Migori|-1.06|34.47|S
KE|Mombasa|Mombasa|-4.05|39.67|SN
KE|Murang'a|Murang'a|-0.72|37.15|S
KE|Nairobi City|Nairobi|-1.29|36.82|SN
KE|Nakuru|Nakuru|-0.30|36.08|SN
KE|Nandi|Kapsabet|0.20|35.10|S
KE|Narok|Narok|-1.08|35.87|S
KE|Nyamira|Nyamira|-0.56|34.93|S
KE|Nyandarua|Ol Kalou|-0.27|36.38|S
KE|Nyeri|Nyeri|-0.42|36.95|S
KE|Samburu|Maralal|1.10|36.70|S
KE|Siaya|Siaya|0.06|34.29|S
KE|Taita Taveta|Mwatate|-3.50|38.38|S
KE|Tana River|Hola|-1.50|40.03|S
KE|Tharaka Nithi|Kathwana|-0.33|37.87|S
KE|Trans Nzoia|Kitale|1.02|35.01|S
KE|Turkana|Lodwar|3.12|35.60|S
KE|Uasin Gishu|Eldoret|0.52|35.27|SN
KE|Vihiga|Mbale|0.08|34.72|S
KE|Wajir|Wajir|1.75|40.06|S
KE|West Pokot|Kapenguria|1.24|35.11|S
KE|Kiambu|Ruiru|-1.15|36.96|N
KE|Kiambu|Kikuyu|-1.25|36.66|N
KE|Kiambu|Thika|-1.03|37.07|N
KE|Nakuru|Naivasha|-0.72|36.43|N
KE|Kiambu|Karuri|-1.18|36.76|N
```

ID — 38 provinces, including the four Papua provinces established in 2022. Banjarbaru replaced Banjarmasin as South Kalimantan's capital. Jakarta remains the functioning national capital pending the effective transfer to Nusantara. Top-ten flags use individual administrative-city populations, including Jakarta's special province-level city.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://kabar24.bisnis.com\&sz=32)

kabar24.bisnis.com+1



IR — 31 provinces. Isfahan/Esfahan, Urmia/Orumiyeh, Hamadan/Hamedan and Bojnord/Bojnurd are spelling variants. The ten largest cities use the 2016 national census, which remains the comparable city-proper ranking used here.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.worldometers.info\&sz=32)

Worldometer



IQ — 19 governorates since Halabja officially separated from Sulaymaniyah in May 2025. Dohuk/Duhok, Basra/Basrah, Karbala/Kerbala and Amarah/Amara are variants. The ten largest cities follow the 2024 census; Kurdish governorate boundaries and disputed internal areas require separate validation.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.euaa.europa.eu\&sz=32)

European Union Agency for Asylum+1



IE — 31 local-authority areas: 26 county councils, three city councils and two combined city-and-county councils. Cork County and Galway County are represented by their largest internal towns rather than council offices located in separately administered cities. The ten largest urban settlements use the 2022 census, counting the five principal cities and five largest other towns.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://data.gov.ie\&sz=32)

data.gov.ie+1



IM — 21 local authorities, including the combined Arbory and Rushen authority and Garff. Eight independently ranked towns and villages are available from the 2021 census; smaller parish centres receive only `S` flags. The six traditional sheadings are a different geographic hierarchy.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://elections.gov.im\&sz=32)

elections.gov.im+1



IL — Six official administrative districts. Nof HaGalil, formerly Nazareth Illit, houses Northern District government offices. Israel's statistical system also reports a separate Judea and Samaria area; it is not treated here as an additional internationally recognised Israeli district. Jerusalem's boundaries and status are disputed. The ten largest cities use provisional 2026 resident estimates.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://ar.nof-hagalil.muni.il\&sz=32)

ar.nof-hagalil.muni.il+1



IT — 20 regions, including five with autonomous status. Apulia/Puglia, Piedmont/Piemonte, Lombardy/Lombardia and Tuscany/Toscana are name variants. Trentino-Alto Adige is also called Trentino-South Tyrol. The ten largest cities follow January 2026 ISTAT municipality populations.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.tuttitalia.it\&sz=32)

Tuttitalia.it



JM — 14 parishes. Kingston and Saint Andrew share a local-government corporation but remain distinct parishes. Half Way Tree represents Saint Andrew's administrative centre. The ten largest urban places follow the 2022 census, including the Kingston metropolitan urban area as a single population centre.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.worldometers.info\&sz=32)

Worldometer



JP — 47 prefectures. Tokyo's `SN` point represents its 23 special wards, rather than a separately incorporated Tokyo City; the metropolitan government sits in Shinjuku. Kochi/Kōchi, Oita/Ōita and Hyogo/Hyōgo are transliteration variants. The ten largest cities follow 2025 city-proper population counts.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.worldometers.info\&sz=32)

Worldometer



JE — 12 parishes, without a separate provincial tier. Saint Helier is the main town; Saint Aubin, Les Quennevais, Gorey and La Rocque are significant smaller settlement representatives, not a census-verified top-five population ranking. Parish population figures cannot be treated as individual village populations.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.statesassembly.je\&sz=32)

R-45-2023+1



JO — 12 governorates. Salt/As-Salt, Karak/Al Karak, Russeifa/Rusayfa and Tafilah/At-Tafilah are spelling variants. The ten largest `N` localities follow the 2015 census, including several separately enumerated urban areas within Greater Amman.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.worldometers.info\&sz=32)

Worldometer



KZ — 17 regions plus three cities of republican significance. Abai, Jetisu and Ulytau were established in 2022; Qonaev became Almaty Region's capital, and Astana reverted from Nur-Sultan to its former name. Oskemen/Ust-Kamenogorsk, Oral/Uralsk and Semey/Semipalatinsk are name variants. Top-ten flags use January 2026 settlement populations.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://stat.gov.kz\&sz=32)

stat.gov.kz+1



KE — 47 counties. Laikipia is represented by Rumuruti, its relocated county-government seat; Kirinyaga by Kerugoya, although the county executive headquarters is in nearby Kutus; and Tharaka Nithi by Kathwana, where a permanent headquarters opened in September 2026. The ten largest urban centres follow the 2019 national census.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://kdsp.devolution.go.ke\&sz=32)

Kenya Devolution Support Program (KDSP)+4



Points still open:

- ID: Check that Overture recognises all six current Papua provinces, Banjarbaru as South Kalimantan's capital and the Jakarta/Nusantara administrative transition. Verify that Bekasi, Depok and Tangerang remain separate from Jakarta's provincial boundary.
- IR: Update the top-ten city ranking if a newer comparable official census becomes available; reconcile older province-name transliterations.
- IQ: Check Overture's recognition of Halabja Governorate and its post-2025 boundary with Sulaymaniyah. Verify disputed administrative areas, particularly around Kirkuk and Nineveh.
- IE: Confirm that SiteBlitz's hierarchy uses 31 local-authority boundaries rather than 26 traditional counties. Avoid assigning Cork County or Galway County businesses to their separately administered city areas.
- IM: Check the merged Arbory and Rushen and Garff authority boundaries. Resolve whether the extraction uses 21 local authorities or six traditional sheadings.
- IL: Ensure Israeli districts and Palestinian ISO `PS` coverage are not double-counted, especially in Jerusalem and the West Bank. Reconcile provisional 2026 city estimates when final figures are published.
- IT: Verify multilingual region names, especially Aosta Valley and Trentino-Alto Adige, against Overture administrative labels.
- JM: Keep Kingston's combined metropolitan population separate from its Kingston and Saint Andrew parish boundaries. Check urban settlements spanning parish borders, particularly Ocho Rios.
- JP: Confirm Tokyo's 23-ward aggregation and avoid treating Shinjuku as an additional top-ten city. Keep Kawasaki distinct from neighbouring Yokohama and Tokyo.
- JE: Obtain comparable settlement-level populations if a strict ten-largest-towns ranking is required. Validate the geographic points for rural parish centres and their relationship to built-up settlement boundaries.
- JO: Decide whether individually enumerated Greater Amman localities should remain separate `N` entries or be consolidated into one continuous urban area.
- KZ: Verify 2022 region-boundary reforms in Overture, particularly Abai, Jetisu and Ulytau. Confirm the separation of Almaty City from Almaty Region and the current spelling Qonaev.
- KE: Verify Rumuruti, Kerugoya/Kutus and Kathwana headquarters assignments. Preserve the census-defined Ruiru, Kikuyu, Thika, Naivasha and Karuri urban centres separately, even when their business-search radii overlap surrounding cities.


---

## Claude Code - 2026-11-08 19:50 UTC - 10_claude.md - attachments: none

## Check of your message-9 list (businesses within 10 km or with that city name)
Round 9: 349 reference lines, 349 cities, 349 with business data (100 %).

Same format again:


## Message 10 of 19 - countries
Kiribati (KI), Kuwait (KW), Kyrgyzstan (KG), Laos (LA), Latvia (LV), Lebanon (LB), Lesotho (LS), Liberia (LR), Libya (LY), Liechtenstein (LI), Lithuania (LT), Luxembourg (LU), Macao SAR China (MO)

For EACH country above give:
1. every first-level administrative division (state / province / region / governorate ... as it is today),
   with its capital or largest city (kind S);
2. the 10 largest cities of the country by population (kind N) - fewer if the country has fewer.
   A city can appear as both S and N; list it once with kind SN.
Uninhabited territories: one line `CC|-|-|||none`.

Output ONLY one code block, one line per city, pipe-separated, no header, no commentary inside it:
`CC|state|city|lat|lon|kind`
- CC = ISO code above; state and city in English (the name a map would show); lat / lon with 2 decimals.
After the code block: one line per country with any naming caveat (renamed divisions, disputed areas),
then the list of points still open.


---

## ChatGPT (Extra High) - 2026-11-08 20:00 UTC - saved as 10_chatgpt.md

```
KI|Abaiang|Taburao|1.85|173.00|S
KI|Abemama|Tabiang|0.49|173.83|S
KI|Aranuka|Takaeang|0.16|173.59|S
KI|Arorae|Tamaroa|-2.63|176.82|S
KI|Banaba|Umwa|-0.87|169.53|S
KI|Beru|Tabiang|-1.32|175.99|S
KI|Betio Town Council|Betio|1.36|172.92|SN
KI|Butaritari|Kuuma|3.17|172.96|S
KI|Eutan Tarawa Council|Abaokoro|1.50|173.02|S
KI|Kiritimati|Tabwakea|2.02|-157.49|SN
KI|Kuria|Oneeke|0.23|173.42|S
KI|Maiana|Tebikerai|1.01|173.00|S
KI|Makin|Little Makin|3.38|172.99|S
KI|Marakei|Rawannawi|2.05|173.26|S
KI|Nikunau|Rungata|-1.34|176.44|S
KI|Nonouti|Toboiaki|-0.74|174.45|S
KI|Onotoa|Tekawa|-1.80|175.53|S
KI|Tabiteuea North|Utiroa|-1.21|174.76|S
KI|Tabiteuea South|Tewai|-1.44|175.01|S
KI|Tabuaeran|Paelau|3.86|-159.36|S
KI|Tamana|Barebuka|-2.49|175.97|S
KI|Teinainano Urban Council|Bairiki|1.33|172.98|SN
KI|Teraina|Tangkore|4.68|-160.40|S
KI|Teinainano Urban Council|Bikenibeu|1.35|173.13|N
KI|Teinainano Urban Council|Teaoraereke|1.33|173.00|N
KI|Teinainano Urban Council|Temwaiku|1.35|173.14|N
KI|Teinainano Urban Council|Eita|1.35|173.10|N
KI|Teinainano Urban Council|Ambo|1.33|173.02|N
KI|Teinainano Urban Council|Bonriki|1.38|173.16|N
KI|Kiritimati|London|1.99|-157.48|N
KW|Capital|Kuwait City|29.37|47.98|S
KW|Al Ahmadi|Al Ahmadi|29.08|48.08|S
KW|Al Farwaniyah|Farwaniya|29.28|47.96|SN
KW|Hawalli|Hawalli|29.33|48.03|SN
KW|Al Jahra|Jahra|29.34|47.66|S
KW|Mubarak Al Kabeer|Mubarak Al Kabeer|29.19|48.06|S
KW|Hawalli|Salmiya|29.34|48.08|N
KW|Al Farwaniyah|Jleeb Al Shuyoukh|29.27|47.93|N
KW|Al Ahmadi|Mahboula|29.15|48.12|N
KW|Al Farwaniyah|Khaitan|29.29|47.98|N
KW|Al Ahmadi|Mangaf|29.10|48.13|N
KW|Al Jahra|Jaber Al Ahmad City|29.34|47.76|N
KW|Al Ahmadi|Fahaheel|29.08|48.13|N
KW|Al Ahmadi|Sabah Al Ahmad City|28.78|48.06|N
KG|Batken|Batken|40.06|70.82|S
KG|Bishkek City|Bishkek|42.87|74.60|SN
KG|Chuy|Tokmok|42.84|75.30|SN
KG|Issyk-Kul|Karakol|42.49|78.39|SN
KG|Jalal-Abad|Manas|40.93|73.00|SN
KG|Naryn|Naryn|41.43|75.99|S
KG|Osh Region|Uzgen|40.77|73.30|SN
KG|Osh City|Osh|40.53|72.80|SN
KG|Talas|Talas|42.52|72.24|S
KG|Jalal-Abad|Bazar-Korgon|41.04|72.75|N
KG|Chuy|Kara-Balta|42.81|73.85|N
KG|Issyk-Kul|Balykchy|42.46|76.19|N
KG|Batken|Kyzyl-Kiya|40.26|72.13|N
LA|Attapeu|Attapeu|14.81|106.84|S
LA|Bokeo|Houayxay|20.27|100.41|S
LA|Bolikhamxay|Paksan|18.39|103.66|S
LA|Champasak|Pakse|15.12|105.80|SN
LA|Houaphanh|Xam Neua|20.42|104.04|SN
LA|Khammouane|Thakhek|17.41|104.83|SN
LA|Luang Namtha|Luang Namtha|20.95|101.41|S
LA|Luang Prabang|Luang Prabang|19.89|102.15|SN
LA|Oudomxay|Muang Xay|20.69|101.99|SN
LA|Phongsaly|Phongsaly|21.68|102.10|S
LA|Salavan|Salavan|15.71|106.41|S
LA|Savannakhet|Savannakhet|16.57|104.76|SN
LA|Sekong|Sekong|15.35|106.72|S
LA|Vientiane Capital|Vientiane|17.97|102.60|SN
LA|Vientiane Province|Phonhong|18.50|102.42|S
LA|Xaisomboun|Anouvong|18.98|103.11|S
LA|Xayaboury|Xayaboury|19.25|101.71|S
LA|Xiangkhouang|Phonsavan|19.45|103.19|SN
LA|Bokeo|Ban Khoan|20.35|100.09|N
LA|Savannakhet|Ban Xeno|16.68|104.99|N
LV|Ādaži|Ādaži|57.08|24.33|S
LV|Aizkraukle|Aizkraukle|56.60|25.26|S
LV|Alūksne|Alūksne|57.42|27.05|S
LV|Augšdaugava|Ilūkste|55.98|26.29|S
LV|Balvi|Balvi|57.13|27.27|S
LV|Bauska|Bauska|56.41|24.19|S
LV|Cēsis|Cēsis|57.31|25.27|S
LV|Dienvidkurzeme|Grobiņa|56.54|21.17|S
LV|Dobele|Dobele|56.63|23.28|S
LV|Gulbene|Gulbene|57.18|26.76|S
LV|Jēkabpils|Jēkabpils|56.50|25.87|SN
LV|Jelgava Municipality|Ozolnieki|56.69|23.79|S
LV|Ķekava|Ķekava|56.83|24.24|S
LV|Krāslava|Krāslava|55.90|27.17|S
LV|Kuldīga|Kuldīga|56.97|21.97|S
LV|Limbaži|Limbaži|57.51|24.71|S
LV|Līvāni|Līvāni|56.35|26.18|S
LV|Ludza|Ludza|56.55|27.72|S
LV|Madona|Madona|56.85|26.22|S
LV|Mārupe|Mārupe|56.90|24.05|S
LV|Ogre|Ogre|56.82|24.61|SN
LV|Olaine|Olaine|56.79|23.94|S
LV|Preiļi|Preiļi|56.29|26.72|S
LV|Rēzekne Municipality|Viļāni|56.55|26.93|S
LV|Ropaži|Ulbroka|56.94|24.29|S
LV|Salaspils|Salaspils|56.86|24.36|S
LV|Saldus|Saldus|56.67|22.49|S
LV|Saulkrasti|Saulkrasti|57.26|24.41|S
LV|Sigulda|Sigulda|57.15|24.86|S
LV|Smiltene|Smiltene|57.42|25.90|S
LV|Talsi|Talsi|57.24|22.59|S
LV|Tukums|Tukums|56.97|23.16|S
LV|Valka|Valka|57.78|26.02|S
LV|Valmiera|Valmiera|57.54|25.43|SN
LV|Ventspils Municipality|Ugāle|57.28|22.05|S
LV|Daugavpils City|Daugavpils|55.87|26.53|SN
LV|Jelgava City|Jelgava|56.65|23.71|SN
LV|Jūrmala City|Jūrmala|56.97|23.77|SN
LV|Liepāja City|Liepāja|56.50|21.01|SN
LV|Rēzekne City|Rēzekne|56.51|27.34|SN
LV|Riga City|Riga|56.95|24.11|SN
LV|Ventspils City|Ventspils|57.39|21.56|SN
LB|Akkar|Halba|34.54|36.08|S
LB|Baalbek-Hermel|Baalbek|34.01|36.22|S
LB|Beirut|Beirut|33.89|35.50|SN
LB|Beqaa|Zahle|33.85|35.90|SN
LB|Keserwan-Jbeil|Jounieh|33.98|35.62|SN
LB|Mount Lebanon|Baabda|33.83|35.54|S
LB|Nabatieh|Nabatieh|33.38|35.48|SN
LB|North Lebanon|Tripoli|34.44|35.84|SN
LB|South Lebanon|Sidon|33.56|35.37|SN
LB|South Lebanon|Tyre|33.27|35.20|N
LB|Mount Lebanon|Aley|33.81|35.60|N
LB|Nabatieh|Habbouch|33.41|35.48|N
LB|Baalbek-Hermel|Arsal|34.18|36.42|N
LS|Berea|Teyateyaneng|-29.15|27.74|SN
LS|Butha-Buthe|Butha-Buthe|-28.77|28.25|SN
LS|Leribe|Hlotse|-28.87|28.04|SN
LS|Mafeteng|Mafeteng|-29.82|27.24|SN
LS|Maseru|Maseru|-29.32|27.48|SN
LS|Mohale's Hoek|Mohale's Hoek|-30.16|27.48|SN
LS|Mokhotlong|Mokhotlong|-29.29|29.07|S
LS|Qacha's Nek|Qacha's Nek|-30.12|28.69|SN
LS|Quthing|Quthing|-30.40|27.57|SN
LS|Thaba-Tseka|Thaba-Tseka|-29.52|28.61|SN
LS|Leribe|Maputsoe|-28.89|27.90|N
LR|Bomi|Tubmanburg|6.87|-10.82|S
LR|Bong|Gbarnga|7.00|-9.47|SN
LR|Gbarpolu|Bopolu|7.07|-10.49|S
LR|Grand Bassa|Buchanan|5.88|-10.05|SN
LR|Grand Cape Mount|Robertsport|6.75|-11.37|S
LR|Grand Gedeh|Zwedru|6.07|-8.13|S
LR|Grand Kru|Barclayville|4.68|-8.23|S
LR|Lofa|Voinjama|8.42|-9.75|SN
LR|Margibi|Kakata|6.53|-10.35|SN
LR|Maryland|Harper|4.38|-7.72|S
LR|Montserrado|Bensonville|6.45|-10.61|S
LR|Nimba|Sanniquellie|7.36|-8.71|S
LR|River Cess|Cestos City|5.47|-9.58|S
LR|River Gee|Fish Town|5.20|-7.88|S
LR|Sinoe|Greenville|5.01|-9.04|S
LR|Montserrado|Monrovia|6.31|-10.80|N
LR|Montserrado|Paynesville|6.29|-10.71|N
LR|Nimba|Ganta|7.24|-8.99|N
LR|Margibi|Harbel|6.28|-10.35|N
LR|Maryland|Pleebo|4.59|-7.68|N
LR|Lofa|Foya|8.37|-10.21|N
LY|Al Butnan|Tobruk|32.08|23.96|SN
LY|Al Jabal al Akhdar|Al Bayda|32.76|21.76|SN
LY|Al Jabal al Gharbi|Gharyan|32.18|13.02|S
LY|Al Jafara|Aziziyah|32.53|13.02|S
LY|Al Jufra|Hun|29.13|15.95|S
LY|Al Kufra|Al Jawf|24.22|23.30|S
LY|Al Marj|Al Marj|32.49|20.83|SN
LY|Al Marqab|Al Khums|32.65|14.26|S
LY|Al Wahat|Ajdabiya|30.75|20.23|SN
LY|An Nuqat al Khams|Zuwara|32.93|12.08|S
LY|Az Zawiyah|Zawiya|32.76|12.73|SN
LY|Benghazi|Benghazi|32.12|20.07|SN
LY|Derna|Derna|32.77|22.64|S
LY|Ghat|Ghat|25.71|10.18|S
LY|Misrata|Misrata|32.38|15.09|SN
LY|Murzuq|Murzuq|25.92|13.92|S
LY|Nalut|Nalut|31.87|10.98|S
LY|Sabha|Sabha|27.03|14.43|SN
LY|Sirte|Sirte|31.21|16.59|S
LY|Tripoli|Tripoli|32.89|13.19|SN
LY|Wadi al Hayaa|Ubari|26.59|12.78|S
LY|Wadi ash Shati|Brak|27.55|14.27|S
LY|Misrata|Zliten|32.47|14.57|N
LI|Balzers|Balzers|47.07|9.50|SN
LI|Eschen|Eschen|47.21|9.52|SN
LI|Gamprin|Gamprin|47.22|9.51|SN
LI|Mauren|Mauren|47.22|9.54|SN
LI|Planken|Planken|47.19|9.55|S
LI|Ruggell|Ruggell|47.24|9.52|SN
LI|Schaan|Schaan|47.16|9.51|SN
LI|Schellenberg|Schellenberg|47.23|9.55|SN
LI|Triesen|Triesen|47.11|9.52|SN
LI|Triesenberg|Triesenberg|47.12|9.54|SN
LI|Vaduz|Vaduz|47.14|9.52|SN
LT|Alytus|Alytus|54.40|24.05|SN
LT|Kaunas|Kaunas|54.90|23.90|SN
LT|Klaipėda|Klaipėda|55.70|21.14|SN
LT|Marijampolė|Marijampolė|54.56|23.35|SN
LT|Panevėžys|Panevėžys|55.73|24.36|SN
LT|Šiauliai|Šiauliai|55.93|23.32|SN
LT|Tauragė|Tauragė|55.25|22.29|S
LT|Telšiai|Telšiai|55.99|22.25|S
LT|Utena|Utena|55.50|25.60|SN
LT|Vilnius|Vilnius|54.69|25.28|SN
LT|Telšiai|Mažeikiai|56.31|22.34|N
LT|Kaunas|Jonava|55.08|24.28|N
LU|Capellen|Capellen|49.65|5.99|S
LU|Clervaux|Clervaux|50.05|6.03|S
LU|Diekirch|Diekirch|49.87|6.16|S
LU|Echternach|Echternach|49.81|6.42|S
LU|Esch-sur-Alzette|Esch-sur-Alzette|49.50|5.98|SN
LU|Grevenmacher|Grevenmacher|49.68|6.44|S
LU|Luxembourg|Luxembourg|49.61|6.13|SN
LU|Mersch|Mersch|49.75|6.11|S
LU|Redange|Redange-sur-Attert|49.76|5.89|S
LU|Remich|Remich|49.55|6.36|S
LU|Vianden|Vianden|49.94|6.21|S
LU|Wiltz|Wiltz|49.97|5.94|S
LU|Esch-sur-Alzette|Differdange|49.52|5.89|N
LU|Esch-sur-Alzette|Dudelange|49.48|6.09|N
LU|Esch-sur-Alzette|Pétange|49.56|5.88|N
LU|Esch-sur-Alzette|Sanem|49.55|5.93|N
LU|Luxembourg|Hesperange|49.57|6.15|N
LU|Esch-sur-Alzette|Schifflange|49.51|6.01|N
LU|Esch-sur-Alzette|Bettembourg|49.52|6.10|N
LU|Capellen|Mamer|49.63|6.02|N
MO|Nossa Senhora de Fátima|Areia Preta|22.21|113.55|S
MO|Santo António|Patane|22.20|113.54|S
MO|São Lázaro|São Lázaro|22.20|113.55|S
MO|Sé|Macau|22.19|113.54|SN
MO|São Lourenço|Barra|22.18|113.53|S
MO|Nossa Senhora do Carmo|Taipa|22.16|113.56|S
MO|São Francisco Xavier|Coloane|22.12|113.56|S
MO|Cotai|Cotai|22.15|113.57|S
```

KI — Kiribati uses 23 island councils for local administration; these are coverage proxies rather than a conventional provincial tier. BTC, TUC and ETC are the Betio, Teinainano and Eutan Tarawa councils. Kanton is geographically recognised but has no separate council in the current 23-council list. The ten `N` villages follow the 2020 census.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://mcia.gov.ki\&sz=32)

Ministry of Culture and Internal Affairs+2



KW — Six governorates. Capital is also called Al Asimah; Al Farwaniyah/Farwaniya and Al Jahra/Jahra are name variants. The ten `N` flags use June 2026 residential-locality populations, rather than the census's larger grouped urban areas. Some are suburbs rather than legally separate cities.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://timeskuwait.com\&sz=32)

Times Kuwait+1



KG — Seven regions and two separately administered cities. Jalal-Abad city was renamed Manas in September 2025, but Jalal-Abad Region retains its name. Bishkek and Osh are outside their surrounding oblast administrations; Tokmok and Uzgen represent those regions internally.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://assets.publishing.service.gov.uk\&sz=32)

assets.publishing.service.gov.uk



LA — Seventeen provinces plus Vientiane Capital. Xam Neua/Sam Neua, Houayxay/Huay Xai, Phonsavan/Muang Phonsavan and Xayaboury/Sayaboury are naming variants. The `N` ranking uses settlement-level GeoNames estimates of differing years; Ban Khoan is a particularly uncertain population record. Laos's 2026 subdistrict reform does not change this first-level structure.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://investlaos.gov.la\&sz=32)

Investment Promotion and Management Committee+2



LV — Thirty-five municipalities and seven separately administered state cities, totalling 42 units following the July 2025 absorption of Varakļāni into Madona. Augšdaugava and the rural Jelgava, Rēzekne and Ventspils municipalities are distinguished from their namesake cities.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://likumi.lv\&sz=32)

LIKUMI.LV+1



LB — Nine governorates. Keserwan-Jbeil is also written Kesrouan-Jbeil; Beqaa/Bekaa, Zahle/Zahlé, Sidon/Saida and Tyre/Sour are common variants. No recent comprehensive national census supports a fully comparable top-ten settlement ranking, particularly across Greater Beirut.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.downloadexcelfiles.com\&sz=32)

Capital



LS — Ten districts. Butha-Buthe/Botha-Bothe, Hlotse/Leribe and Quthing/Moyeni are common alternative names. Maputsoe is the largest additional town in Leribe District. The ten `N` entries follow the published urban-centre ranking.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.bos.gov.ls\&sz=32)

bos.gov.ls



LR — Fifteen counties. Bensonville is the Montserrado county seat, while Monrovia and Paynesville are the principal urban centres. Cestos City is also called River Cess, and Ganta is also called Gompa. Paynesville and Monrovia overlap in metropolitan-area statistics but are represented separately as municipalities.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://insightsliberia.com\&sz=32)

Insights Liberia+1



LY — Twenty-two districts under the commonly used administrative-boundary classification. Al Bayda/Beida, Zawiya/Az Zawiyah, Ajdabiya/Ajdabiyah and Sabha/Sebha are variants. City rankings rely on estimates because Libya lacks a recent comprehensive census; district and municipality hierarchies can differ between data providers.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.gov.uk\&sz=32)

GOV.UK



LI — Eleven municipalities (Gemeinden). Vaduz is the national capital, while Schaan is the most populous municipality. Planken is excluded from the ten `N` flags because it is the smallest municipality by population.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://stateintegrity.org.uk\&sz=32)

State Integrity



LT — Ten counties (apskritys), used as geographic and statistical first-level units; their governing administrations were abolished in 2010. The ten `N` entries use city-proper populations. Vilnius/Vilna, Kaunas/Kovno and Klaipėda/Memel have historic alternative names.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.worldometers.info\&sz=32)

Worldometer



LU — Twelve cantons used as first-level geographic units; municipalities are the functioning local-government level. The ten `N` entries use January 2026 municipality populations, which can include surrounding villages rather than only the named settlement.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://statistiques.public.lu\&sz=32)

Luxembourg+2



MO — Macau has no conventional first-level provinces. Seven historical parishes and Cotai are included as geographic coverage proxies, not separate governing districts. Macau/Macao is one continuous city, so it has only one `N` flag. The territory is also represented within China's provincial-level structure under `CN`.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.eastasianjournal.com\&sz=32)

East Asian Journal



Points still open:

- KI: Validate the exact settlement coordinates for the most remote island councils, particularly Makin, Tamana, Beru and Teraina. Check whether Kanton requires a separate non-commercial coverage record.
- KW: Reconcile the June 2026 residential-locality ranking with grouped census urban areas. Confirm Jaber Al Ahmad City's governorate assignment against Overture's administrative polygons.
- KG: Check whether Overture and historical business records use Manas or Jalal-Abad for the renamed city; retain the older name as an alias.
- LA: Verify Ban Khoan's reported population and mapping identity. A consistent 2015 census ranking differs from the GeoNames-based ten-city list.
- LV: Ensure Varakļāni is no longer treated as a separate municipality. Keep separately administered state cities distinct from adjacent municipalities.
- LB: Obtain a consistent locality-level ranking if strict population ordering is required; Habbouch, Arsal and other settlements have incompatible estimates.
- LS: Confirm that Hlotse and Maputsoe are treated as separate towns within Leribe District.
- LR: Avoid double-counting Greater Monrovia businesses under Monrovia and Paynesville. Verify the map labels for Cestos City and Fish Town.
- LY: Validate all 22 district boundaries and population rankings against the particular administrative hierarchy used in the Overture extract.
- LI: Check the municipality versus village-centre boundaries, particularly Gamprin and Schellenberg.
- LT: Confirm that Overture exposes the ten counties rather than only the current municipalities as its highest subnational layer.
- LU: Compare municipality-level and actual locality-level population rankings; Sanem and Pétange contain multiple settlements.
- MO: Confirm whether the extraction should use the seven historical parishes plus Cotai or a single Macau-wide geographic unit. Avoid duplicate extraction under `CN` and `MO`.


---

## Claude Code - 2026-11-08 20:01 UTC - 11_claude.md - attachments: none

# World coverage - every country, every state, its main cities

Context: SiteBlitz finds small businesses (to sell websites to those without one). Its data source is
Overture Maps Places (open data, about 60-90 million places). We are extracting every place of every country
into files organised country -> state -> city. To check that no state or major city is missing, we need, for
every country in the world (A-Z, ISO 3166-1, 249 entries incl. territories), a reference list of its states
and main cities. We go alphabetically, about 13 countries per message, 19 messages in total.

## Check of the lists so far (businesses within 10 km or with that city name)
Round 1: 263 reference lines, 260 cities, 259 with business data (100 %).
Round 2: 251 reference lines, 251 cities, 250 with business data (100 %).
Round 3: 192 reference lines, 190 cities, 190 with business data (100 %).
Round 4: 221 reference lines, 221 cities, 221 with business data (100 %).
Round 5: 223 reference lines, 223 cities, 219 with business data (98 %).
Round 6: 238 reference lines, 238 cities, 235 with business data (99 %).
Round 7: 160 reference lines, 159 cities, 159 with business data (100 %).
Round 8: 230 reference lines, 229 cities, 229 with business data (100 %).
Round 9: 349 reference lines, 349 cities, 349 with business data (100 %).
Round 10: 238 reference lines, 238 cities, 234 with business data (98 %).

Same format again:


## Message 11 of 19 - countries
Madagascar (MG), Malawi (MW), Malaysia (MY), Maldives (MV), Mali (ML), Malta (MT), Marshall Islands (MH), Martinique (MQ), Mauritania (MR), Mauritius (MU), Mayotte (YT), Mexico (MX), Micronesia (FM)

For EACH country above give:
1. every first-level administrative division (state / province / region / governorate ... as it is today),
   with its capital or largest city (kind S);
2. the 10 largest cities of the country by population (kind N) - fewer if the country has fewer.
   A city can appear as both S and N; list it once with kind SN.
Uninhabited territories: one line `CC|-|-|||none`.

Output ONLY one code block, one line per city, pipe-separated, no header, no commentary inside it:
`CC|state|city|lat|lon|kind`
- CC = ISO code above; state and city in English (the name a map would show); lat / lon with 2 decimals.
After the code block: one line per country with any naming caveat (renamed divisions, disputed areas),
then the list of points still open.


---

## ChatGPT (Extra High) - 2026-11-08 20:11 UTC - saved as 11_chatgpt.md

```
MG|Alaotra-Mangoro|Ambatondrazaka|-17.83|48.43|S
MG|Ambatosoa|Maroantsetra|-15.44|49.74|S
MG|Amoron'i Mania|Ambositra|-20.53|47.25|S
MG|Analamanga|Antananarivo|-18.91|47.54|SN
MG|Analanjirofo|Fenoarivo Atsinanana|-17.38|49.41|S
MG|Androy|Ambovombe-Androy|-25.18|46.08|S
MG|Anosy|Tôlanaro|-25.03|46.99|S
MG|Atsimo-Andrefana|Toliara|-23.35|43.67|SN
MG|Atsimo-Atsinanana|Farafangana|-22.82|47.83|S
MG|Atsinanana|Toamasina|-18.15|49.40|SN
MG|Betsiboka|Maevatanana|-16.95|46.83|S
MG|Boeny|Mahajanga|-15.72|46.32|SN
MG|Bongolava|Tsiroanomandidy|-18.77|46.03|S
MG|Diana|Antsiranana|-12.28|49.29|SN
MG|Fitovinany|Manakara|-22.15|48.02|S
MG|Haute Matsiatra|Fianarantsoa|-21.45|47.08|SN
MG|Ihorombe|Ihosy|-22.40|46.12|S
MG|Itasy|Miarinarivo|-18.96|46.91|S
MG|Melaky|Maintirano|-18.06|44.02|S
MG|Menabe|Morondava|-20.28|44.28|S
MG|Sava|Sambava|-14.27|50.17|SN
MG|Sofia|Antsohihy|-14.88|47.99|S
MG|Vakinankaratra|Antsirabe|-19.87|47.03|SN
MG|Vatovavy|Mananjary|-21.22|48.34|S
MG|Itasy|Imerintsiatosika|-18.98|47.32|N
MG|Sava|Antalaha|-14.90|50.28|N
MW|Central Region|Lilongwe|-13.97|33.79|SN
MW|Northern Region|Mzuzu|-11.46|34.02|SN
MW|Southern Region|Blantyre|-15.79|35.01|SN
MW|Southern Region|Zomba|-15.39|35.32|N
MW|Northern Region|Karonga|-9.93|33.93|N
MW|Central Region|Kasungu|-13.03|33.48|N
MW|Southern Region|Mangochi|-14.48|35.26|N
MW|Central Region|Salima|-13.78|34.46|N
MW|Southern Region|Liwonde|-15.07|35.23|N
MW|Southern Region|Balaka|-14.98|34.96|N
MY|Johor|Johor Bahru|1.49|103.74|SN
MY|Kedah|Alor Setar|6.12|100.37|S
MY|Kelantan|Kota Bharu|6.13|102.24|S
MY|Malacca|Malacca City|2.20|102.25|S
MY|Negeri Sembilan|Seremban|2.73|101.94|S
MY|Pahang|Kuantan|3.81|103.33|S
MY|Penang|George Town|5.42|100.34|SN
MY|Perak|Ipoh|4.60|101.09|S
MY|Perlis|Kangar|6.44|100.20|S
MY|Sabah|Kota Kinabalu|5.98|116.07|S
MY|Sarawak|Kuching|1.55|110.34|S
MY|Selangor|Shah Alam|3.07|101.52|SN
MY|Terengganu|Kuala Terengganu|5.33|103.14|S
MY|Federal Territory of Kuala Lumpur|Kuala Lumpur|3.14|101.69|SN
MY|Federal Territory of Labuan|Victoria|5.28|115.24|S
MY|Federal Territory of Putrajaya|Putrajaya|2.93|101.69|S
MY|Selangor|Kajang|2.99|101.79|N
MY|Penang|Seberang Perai|5.38|100.40|N
MY|Selangor|Subang Jaya|3.04|101.58|N
MY|Selangor|Klang|3.04|101.45|N
MY|Selangor|Petaling Jaya|3.10|101.64|N
MY|Selangor|Selayang|3.25|101.65|N
MV|Haa Alifu|Dhidhdhoo|6.89|73.11|S
MV|Haa Dhaalu|Kulhudhuffushi|6.62|73.07|SN
MV|Shaviyani|Funadhoo|6.15|73.29|S
MV|Noonu|Manadhoo|5.76|73.41|S
MV|Raa|Ungoofaaru|5.67|73.02|S
MV|Baa|Eydhafushi|5.10|73.07|S
MV|Lhaviyani|Naifaru|5.44|73.37|SN
MV|Kaafu|Thulusdhoo|4.37|73.65|S
MV|Alifu Alifu|Rasdhoo|4.26|72.99|S
MV|Alifu Dhaalu|Mahibadhoo|3.76|72.97|S
MV|Vaavu|Felidhoo|3.47|73.55|S
MV|Meemu|Muli|2.92|73.58|S
MV|Faafu|Nilandhoo|3.06|72.89|S
MV|Dhaalu|Kudahuvadhoo|2.67|72.90|S
MV|Thaa|Veymandoo|2.18|73.12|S
MV|Laamu|Fonadhoo|1.83|73.50|S
MV|Gaafu Alifu|Villingili|0.76|73.43|S
MV|Gaafu Dhaalu|Thinadhoo|0.53|73.00|SN
MV|Gnaviyani|Fuvahmulah|-0.30|73.42|SN
MV|Seenu|Hithadhoo|-0.60|73.08|SN
MV|Malé City|Malé|4.18|73.51|SN
MV|Malé City|Hulhumalé|4.21|73.54|N
MV|Malé City|Villimalé|4.17|73.48|N
MV|Laamu|Gan|1.92|73.54|N
MV|Kaafu|Maafushi|3.94|73.49|N
ML|Bamako District|Bamako|12.65|-8.00|SN
ML|Bandiagara|Bandiagara|14.35|-3.61|S
ML|Bougouni|Bougouni|11.41|-7.49|SN
ML|Dioïla|Dioïla|12.49|-6.80|S
ML|Douentza|Douentza|15.01|-2.95|S
ML|Gao|Gao|16.27|-0.05|SN
ML|Kayes|Kayes|14.45|-11.44|SN
ML|Kidal|Kidal|18.46|1.41|S
ML|Kita|Kita|13.04|-9.49|S
ML|Koulikoro|Koulikoro|12.86|-7.56|S
ML|Koutiala|Koutiala|12.39|-5.47|SN
ML|Ménaka|Ménaka|15.92|2.40|S
ML|Mopti|Mopti|14.49|-4.20|SN
ML|Nara|Nara|15.17|-7.29|S
ML|Nioro|Nioro du Sahel|15.23|-9.59|S
ML|San|San|13.30|-4.90|SN
ML|Ségou|Ségou|13.44|-6.26|SN
ML|Sikasso|Sikasso|11.32|-5.67|SN
ML|Taoudenni|Taoudenni|22.68|-3.98|S
ML|Timbuktu|Timbuktu|16.77|-3.01|S
ML|Koulikoro|Kati|12.74|-8.07|N
MT|Eastern Region|Birkirkara|35.90|14.46|SN
MT|Gozo Region|Victoria|36.04|14.24|S
MT|Northern Region|St. Paul's Bay|35.95|14.42|SN
MT|Port Region|Żabbar|35.87|14.54|SN
MT|Southern Region|Qormi|35.88|14.47|SN
MT|Western Region|Żebbuġ|35.87|14.44|S
MT|Northern Region|Mosta|35.91|14.43|N
MT|Eastern Region|Sliema|35.91|14.50|N
MT|Southern Region|Marsaskala|35.86|14.56|N
MT|Northern Region|Naxxar|35.91|14.44|N
MT|Eastern Region|Msida|35.90|14.49|N
MT|Northern Region|San Ġwann|35.91|14.48|N
MH|Ailinglaplap|Airuk|7.28|168.82|S
MH|Ailuk|Ailuk|10.22|169.98|S
MH|Arno|Arno|7.07|171.55|S
MH|Aur|Aur|8.15|171.17|S
MH|Bikini & Kili|Kili|5.64|169.12|S
MH|Ebon|Ebon|4.58|168.70|S
MH|Enewetak & Ujelang|Enewetak|11.35|162.34|S
MH|Jabat|Jabat|7.75|168.98|S
MH|Jaluit|Jabor|5.92|169.64|SN
MH|Kwajalein|Ebeye|8.77|167.74|SN
MH|Lae|Lae|8.92|166.26|S
MH|Lib|Lib|8.31|167.38|S
MH|Likiep|Likiep|9.83|169.31|S
MH|Majuro|Majuro|7.09|171.38|S
MH|Maloelap|Taroa|8.71|171.23|S
MH|Mejit|Mejit|10.28|170.86|S
MH|Mili|Mili|6.08|171.74|S
MH|Namorik|Namdrik|5.60|168.10|S
MH|Namu|Loen|7.76|168.23|S
MH|Rongelap|Rongelap|11.16|166.89|S
MH|Ujae|Ujae|8.93|165.76|S
MH|Utrik|Utrik|11.23|169.85|S
MH|Wotho|Wotho|10.17|166.00|S
MH|Wotje|Wotje|9.45|170.24|SN
MH|Majuro|Delap|7.09|171.38|N
MH|Majuro|Djarrit|7.12|171.36|N
MH|Majuro|Rairok|7.08|171.32|N
MH|Majuro|Uliga|7.11|171.37|N
MH|Majuro|Laura|7.15|171.04|N
MH|Majuro|Ajeltake|7.08|171.17|N
MH|Majuro|Woja|7.10|171.10|N
MQ|Fort-de-France Arrondissement|Fort-de-France|14.61|-61.06|SN
MQ|Le Marin Arrondissement|Le Marin|14.47|-60.87|S
MQ|La Trinité Arrondissement|La Trinité|14.74|-60.96|S
MQ|Saint-Pierre Arrondissement|Saint-Pierre|14.74|-61.18|S
MQ|Fort-de-France Arrondissement|Le Lamentin|14.62|-61.00|N
MQ|La Trinité Arrondissement|Le Robert|14.68|-60.94|N
MQ|Fort-de-France Arrondissement|Schœlcher|14.62|-61.10|N
MQ|Le Marin Arrondissement|Ducos|14.58|-60.97|N
MQ|Fort-de-France Arrondissement|Saint-Joseph|14.67|-61.04|N
MQ|Le Marin Arrondissement|Le François|14.62|-60.90|N
MQ|La Trinité Arrondissement|Sainte-Marie|14.78|-60.99|N
MQ|Le Marin Arrondissement|Rivière-Salée|14.53|-60.98|N
MQ|Le Marin Arrondissement|Rivière-Pilote|14.49|-60.90|N
MR|Adrar|Atar|20.52|-13.05|S
MR|Assaba|Kiffa|16.62|-11.40|SN
MR|Brakna|Aleg|17.06|-13.91|S
MR|Dakhlet Nouadhibou|Nouadhibou|20.93|-17.03|SN
MR|Gorgol|Kaédi|16.15|-13.50|SN
MR|Guidimaka|Sélibaby|15.16|-12.18|SN
MR|Hodh Ech Chargui|Néma|16.62|-7.25|SN
MR|Hodh El Gharbi|Aïoun el Atrous|16.66|-9.61|SN
MR|Inchiri|Akjoujt|19.75|-14.39|S
MR|Nouakchott-Nord|Dar Naim|18.08|-15.96|S
MR|Nouakchott-Ouest|Tevragh Zeina|18.12|-15.98|S
MR|Nouakchott-Sud|Arafat|18.08|-15.95|S
MR|Tagant|Tidjikja|18.56|-11.43|S
MR|Tiris Zemmour|Zouérat|22.74|-12.48|SN
MR|Trarza|Rosso|16.51|-15.81|SN
MR|Nouakchott-Ouest|Nouakchott|18.08|-15.98|N
MR|Assaba|Guerou|16.82|-11.83|N
MU|Agalega|Vingt Cinq|-10.44|56.62|S
MU|Black River|Tamarin|-20.33|57.37|S
MU|Cargados Carajos|Raphael Island|-16.45|59.62|S
MU|Flacq|Centre de Flacq|-20.19|57.71|SN
MU|Grand Port|Mahébourg|-20.41|57.70|S
MU|Moka|Moka|-20.22|57.50|S
MU|Pamplemousses|Triolet|-20.06|57.55|SN
MU|Plaines Wilhems|Beau Bassin-Rose Hill|-20.23|57.47|SN
MU|Port Louis|Port Louis|-20.16|57.50|SN
MU|Rivière du Rempart|Mapou|-20.08|57.60|S
MU|Rodrigues|Port Mathurin|-19.68|63.42|S
MU|Savanne|Souillac|-20.52|57.53|S
MU|Plaines Wilhems|Vacoas-Phoenix|-20.30|57.48|N
MU|Plaines Wilhems|Quatre Bornes|-20.26|57.48|N
MU|Plaines Wilhems|Curepipe|-20.32|57.53|N
MU|Rivière du Rempart|Goodlands|-20.04|57.65|N
MU|Flacq|Bel Air Rivière Sèche|-20.26|57.75|N
MU|Moka|St Pierre|-20.22|57.52|N
YT|Acoua|Acoua|-12.72|45.06|S
YT|Bandraboua|Bandraboua|-12.70|45.12|SN
YT|Bandrélé|Bandrélé|-12.91|45.19|S
YT|Bouéni|Bouéni|-12.90|45.08|S
YT|Chiconi|Chiconi|-12.83|45.11|SN
YT|Chirongui|Chirongui|-12.93|45.15|S
YT|Dembeni|Dembeni|-12.84|45.19|SN
YT|Dzaoudzi|Dzaoudzi|-12.79|45.27|SN
YT|Kani-Kéli|Kani-Kéli|-12.96|45.10|S
YT|Koungou|Koungou|-12.74|45.20|SN
YT|Mamoudzou|Mamoudzou|-12.78|45.23|SN
YT|Mtsamboro|Mtsamboro|-12.68|45.07|S
YT|M'Tsangamouji|M'Tsangamouji|-12.76|45.08|SN
YT|Ouangani|Ouangani|-12.83|45.14|SN
YT|Pamandzi|Pamandzi|-12.80|45.28|S
YT|Sada|Sada|-12.85|45.10|SN
YT|Tsingoni|Tsingoni|-12.79|45.10|SN
MX|Aguascalientes|Aguascalientes|21.88|-102.30|S
MX|Baja California|Mexicali|32.62|-115.45|S
MX|Baja California Sur|La Paz|24.14|-110.31|S
MX|Campeche|Campeche|19.85|-90.52|S
MX|Chiapas|Tuxtla Gutiérrez|16.75|-93.12|S
MX|Chihuahua|Chihuahua City|28.63|-106.07|S
MX|Coahuila|Saltillo|25.43|-100.99|S
MX|Colima|Colima|19.24|-103.72|S
MX|Durango|Durango|24.03|-104.65|S
MX|Guanajuato|Guanajuato|21.02|-101.26|S
MX|Guerrero|Chilpancingo|17.55|-99.50|S
MX|Hidalgo|Pachuca|20.12|-98.73|S
MX|Jalisco|Guadalajara|20.67|-103.35|SN
MX|Mexico City|Mexico City|19.43|-99.13|SN
MX|Mexico State|Toluca|19.29|-99.65|S
MX|Michoacán|Morelia|19.70|-101.19|S
MX|Morelos|Cuernavaca|18.92|-99.23|S
MX|Nayarit|Tepic|21.50|-104.89|S
MX|Nuevo León|Monterrey|25.68|-100.31|SN
MX|Oaxaca|Oaxaca City|17.06|-96.72|S
MX|Puebla|Puebla|19.04|-98.20|SN
MX|Querétaro|Querétaro|20.59|-100.39|S
MX|Quintana Roo|Chetumal|18.51|-88.31|S
MX|San Luis Potosí|San Luis Potosí|22.16|-100.99|S
MX|Sinaloa|Culiacán|24.80|-107.39|S
MX|Sonora|Hermosillo|29.07|-110.96|S
MX|Tabasco|Villahermosa|17.99|-92.93|S
MX|Tamaulipas|Ciudad Victoria|23.74|-99.15|S
MX|Tlaxcala|Tlaxcala|19.32|-98.24|S
MX|Veracruz|Xalapa|19.54|-96.91|S
MX|Yucatán|Mérida|20.97|-89.62|S
MX|Zacatecas|Zacatecas|22.77|-102.57|S
MX|Baja California|Tijuana|32.53|-117.04|N
MX|Mexico State|Ecatepec de Morelos|19.60|-99.05|N
MX|Guanajuato|León|21.12|-101.68|N
MX|Chihuahua|Ciudad Juárez|31.74|-106.49|N
MX|Jalisco|Zapopan|20.72|-103.39|N
MX|Mexico State|Ciudad Nezahualcóyotl|19.40|-99.02|N
FM|Chuuk|Weno|7.45|151.84|SN
FM|Kosrae|Tofol|5.32|163.01|SN
FM|Pohnpei|Kolonia|6.96|158.21|SN
FM|Yap|Colonia|9.52|138.12|SN
FM|Pohnpei|Palikir|6.92|158.16|N
FM|Pohnpei|Kitti|6.83|158.26|N
FM|Pohnpei|Nett|6.96|158.25|N
FM|Chuuk|Tol|7.32|151.62|N
FM|Pohnpei|Madolenihmw|6.86|158.33|N
FM|Chuuk|Tonoas|7.38|151.89|N
```

### Naming caveats

MG — 24 regions, including Ambatosoa established in 2025. Fitovinany and Vatovavy are separate regions. Tôlanaro is also called Fort-Dauphin; Haute Matsiatra is also Matsiatra Ambony.

MW — Three regions are used as first-level divisions; Malawi's 28 districts are subordinate administrative units.

MY — 13 states and three federal territories. Victoria is also Bandar Labuan; Malacca is also Melaka. Population rankings use local-authority areas, so Seberang Perai and Selayang represent larger municipal jurisdictions.

MV — 20 administrative atolls plus Malé City. Seenu is also Addu Atoll; Villingili is also Viligili; Villimalé is part of Malé and differs from Villingili in Gaafu Alifu. Gan is in Laamu Atoll.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://statisticsmaldives.gov.mv\&sz=32)

statisticsmaldives.gov.mv+1



ML — 19 regions plus Bamako District, reflecting the expanded regional structure. Timbuktu is also Tombouctou; Taoudenni is also Taoudénit.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://en.wikipedia.org\&sz=32)

Wikipedia



MT — Six local-government regions, distinct from Malta's six statistical districts. Victoria is also Rabat (Gozo); Żebbuġ here refers to the locality on Malta rather than Gozo.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://address.gov.mt\&sz=32)

Office of the Address Registrar+1



MH — 24 municipalities, with Bikini & Kili and Enewetak & Ujelang counted jointly. Rongelap and Bikini atolls had zero residents in the 2021 census. The ten N entries follow individual-settlement populations, rather than treating Majuro and its component neighborhoods as separate population aggregates.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.thefactbook.org\&sz=32)

The Factbook+2



MQ — Martinique is one French territorial collectivity; its four arrondissements are used for geographic subdivision. Schœlcher is also written Schoelcher.

MR — 15 wilayas, including the three Nouakchott divisions. Nouakchott itself spans Nouakchott-Nord, Nouakchott-Ouest and Nouakchott-Sud; the city point is assigned to Ouest as a reference.

MU — Nine geographic districts plus Rodrigues, Agalega and Cargados Carajos dependencies. The geographic districts are retained for mapping although they no longer function as administrative entities. Cargados Carajos is also Saint Brandon; Raphael Island is a small settlement.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://statsmauritius.govmu.org\&sz=32)

statsmauritius.govmu.org+1



YT — Mayotte has 17 communes directly below its single French departmental/territorial level. The top ten are ranked by commune population, not by separately defined built-up urban areas.

MX — 31 states plus Mexico City, which is a separate federal entity. Mexico State means Estado de México, not Mexico City. The top ten use individual-city populations rather than metropolitan areas.

FM — Four states. Kolonia in Pohnpei and Colonia in Yap are different towns; Palikir is the national capital. The population selections mix town centers and populous island municipalities because settlement-level classifications differ.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://wm-site-staging.cloudflare-47b.workers.dev\&sz=32)

Worldometer+1



### Points still open

- Confirm consistent population-boundary rules where cities and municipalities differ, particularly MY, MV, MH and FM.
- Verify sparse or seasonal settlement coverage in MH's Rongelap municipality and MU's Cargados Carajos dependency.
- Reconcile city aliases and municipality names against Overture's actual place labels, especially MY's Seberang Perai, MV's Villingili/Villimalé and FM's island municipalities.
- Validate each point against the extracted business files; the 260 reference rows above are geographic targets, not a claim that business coverage has been checked.


---

## Claude Code - 2026-11-08 20:12 UTC - 12_claude.md - attachments: none

## Check of your message-11 list
Round 11: 260 reference lines, 260 cities, 253 with business data (97 %).
Not covered: - FM: 9/10 cities covered, 498 businesses near them; no data at: Tol
Not covered: - MH: 28/31 cities covered, 538 businesses near them; no data at: Airuk, Jabat, Lib
Not covered: - MR: 16/17 cities covered, 4,364 businesses near them; no data at: Guerou
Not covered: - MU: 16/18 cities covered, 72,942 businesses near them; no data at: Vingt Cinq, Raphael Island

Same format again:


## Message 12 of 19 - countries
Moldova (MD), Monaco (MC), Mongolia (MN), Montenegro (ME), Montserrat (MS), Morocco (MA), Mozambique (MZ), Myanmar (Burma) (MM), Namibia (NA), Nauru (NR), Nepal (NP), Netherlands (NL), New Caledonia (NC)

For EACH country above give:
1. every first-level administrative division (state / province / region / governorate ... as it is today),
   with its capital or largest city (kind S);
2. the 10 largest cities of the country by population (kind N) - fewer if the country has fewer.
   A city can appear as both S and N; list it once with kind SN.
Uninhabited territories: one line `CC|-|-|||none`.

Output ONLY one code block, one line per city, pipe-separated, no header, no commentary inside it:
`CC|state|city|lat|lon|kind`
- CC = ISO code above; state and city in English (the name a map would show); lat / lon with 2 decimals.
After the code block: one line per country with any naming caveat (renamed divisions, disputed areas),
then the list of points still open.


---

## ChatGPT (Extra High) - 2026-11-08 20:21 UTC - saved as 12_chatgpt.md

```
MD|Anenii Noi|Anenii Noi|46.88|29.22|S
MD|Basarabeasca|Basarabeasca|46.33|28.97|S
MD|Briceni|Briceni|48.36|27.08|S
MD|Cahul|Cahul|45.90|28.19|SN
MD|Cantemir|Cantemir|46.28|28.20|S
MD|Călărași|Călărași|47.25|28.31|S
MD|Căușeni|Căușeni|46.64|29.41|S
MD|Cimișlia|Cimișlia|46.52|28.79|S
MD|Criuleni|Criuleni|47.21|29.16|S
MD|Dondușeni|Dondușeni|48.22|27.58|S
MD|Drochia|Drochia|48.03|27.82|S
MD|Dubăsari|Cocieri|47.30|29.11|S
MD|Edineț|Edineț|48.17|27.31|S
MD|Fălești|Fălești|47.57|27.71|S
MD|Florești|Florești|47.89|28.30|S
MD|Glodeni|Glodeni|47.77|27.51|S
MD|Hîncești|Hîncești|46.83|28.59|S
MD|Ialoveni|Ialoveni|46.94|28.78|S
MD|Leova|Leova|46.48|28.25|S
MD|Nisporeni|Nisporeni|47.08|28.18|S
MD|Ocnița|Ocnița|48.39|27.44|S
MD|Orhei|Orhei|47.38|28.82|SN
MD|Rezina|Rezina|47.74|28.96|S
MD|Rîșcani|Rîșcani|47.95|27.56|S
MD|Sîngerei|Sîngerei|47.64|28.14|S
MD|Soroca|Soroca|48.16|28.30|S
MD|Strășeni|Strășeni|47.14|28.62|S
MD|Șoldănești|Șoldănești|47.82|28.80|S
MD|Ștefan Vodă|Ștefan Vodă|46.51|29.66|S
MD|Taraclia|Taraclia|45.90|28.67|S
MD|Telenești|Telenești|47.50|28.37|S
MD|Ungheni|Ungheni|47.20|27.80|SN
MD|Bălți Municipality|Bălți|47.76|27.93|SN
MD|Bender Municipality|Bender|46.83|29.48|SN
MD|Chișinău Municipality|Chișinău|47.01|28.86|SN
MD|Gagauzia|Comrat|46.30|28.66|S
MD|Transnistria|Tiraspol|46.85|29.63|SN
MD|Transnistria|Rîbnița|47.77|29.00|N
MD|Chișinău Municipality|Durlești|47.01|28.76|N
MD|Transnistria|Dubăsari|47.27|29.16|N
MC|Fontvieille|Fontvieille|43.73|7.42|S
MC|Jardin Exotique|Jardin Exotique|43.73|7.41|S
MC|La Condamine|La Condamine|43.73|7.42|S
MC|La Rousse|La Rousse|43.75|7.43|S
MC|Larvotto|Larvotto|43.75|7.43|S
MC|Les Moneghetti|Les Moneghetti|43.73|7.42|S
MC|Monaco-Ville|Monaco-Ville|43.73|7.42|S
MC|Monte Carlo|Monte Carlo|43.74|7.43|S
MC|Monaco|Monaco|43.73|7.42|N
MN|Arkhangai|Tsetserleg|47.48|101.45|S
MN|Bayankhongor|Bayankhongor|46.19|100.72|SN
MN|Bayan-Ölgii|Ölgii|48.97|89.97|SN
MN|Bulgan|Bulgan|48.81|103.53|S
MN|Darkhan-Uul|Darkhan|49.46|105.92|SN
MN|Dornod|Choibalsan|48.07|114.53|SN
MN|Dornogovi|Sainshand|44.88|110.12|S
MN|Dundgovi|Mandalgovi|45.76|106.27|S
MN|Govi-Altai|Altai|46.37|96.26|S
MN|Govisümber|Choir|46.36|108.36|S
MN|Khentii|Chinggis City|47.32|110.65|S
MN|Khovd|Khovd|48.00|91.64|SN
MN|Khövsgöl|Mörön|49.64|100.16|SN
MN|Orkhon|Erdenet|49.03|104.04|SN
MN|Ömnögovi|Dalanzadgad|43.57|104.42|S
MN|Övörkhangai|Arvaikheer|46.26|102.78|SN
MN|Selenge|Sükhbaatar|50.24|106.21|S
MN|Sükhbaatar|Baruun-Urt|46.68|113.28|S
MN|Töv|Zuunmod|47.70|106.95|S
MN|Ulaanbaatar|Ulaanbaatar|47.92|106.92|SN
MN|Uvs|Ulaangom|49.98|92.07|S
MN|Zavkhan|Uliastai|47.74|96.84|S
MN|Ulaanbaatar|Nalaikh|47.77|107.25|N
ME|Andrijevica|Andrijevica|42.73|19.79|S
ME|Bar|Bar|42.10|19.10|SN
ME|Berane|Berane|42.84|19.87|S
ME|Bijelo Polje|Bijelo Polje|43.04|19.75|SN
ME|Budva|Budva|42.29|18.84|SN
ME|Cetinje|Cetinje|42.39|18.92|SN
ME|Danilovgrad|Danilovgrad|42.55|19.11|S
ME|Gusinje|Gusinje|42.56|19.83|S
ME|Herceg Novi|Herceg Novi|42.45|18.54|S
ME|Kolašin|Kolašin|42.82|19.52|S
ME|Kotor|Kotor|42.42|18.77|S
ME|Mojkovac|Mojkovac|42.96|19.58|S
ME|Nikšić|Nikšić|42.77|18.94|SN
ME|Petnjica|Petnjica|42.91|20.05|S
ME|Plav|Plav|42.60|19.95|S
ME|Pljevlja|Pljevlja|43.36|19.36|SN
ME|Plužine|Plužine|43.15|18.84|S
ME|Podgorica|Podgorica|42.44|19.26|SN
ME|Rožaje|Rožaje|42.84|20.17|SN
ME|Šavnik|Šavnik|42.96|19.09|S
ME|Tivat|Tivat|42.43|18.70|SN
ME|Tuzi|Tuzi|42.37|19.33|S
ME|Ulcinj|Ulcinj|41.93|19.21|SN
ME|Žabljak|Žabljak|43.16|19.13|S
ME|Zeta|Golubovci|42.37|19.22|S
MS|Saint Anthony|Plymouth|16.71|-62.21|S
MS|Saint George|Harris|16.74|-62.17|S
MS|Saint Peter|Brades|16.79|-62.21|SN
MS|Saint Peter|Look Out|16.79|-62.18|N
MS|Saint Peter|Davy Hill|16.79|-62.21|N
MS|Saint Peter|St. John's|16.78|-62.19|N
MS|Saint Peter|St. Peter's|16.77|-62.22|N
MS|Saint Peter|Olveston|16.75|-62.23|N
MS|Saint Peter|Salem|16.75|-62.22|N
MS|Saint Peter|Woodlands|16.76|-62.22|N
MS|Saint Peter|Baker Hill|16.77|-62.20|N
MS|Saint Peter|Barzeys|16.78|-62.18|N
MA|Béni Mellal-Khénifra|Béni Mellal|32.34|-6.36|S
MA|Casablanca-Settat|Casablanca|33.57|-7.59|SN
MA|Dakhla-Oued Ed-Dahab|Dakhla|23.68|-15.96|S
MA|Drâa-Tafilalet|Errachidia|31.93|-4.42|S
MA|Fès-Meknès|Fès|34.06|-4.98|SN
MA|Guelmim-Oued Noun|Guelmim|28.99|-10.06|S
MA|Laâyoune-Sakia El Hamra|Laâyoune|27.15|-13.20|S
MA|Marrakech-Safi|Marrakech|31.63|-8.00|SN
MA|Oriental|Oujda|34.68|-1.91|SN
MA|Rabat-Salé-Kénitra|Rabat|34.02|-6.84|SN
MA|Souss-Massa|Agadir|30.42|-9.60|SN
MA|Tanger-Tétouan-Al Hoceïma|Tangier|35.76|-5.83|SN
MA|Rabat-Salé-Kénitra|Salé|34.05|-6.80|N
MA|Fès-Meknès|Meknès|33.90|-5.55|N
MA|Rabat-Salé-Kénitra|Kénitra|34.26|-6.58|N
MZ|Cabo Delgado|Pemba|-12.97|40.52|SN
MZ|Gaza|Xai-Xai|-25.05|33.64|S
MZ|Inhambane|Inhambane|-23.87|35.38|S
MZ|Manica|Chimoio|-19.12|33.48|SN
MZ|Maputo City|Maputo|-25.97|32.58|SN
MZ|Maputo Province|Matola|-25.96|32.46|SN
MZ|Nampula|Nampula|-15.12|39.27|SN
MZ|Niassa|Lichinga|-13.31|35.24|SN
MZ|Sofala|Beira|-19.84|34.84|SN
MZ|Tete|Tete|-16.16|33.59|SN
MZ|Zambézia|Quelimane|-17.88|36.89|SN
MZ|Nampula|Nacala|-14.56|40.69|N
MM|Ayeyarwady Region|Pathein|16.78|94.73|SN
MM|Bago Region|Bago|17.34|96.48|SN
MM|Chin State|Hakha|22.65|93.60|S
MM|Kachin State|Myitkyina|25.38|97.40|SN
MM|Kayah State|Loikaw|19.68|97.21|S
MM|Kayin State|Hpa-An|16.89|97.63|S
MM|Magway Region|Magway|20.15|94.94|S
MM|Mandalay Region|Mandalay|21.98|96.09|SN
MM|Mon State|Mawlamyine|16.49|97.62|SN
MM|Naypyidaw Union Territory|Naypyidaw|19.76|96.08|SN
MM|Rakhine State|Sittwe|20.15|92.90|S
MM|Sagaing Region|Sagaing|21.88|95.98|S
MM|Shan State|Taunggyi|20.79|97.04|SN
MM|Tanintharyi Region|Dawei|14.08|98.20|S
MM|Yangon Region|Yangon|16.84|96.17|SN
MM|Sagaing Region|Kalay|23.19|94.05|N
MM|Mandalay Region|Pyin Oo Lwin|22.04|96.47|N
NA|Erongo|Swakopmund|-22.68|14.53|SN
NA|Hardap|Mariental|-24.63|17.96|S
NA|ǁKaras|Keetmanshoop|-26.57|18.13|S
NA|Kavango East|Rundu|-17.93|19.77|SN
NA|Kavango West|Nkurenkuru|-17.62|18.62|S
NA|Khomas|Windhoek|-22.56|17.08|SN
NA|Kunene|Opuwo|-18.06|13.84|S
NA|Ohangwena|Eenhana|-17.47|16.33|S
NA|Omaheke|Gobabis|-22.45|18.97|S
NA|Omusati|Outapi|-17.51|14.98|S
NA|Oshana|Oshakati|-17.79|15.70|SN
NA|Oshikoto|Omuthiya|-18.36|16.58|S
NA|Otjozondjupa|Otjiwarongo|-20.46|16.65|SN
NA|Zambezi|Katima Mulilo|-17.50|24.27|SN
NA|Erongo|Walvis Bay|-22.96|14.51|N
NA|Otjozondjupa|Okahandja|-21.98|16.91|N
NA|Hardap|Rehoboth|-23.32|17.09|N
NA|Oshikoto|Tsumeb|-19.24|17.71|N
NR|Aiwo|Aiwo|-0.53|166.91|SN
NR|Anabar|Anabar|-0.51|166.95|SN
NR|Anetan|Anetan|-0.50|166.94|SN
NR|Anibare|Anibare|-0.53|166.95|S
NR|Baitsi|Baitsi|-0.51|166.93|S
NR|Boe|Boe|-0.54|166.91|SN
NR|Buada|Buada|-0.54|166.93|SN
NR|Denigomodu|Denigomodu|-0.52|166.91|S
NR|Ewa|Ewa|-0.51|166.94|SN
NR|Ijuw|Ijuw|-0.52|166.95|S
NR|Meneng|Meneng|-0.54|166.95|SN
NR|Nibok|Nibok|-0.52|166.92|SN
NR|Uaboe|Uaboe|-0.51|166.92|S
NR|Yaren|Yaren|-0.55|166.92|SN
NR|Denigomodu|Location|-0.52|166.91|N
NP|Bagmati|Hetauda|27.43|85.03|S
NP|Gandaki|Pokhara|28.21|83.99|SN
NP|Karnali|Birendranagar|28.60|81.63|S
NP|Koshi|Biratnagar|26.45|87.27|SN
NP|Lumbini|Deukhuri|27.85|82.72|S
NP|Madhesh|Janakpur|26.73|85.93|SN
NP|Sudurpashchim|Godawari|28.83|80.56|S
NP|Bagmati|Kathmandu|27.72|85.32|N
NP|Bagmati|Bharatpur|27.68|84.43|N
NP|Bagmati|Lalitpur|27.66|85.32|N
NP|Madhesh|Birgunj|27.01|84.88|N
NP|Lumbini|Ghorahi|28.03|82.50|N
NP|Sudurpashchim|Dhangadhi|28.70|80.60|N
NP|Koshi|Itahari|26.67|87.27|N
NL|Drenthe|Assen|53.00|6.56|S
NL|Flevoland|Lelystad|52.51|5.47|S
NL|Friesland|Leeuwarden|53.20|5.80|S
NL|Gelderland|Arnhem|51.98|5.91|S
NL|Groningen|Groningen|53.22|6.57|SN
NL|Limburg|Maastricht|50.85|5.69|S
NL|North Brabant|'s-Hertogenbosch|51.69|5.30|S
NL|North Holland|Haarlem|52.39|4.65|S
NL|Overijssel|Zwolle|52.52|6.09|S
NL|South Holland|The Hague|52.08|4.30|SN
NL|Utrecht|Utrecht|52.09|5.12|SN
NL|Zeeland|Middelburg|51.50|3.61|S
NL|Bonaire|Kralendijk|12.15|-68.27|S
NL|Saba|The Bottom|17.63|-63.25|S
NL|Sint Eustatius|Oranjestad|17.49|-62.98|S
NL|North Holland|Amsterdam|52.37|4.90|N
NL|South Holland|Rotterdam|51.92|4.48|N
NL|North Brabant|Eindhoven|51.44|5.48|N
NL|Flevoland|Almere|52.37|5.22|N
NL|North Brabant|Tilburg|51.56|5.09|N
NL|North Brabant|Breda|51.59|4.78|N
NL|Gelderland|Nijmegen|51.84|5.87|N
NC|Loyalty Islands|Wé|-20.92|167.28|S
NC|North Province|Koné|-21.06|164.86|SN
NC|South Province|Nouméa|-22.28|166.46|SN
NC|South Province|Dumbéa|-22.15|166.46|N
NC|South Province|Païta|-22.13|166.37|N
NC|South Province|Le Mont-Dore|-22.28|166.58|N
NC|South Province|Bourail|-21.57|165.50|N
NC|North Province|Poindimié|-20.93|165.33|N
NC|North Province|Koumac|-20.56|164.29|N
NC|North Province|Canala|-21.53|165.96|N
NC|North Province|Houaïlou|-21.29|165.62|N
```

### Naming caveats

MD — 32 districts, three municipalities, Gagauzia and Transnistria. Transnistria is internationally recognized as part of Moldova but administered separately; Bender and Tiraspol have overlapping territorial-status considerations. A proposed administrative reform has not been applied to this list.

MC — Monaco is one municipality, not eight municipalities. The eight named quartiers are included as geographic subdivisions for coverage checking; the only city-level N entry is Monaco.

MN — 21 aimags plus the independently administered capital Ulaanbaatar. Chinggis City was formerly Öndörkhaan; Nalaikh is administratively part of Ulaanbaatar.

ME — 25 municipalities, including Zeta and Tuzi. Golubovci is the administrative centre of Zeta; Cetinje is the historic royal capital.

MS — Three historic parishes. Saint Anthony and Saint George are largely uninhabited volcanic exclusion areas. Plymouth remains the official capital but is abandoned; Brades is the functioning administrative centre.

MA — 12 regions. Dakhla-Oued Ed-Dahab and Laâyoune-Sakia El Hamra include territory within disputed Western Sahara. Tangier is also Tanger, and Fès is also Fez.

MZ — Ten provinces plus Maputo City as a separate provincial-level entity. Matola is the capital of Maputo Province; Maputo City is not part of that province.

MM — Seven states, seven regions and Naypyidaw Union Territory. Myanmar is also called Burma; Yangon is Rangoon, Ayeyarwady is Irrawaddy, and Kayin is Karen. Recent census coverage is affected by conflict.

NA — 14 regions. Zambezi was formerly Caprivi; ǁKaras was formerly Karas. Some data sources use `//Karas` instead of the click-character spelling.

NR — 14 districts and no conventional cities. District-centre names are used as settlement proxies; Location is a populated settlement within Denigomodu, not a separate district.

NP — Seven provinces. Province No. 1 is now Koshi. Lumbini's designated capital is Deukhuri/Rapti Valley rather than Butwal; Sudurpashchim's designated capital is Godawari, while provincial offices have continued operating in Dhangadhi.

NL — 12 European provinces plus Bonaire, Saba and Sint Eustatius, which are Caribbean public bodies rather than provinces. The Hague is Den Haag; 's-Hertogenbosch is Den Bosch. Aruba, Curaçao and Sint Maarten have separate ISO codes.

NC — Three provinces. Wé is on Lifou in the Loyalty Islands; Nouméa is the territorial capital. The N entries represent urban settlements rather than ranking all geographically extensive rural and island communes by total population.

### Points still open

- Round 11 unresolved: FM — Tol; MH — Airuk, Jabat, Lib; MR — Guerou; MU — Vingt Cinq, Raphael Island.
- Round 12 coverage: 233 reference rows prepared; Overture business-data coverage has not yet been checked.
- Sparse or unusual settlements: Check Montserrat's abandoned southern settlements, Nauru's Location, Monaco's quartiers, and the Netherlands' Caribbean public bodies separately from ordinary city records.
- Population-definition differences: Verify municipality-versus-urban-settlement rankings for Moldova, Mongolia, Nepal and New Caledonia against the chosen population dataset.


---

## Claude Code - 2026-11-08 20:21 UTC - 13_claude.md - attachments: none

## Check of your message-12 list
Round 12: 233 reference lines, 233 cities, 231 with business data (99 %).
Not covered: - NL: 20/22 cities covered, 537,748 businesses near them; no data at: The Bottom, Oranjestad

Same format again:


## Message 13 of 19 - countries
New Zealand (NZ), Nicaragua (NI), Niger (NE), Nigeria (NG), Niue (NU), Norfolk Island (NF), North Korea (KP), North Macedonia (MK), Northern Mariana Islands (MP), Norway (NO), Oman (OM), Pakistan (PK), Palau (PW)

For EACH country above give:
1. every first-level administrative division (state / province / region / governorate ... as it is today),
   with its capital or largest city (kind S);
2. the 10 largest cities of the country by population (kind N) - fewer if the country has fewer.
   A city can appear as both S and N; list it once with kind SN.
Uninhabited territories: one line `CC|-|-|||none`.

Output ONLY one code block, one line per city, pipe-separated, no header, no commentary inside it:
`CC|state|city|lat|lon|kind`
- CC = ISO code above; state and city in English (the name a map would show); lat / lon with 2 decimals.
After the code block: one line per country with any naming caveat (renamed divisions, disputed areas),
then the list of points still open.


---

## ChatGPT (Extra High) - 2026-11-08 20:29 UTC - saved as 13_chatgpt.md

```
NZ|Auckland|Auckland|-36.85|174.76|SN
NZ|Bay of Plenty|Tauranga|-37.69|176.17|SN
NZ|Canterbury|Christchurch|-43.53|172.64|SN
NZ|Chatham Islands|Waitangi|-43.95|-176.56|S
NZ|Gisborne|Gisborne|-38.66|178.02|S
NZ|Hawke's Bay|Napier|-39.49|176.91|SN
NZ|Manawatū-Whanganui|Palmerston North|-40.35|175.61|SN
NZ|Marlborough|Blenheim|-41.51|173.96|S
NZ|Nelson|Nelson|-41.27|173.28|S
NZ|Northland|Whangārei|-35.73|174.32|S
NZ|Otago|Dunedin|-45.87|170.50|SN
NZ|Southland|Invercargill|-46.41|168.35|S
NZ|Taranaki|New Plymouth|-39.06|174.08|SN
NZ|Tasman|Richmond|-41.34|173.18|S
NZ|Waikato|Hamilton|-37.78|175.28|SN
NZ|Wellington|Wellington|-41.29|174.78|SN
NZ|West Coast|Greymouth|-42.45|171.21|S
NZ|Wellington|Lower Hutt|-41.21|174.91|N
NI|Boaco|Boaco|12.47|-85.66|S
NI|Carazo|Jinotepe|11.85|-86.20|S
NI|Chinandega|Chinandega|12.63|-87.13|SN
NI|Chontales|Juigalpa|12.09|-85.37|S
NI|Estelí|Estelí|13.09|-86.35|SN
NI|Granada|Granada|11.93|-85.96|SN
NI|Jinotega|Jinotega|13.09|-86.00|S
NI|León|León|12.44|-86.88|SN
NI|Madriz|Somoto|13.48|-86.58|S
NI|Managua|Managua|12.13|-86.25|SN
NI|Masaya|Masaya|11.97|-86.10|SN
NI|Matagalpa|Matagalpa|12.93|-85.92|SN
NI|Nueva Segovia|Ocotal|13.63|-86.48|S
NI|Rivas|Rivas|11.44|-85.83|S
NI|Río San Juan|San Carlos|11.12|-84.78|S
NI|North Caribbean Coast|Bilwi|14.03|-83.39|SN
NI|South Caribbean Coast|Bluefields|12.01|-83.76|S
NI|Managua|Tipitapa|12.20|-86.10|N
NI|Managua|Ciudad Sandino|12.16|-86.34|N
NE|Agadez|Agadez|16.97|7.99|SN
NE|Diffa|Diffa|13.32|12.61|S
NE|Dosso|Dosso|13.05|3.19|SN
NE|Maradi|Maradi|13.50|7.10|SN
NE|Niamey|Niamey|13.52|2.12|SN
NE|Tahoua|Tahoua|14.89|5.27|SN
NE|Tillabéri|Tillabéri|14.21|1.45|S
NE|Zinder|Zinder|13.80|8.99|SN
NE|Agadez|Arlit|18.73|7.39|N
NE|Tahoua|Birni N'Konni|13.80|5.25|N
NE|Dosso|Gaya|11.89|3.45|N
NE|Maradi|Tessaoua|13.75|7.99|N
NG|Abia|Umuahia|5.53|7.49|S
NG|Adamawa|Yola|9.21|12.48|S
NG|Akwa Ibom|Uyo|5.04|7.93|SN
NG|Anambra|Awka|6.21|7.07|S
NG|Bauchi|Bauchi|10.32|9.84|S
NG|Bayelsa|Yenagoa|4.92|6.27|S
NG|Benue|Makurdi|7.74|8.52|S
NG|Borno|Maiduguri|11.83|13.15|S
NG|Cross River|Calabar|4.95|8.33|S
NG|Delta|Asaba|6.20|6.73|S
NG|Ebonyi|Abakaliki|6.32|8.11|S
NG|Edo|Benin City|6.34|5.63|SN
NG|Ekiti|Ado Ekiti|7.62|5.22|S
NG|Enugu|Enugu|6.44|7.51|S
NG|Federal Capital Territory|Abuja|9.06|7.49|S
NG|Gombe|Gombe|10.29|11.17|S
NG|Imo|Owerri|5.49|7.03|SN
NG|Jigawa|Dutse|11.76|9.34|S
NG|Kaduna|Kaduna|10.52|7.44|SN
NG|Kano|Kano|12.00|8.52|SN
NG|Katsina|Katsina|12.99|7.60|S
NG|Kebbi|Birnin Kebbi|12.45|4.20|S
NG|Kogi|Lokoja|7.80|6.74|S
NG|Kwara|Ilorin|8.50|4.55|S
NG|Lagos|Ikeja|6.60|3.34|S
NG|Nasarawa|Lafia|8.49|8.52|S
NG|Niger|Minna|9.62|6.55|S
NG|Ogun|Abeokuta|7.15|3.35|S
NG|Ondo|Akure|7.26|5.20|S
NG|Osun|Osogbo|7.77|4.56|S
NG|Oyo|Ibadan|7.39|3.90|SN
NG|Plateau|Jos|9.93|8.89|S
NG|Rivers|Port Harcourt|4.82|7.05|SN
NG|Sokoto|Sokoto|13.06|5.24|S
NG|Taraba|Jalingo|8.90|11.36|S
NG|Yobe|Damaturu|11.75|11.96|S
NG|Zamfara|Gusau|12.16|6.66|S
NG|Lagos|Lagos|6.45|3.39|N
NG|Anambra|Onitsha|6.15|6.79|N
NG|Delta|Warri|5.52|5.75|N
NU|Alofi North|Alofi|-19.04|-169.92|SN
NU|Alofi South|Alofi|-19.06|-169.92|SN
NU|Avatele|Avatele|-19.12|-169.91|SN
NU|Hakupu|Hakupu|-19.13|-169.85|SN
NU|Hikutavake|Hikutavake|-18.96|-169.88|S
NU|Lakepa|Lakepa|-19.01|-169.80|SN
NU|Liku|Liku|-19.05|-169.79|SN
NU|Makefu|Makefu|-19.00|-169.91|S
NU|Mutalau|Mutalau|-18.96|-169.83|SN
NU|Namukulu|Namukulu|-18.98|-169.88|S
NU|Tamakautoga|Tamakautoga|-19.10|-169.92|SN
NU|Toi|Toi|-18.97|-169.85|S
NU|Tuapa|Tuapa|-18.99|-169.90|SN
NU|Vaiea|Vaiea|-19.13|-169.88|SN
NF|Norfolk Island|Kingston|-29.05|167.97|SN
NF|Norfolk Island|Burnt Pine|-29.03|167.95|N
KP|Chagang|Kanggye|40.97|126.59|S
KP|Kangwon|Wonsan|39.15|127.44|SN
KP|North Hamgyong|Chongjin|41.80|129.78|SN
KP|North Hwanghae|Sariwon|38.51|125.75|SN
KP|North Pyongan|Sinuiju|40.10|124.40|SN
KP|Ryanggang|Hyesan|41.40|128.18|S
KP|South Hamgyong|Hamhung|39.92|127.54|SN
KP|South Hwanghae|Haeju|38.04|125.71|S
KP|South Pyongan|Pyongsong|39.25|125.87|S
KP|Pyongyang|Pyongyang|39.03|125.75|SN
KP|Nampo|Nampo|38.74|125.41|SN
KP|Kaesong|Kaesong|37.97|126.55|SN
KP|Rason|Rason|42.34|130.39|S
KP|South Hamgyong|Tanchon|40.46|128.91|N
KP|South Pyongan|Kaechon|39.70|125.91|N
MK|Aerodrom|Aerodrom|41.99|21.47|S
MK|Aračinovo|Aračinovo|42.02|21.56|S
MK|Berovo|Berovo|41.71|22.86|S
MK|Bitola|Bitola|41.03|21.34|SN
MK|Bogdanci|Bogdanci|41.20|22.58|S
MK|Bogovinje|Bogovinje|41.92|20.92|S
MK|Bosilovo|Bosilovo|41.44|22.73|S
MK|Brvenica|Brvenica|41.97|20.98|S
MK|Butel|Butel|42.02|21.45|S
MK|Centar|Skopje|42.00|21.43|SN
MK|Centar Župa|Centar Župa|41.48|20.56|S
MK|Čair|Čair|42.02|21.44|S
MK|Čaška|Čaška|41.65|21.69|S
MK|Češinovo-Obleševo|Obleševo|41.90|22.33|S
MK|Čučer-Sandevo|Čučer-Sandevo|42.10|21.39|S
MK|Debar|Debar|41.53|20.53|S
MK|Debarca|Belčišta|41.35|20.82|S
MK|Delčevo|Delčevo|41.97|22.77|S
MK|Demir Hisar|Demir Hisar|41.22|21.20|S
MK|Demir Kapija|Demir Kapija|41.41|22.24|S
MK|Dojran|Star Dojran|41.18|22.72|S
MK|Dolneni|Dolneni|41.43|21.45|S
MK|Gazi Baba|Gazi Baba|42.01|21.50|S
MK|Gevgelija|Gevgelija|41.14|22.50|S
MK|Gjorče Petrov|Gjorče Petrov|42.01|21.35|S
MK|Gostivar|Gostivar|41.80|20.91|SN
MK|Gradsko|Gradsko|41.57|21.95|S
MK|Ilinden|Ilinden|41.99|21.58|S
MK|Jegunovce|Jegunovce|42.07|21.12|S
MK|Karbinci|Karbinci|41.82|22.21|S
MK|Karpoš|Karpoš|42.00|21.39|S
MK|Kavadarci|Kavadarci|41.43|22.01|S
MK|Kičevo|Kičevo|41.51|20.96|S
MK|Kisela Voda|Kisela Voda|41.95|21.50|S
MK|Kočani|Kočani|41.92|22.41|S
MK|Konče|Konče|41.49|22.38|S
MK|Kratovo|Kratovo|42.08|22.18|S
MK|Kriva Palanka|Kriva Palanka|42.20|22.33|S
MK|Krivogaštani|Krivogaštani|41.34|21.35|S
MK|Kruševo|Kruševo|41.37|21.25|S
MK|Kumanovo|Kumanovo|42.13|21.71|SN
MK|Lipkovo|Lipkovo|42.16|21.59|S
MK|Lozovo|Lozovo|41.79|21.90|S
MK|Makedonska Kamenica|Makedonska Kamenica|42.02|22.59|S
MK|Makedonski Brod|Makedonski Brod|41.51|21.22|S
MK|Mavrovo and Rostuša|Rostuša|41.61|20.60|S
MK|Mogila|Mogila|41.11|21.38|S
MK|Negotino|Negotino|41.48|22.09|S
MK|Novaci|Novaci|41.04|21.45|S
MK|Novo Selo|Novo Selo|41.41|22.88|S
MK|Ohrid|Ohrid|41.12|20.80|SN
MK|Pehčevo|Pehčevo|41.76|22.89|S
MK|Petrovec|Petrovec|41.94|21.61|S
MK|Plasnica|Plasnica|41.47|21.12|S
MK|Prilep|Prilep|41.34|21.55|SN
MK|Probištip|Probištip|42.00|22.18|S
MK|Radoviš|Radoviš|41.64|22.46|S
MK|Rankovce|Rankovce|42.17|22.12|S
MK|Resen|Resen|41.09|21.01|S
MK|Rosoman|Rosoman|41.52|21.95|S
MK|Saraj|Saraj|42.00|21.33|S
MK|Sopište|Sopište|41.95|21.43|S
MK|Staro Nagoričane|Staro Nagoričane|42.20|21.83|S
MK|Struga|Struga|41.18|20.68|S
MK|Strumica|Strumica|41.44|22.64|SN
MK|Studeničani|Studeničani|41.92|21.55|S
MK|Sveti Nikole|Sveti Nikole|41.87|21.94|S
MK|Štip|Štip|41.75|22.20|SN
MK|Šuto Orizari|Šuto Orizari|42.04|21.42|S
MK|Tearce|Tearce|42.07|21.05|S
MK|Tetovo|Tetovo|42.01|20.97|SN
MK|Valandovo|Valandovo|41.32|22.56|S
MK|Vasilevo|Vasilevo|41.48|22.64|S
MK|Veles|Veles|41.72|21.78|SN
MK|Vevčani|Vevčani|41.24|20.59|S
MK|Vinica|Vinica|41.88|22.51|S
MK|Vrapčište|Vrapčište|41.84|20.88|S
MK|Zelenikovo|Zelenikovo|41.88|21.59|S
MK|Zrnovci|Zrnovci|41.86|22.45|S
MK|Želino|Želino|41.98|21.05|S
MP|Northern Islands|Agrihan|18.77|145.67|S
MP|Rota|Songsong|14.15|145.14|S
MP|Saipan|Garapan|15.21|145.72|SN
MP|Tinian|San Jose|14.97|145.63|S
MP|Saipan|Kagman|15.18|145.78|N
MP|Saipan|Finasisu|15.16|145.73|N
MP|Saipan|San Antonio|15.15|145.70|N
MP|Saipan|Koblerville|15.15|145.73|N
MP|Saipan|Chalan Kanoa|15.15|145.72|N
MP|Saipan|Dandan|15.16|145.76|N
MP|Saipan|San Jose|15.17|145.74|N
MP|Saipan|Gualo Rai|15.19|145.72|N
MP|Saipan|San Vicente|15.17|145.77|N
NO|Agder|Kristiansand|58.15|7.99|SN
NO|Akershus|Lillestrøm|59.96|11.05|S
NO|Buskerud|Drammen|59.74|10.21|SN
NO|Finnmark|Vadsø|70.07|29.75|S
NO|Innlandet|Hamar|60.79|11.07|S
NO|Møre og Romsdal|Molde|62.74|7.16|S
NO|Nordland|Bodø|67.28|14.40|S
NO|Oslo|Oslo|59.91|10.75|SN
NO|Rogaland|Stavanger|58.97|5.73|SN
NO|Telemark|Skien|59.21|9.61|SN
NO|Troms|Tromsø|69.65|18.96|S
NO|Trøndelag|Steinkjer|64.02|11.50|S
NO|Vestfold|Tønsberg|59.27|10.41|SN
NO|Vestland|Bergen|60.39|5.32|SN
NO|Østfold|Sarpsborg|59.28|11.11|S
NO|Trøndelag|Trondheim|63.43|10.40|N
NO|Østfold|Fredrikstad|59.22|10.93|N
NO|Møre og Romsdal|Ålesund|62.47|6.15|N
OM|Ad Dakhiliyah|Nizwa|22.93|57.53|SN
OM|Ad Dhahirah|Ibri|23.23|56.52|S
OM|Al Batinah North|Sohar|24.35|56.73|SN
OM|Al Batinah South|Rustaq|23.39|57.42|S
OM|Al Buraimi|Al Buraimi|24.25|55.80|SN
OM|Al Wusta|Haima|19.97|56.28|S
OM|Ash Sharqiyah North|Ibra|22.69|58.53|S
OM|Ash Sharqiyah South|Sur|22.57|59.53|SN
OM|Dhofar|Salalah|17.02|54.09|SN
OM|Musandam|Khasab|26.18|56.25|S
OM|Muscat|Muscat|23.61|58.59|S
OM|Muscat|Seeb|23.67|58.19|N
OM|Muscat|Bawshar|23.57|58.42|N
OM|Muscat|Muttrah|23.62|58.56|N
OM|Muscat|Al Amarat|23.51|58.53|N
OM|Ash Sharqiyah South|Ja'alan Bani Bu Ali|22.00|59.34|N
PK|Azad Jammu and Kashmir|Muzaffarabad|34.37|73.47|S
PK|Balochistan|Quetta|30.18|66.98|SN
PK|Gilgit-Baltistan|Gilgit|35.92|74.31|S
PK|Islamabad Capital Territory|Islamabad|33.69|73.06|SN
PK|Khyber Pakhtunkhwa|Peshawar|34.01|71.58|SN
PK|Punjab|Lahore|31.55|74.34|SN
PK|Sindh|Karachi|24.86|67.01|SN
PK|Punjab|Faisalabad|31.42|73.08|N
PK|Punjab|Rawalpindi|33.60|73.05|N
PK|Punjab|Gujranwala|32.16|74.19|N
PK|Punjab|Multan|30.20|71.47|N
PK|Sindh|Hyderabad|25.40|68.37|N
PW|Aimeliik|Ngchemiangel|7.45|134.48|S
PW|Airai|Ngetkib|7.37|134.54|SN
PW|Angaur|Ngaramasch|6.90|134.13|S
PW|Hatohobei|Tobi|3.00|131.12|S
PW|Kayangel|Kayangel|8.08|134.72|S
PW|Koror|Koror|7.34|134.47|SN
PW|Melekeok|Melekeok|7.50|134.64|S
PW|Ngaraard|Ulimang|7.62|134.64|S
PW|Ngarchelong|Mengellang|7.70|134.63|S
PW|Ngardmau|Urdmang|7.61|134.57|S
PW|Ngatpang|Ngereklmadel|7.49|134.49|S
PW|Ngchesar|Ngersuul|7.47|134.61|S
PW|Ngeremlengui|Imeong|7.53|134.53|S
PW|Ngiwal|Ngerkeai|7.55|134.64|S
PW|Peleliu|Kloulklubed|7.04|134.26|SN
PW|Sonsorol|Dongosaru|5.33|132.22|S
PW|Airai|Ngerusar|7.36|134.54|N
PW|Koror|Meyuns|7.35|134.46|N
PW|Ngeremlengui|Bkulangriil|7.52|134.51|N
```

### Naming caveats

NZ — Sixteen regions plus the separately administered Chatham Islands Territory, which lies outside the regional-council system. Whangārei is also Whangarei; Manawatū-Whanganui is also Manawatu-Wanganui. Hibiscus Coast is excluded from the top-ten city ranking because it is treated as an Auckland urban area rather than a separate city.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.stats.govt.nz\&sz=32)

Stats NZ+1



NI — Fifteen departments plus two Caribbean autonomous regions. North Caribbean Coast is RACCN, formerly RAAN; South Caribbean Coast is RACCS, formerly RAAS. Bilwi is also Puerto Cabezas. The top ten follow 2023 national population estimates.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.worldometers.info\&sz=32)

Worldometer



NE — Seven regions plus the Niamey Capital District. Birni N'Konni is also Birni Nkonni; Tillabéri is also Tillabéry. The ten largest use the 2012 city-census baseline, as more recent urban-agglomeration estimates rank some differently.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://en.wikipedia.org\&sz=32)

Wikipedia+1



NG — Thirty-six states plus the Federal Capital Territory. Ikeja is the capital of Lagos State, while Lagos is its largest city. Top-ten N designations follow the UN 2025 urban-area estimates, under which Onitsha and Owerri rank unusually high compared with older city-proper rankings; Abuja is still included as the FCT capital.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://statisticstimes.com\&sz=32)

Statistics Times



NU — Fourteen village council areas. Alofi North and Alofi South share the settlement name Alofi, but are distinct census divisions. Their SN markers and the other village markers use the 2022 census village populations.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://niuestatistics.nu\&sz=32)

Niue Statistics Office



NF — Norfolk Island has no separate first-level provincial system. Kingston is the administrative capital; Burnt Pine is its main commercial settlement. Both are represented under the island-wide local-government area.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://geodatakit.com\&sz=32)

CSV, JSON & GeoJSON · GeoDataKit



KP — Nine provinces plus four directly administered or special cities: Pyongyang, Nampo, Kaesong and Rason. Ryanggang is also Yanggang, Chagang is also Jagang, and Sinuiju is also Sinŭiju. The N ranking uses conventional city populations rather than the newer UN urban-area estimates, which sometimes identify individual urban districts as separate cities.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.thefactbook.org\&sz=32)

The Factbook+1



MK — Eight statistical regions are not the first-level municipal-government units used here. All 80 municipalities are included, including 10 within Greater Skopje; Skopje is represented under central Skopje. Češinovo-Obleševo has its centre at Obleševo, Debarca at Belčišta, Dojran at Star Dojran and Mavrovo and Rostuša at Rostuša.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://assets.publishing.service.gov.uk\&sz=32)

GOV.UK+1



MP — Four municipalities: Saipan, Tinian, Rota and Northern Islands. Tinian and Aguiguan are administered together. The Northern Islands have very few permanent residents; Agrihan is used as the principal populated reference settlement. Saipan's N villages reflect the 2020 census and San Jose appears separately on Saipan and Tinian.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://opd.gov.mp\&sz=32)

INTRODUCTION+1



NO — Fifteen counties following the 2024 splits of Viken, Vestfold og Telemark and Troms og Finnmark. Akershus is represented by Lillestrøm as a major city rather than its county offices in Oslo. Norway's official urban-settlement classification combines Stavanger/Sandnes, Fredrikstad/Sarpsborg and Porsgrunn/Skien; the N choices use identifiable constituent cities.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.ssb.no\&sz=32)

SSB+1



OM — Eleven governorates. Al Batinah and Ash Sharqiyah each have separate North and South governorates. Muscat's urban area covers multiple separately named places, including Seeb, Bawshar and Muttrah; the N markers use the 2020 census settlement ranking.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.fm.gov.om\&sz=32)

fm.gov.om+1



PK — Four provinces, Islamabad Capital Territory, Gilgit-Baltistan and Azad Jammu and Kashmir. The last two are Pakistan-administered territories in the internationally disputed Kashmir region; their status is not equivalent to ordinary provinces. Pakistan's N markers follow the 2023 national census, with Karachi first and Islamabad tenth.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.pbos.gov.pk\&sz=32)

Punjab Board of Secondary Education+1



PW — Sixteen states. Palau's national capital is Ngerulmud in Melekeok State, while Koror is its largest city. Melekeok village is used for the state seat, Ngetkib for Airai, and Ngereklmadel for Ngatpang. Palau has fewer than ten separately ranked built-up settlements in the 2020 census, so N markers are limited accordingly.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.palaugov.pw\&sz=32)

palaugov.pw+2



### Points still open

- Round 11: FM — Tol; MH — Airuk, Jabat, Lib; MR — Guerou; MU — Vingt Cinq, Raphael Island. Seven previously unmatched reference points.
- Round 12: NL — The Bottom (Saba), Oranjestad (Sint Eustatius). Two previously unmatched reference points.
- Round 13: Match all new reference points against Overture business data; coverage is not yet verified.
- Geographic exceptions: Verify sparse island settlements in NU, NF, MP and PW, where village-level data and municipality-level place names may not align.
- Administrative and population definitions: Reconcile North Macedonia's Skopje municipalities, Norway's combined urban settlements, Niger's changing population rankings and Pakistan's disputed administrative territories before treating the reference as a strict validation dataset.


---

## Claude Code - 2026-11-08 20:30 UTC - 14_claude.md - attachments: none

## Check of your message-13 list
Round 13: 278 reference lines, 278 cities, 274 with business data (99 %).
Not covered: - MP: 12/13 cities covered, 9,509 businesses near them; no data at: Agrihan
Not covered: - PW: 16/19 cities covered, 1,803 businesses near them; no data at: Ngaramasch, Tobi, Dongosaru

Same format again:


## Message 14 of 19 - countries
Palestinian Territories (PS), Panama (PA), Papua New Guinea (PG), Paraguay (PY), Peru (PE), Philippines (PH), Pitcairn Islands (PN), Poland (PL), Portugal (PT), Puerto Rico (PR), Qatar (QA), Réunion (RE), Romania (RO)

For EACH country above give:
1. every first-level administrative division (state / province / region / governorate ... as it is today),
   with its capital or largest city (kind S);
2. the 10 largest cities of the country by population (kind N) - fewer if the country has fewer.
   A city can appear as both S and N; list it once with kind SN.
Uninhabited territories: one line `CC|-|-|||none`.

Output ONLY one code block, one line per city, pipe-separated, no header, no commentary inside it:
`CC|state|city|lat|lon|kind`
- CC = ISO code above; state and city in English (the name a map would show); lat / lon with 2 decimals.
After the code block: one line per country with any naming caveat (renamed divisions, disputed areas),
then the list of points still open.


---

## ChatGPT (Extra High) - 2026-11-08 20:42 UTC - saved as 14_chatgpt.md

```
PS|Bethlehem|Bethlehem|31.70|35.20|S
PS|Deir al-Balah|Deir al-Balah|31.42|34.35|SN
PS|Gaza|Gaza|31.50|34.47|SN
PS|Hebron|Hebron|31.53|35.10|SN
PS|Jenin|Jenin|32.46|35.30|S
PS|Jericho|Jericho|31.86|35.46|S
PS|Jerusalem|East Jerusalem|31.78|35.24|SN
PS|Khan Yunis|Khan Yunis|31.35|34.30|SN
PS|Nablus|Nablus|32.22|35.26|SN
PS|North Gaza|Jabalia|31.53|34.48|SN
PS|Qalqilya|Qalqilya|32.19|34.97|S
PS|Rafah|Rafah|31.30|34.25|SN
PS|Ramallah and al-Bireh|Ramallah|31.90|35.20|S
PS|Salfit|Salfit|32.08|35.18|S
PS|Tubas|Tubas|32.32|35.37|S
PS|Tulkarm|Tulkarm|32.31|35.03|S
PS|North Gaza|Beit Lahia|31.55|34.50|N
PS|Deir al-Balah|Nuseirat|31.45|34.39|N
PA|Bocas del Toro|Bocas del Toro|9.34|-82.24|S
PA|Chiriquí|David|8.43|-82.43|SN
PA|Coclé|Penonomé|8.52|-80.36|S
PA|Colón|Colón|9.36|-79.90|SN
PA|Darién|La Palma|8.41|-78.15|S
PA|Herrera|Chitré|7.96|-80.43|SN
PA|Los Santos|Las Tablas|7.77|-80.28|S
PA|Panamá|Panama City|8.98|-79.52|SN
PA|Panamá Oeste|La Chorrera|8.88|-79.78|SN
PA|Veraguas|Santiago de Veraguas|8.10|-80.98|SN
PA|Emberá-Wounaan|Unión Chocó|8.08|-77.54|S
PA|Guna Yala|Gaigirgordub|9.56|-78.95|S
PA|Ngäbe-Buglé|Llano Tugrí|8.48|-81.71|S
PA|Panamá|San Miguelito|9.03|-79.50|N
PA|Panamá Oeste|Arraiján|8.95|-79.65|N
PA|Panamá Oeste|Vista Alegre|8.93|-79.70|N
PA|Bocas del Toro|Changuinola|9.43|-82.52|N
PG|Autonomous Region of Bougainville|Buka|-5.43|154.67|S
PG|Central|Kwikila|-9.81|147.66|S
PG|Chimbu|Kundiawa|-6.02|144.97|S
PG|East New Britain|Kokopo|-4.35|152.26|SN
PG|East Sepik|Wewak|-3.55|143.63|SN
PG|Eastern Highlands|Goroka|-6.08|145.39|SN
PG|Enga|Wabag|-5.49|143.72|S
PG|Gulf|Kerema|-7.97|145.77|S
PG|Hela|Tari|-5.85|142.95|S
PG|Jiwaka|Banz|-5.80|144.61|S
PG|Madang|Madang|-5.22|145.79|SN
PG|Manus|Lorengau|-2.02|147.28|S
PG|Milne Bay|Alotau|-10.31|150.45|S
PG|Morobe|Lae|-6.73|146.99|SN
PG|National Capital District|Port Moresby|-9.44|147.18|SN
PG|New Ireland|Kavieng|-2.57|150.80|S
PG|Northern|Popondetta|-8.77|148.24|SN
PG|Southern Highlands|Mendi|-6.15|143.65|S
PG|West New Britain|Kimbe|-5.55|150.15|SN
PG|West Sepik|Vanimo|-2.68|141.30|S
PG|Western|Daru|-9.08|143.21|S
PG|Western Highlands|Mount Hagen|-5.86|144.23|SN
PG|Autonomous Region of Bougainville|Arawa|-6.22|155.54|N
PY|Alto Paraguay|Fuerte Olimpo|-21.04|-57.87|S
PY|Alto Paraná|Ciudad del Este|-25.51|-54.61|SN
PY|Amambay|Pedro Juan Caballero|-22.55|-55.73|S
PY|Boquerón|Filadelfia|-22.36|-60.03|S
PY|Caaguazú|Coronel Oviedo|-25.45|-56.44|S
PY|Caazapá|Caazapá|-26.20|-56.37|S
PY|Canindeyú|Salto del Guairá|-24.06|-54.31|S
PY|Capital District|Asunción|-25.28|-57.64|SN
PY|Central|Areguá|-25.31|-57.38|S
PY|Concepción|Concepción|-23.41|-57.43|S
PY|Cordillera|Caacupé|-25.39|-57.14|S
PY|Guairá|Villarrica|-25.78|-56.45|S
PY|Itapúa|Encarnación|-27.33|-55.87|SN
PY|Misiones|San Juan Bautista|-26.67|-57.15|S
PY|Ñeembucú|Pilar|-26.87|-58.29|S
PY|Paraguarí|Paraguarí|-25.62|-57.15|S
PY|Presidente Hayes|Villa Hayes|-25.09|-57.52|S
PY|San Pedro|San Pedro de Ycuamandiyú|-24.09|-57.08|S
PY|Central|San Lorenzo|-25.34|-57.51|N
PY|Central|Capiatá|-25.35|-57.42|N
PY|Central|Luque|-25.27|-57.49|N
PY|Central|Lambaré|-25.35|-57.60|N
PY|Central|Limpio|-25.17|-57.48|N
PY|Central|Fernando de la Mora|-25.32|-57.54|N
PY|Central|Ñemby|-25.39|-57.54|N
PE|Amazonas|Chachapoyas|-6.23|-77.87|S
PE|Áncash|Huaraz|-9.53|-77.53|S
PE|Apurímac|Abancay|-13.64|-72.88|S
PE|Arequipa|Arequipa|-16.40|-71.54|SN
PE|Ayacucho|Ayacucho|-13.16|-74.22|S
PE|Cajamarca|Cajamarca|-7.16|-78.52|S
PE|Callao|Callao|-12.06|-77.13|SN
PE|Cusco|Cusco|-13.52|-71.97|SN
PE|Huancavelica|Huancavelica|-12.79|-74.97|S
PE|Huánuco|Huánuco|-9.93|-76.24|S
PE|Ica|Ica|-14.07|-75.73|S
PE|Junín|Huancayo|-12.07|-75.21|SN
PE|La Libertad|Trujillo|-8.11|-79.03|SN
PE|Lambayeque|Chiclayo|-6.77|-79.84|SN
PE|Lima Province|Lima|-12.05|-77.04|SN
PE|Lima Region|Huacho|-11.12|-77.61|S
PE|Loreto|Iquitos|-3.75|-73.25|SN
PE|Madre de Dios|Puerto Maldonado|-12.59|-69.19|S
PE|Moquegua|Moquegua|-17.20|-70.93|S
PE|Pasco|Cerro de Pasco|-10.68|-76.26|S
PE|Piura|Piura|-5.19|-80.63|SN
PE|Puno|Puno|-15.84|-70.02|S
PE|San Martín|Moyobamba|-6.03|-76.97|S
PE|Tacna|Tacna|-18.01|-70.25|S
PE|Tumbes|Tumbes|-3.57|-80.45|S
PE|Ucayali|Pucallpa|-8.38|-74.55|S
PE|Áncash|Chimbote|-9.07|-78.59|N
PH|Abra|Bangued|17.61|120.64|S
PH|Agusan del Norte|Cabadbaran|9.12|125.53|S
PH|Agusan del Sur|Prosperidad|8.61|125.92|S
PH|Aklan|Kalibo|11.71|122.36|S
PH|Albay|Legazpi|13.14|123.73|S
PH|Antique|San Jose de Buenavista|10.74|121.94|S
PH|Apayao|Kabugao|18.02|121.18|S
PH|Aurora|Baler|15.76|121.56|S
PH|Basilan|Lamitan|6.66|122.13|S
PH|Bataan|Balanga|14.68|120.54|S
PH|Batanes|Basco|20.45|121.97|S
PH|Batangas|Batangas City|13.76|121.06|S
PH|Benguet|La Trinidad|16.45|120.59|S
PH|Biliran|Naval|11.56|124.40|S
PH|Bohol|Tagbilaran|9.65|123.85|S
PH|Bukidnon|Malaybalay|8.15|125.13|S
PH|Bulacan|Malolos|14.84|120.81|S
PH|Cagayan|Tuguegarao|17.61|121.73|S
PH|Camarines Norte|Daet|14.11|122.95|S
PH|Camarines Sur|Pili|13.56|123.27|S
PH|Camiguin|Mambajao|9.25|124.71|S
PH|Capiz|Roxas City|11.59|122.75|S
PH|Catanduanes|Virac|13.58|124.24|S
PH|Cavite|Imus|14.43|120.94|S
PH|Cebu|Cebu City|10.32|123.89|SN
PH|Cotabato|Kidapawan|7.01|125.09|S
PH|Davao de Oro|Nabunturan|7.60|125.97|S
PH|Davao del Norte|Tagum|7.45|125.81|S
PH|Davao del Sur|Digos|6.75|125.36|S
PH|Davao Occidental|Malita|6.41|125.61|S
PH|Davao Oriental|Mati|6.95|126.22|S
PH|Dinagat Islands|San Jose|10.02|125.56|S
PH|Eastern Samar|Borongan|11.61|125.43|S
PH|Guimaras|Jordan|10.60|122.59|S
PH|Ifugao|Lagawe|16.80|121.12|S
PH|Ilocos Norte|Laoag|18.20|120.60|S
PH|Ilocos Sur|Vigan|17.58|120.39|S
PH|Iloilo|Iloilo City|10.72|122.56|S
PH|Isabela|Ilagan|17.15|121.89|S
PH|Kalinga|Tabuk|17.47|121.47|S
PH|La Union|San Fernando|16.62|120.32|S
PH|Laguna|Santa Cruz|14.28|121.42|S
PH|Lanao del Norte|Tubod|8.05|123.79|S
PH|Lanao del Sur|Marawi|8.00|124.30|S
PH|Leyte|Tacloban|11.24|125.00|S
PH|Maguindanao del Norte|Datu Odin Sinsuat|7.23|124.19|S
PH|Maguindanao del Sur|Buluan|6.72|124.80|S
PH|Marinduque|Boac|13.45|121.84|S
PH|Masbate|Masbate City|12.37|123.62|S
PH|Misamis Occidental|Oroquieta|8.49|123.81|S
PH|Misamis Oriental|Cagayan de Oro|8.48|124.65|S
PH|Mountain Province|Bontoc|17.09|120.98|S
PH|National Capital Region|Manila|14.60|120.98|SN
PH|Negros Occidental|Bacolod|10.67|122.95|S
PH|Negros Oriental|Dumaguete|9.31|123.31|S
PH|Northern Samar|Catarman|12.50|124.64|S
PH|Nueva Ecija|Palayan|15.54|121.09|S
PH|Nueva Vizcaya|Bayombong|16.48|121.15|S
PH|Occidental Mindoro|Mamburao|13.22|120.60|S
PH|Oriental Mindoro|Calapan|13.41|121.18|S
PH|Palawan|Puerto Princesa|9.74|118.74|S
PH|Pampanga|San Fernando|15.03|120.69|S
PH|Pangasinan|Lingayen|16.02|120.23|S
PH|Quezon|Lucena|13.94|121.62|S
PH|Quirino|Cabarroguis|16.52|121.52|S
PH|Rizal|Antipolo|14.59|121.18|SN
PH|Romblon|Romblon|12.58|122.27|S
PH|Samar|Catbalogan|11.78|124.89|S
PH|Sarangani|Alabel|6.10|125.29|S
PH|Siquijor|Siquijor|9.21|123.51|S
PH|Sorsogon|Sorsogon City|12.97|124.01|S
PH|South Cotabato|Koronadal|6.50|124.85|S
PH|Southern Leyte|Maasin|10.13|124.84|S
PH|Sultan Kudarat|Isulan|6.63|124.61|S
PH|Sulu|Jolo|6.05|121.00|S
PH|Surigao del Norte|Surigao City|9.79|125.50|S
PH|Surigao del Sur|Tandag|9.07|126.20|S
PH|Tarlac|Tarlac City|15.48|120.60|S
PH|Tawi-Tawi|Bongao|5.03|119.77|S
PH|Zambales|Iba|15.33|119.98|S
PH|Zamboanga del Norte|Dipolog|8.59|123.34|S
PH|Zamboanga del Sur|Pagadian|7.83|123.44|S
PH|Zamboanga Sibugay|Ipil|7.79|122.59|S
PH|National Capital Region|Quezon City|14.68|121.04|N
PH|National Capital Region|Caloocan|14.65|120.97|N
PH|National Capital Region|Taguig|14.52|121.05|N
PH|National Capital Region|Pasig|14.58|121.08|N
PH|Davao del Sur|Davao City|7.07|125.61|N
PH|Zamboanga del Sur|Zamboanga City|6.91|122.07|N
PH|Cavite|Dasmariñas|14.33|120.94|N
PN|Pitcairn Island|Adamstown|-25.07|-130.10|SN
PL|Greater Poland|Poznań|52.41|16.93|SN
PL|Kuyavian-Pomeranian|Bydgoszcz|53.12|18.01|SN
PL|Kuyavian-Pomeranian|Toruń|53.01|18.61|S
PL|Lesser Poland|Kraków|50.06|19.94|SN
PL|Łódź|Łódź|51.76|19.46|SN
PL|Lower Silesian|Wrocław|51.11|17.03|SN
PL|Lublin|Lublin|51.25|22.57|SN
PL|Lubusz|Gorzów Wielkopolski|52.74|15.23|S
PL|Lubusz|Zielona Góra|51.94|15.50|S
PL|Masovian|Warsaw|52.23|21.01|SN
PL|Opole|Opole|50.67|17.93|S
PL|Podlaskie|Białystok|53.13|23.17|SN
PL|Pomeranian|Gdańsk|54.35|18.65|SN
PL|Silesian|Katowice|50.26|19.02|S
PL|Subcarpathian|Rzeszów|50.04|22.00|S
PL|Świętokrzyskie|Kielce|50.87|20.63|S
PL|Warmian-Masurian|Olsztyn|53.78|20.49|S
PL|West Pomeranian|Szczecin|53.43|14.55|SN
PT|Aveiro|Aveiro|40.64|-8.65|S
PT|Azores|Ponta Delgada|37.74|-25.67|S
PT|Beja|Beja|38.01|-7.86|S
PT|Braga|Braga|41.55|-8.43|SN
PT|Bragança|Bragança|41.81|-6.76|S
PT|Castelo Branco|Castelo Branco|39.82|-7.49|S
PT|Coimbra|Coimbra|40.20|-8.43|SN
PT|Évora|Évora|38.57|-7.91|S
PT|Faro|Faro|37.02|-7.93|S
PT|Guarda|Guarda|40.54|-7.27|S
PT|Leiria|Leiria|39.74|-8.81|S
PT|Lisbon|Lisbon|38.72|-9.14|SN
PT|Madeira|Funchal|32.65|-16.91|SN
PT|Portalegre|Portalegre|39.30|-7.43|S
PT|Porto|Porto|41.15|-8.61|SN
PT|Santarém|Santarém|39.24|-8.69|S
PT|Setúbal|Setúbal|38.52|-8.89|SN
PT|Viana do Castelo|Viana do Castelo|41.70|-8.83|S
PT|Vila Real|Vila Real|41.30|-7.74|S
PT|Viseu|Viseu|40.66|-7.91|S
PT|Porto|Vila Nova de Gaia|41.13|-8.62|N
PT|Lisbon|Amadora|38.76|-9.23|N
PT|Setúbal|Almada|38.68|-9.16|N
PT|Lisbon|Agualva-Cacém|38.77|-9.30|N
PR|Adjuntas|Adjuntas|18.16|-66.72|S
PR|Aguada|Aguada|18.38|-67.19|S
PR|Aguadilla|Aguadilla|18.43|-67.15|S
PR|Aguas Buenas|Aguas Buenas|18.26|-66.10|S
PR|Aibonito|Aibonito|18.14|-66.27|S
PR|Añasco|Añasco|18.28|-67.14|S
PR|Arecibo|Arecibo|18.47|-66.72|SN
PR|Arroyo|Arroyo|17.97|-66.06|S
PR|Barceloneta|Barceloneta|18.46|-66.54|S
PR|Barranquitas|Barranquitas|18.19|-66.31|S
PR|Bayamón|Bayamón|18.40|-66.16|SN
PR|Cabo Rojo|Cabo Rojo|18.09|-67.15|S
PR|Caguas|Caguas|18.23|-66.04|SN
PR|Camuy|Camuy|18.48|-66.85|S
PR|Canóvanas|Canóvanas|18.38|-65.90|S
PR|Carolina|Carolina|18.38|-65.96|SN
PR|Cataño|Cataño|18.44|-66.12|S
PR|Cayey|Cayey|18.11|-66.17|S
PR|Ceiba|Ceiba|18.26|-65.65|S
PR|Ciales|Ciales|18.34|-66.47|S
PR|Cidra|Cidra|18.18|-66.16|S
PR|Coamo|Coamo|18.08|-66.36|S
PR|Comerío|Comerío|18.22|-66.23|S
PR|Corozal|Corozal|18.34|-66.32|S
PR|Culebra|Culebra|18.31|-65.30|S
PR|Dorado|Dorado|18.46|-66.27|S
PR|Fajardo|Fajardo|18.33|-65.65|S
PR|Florida|Florida|18.36|-66.56|S
PR|Guánica|Guánica|17.97|-66.91|S
PR|Guayama|Guayama|17.98|-66.11|S
PR|Guayanilla|Guayanilla|18.02|-66.79|S
PR|Guaynabo|Guaynabo|18.36|-66.11|SN
PR|Gurabo|Gurabo|18.25|-65.97|S
PR|Hatillo|Hatillo|18.49|-66.83|S
PR|Hormigueros|Hormigueros|18.14|-67.13|S
PR|Humacao|Humacao|18.15|-65.83|S
PR|Isabela|Isabela|18.50|-67.02|S
PR|Jayuya|Jayuya|18.22|-66.59|S
PR|Juana Díaz|Juana Díaz|18.05|-66.51|S
PR|Juncos|Juncos|18.23|-65.92|S
PR|Lajas|Lajas|18.05|-67.06|S
PR|Lares|Lares|18.29|-66.88|S
PR|Las Marías|Las Marías|18.25|-66.99|S
PR|Las Piedras|Las Piedras|18.18|-65.87|S
PR|Loíza|Loíza|18.43|-65.88|S
PR|Luquillo|Luquillo|18.37|-65.72|S
PR|Manatí|Manatí|18.43|-66.49|S
PR|Maricao|Maricao|18.18|-66.98|S
PR|Maunabo|Maunabo|18.01|-65.90|S
PR|Mayagüez|Mayagüez|18.20|-67.14|SN
PR|Moca|Moca|18.39|-67.11|S
PR|Morovis|Morovis|18.33|-66.41|S
PR|Naguabo|Naguabo|18.21|-65.73|S
PR|Naranjito|Naranjito|18.30|-66.24|S
PR|Orocovis|Orocovis|18.23|-66.39|S
PR|Patillas|Patillas|18.00|-66.01|S
PR|Peñuelas|Peñuelas|18.06|-66.72|S
PR|Ponce|Ponce|18.01|-66.61|SN
PR|Quebradillas|Quebradillas|18.47|-66.94|S
PR|Rincón|Rincón|18.34|-67.25|S
PR|Río Grande|Río Grande|18.38|-65.83|S
PR|Sabana Grande|Sabana Grande|18.08|-66.96|S
PR|Salinas|Salinas|17.98|-66.30|S
PR|San Germán|San Germán|18.08|-67.04|S
PR|San Juan|San Juan|18.45|-66.07|SN
PR|San Lorenzo|San Lorenzo|18.19|-65.96|S
PR|San Sebastián|San Sebastián|18.34|-66.99|S
PR|Santa Isabel|Santa Isabel|17.97|-66.40|S
PR|Toa Alta|Toa Alta|18.39|-66.25|S
PR|Toa Baja|Toa Baja|18.45|-66.26|SN
PR|Trujillo Alto|Trujillo Alto|18.36|-66.02|SN
PR|Utuado|Utuado|18.27|-66.70|S
PR|Vega Alta|Vega Alta|18.41|-66.33|S
PR|Vega Baja|Vega Baja|18.45|-66.39|S
PR|Vieques|Vieques|18.15|-65.44|S
PR|Villalba|Villalba|18.13|-66.49|S
PR|Yabucoa|Yabucoa|18.05|-65.88|S
PR|Yauco|Yauco|18.03|-66.85|S
QA|Al Daayen|Umm Qarn|25.58|51.45|S
QA|Al Khor and Al Thakhira|Al Khor|25.68|51.51|SN
QA|Al Rayyan|Al Rayyan|25.29|51.42|SN
QA|Al Shahaniya|Al Shahaniya|25.37|51.23|SN
QA|Al Shamal|Madinat ash Shamal|26.13|51.20|S
QA|Al Wakrah|Al Wakrah|25.17|51.60|SN
QA|Doha|Doha|25.29|51.53|SN
QA|Umm Salal|Umm Salal Ali|25.47|51.40|S
QA|Doha|Doha Industrial Area|25.20|51.45|N
QA|Umm Salal|Umm Salal Mohammed|25.42|51.39|N
QA|Al Wakrah|Al Wukair|25.13|51.58|N
QA|Al Daayen|Al Kheesa|25.42|51.48|N
QA|Al Rayyan|Rawdat Rashed|25.34|51.05|N
RE|Saint-Benoît Arrondissement|Saint-Benoît|-21.03|55.72|SN
RE|Saint-Denis Arrondissement|Saint-Denis|-20.88|55.45|SN
RE|Saint-Paul Arrondissement|Saint-Paul|-21.01|55.27|SN
RE|Saint-Pierre Arrondissement|Saint-Pierre|-21.34|55.48|SN
RE|Saint-Pierre Arrondissement|Le Tampon|-21.28|55.52|N
RE|Saint-Benoît Arrondissement|Saint-André|-20.96|55.65|N
RE|Saint-Pierre Arrondissement|Saint-Louis|-21.29|55.41|N
RE|Saint-Pierre Arrondissement|Saint-Joseph|-21.38|55.62|N
RE|Saint-Denis Arrondissement|Sainte-Marie|-20.90|55.55|N
RE|Saint-Paul Arrondissement|La Possession|-20.93|55.33|N
RO|Alba|Alba Iulia|46.07|23.57|S
RO|Arad|Arad|46.18|21.31|S
RO|Argeș|Pitești|44.86|24.87|S
RO|Bacău|Bacău|46.57|26.91|S
RO|Bihor|Oradea|47.05|21.93|SN
RO|Bistrița-Năsăud|Bistrița|47.13|24.50|S
RO|Botoșani|Botoșani|47.75|26.67|S
RO|Brăila|Brăila|45.27|27.96|S
RO|Brașov|Brașov|45.65|25.60|SN
RO|Bucharest Municipality|Bucharest|44.43|26.10|SN
RO|Buzău|Buzău|45.15|26.82|S
RO|Călărași|Călărași|44.21|27.33|S
RO|Caraș-Severin|Reșița|45.30|21.89|S
RO|Cluj|Cluj-Napoca|46.77|23.59|SN
RO|Constanța|Constanța|44.18|28.65|SN
RO|Covasna|Sfântu Gheorghe|45.87|25.79|S
RO|Dâmbovița|Târgoviște|44.93|25.46|S
RO|Dolj|Craiova|44.32|23.80|SN
RO|Galați|Galați|45.44|28.04|SN
RO|Giurgiu|Giurgiu|43.90|25.97|S
RO|Gorj|Târgu Jiu|45.05|23.27|S
RO|Harghita|Miercurea Ciuc|46.36|25.80|S
RO|Hunedoara|Deva|45.88|22.90|S
RO|Ialomița|Slobozia|44.56|27.37|S
RO|Iași|Iași|47.16|27.59|SN
RO|Ilfov|Popești-Leordeni|44.38|26.17|S
RO|Maramureș|Baia Mare|47.66|23.57|S
RO|Mehedinți|Drobeta-Turnu Severin|44.63|22.66|S
RO|Mureș|Târgu Mureș|46.54|24.56|S
RO|Neamț|Piatra Neamț|46.93|26.37|S
RO|Olt|Slatina|44.43|24.37|S
RO|Prahova|Ploiești|44.95|26.02|SN
RO|Sălaj|Zalău|47.19|23.06|S
RO|Satu Mare|Satu Mare|47.79|22.89|S
RO|Sibiu|Sibiu|45.80|24.15|S
RO|Suceava|Suceava|47.63|26.26|S
RO|Teleorman|Alexandria|43.97|25.33|S
RO|Timiș|Timișoara|45.75|21.23|SN
RO|Tulcea|Tulcea|45.18|28.80|S
RO|Vâlcea|Râmnicu Vâlcea|45.10|24.37|S
RO|Vaslui|Vaslui|46.64|27.73|S
RO|Vrancea|Focșani|45.70|27.18|S
```

### Naming caveats

PS — 16 governorates: 11 in the West Bank and five in Gaza. East Jerusalem has disputed sovereignty and administrative status. Gaza population rankings use prewar data and do not reflect displacement and destruction since October 2023.

PA — Ten provinces and three province-level indigenous comarcas. Guna Yala's Gaigirgordub is also known as El Porvenir; Llano Tugrí is also Buäbti. Other indigenous comarcas are subordinate administrative units.

PG — Twenty provinces, the Autonomous Region of Bougainville and the National Capital District. Central Province's administration is based in Port Moresby, outside the province, so Kwikila is used as a local reference. Jiwaka's capital arrangements have involved Banz and Kurumul.

PY — Seventeen departments plus the separately administered Asunción Capital District. Ciudad del Este was formerly Puerto Presidente Stroessner. San Pedro de Ycuamandiyú is commonly shortened to San Pedro.

PE — Twenty-four departments plus Callao and the separately governed Lima Province. Lima Region is distinct from Lima Province and has its regional-government seat in Huacho. Ayacucho is also historically Huamanga.

PH — Eighty-two provinces plus the National Capital Region are used as geographic reference units; administrative regions form a separate grouping above provinces. Sulu is associated with Zamboanga Peninsula following its removal from BARMM, Negros Island Region was restored in 2024, and Maguindanao is divided into two provinces. Several highly urbanized cities are administratively independent of their surrounding provinces.

PN — Only Pitcairn Island is permanently inhabited; Adamstown is its sole settlement. Henderson, Ducie and Oeno islands have no permanent residents.

PL — Sixteen voivodeships. Kuyavian-Pomeranian has administrative seats in Bydgoszcz and Toruń; Lubusz has seats in Gorzów Wielkopolski and Zielona Góra. Accordingly, both cities are included for each of those voivodeships.

PT — Eighteen mainland districts plus the autonomous regions of the Azores and Madeira. The Azores have government functions distributed among Ponta Delgada, Horta and Angra do Heroísmo; Ponta Delgada is used as the principal population reference.

PR — Seventy-eight municipalities are used as the primary local geographic units because Puerto Rico has no state or provincial tier. The settlement centres share the municipality names; Vieques and Culebra are separate island municipalities.

QA — Eight municipalities. Al Khor and Al Thakhira is also called Al Khor; Al Daayen is also Ad-Daayen. Doha Industrial Area is a census locality within Doha's urban region rather than an independent municipality.

RE — Réunion is one French overseas department and region; its four arrondissements are used as geographic subdivisions. The ten largest entries are based on commune populations rather than strictly defined built-up urban areas.

RO — Forty-one counties plus Bucharest municipality. Ilfov County's administrative seat is in Bucharest, outside the county, so Popești-Leordeni is used as its largest in-county city. Cluj-Napoca is also commonly called Cluj.

### Points still open

- Round 11: FM — Tol; MH — Airuk, Jabat, Lib; MR — Guerou; MU — Vingt Cinq, Raphael Island. Seven unmatched points.
- Round 12: NL — The Bottom, Oranjestad. Two unmatched points.
- Round 13: MP — Agrihan; PW — Ngaramasch, Tobi, Dongosaru. Four unmatched points.
- Round 14: 386 reference rows across 13 countries, pending comparison with extracted Overture business data.
- Administrative exceptions: Check Gaza's displaced settlements, Panama's small indigenous comarca capitals, Bougainville and Jiwaka administrative seats, the Philippines' independent cities, and Pitcairn's single permanently inhabited settlement.
- Population comparability: The N selections combine available national censuses and settlement-level estimates; municipality populations and contiguous urban-area populations can produce different top-ten rankings.


---

## Claude Code - 2026-11-08 20:43 UTC - 15_claude.md - attachments: none

## Check of your message-14 list
Round 14: 386 reference lines, 386 cities, 385 with business data (100 %).
Not covered: - PA: 16/17 cities covered, 50,653 businesses near them; no data at: Gaigirgordub

Same format again:


## Message 15 of 19 - countries
Russia (RU), Rwanda (RW), Samoa (WS), San Marino (SM), São Tomé & Príncipe (ST), Saudi Arabia (SA), Senegal (SN), Serbia (RS), Seychelles (SC), Sierra Leone (SL), Singapore (SG), Sint Maarten (SX), Slovakia (SK)

For EACH country above give:
1. every first-level administrative division (state / province / region / governorate ... as it is today),
   with its capital or largest city (kind S);
2. the 10 largest cities of the country by population (kind N) - fewer if the country has fewer.
   A city can appear as both S and N; list it once with kind SN.
Uninhabited territories: one line `CC|-|-|||none`.

Output ONLY one code block, one line per city, pipe-separated, no header, no commentary inside it:
`CC|state|city|lat|lon|kind`
- CC = ISO code above; state and city in English (the name a map would show); lat / lon with 2 decimals.
After the code block: one line per country with any naming caveat (renamed divisions, disputed areas),
then the list of points still open.


---

## ChatGPT (Extra High) - 2026-11-08 20:50 UTC - saved as 15_chatgpt.md

```
RU|Adygea|Maykop|44.61|40.10|S
RU|Altai Republic|Gorno-Altaysk|51.96|85.96|S
RU|Bashkortostan|Ufa|54.74|55.97|SN
RU|Buryatia|Ulan-Ude|51.83|107.58|S
RU|Chechnya|Grozny|43.32|45.69|S
RU|Chuvashia|Cheboksary|56.13|47.25|S
RU|Dagestan|Makhachkala|42.98|47.50|S
RU|Ingushetia|Magas|43.17|44.81|S
RU|Kabardino-Balkaria|Nalchik|43.49|43.60|S
RU|Kalmykia|Elista|46.31|44.27|S
RU|Karachay-Cherkessia|Cherkessk|44.22|42.05|S
RU|Karelia|Petrozavodsk|61.79|34.35|S
RU|Khakassia|Abakan|53.72|91.43|S
RU|Komi|Syktyvkar|61.67|50.84|S
RU|Mari El|Yoshkar-Ola|56.63|47.90|S
RU|Mordovia|Saransk|54.18|45.18|S
RU|North Ossetia-Alania|Vladikavkaz|43.02|44.68|S
RU|Sakha|Yakutsk|62.03|129.73|S
RU|Tatarstan|Kazan|55.79|49.12|SN
RU|Tuva|Kyzyl|51.72|94.44|S
RU|Udmurtia|Izhevsk|56.85|53.21|S
RU|Altai Krai|Barnaul|53.35|83.77|S
RU|Kamchatka Krai|Petropavlovsk-Kamchatsky|53.04|158.65|S
RU|Khabarovsk Krai|Khabarovsk|48.48|135.08|S
RU|Krasnodar Krai|Krasnodar|45.04|38.98|SN
RU|Krasnoyarsk Krai|Krasnoyarsk|56.01|92.87|SN
RU|Perm Krai|Perm|58.01|56.25|S
RU|Primorsky Krai|Vladivostok|43.12|131.89|S
RU|Stavropol Krai|Stavropol|45.04|41.97|S
RU|Zabaykalsky Krai|Chita|52.03|113.50|S
RU|Amur Oblast|Blagoveshchensk|50.29|127.53|S
RU|Arkhangelsk Oblast|Arkhangelsk|64.54|40.54|S
RU|Astrakhan Oblast|Astrakhan|46.35|48.04|S
RU|Belgorod Oblast|Belgorod|50.60|36.59|S
RU|Bryansk Oblast|Bryansk|53.24|34.37|S
RU|Chelyabinsk Oblast|Chelyabinsk|55.16|61.40|SN
RU|Irkutsk Oblast|Irkutsk|52.29|104.28|S
RU|Ivanovo Oblast|Ivanovo|57.00|40.97|S
RU|Kaliningrad Oblast|Kaliningrad|54.71|20.51|S
RU|Kaluga Oblast|Kaluga|54.51|36.26|S
RU|Kemerovo Oblast|Kemerovo|55.35|86.09|S
RU|Kirov Oblast|Kirov|58.60|49.67|S
RU|Kostroma Oblast|Kostroma|57.77|40.93|S
RU|Kurgan Oblast|Kurgan|55.44|65.34|S
RU|Kursk Oblast|Kursk|51.73|36.19|S
RU|Leningrad Oblast|Gatchina|59.57|30.13|S
RU|Lipetsk Oblast|Lipetsk|52.61|39.60|S
RU|Magadan Oblast|Magadan|59.56|150.80|S
RU|Moscow Oblast|Krasnogorsk|55.82|37.34|S
RU|Murmansk Oblast|Murmansk|68.97|33.08|S
RU|Nizhny Novgorod Oblast|Nizhny Novgorod|56.33|44.00|SN
RU|Novgorod Oblast|Veliky Novgorod|58.52|31.28|S
RU|Novosibirsk Oblast|Novosibirsk|55.03|82.92|SN
RU|Omsk Oblast|Omsk|54.99|73.37|S
RU|Orenburg Oblast|Orenburg|51.77|55.10|S
RU|Oryol Oblast|Oryol|52.97|36.06|S
RU|Penza Oblast|Penza|53.20|45.00|S
RU|Pskov Oblast|Pskov|57.82|28.33|S
RU|Rostov Oblast|Rostov-on-Don|47.22|39.72|S
RU|Ryazan Oblast|Ryazan|54.63|39.74|S
RU|Sakhalin Oblast|Yuzhno-Sakhalinsk|46.96|142.74|S
RU|Samara Oblast|Samara|53.20|50.15|S
RU|Saratov Oblast|Saratov|51.54|46.01|S
RU|Smolensk Oblast|Smolensk|54.78|32.05|S
RU|Sverdlovsk Oblast|Yekaterinburg|56.84|60.61|SN
RU|Tambov Oblast|Tambov|52.73|41.44|S
RU|Tomsk Oblast|Tomsk|56.49|84.95|S
RU|Tula Oblast|Tula|54.20|37.62|S
RU|Tver Oblast|Tver|56.86|35.92|S
RU|Tyumen Oblast|Tyumen|57.15|65.53|S
RU|Ulyanovsk Oblast|Ulyanovsk|54.32|48.39|S
RU|Vladimir Oblast|Vladimir|56.13|40.41|S
RU|Volgograd Oblast|Volgograd|48.71|44.51|S
RU|Vologda Oblast|Vologda|59.22|39.89|S
RU|Voronezh Oblast|Voronezh|51.67|39.18|S
RU|Yaroslavl Oblast|Yaroslavl|57.63|39.87|S
RU|Moscow|Moscow|55.75|37.62|SN
RU|Saint Petersburg|Saint Petersburg|59.93|30.32|SN
RU|Jewish Autonomous Oblast|Birobidzhan|48.79|132.92|S
RU|Chukotka Autonomous Okrug|Anadyr|64.73|177.51|S
RU|Khanty-Mansi Autonomous Okrug|Khanty-Mansiysk|61.00|69.02|S
RU|Nenets Autonomous Okrug|Naryan-Mar|67.64|53.01|S
RU|Yamalo-Nenets Autonomous Okrug|Salekhard|66.53|66.60|S
RW|Kigali City|Kigali|-1.95|30.06|SN
RW|Eastern Province|Rwamagana|-1.95|30.43|S
RW|Northern Province|Musanze|-1.50|29.63|SN
RW|Southern Province|Nyanza|-2.35|29.75|SN
RW|Western Province|Kibuye|-2.06|29.35|S
RW|Western Province|Gisenyi|-1.70|29.26|N
RW|Southern Province|Butare|-2.60|29.74|N
RW|Southern Province|Muhanga|-2.08|29.76|N
RW|Northern Province|Byumba|-1.58|30.06|N
RW|Western Province|Cyangugu|-2.48|28.90|N
RW|Western Province|Bugarama|-2.69|29.01|N
RW|Eastern Province|Kayonza|-1.91|30.65|N
WS|A'ana|Leulumoega|-13.83|-171.98|S
WS|Aiga-i-le-Tai|Mulifanua|-13.83|-172.04|S
WS|Atua|Lufilufi|-13.88|-171.60|S
WS|Fa'asaleleaga|Salelologa|-13.74|-172.22|SN
WS|Gaga'emauga|Saleaula|-13.50|-172.30|S
WS|Gaga'ifomauga|Safotu|-13.45|-172.42|S
WS|Palauli|Vailoa|-13.76|-172.31|S
WS|Satupa'itea|Satupa'itea|-13.71|-172.58|S
WS|Tuamasaga|Apia|-13.83|-171.76|SN
WS|Va'a-o-Fonoti|Samamea|-13.94|-171.54|S
WS|Vaisigano|Asau|-13.52|-172.64|S
WS|Tuamasaga|Vaitele Fou|-13.84|-171.80|N
WS|Tuamasaga|Vaitele Uta|-13.84|-171.81|N
WS|Tuamasaga|Faleula|-13.82|-171.84|N
WS|Tuamasaga|Siusega|-13.84|-171.81|N
WS|A'ana|Faleasiu|-13.83|-171.99|N
WS|Tuamasaga|Leauva'a|-13.84|-171.91|N
WS|Tuamasaga|Vaiusu|-13.84|-171.79|N
WS|Tuamasaga|Malie|-13.80|-171.84|N
SM|Acquaviva|Acquaviva|43.95|12.42|SN
SM|Borgo Maggiore|Borgo Maggiore|43.94|12.45|SN
SM|Chiesanuova|Chiesanuova|43.90|12.42|S
SM|Domagnano|Domagnano|43.95|12.47|SN
SM|Faetano|Faetano|43.93|12.50|S
SM|Fiorentino|Fiorentino|43.91|12.46|SN
SM|Montegiardino|Montegiardino|43.91|12.48|S
SM|San Marino|San Marino|43.94|12.45|SN
SM|Serravalle|Serravalle|43.97|12.48|SN
SM|Serravalle|Dogana|43.98|12.49|N
SM|Borgo Maggiore|Valdragone|43.94|12.46|N
SM|Borgo Maggiore|Cailungo|43.95|12.45|N
SM|San Marino|Murata|43.92|12.45|N
ST|Água Grande|São Tomé|0.34|6.73|SN
ST|Cantagalo|Santana|0.26|6.74|SN
ST|Caué|São João dos Angolares|0.13|6.65|SN
ST|Lembá|Neves|0.36|6.55|SN
ST|Lobata|Guadalupe|0.38|6.64|SN
ST|Mé-Zóchi|Trindade|0.30|6.68|SN
ST|Príncipe Autonomous Region|Santo António|1.64|7.42|SN
ST|Caué|Porto Alegre|0.03|6.54|N
ST|Lembá|Santa Catarina|0.25|6.48|N
ST|Cantagalo|Ribeira Afonso|0.20|6.71|N
SA|Al Bahah|Al Bahah|20.01|41.47|S
SA|Al Jawf|Sakaka|29.97|40.21|S
SA|Al Qassim|Buraydah|26.36|43.98|SN
SA|Asir|Abha|18.22|42.51|S
SA|Eastern Province|Dammam|26.43|50.10|SN
SA|Hail|Hail|27.52|41.69|S
SA|Jazan|Jazan|16.89|42.55|S
SA|Madinah|Medina|24.47|39.61|SN
SA|Makkah|Mecca|21.42|39.83|SN
SA|Najran|Najran|17.49|44.13|S
SA|Northern Borders|Arar|30.98|41.04|S
SA|Riyadh|Riyadh|24.71|46.68|SN
SA|Tabuk|Tabuk|28.38|36.56|SN
SA|Makkah|Jeddah|21.54|39.17|N
SA|Eastern Province|Hofuf|25.36|49.59|N
SA|Makkah|Taif|21.27|40.42|N
SA|Asir|Khamis Mushait|18.31|42.73|N
SN|Dakar|Dakar|14.69|-17.44|SN
SN|Diourbel|Diourbel|14.66|-16.24|SN
SN|Fatick|Fatick|14.33|-16.41|S
SN|Kaffrine|Kaffrine|14.10|-15.55|S
SN|Kaolack|Kaolack|14.15|-16.07|SN
SN|Kédougou|Kédougou|12.56|-12.17|S
SN|Kolda|Kolda|12.88|-14.95|S
SN|Louga|Louga|15.62|-16.22|S
SN|Matam|Matam|15.66|-13.26|S
SN|Saint-Louis|Saint-Louis|16.03|-16.50|SN
SN|Sédhiou|Sédhiou|12.71|-15.56|S
SN|Tambacounda|Tambacounda|13.77|-13.67|S
SN|Thiès|Thiès|14.79|-16.93|SN
SN|Ziguinchor|Ziguinchor|12.57|-16.27|SN
SN|Diourbel|Touba|14.85|-15.88|N
SN|Dakar|Rufisque|14.72|-17.27|N
SN|Thiès|Mbour|14.42|-16.97|N
SN|Dakar|Tivaouane Peulh-Niaga|14.83|-17.28|N
RS|Belgrade|Belgrade|44.82|20.46|SN
RS|Bor District|Bor|44.07|22.10|S
RS|Braničevo District|Požarevac|44.62|21.19|S
RS|Jablanica District|Leskovac|42.99|21.95|S
RS|Kolubara District|Valjevo|44.27|19.88|S
RS|Mačva District|Šabac|44.75|19.69|S
RS|Moravica District|Čačak|43.89|20.35|SN
RS|Nišava District|Niš|43.32|21.90|SN
RS|Pčinja District|Vranje|42.55|21.90|S
RS|Pirot District|Pirot|43.15|22.59|S
RS|Podunavlje District|Smederevo|44.66|20.93|SN
RS|Pomoravlje District|Jagodina|43.98|21.26|S
RS|Rasina District|Kruševac|43.58|21.33|S
RS|Raška District|Kraljevo|43.72|20.69|S
RS|Šumadija District|Kragujevac|44.01|20.91|SN
RS|Toplica District|Prokuplje|43.23|21.59|S
RS|Zaječar District|Zaječar|43.90|22.26|S
RS|Zlatibor District|Užice|43.86|19.85|S
RS|Central Banat District|Zrenjanin|45.38|20.39|SN
RS|North Bačka District|Subotica|46.10|19.67|SN
RS|North Banat District|Kikinda|45.83|20.46|S
RS|South Bačka District|Novi Sad|45.25|19.84|SN
RS|South Banat District|Pančevo|44.87|20.64|SN
RS|Srem District|Sremska Mitrovica|44.98|19.61|S
RS|West Bačka District|Sombor|45.78|19.11|S
RS|Kosovo District|Pristina|42.66|21.16|S
RS|Kosovo-Pomoravlje District|Gjilan|42.46|21.47|S
RS|Kosovska Mitrovica District|Mitrovica|42.89|20.87|S
RS|Peć District|Peja|42.66|20.29|S
RS|Prizren District|Prizren|42.21|20.74|S
RS|Raška District|Novi Pazar|43.14|20.52|N
SC|Anse aux Pins|Anse aux Pins|-4.70|55.52|S
SC|Anse Boileau|Anse Boileau|-4.72|55.48|SN
SC|Anse Etoile|Anse Etoile|-4.61|55.46|SN
SC|Anse Royale|Anse Royale|-4.74|55.52|SN
SC|Au Cap|Au Cap|-4.71|55.52|S
SC|Baie Lazare|Baie Lazare|-4.75|55.48|S
SC|Baie Sainte Anne|Baie Sainte Anne|-4.35|55.75|SN
SC|Beau Vallon|Beau Vallon|-4.61|55.43|SN
SC|Bel Air|Bel Air|-4.63|55.44|S
SC|Bel Ombre|Bel Ombre|-4.62|55.42|SN
SC|Cascade|Cascade|-4.67|55.50|SN
SC|English River|Victoria|-4.62|55.45|SN
SC|Glacis|Glacis|-4.59|55.44|S
SC|Grand Anse Mahé|Grand Anse|-4.68|55.46|S
SC|Grand Anse Praslin|Grand Anse Praslin|-4.32|55.72|SN
SC|Ile Perseverance|Ile Perseverance|-4.59|55.47|S
SC|La Digue and Inner Islands|La Passe|-4.35|55.83|SN
SC|Les Mamelles|Les Mamelles|-4.65|55.47|S
SC|Mont Buxton|Mont Buxton|-4.61|55.45|S
SC|Mont Fleuri|Mont Fleuri|-4.64|55.46|S
SC|Plaisance|Plaisance|-4.65|55.46|S
SC|Pointe Larue|Pointe Larue|-4.67|55.52|S
SC|Port Glaud|Port Glaud|-4.66|55.42|S
SC|Roche Caiman|Roche Caiman|-4.64|55.47|S
SC|Saint Louis|Saint Louis|-4.62|55.44|S
SC|Takamaka|Takamaka|-4.78|55.50|S
SL|Eastern Province|Kenema|7.88|-11.19|SN
SL|Northern Province|Makeni|8.88|-12.05|SN
SL|North Western Province|Port Loko|8.77|-12.79|SN
SL|Southern Province|Bo|7.96|-11.74|SN
SL|Western Area|Freetown|8.48|-13.23|SN
SL|Eastern Province|Koidu|8.64|-10.97|N
SL|Western Area|Waterloo|8.34|-13.07|N
SL|Northern Province|Magburaka|8.72|-11.95|N
SL|Western Area|Goderich|8.43|-13.29|N
SL|Eastern Province|Daru|7.99|-10.85|N
SG|Central Region|Singapore|1.29|103.85|S
SG|East Region|Tampines|1.35|103.94|SN
SG|North Region|Woodlands|1.44|103.79|SN
SG|North-East Region|Sengkang|1.39|103.90|SN
SG|West Region|Jurong East|1.33|103.74|S
SG|East Region|Bedok|1.32|103.93|N
SG|West Region|Jurong West|1.34|103.70|N
SG|North Region|Yishun|1.43|103.84|N
SG|North-East Region|Hougang|1.37|103.89|N
SG|North-East Region|Punggol|1.40|103.91|N
SG|West Region|Choa Chu Kang|1.39|103.75|N
SG|West Region|Bukit Batok|1.35|103.75|N
SX|Sint Maarten|Philipsburg|18.02|-63.04|SN
SX|Sint Maarten|Lower Prince's Quarter|18.05|-63.04|N
SX|Sint Maarten|Cul de Sac|18.04|-63.06|N
SX|Sint Maarten|Cole Bay|18.03|-63.08|N
SX|Sint Maarten|Upper Prince's Quarter|18.05|-63.02|N
SX|Sint Maarten|Little Bay|18.02|-63.06|N
SX|Sint Maarten|Dutch Quarter|18.05|-63.05|N
SX|Sint Maarten|Simpson Bay|18.04|-63.11|N
SX|Sint Maarten|Lowlands|18.05|-63.12|N
SX|Sint Maarten|Maho|18.05|-63.12|N
SK|Banská Bystrica Region|Banská Bystrica|48.74|19.15|SN
SK|Bratislava Region|Bratislava|48.15|17.11|SN
SK|Košice Region|Košice|48.72|21.26|SN
SK|Nitra Region|Nitra|48.31|18.09|SN
SK|Prešov Region|Prešov|49.00|21.24|SN
SK|Trenčín Region|Trenčín|48.89|18.04|SN
SK|Trnava Region|Trnava|48.38|17.59|SN
SK|Žilina Region|Žilina|49.22|18.74|SN
SK|Žilina Region|Martin|49.07|18.92|N
SK|Prešov Region|Poprad|49.06|20.30|N
```

### Naming caveats

RU — 83 internationally recognized federal subjects are included. Russia additionally claims Crimea, Sevastopol, Donetsk, Luhansk, Kherson and Zaporizhzhia, which are internationally recognized as Ukrainian territory and therefore excluded from RU rows. Moscow Oblast's administrative seat is Krasnogorsk; Leningrad Oblast's is Gatchina. The ten largest cities follow 2025 population estimates.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://iarpa.org\&sz=32)

iarpa.org+1



RW — Four provinces plus Kigali City. Ruhengeri is now Musanze; Gitarama is Muhanga; Butare is also Huye. Kibuye is the Western Province administrative centre. N entries use identifiable urban localities, not entire district populations.

WS — Eleven traditional administrative districts, distinct from Samoa's 51 electoral constituencies. Districts generally lack conventional urban capitals, so principal villages or traditional centres are used. Vaitele Fou and Vaitele Uta are distinct census settlements.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://thefactbook.org\&sz=32)

The Factbook+1



SM — Nine castelli. San Marino is the national capital, while Serravalle is the most populous municipality. Dogana, Valdragone, Cailungo and Murata are separate populated settlements within existing castelli.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.visitsanmarino.com\&sz=32)

Visit San Marino+1



ST — Six districts on São Tomé and the Autonomous Region of Príncipe are used as operational administrative units. The country also has a broader two-island provincial classification. Santo António is Príncipe's administrative centre.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://documents1.worldbank.org\&sz=32)

World Bank+1



SA — Thirteen administrative regions. Asir is also Aseer, Al Qassim is also Qassim, and Hofuf is also Al Ahsa or Al Hufuf. The ten largest cities follow the 2022 national census, with Hofuf representing the combined Hofuf–Al Mubarraz urban locality.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://saudipedia.com\&sz=32)

Saudipedia+1



SN — Fourteen regions. Touba is in Diourbel Region, not the city of Diourbel. The ten N entries follow the 2023 census's urban-commune classification, which combines Dakar with its contiguous urban localities, including Pikine and Guédiawaye.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.vie-publique.sn\&sz=32)

Vie Publique Sénégal+1



RS — Twenty-nine districts plus Belgrade under Serbia's territorial classification. Five Kosovo-related districts are included for geographic reference but are not administered by Serbia; Kosovo has its own de facto administrative system, and its independence is internationally disputed. The ten N entries outside Kosovo follow Serbia's 2022 census.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://stat.gov.rs\&sz=32)

stat.gov.rs+1



SC — Twenty-six districts. Ile Perseverance is the newer residential district; Au Cap was formerly Anse Louis. District centres and major settlements are used because Seychelles does not have a standardized ten-city population hierarchy; Victoria is the capital.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://sum.sc\&sz=32)

Seychelles United Movement+1



SL — Four provinces plus Western Area. North Western Province was separated from Northern Province in 2017. Koidu is also Koidu-New Sembehun. City population estimates differ substantially between the 2015 and 2021 censuses.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.worldometers.info\&sz=32)

Worldometer



SG — Five planning regions are used as geographic subdivisions; Singapore is administratively a single city-state. The N entries are the ten most populous planning areas in June 2025, rather than ten independent cities.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://popquery.onemap.gov.sg\&sz=32)

popquery.onemap.gov.sg+2



SX — Sint Maarten is a constituent country of the Kingdom of the Netherlands without formal provincial subdivisions. Philipsburg is the capital; the N entries are neighborhood or settlement proxies, not independently incorporated cities. Lower Prince's Quarter is also written Lower Princess Quarter.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://stats.sintmaartengov.org\&sz=32)

stats.sintmaartengov.org+1



SK — Eight regions (kraje). Bratislava and Košice are also regional capitals; Martin and Poprad complete the ten largest cities. Regional names are shown with the English word Region, and the cities retain their Slovak spellings.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://amcham.sk\&sz=32)

amcham.sk



### Points still open

- Round 11: FM — Tol; MH — Airuk, Jabat, Lib; MR — Guerou; MU — Vingt Cinq, Raphael Island.
- Round 12: NL — The Bottom, Oranjestad.
- Round 13: MP — Agrihan; PW — Ngaramasch, Tobi, Dongosaru.
- Round 14: PA — Gaigirgordub.
- Round 15: Check the new reference rows against Overture business data; coverage is not yet verified.
- Special geographic cases: Verify Samoa's traditional district centres, Seychelles' small district settlements, São Tomé and Príncipe's administrative hierarchy, and Sint Maarten's neighborhood-based coverage.
- Territorial consistency: Keep Russia's disputed territorial claims and Serbia's Kosovo-related districts explicitly flagged so that business records are not incorrectly assigned across internationally disputed boundaries.


---

## Claude Code - 2026-11-08 20:50 UTC - 16_claude.md - attachments: none

## Check of your message-15 list
Round 15: 271 reference lines, 271 cities, 267 with business data (99 %).
Not covered: - RS: 27/31 cities covered, 80,266 businesses near them; no data at: Pristina, Gjilan, Peja, Prizren

Same format again:


## Message 16 of 19 - countries
Slovenia (SI), Solomon Islands (SB), Somalia (SO), South Africa (ZA), South Georgia & South Sandwich Islands (GS), South Korea (KR), South Sudan (SS), Spain (ES), Sri Lanka (LK), St. Barthélemy (BL), St. Helena (SH), St. Kitts & Nevis (KN), St. Lucia (LC)

For EACH country above give:
1. every first-level administrative division (state / province / region / governorate ... as it is today),
   with its capital or largest city (kind S);
2. the 10 largest cities of the country by population (kind N) - fewer if the country has fewer.
   A city can appear as both S and N; list it once with kind SN.
Uninhabited territories: one line `CC|-|-|||none`.

Output ONLY one code block, one line per city, pipe-separated, no header, no commentary inside it:
`CC|state|city|lat|lon|kind`
- CC = ISO code above; state and city in English (the name a map would show); lat / lon with 2 decimals.
After the code block: one line per country with any naming caveat (renamed divisions, disputed areas),
then the list of points still open.


---

## ChatGPT (Extra High) - 2026-11-08 21:04 UTC - saved as 16_chatgpt.md

```
SI|Ajdovščina|Ajdovščina|45.89|13.90|S
SI|Ankaran|Ankaran|45.58|13.74|S
SI|Apače|Apače|46.70|15.91|S
SI|Beltinci|Beltinci|46.61|16.24|S
SI|Benedikt|Benedikt|46.62|15.90|S
SI|Bistrica ob Sotli|Bistrica ob Sotli|46.06|15.66|S
SI|Bled|Bled|46.37|14.11|S
SI|Bloke|Nova vas|45.77|14.51|S
SI|Bohinj|Bohinjska Bistrica|46.28|13.95|S
SI|Borovnica|Borovnica|45.90|14.38|S
SI|Bovec|Bovec|46.34|13.55|S
SI|Braslovče|Braslovče|46.28|15.04|S
SI|Brda|Dobrovo|46.00|13.53|S
SI|Brezovica|Brezovica pri Ljubljani|45.96|14.43|S
SI|Brežice|Brežice|45.90|15.59|S
SI|Cankova|Cankova|46.72|16.02|S
SI|Celje|Celje|46.23|15.26|SN
SI|Cerklje na Gorenjskem|Cerklje na Gorenjskem|46.25|14.49|S
SI|Cerknica|Cerknica|45.80|14.39|S
SI|Cerkno|Cerkno|46.13|13.99|S
SI|Cerkvenjak|Cerkvenjak|46.57|15.94|S
SI|Cirkulane|Cirkulane|46.33|16.00|S
SI|Črenšovci|Črenšovci|46.57|16.29|S
SI|Črna na Koroškem|Črna na Koroškem|46.47|14.85|S
SI|Črnomelj|Črnomelj|45.54|15.19|S
SI|Destrnik|Destrnik|46.49|15.88|S
SI|Divača|Divača|45.68|13.97|S
SI|Dobje|Dobje pri Planini|46.14|15.39|S
SI|Dobrepolje|Videm|45.85|14.71|S
SI|Dobrna|Dobrna|46.34|15.23|S
SI|Dobrova-Polhov Gradec|Dobrova|46.06|14.32|S
SI|Dobrovnik|Dobrovnik|46.65|16.35|S
SI|Dol pri Ljubljani|Dol pri Ljubljani|46.09|14.64|S
SI|Dolenjske Toplice|Dolenjske Toplice|45.73|15.01|S
SI|Domžale|Domžale|46.14|14.64|S
SI|Dornava|Dornava|46.44|15.99|S
SI|Dravograd|Dravograd|46.59|15.02|S
SI|Duplek|Spodnji Duplek|46.50|15.75|S
SI|Gorenja vas-Poljane|Gorenja vas|46.11|14.11|S
SI|Gorišnica|Gorišnica|46.41|16.01|S
SI|Gorje|Zgornje Gorje|46.38|14.07|S
SI|Gornja Radgona|Gornja Radgona|46.68|15.99|S
SI|Gornji Grad|Gornji Grad|46.30|14.81|S
SI|Gornji Petrovci|Gornji Petrovci|46.80|16.22|S
SI|Grad|Grad|46.81|16.11|S
SI|Grosuplje|Grosuplje|45.96|14.66|S
SI|Hajdina|Zgornja Hajdina|46.42|15.82|S
SI|Hoče-Slivnica|Spodnje Hoče|46.48|15.65|S
SI|Hodoš|Hodoš|46.83|16.32|S
SI|Horjul|Horjul|46.02|14.30|S
SI|Hrastnik|Hrastnik|46.14|15.08|S
SI|Hrpelje-Kozina|Hrpelje|45.61|13.94|S
SI|Idrija|Idrija|46.00|13.98|S
SI|Ig|Ig|45.96|14.53|S
SI|Ilirska Bistrica|Ilirska Bistrica|45.58|14.28|S
SI|Ivančna Gorica|Ivančna Gorica|45.94|14.80|S
SI|Izola|Izola|45.53|13.67|S
SI|Jesenice|Jesenice|46.44|14.05|S
SI|Jezersko|Zgornje Jezersko|46.39|14.50|S
SI|Juršinci|Juršinci|46.49|15.98|S
SI|Kamnik|Kamnik|46.23|14.61|SN
SI|Kanal ob Soči|Kanal|46.07|13.62|S
SI|Kidričevo|Kidričevo|46.40|15.79|S
SI|Kobarid|Kobarid|46.25|13.58|S
SI|Kobilje|Kobilje|46.69|16.39|S
SI|Kočevje|Kočevje|45.64|14.86|S
SI|Komen|Komen|45.82|13.75|S
SI|Komenda|Komenda|46.21|14.54|S
SI|Koper|Koper|45.55|13.73|SN
SI|Kostanjevica na Krki|Kostanjevica na Krki|45.83|15.44|S
SI|Kostel|Vas|45.51|14.87|S
SI|Kozje|Kozje|46.07|15.56|S
SI|Kranj|Kranj|46.24|14.36|SN
SI|Kranjska Gora|Kranjska Gora|46.48|13.79|S
SI|Križevci|Križevci pri Ljutomeru|46.57|16.11|S
SI|Krško|Krško|45.96|15.49|S
SI|Kungota|Zgornja Kungota|46.64|15.60|S
SI|Kuzma|Kuzma|46.84|16.08|S
SI|Laško|Laško|46.15|15.24|S
SI|Lenart|Lenart v Slovenskih goricah|46.58|15.83|S
SI|Lendava|Lendava|46.55|16.44|S
SI|Litija|Litija|46.06|14.83|S
SI|Ljubljana|Ljubljana|46.05|14.51|SN
SI|Ljubno|Ljubno ob Savinji|46.34|14.83|S
SI|Ljutomer|Ljutomer|46.52|16.19|S
SI|Log-Dragomer|Log pri Brezovici|46.02|14.37|S
SI|Logatec|Logatec|45.92|14.24|S
SI|Loška dolina|Stari trg pri Ložu|45.65|14.50|S
SI|Loški Potok|Hrib-Loški Potok|45.69|14.60|S
SI|Lovrenc na Pohorju|Lovrenc na Pohorju|46.54|15.40|S
SI|Luče|Luče|46.35|14.75|S
SI|Lukovica|Lukovica pri Domžalah|46.17|14.69|S
SI|Majšperk|Majšperk|46.35|15.73|S
SI|Makole|Makole|46.32|15.67|S
SI|Maribor|Maribor|46.56|15.65|SN
SI|Markovci|Markovci|46.39|15.96|S
SI|Medvode|Medvode|46.14|14.40|S
SI|Mengeš|Mengeš|46.17|14.57|S
SI|Metlika|Metlika|45.65|15.32|S
SI|Mežica|Mežica|46.52|14.85|S
SI|Miklavž na Dravskem polju|Miklavž na Dravskem Polju|46.51|15.70|S
SI|Miren-Kostanjevica|Miren|45.84|13.63|S
SI|Mirna|Mirna|45.95|15.06|S
SI|Mirna Peč|Mirna Peč|45.85|15.09|S
SI|Mislinja|Mislinja|46.44|15.20|S
SI|Mokronog-Trebelno|Mokronog|45.91|15.16|S
SI|Moravče|Moravče|46.14|14.75|S
SI|Moravske Toplice|Moravske Toplice|46.69|16.22|S
SI|Mozirje|Mozirje|46.34|14.96|S
SI|Murska Sobota|Murska Sobota|46.64|16.15|S
SI|Muta|Muta|46.61|15.16|S
SI|Naklo|Naklo|46.27|14.32|S
SI|Nazarje|Nazarje|46.28|14.92|S
SI|Nova Gorica|Nova Gorica|45.96|13.65|S
SI|Novo mesto|Novo mesto|45.80|15.17|SN
SI|Odranci|Odranci|46.59|16.28|S
SI|Oplotnica|Oplotnica|46.39|15.45|S
SI|Ormož|Ormož|46.44|16.15|S
SI|Osilnica|Osilnica|45.54|14.72|S
SI|Pesnica|Pesnica pri Mariboru|46.61|15.68|S
SI|Piran|Piran|45.53|13.57|S
SI|Pivka|Pivka|45.68|14.25|S
SI|Podčetrtek|Podčetrtek|46.17|15.60|S
SI|Podlehnik|Podlehnik|46.33|15.88|S
SI|Podvelka|Podvelka|46.62|15.39|S
SI|Poljčane|Poljčane|46.31|15.58|S
SI|Polzela|Polzela|46.28|15.07|S
SI|Postojna|Postojna|45.77|14.21|S
SI|Prebold|Prebold|46.24|15.09|S
SI|Preddvor|Preddvor|46.30|14.42|S
SI|Prevalje|Prevalje|46.56|14.88|S
SI|Ptuj|Ptuj|46.42|15.87|SN
SI|Puconci|Puconci|46.72|16.10|S
SI|Rače-Fram|Rače|46.45|15.63|S
SI|Radeče|Radeče|46.07|15.18|S
SI|Radenci|Radenci|46.62|16.05|S
SI|Radlje ob Dravi|Radlje ob Dravi|46.61|15.24|S
SI|Radovljica|Radovljica|46.34|14.21|S
SI|Ravne na Koroškem|Ravne na Koroškem|46.55|14.96|S
SI|Razkrižje|Razkrižje|46.52|16.27|S
SI|Rečica ob Savinji|Rečica ob Savinji|46.32|14.92|S
SI|Renče-Vogrsko|Bukovica|45.90|13.68|S
SI|Ribnica|Ribnica|45.74|14.73|S
SI|Ribnica na Pohorju|Ribnica na Pohorju|46.54|15.27|S
SI|Rogaška Slatina|Rogaška Slatina|46.25|15.63|S
SI|Rogašovci|Rogašovci|46.81|16.03|S
SI|Rogatec|Rogatec|46.23|15.70|S
SI|Ruše|Ruše|46.52|15.48|S
SI|Šalovci|Šalovci|46.85|16.26|S
SI|Selnica ob Dravi|Selnica ob Dravi|46.55|15.49|S
SI|Semič|Semič|45.65|15.18|S
SI|Šempeter-Vrtojba|Šempeter pri Gorici|45.93|13.64|S
SI|Šenčur|Šenčur|46.24|14.42|S
SI|Šentilj|Šentilj v Slovenskih goricah|46.69|15.71|S
SI|Šentjernej|Šentjernej|45.84|15.34|S
SI|Šentjur|Šentjur|46.27|15.41|S
SI|Šentrupert|Šentrupert|45.99|15.08|S
SI|Sevnica|Sevnica|46.01|15.30|S
SI|Sežana|Sežana|45.73|13.87|S
SI|Škocjan|Škocjan|45.92|15.31|S
SI|Škofja Loka|Škofja Loka|46.14|14.28|S
SI|Škofljica|Škofljica|45.98|14.57|S
SI|Slovenj Gradec|Slovenj Gradec|46.49|15.07|S
SI|Slovenska Bistrica|Slovenska Bistrica|46.39|15.57|S
SI|Slovenske Konjice|Slovenske Konjice|46.34|15.42|S
SI|Šmarje pri Jelšah|Šmarje pri Jelšah|46.23|15.52|S
SI|Šmarješke Toplice|Šmarješke Toplice|45.87|15.23|S
SI|Šmartno ob Paki|Šmartno ob Paki|46.33|15.03|S
SI|Šmartno pri Litiji|Šmartno pri Litiji|46.05|14.84|S
SI|Sodražica|Sodražica|45.76|14.64|S
SI|Solčava|Solčava|46.40|14.68|S
SI|Šoštanj|Šoštanj|46.38|15.05|S
SI|Središče ob Dravi|Središče ob Dravi|46.40|16.27|S
SI|Starše|Starše|46.47|15.76|S
SI|Štore|Štore|46.22|15.31|S
SI|Straža|Straža|45.78|15.09|S
SI|Sveta Ana|Sveta Ana v Slovenskih goricah|46.65|15.85|S
SI|Sveta Trojica v Slovenskih goricah|Sveta Trojica v Slovenskih goricah|46.57|15.88|S
SI|Sveti Andraž v Slovenskih goricah|Vitomarci|46.52|15.95|S
SI|Sveti Jurij ob Ščavnici|Sveti Jurij ob Ščavnici|46.57|16.02|S
SI|Sveti Jurij v Slovenskih goricah|Jurovski Dol|46.62|15.78|S
SI|Sveti Tomaž|Sveti Tomaž|46.48|16.08|S
SI|Tabor|Tabor|46.21|15.02|S
SI|Tišina|Tišina|46.65|16.08|S
SI|Tolmin|Tolmin|46.19|13.73|S
SI|Trbovlje|Trbovlje|46.15|15.05|SN
SI|Trebnje|Trebnje|45.91|15.01|S
SI|Trnovska vas|Trnovska vas|46.53|15.89|S
SI|Trzin|Trzin|46.13|14.56|S
SI|Tržič|Tržič|46.36|14.30|S
SI|Turnišče|Turnišče|46.61|16.32|S
SI|Velenje|Velenje|46.36|15.11|SN
SI|Velika Polana|Velika Polana|46.57|16.34|S
SI|Velike Lašče|Velike Lašče|45.83|14.64|S
SI|Veržej|Veržej|46.58|16.16|S
SI|Videm|Videm pri Ptuju|46.36|15.88|S
SI|Vipava|Vipava|45.84|13.96|S
SI|Vitanje|Vitanje|46.38|15.30|S
SI|Vodice|Vodice|46.19|14.49|S
SI|Vojnik|Vojnik|46.29|15.30|S
SI|Vransko|Vransko|46.24|14.95|S
SI|Vrhnika|Vrhnika|45.95|14.33|S
SI|Vuzenica|Vuzenica|46.60|15.17|S
SI|Zagorje ob Savi|Zagorje ob Savi|46.13|15.00|S
SI|Žalec|Žalec|46.25|15.17|S
SI|Zavrč|Zavrč|46.36|16.05|S
SI|Železniki|Železniki|46.23|14.17|S
SI|Žetale|Žetale|46.27|15.79|S
SI|Žiri|Žiri|46.05|14.11|S
SI|Žirovnica|Breznica|46.40|14.15|S
SI|Zreče|Zreče|46.42|15.37|S
SI|Žužemberk|Žužemberk|45.82|14.95|S
SB|Central|Tulagi|-9.10|160.15|SN
SB|Choiseul|Taro|-6.71|156.40|S
SB|Guadalcanal|Tandai|-9.42|159.90|S
SB|Honiara Capital Territory|Honiara|-9.43|159.95|SN
SB|Isabel|Buala|-8.15|159.59|SN
SB|Makira-Ulawa|Kirakira|-10.46|161.92|SN
SB|Malaita|Auki|-8.77|160.70|SN
SB|Rennell and Bellona|Tigoa|-11.56|160.06|S
SB|Temotu|Lata|-10.72|165.83|SN
SB|Western|Gizo|-8.11|156.84|SN
SB|Western|Noro|-8.23|157.20|N
SB|Western|Munda|-8.33|157.26|N
SB|Western|Nusa Roviana|-8.33|157.28|N
SO|Awdal|Borama|9.94|43.18|SN
SO|Bakool|Hudur|4.12|43.89|S
SO|Banadir|Mogadishu|2.05|45.32|SN
SO|Bari|Bosaso|11.28|49.18|SN
SO|Bay|Baidoa|3.11|43.65|SN
SO|Galgaduud|Dhusamareb|5.54|46.39|S
SO|Gedo|Garbaharey|3.33|42.22|S
SO|Hiran|Beledweyne|4.74|45.20|SN
SO|Lower Juba|Kismayo|-0.36|42.55|SN
SO|Lower Shabelle|Marka|1.71|44.77|S
SO|Middle Juba|Bu'ale|1.08|42.58|S
SO|Middle Shabelle|Jowhar|2.78|45.50|S
SO|Mudug|Galkayo|6.77|47.43|SN
SO|Nugal|Garowe|8.41|48.48|S
SO|Sanaag|Erigavo|10.62|47.37|S
SO|Sool|Las Anod|8.48|47.36|S
SO|Togdheer|Burao|9.52|45.53|SN
SO|Woqooyi Galbeed|Hargeisa|9.56|44.07|SN
SO|Woqooyi Galbeed|Berbera|10.44|45.01|N
ZA|Eastern Cape|Bhisho|-32.85|27.44|S
ZA|Free State|Bloemfontein|-29.12|26.22|S
ZA|Gauteng|Johannesburg|-26.20|28.05|SN
ZA|KwaZulu-Natal|Pietermaritzburg|-29.61|30.39|SN
ZA|Limpopo|Polokwane|-23.90|29.45|S
ZA|Mpumalanga|Mbombela|-25.47|30.97|S
ZA|North West|Mahikeng|-25.87|25.64|S
ZA|Northern Cape|Kimberley|-28.74|24.76|S
ZA|Western Cape|Cape Town|-33.93|18.42|SN
ZA|KwaZulu-Natal|Durban|-29.86|31.02|N
ZA|Gauteng|Pretoria|-25.75|28.19|N
ZA|Gauteng|Soweto|-26.25|27.85|N
ZA|Eastern Cape|Gqeberha|-33.96|25.62|N
ZA|Gauteng|Benoni|-26.19|28.32|N
ZA|Gauteng|Tembisa|-25.99|28.23|N
ZA|Eastern Cape|East London|-33.02|27.91|N
GS|-|-|||none
KR|Busan|Busan|35.18|129.07|SN
KR|Chungcheongbuk-do|Cheongju|36.64|127.49|S
KR|Chungcheongnam-do|Hongseong|36.60|126.66|S
KR|Daegu|Daegu|35.87|128.60|SN
KR|Daejeon|Daejeon|36.35|127.38|SN
KR|Gangwon Special Self-Governing Province|Chuncheon|37.88|127.73|S
KR|Gwangju|Gwangju|35.16|126.85|SN
KR|Gyeonggi-do|Suwon|37.26|127.03|SN
KR|Gyeongsangbuk-do|Andong|36.57|128.73|S
KR|Gyeongsangnam-do|Changwon|35.23|128.68|S
KR|Incheon|Incheon|37.46|126.70|SN
KR|Jeju Special Self-Governing Province|Jeju City|33.50|126.53|S
KR|Jeonbuk Special Self-Governing Province|Jeonju|35.82|127.15|S
KR|Jeollanam-do|Muan|34.99|126.48|S
KR|Sejong|Sejong|36.48|127.29|S
KR|Seoul|Seoul|37.57|126.98|SN
KR|Ulsan|Ulsan|35.54|129.31|SN
KR|Gyeonggi-do|Yongin|37.24|127.18|N
KR|Gyeonggi-do|Goyang|37.66|126.84|N
SS|Abyei Administrative Area|Abyei|9.60|28.43|S
SS|Central Equatoria|Juba|4.85|31.58|SN
SS|Eastern Equatoria|Torit|4.41|32.57|S
SS|Greater Pibor Administrative Area|Pibor|6.80|33.12|S
SS|Jonglei|Bor|6.21|31.56|SN
SS|Lakes|Rumbek|6.81|29.68|SN
SS|Northern Bahr el Ghazal|Aweil|8.77|27.40|SN
SS|Ruweng Administrative Area|Pariang|9.91|29.98|S
SS|Unity|Bentiu|9.26|29.80|SN
SS|Upper Nile|Malakal|9.53|31.66|SN
SS|Warrap|Kuajok|8.30|27.99|SN
SS|Western Bahr el Ghazal|Wau|7.70|27.99|SN
SS|Western Equatoria|Yambio|4.57|28.39|SN
SS|Central Equatoria|Yei|4.09|30.68|N
ES|Andalusia|Seville|37.39|-5.99|SN
ES|Aragon|Zaragoza|41.65|-0.89|SN
ES|Asturias|Oviedo|43.36|-5.85|S
ES|Balearic Islands|Palma|39.57|2.65|SN
ES|Basque Country|Vitoria-Gasteiz|42.85|-2.67|S
ES|Canary Islands|Las Palmas de Gran Canaria|28.12|-15.44|SN
ES|Canary Islands|Santa Cruz de Tenerife|28.46|-16.25|S
ES|Cantabria|Santander|43.46|-3.81|S
ES|Castile and León|Valladolid|41.65|-4.73|S
ES|Castile-La Mancha|Toledo|39.86|-4.03|S
ES|Catalonia|Barcelona|41.39|2.17|SN
ES|Ceuta|Ceuta|35.89|-5.32|S
ES|Extremadura|Mérida|38.92|-6.34|S
ES|Galicia|Santiago de Compostela|42.88|-8.54|S
ES|La Rioja|Logroño|42.47|-2.44|S
ES|Madrid|Madrid|40.42|-3.70|SN
ES|Melilla|Melilla|35.29|-2.94|S
ES|Murcia|Murcia|37.99|-1.13|SN
ES|Navarre|Pamplona|42.82|-1.64|S
ES|Valencian Community|Valencia|39.47|-0.38|SN
ES|Andalusia|Málaga|36.72|-4.42|N
ES|Valencian Community|Alicante|38.35|-0.48|N
LK|Central Province|Kandy|7.29|80.64|SN
LK|Eastern Province|Trincomalee|8.59|81.22|S
LK|North Central Province|Anuradhapura|8.31|80.40|S
LK|North Western Province|Kurunegala|7.49|80.36|S
LK|Northern Province|Jaffna|9.66|80.01|SN
LK|Sabaragamuwa Province|Ratnapura|6.68|80.40|S
LK|Southern Province|Galle|6.05|80.22|SN
LK|Uva Province|Badulla|6.99|81.06|S
LK|Western Province|Colombo|6.93|79.86|SN
LK|Western Province|Dehiwala-Mount Lavinia|6.85|79.87|N
LK|Western Province|Moratuwa|6.77|79.88|N
LK|Western Province|Negombo|7.21|79.84|N
LK|Western Province|Sri Jayawardenepura Kotte|6.90|79.90|N
LK|Eastern Province|Kalmunai|7.42|81.83|N
LK|Eastern Province|Batticaloa|7.72|81.70|N
BL|Saint Barthélemy|Gustavia|17.90|-62.85|SN
SH|Saint Helena|Jamestown|-15.93|-5.72|SN
SH|Ascension Island|Georgetown|-7.93|-14.41|SN
SH|Tristan da Cunha|Edinburgh of the Seven Seas|-37.07|-12.31|SN
SH|Saint Helena|Half Tree Hollow|-15.93|-5.72|N
SH|Saint Helena|Longwood|-15.95|-5.67|N
SH|Saint Helena|Saint Paul's|-15.96|-5.72|N
SH|Saint Helena|Levelwood|-15.97|-5.66|N
SH|Saint Helena|Sandy Bay|-15.98|-5.72|N
SH|Saint Helena|Blue Hill|-15.97|-5.76|N
SH|Saint Helena|Alarm Forest|-15.94|-5.70|N
KN|Christ Church Nichola Town|Nichola Town|17.36|-62.75|SN
KN|Saint Anne Sandy Point|Sandy Point Town|17.36|-62.84|SN
KN|Saint George Basseterre|Basseterre|17.30|-62.73|SN
KN|Saint George Gingerland|Market Shop|17.12|-62.55|S
KN|Saint James Windward|Newcastle|17.21|-62.60|S
KN|Saint John Capisterre|Dieppe Bay Town|17.41|-62.81|S
KN|Saint John Figtree|Figtree|17.12|-62.61|S
KN|Saint Mary Cayon|Cayon|17.35|-62.74|SN
KN|Saint Paul Capisterre|Saint Paul's|17.40|-62.82|SN
KN|Saint Paul Charlestown|Charlestown|17.13|-62.62|SN
KN|Saint Peter Basseterre|Monkey Hill|17.32|-62.71|S
KN|Saint Thomas Lowland|Cotton Ground|17.17|-62.62|S
KN|Saint Thomas Middle Island|Middle Island|17.32|-62.79|S
KN|Trinity Palmetto Point|Palmetto Point|17.31|-62.77|S
KN|Saint Thomas Middle Island|Old Road Town|17.32|-62.81|N
KN|Saint Peter Basseterre|Conaree|17.31|-62.70|N
KN|Saint John Figtree|Bath Village|17.13|-62.62|N
KN|Saint George Basseterre|Frigate Bay|17.29|-62.70|N
LC|Anse la Raye|Anse la Raye|13.94|-61.04|S
LC|Canaries|Canaries|13.90|-61.07|S
LC|Castries|Castries|14.00|-61.01|SN
LC|Choiseul|Choiseul|13.77|-61.05|SN
LC|Dennery|Dennery|13.91|-60.89|SN
LC|Gros Islet|Gros Islet|14.08|-60.95|SN
LC|Laborie|Laborie|13.75|-60.99|SN
LC|Micoud|Micoud|13.82|-60.90|SN
LC|Soufrière|Soufrière|13.86|-61.06|SN
LC|Vieux Fort|Vieux Fort|13.72|-60.95|SN
LC|Castries|Bisee|14.02|-60.97|N
LC|Castries|Ciceron|13.99|-61.01|N
```

### Naming caveats

SI — All 212 municipalities are included as first-level local-government units, rather than the 12 statistical regions. Several municipal seats differ from their municipality names, including Brda–Dobrovo, Bloke–Nova vas and Žirovnica–Breznica.

SB — Nine provinces plus Honiara Capital Territory. Honiara serves as Guadalcanal Province's administrative centre but is separately governed; Tandai is used as an in-province geographic reference.

SO — Eighteen traditional regions, including the Somaliland-administered north. Somaliland's independence and the status of Sool and Sanaag are disputed; newer federal-member-state boundaries do not always coincide with these historical regions. Berbera is within the newer Sahil division used by Somaliland.

ZA — Nine provinces. Bhisho is also Bisho; Mbombela was formerly Nelspruit; Mahikeng was formerly Mafikeng; Gqeberha was formerly Port Elizabeth. Large-city rankings distinguish named urban settlements from metropolitan municipalities.

GS — No permanent civilian population. Grytviken and King Edward Point have temporary or rotating personnel, but the requested uninhabited-territory convention is applied.

KR — Seventeen first-level divisions. Gangwon and Jeonbuk now have special self-governing provincial status; Jeju already held that status. South Jeolla's administrative seat is in Muan, and South Chungcheong's is in the Hongseong area.

SS — Ten states plus Abyei, Greater Pibor and Ruweng administrative areas. Abyei's sovereignty and administration remain disputed with Sudan; conflict and displacement affect population estimates.

ES — Seventeen autonomous communities plus Ceuta and Melilla. The Canary Islands have two capitals, Las Palmas de Gran Canaria and Santa Cruz de Tenerife. Ceuta and Melilla are Spanish autonomous cities on the North African coast.

LK — Nine provinces. Colombo is the principal city and Western Province capital; Sri Jayawardenepura Kotte is the national legislative and administrative capital. Population comparisons depend on municipal versus continuous urban-area boundaries.

BL — Saint Barthélemy is a single French overseas collectivity with Gustavia as its principal town; no separate first-level provinces or regions.

SH — Three constituent territories: Saint Helena, Ascension Island and Tristan da Cunha. The additional N entries are villages or settlement areas rather than independently incorporated cities.

KN — Fourteen parishes across Saint Kitts and Nevis. Basseterre is the federal capital, while Charlestown is Nevis's main town. Old Road Town belongs to Saint Thomas Middle Island parish.

LC — Ten districts/quarters. Gros Islet and Castries are major population centres; Bisee and Ciceron are populated urban localities within the wider Castries area. Some sources use alternative population rankings based on district rather than settlement totals.

### Points still open

- Round 11: FM — Tol; MH — Airuk, Jabat, Lib; MR — Guerou; MU — Vingt Cinq, Raphael Island.
- Round 12: NL — The Bottom, Oranjestad.
- Round 13: MP — Agrihan; PW — Ngaramasch, Tobi, Dongosaru.
- Round 14: PA — Gaigirgordub.
- Round 15: RS — Pristina, Gjilan, Peja, Prizren. These are Kosovo cities and may require checking under ISO code XK rather than RS.
- Round 16: 372 reference rows prepared across 13 countries; Overture business-data coverage is pending.
- Special checks: Solomon Islands' small provincial settlements, Somalia's disputed regional boundaries, South Sudan's administrative areas, Saint Helena's remote settlements, and Slovenia's small municipal seats.
- Population matching: City-proper, municipality and metropolitan-area definitions should be normalized before using N entries as strict completeness checks.


---

## Claude Code - 2026-11-08 21:04 UTC - 17_claude.md - attachments: none

## Check of your message-16 list
Round 16: 372 reference lines, 371 cities, 367 with business data (99 %).
Not covered: - SB: 12/13 cities covered, 1,085 businesses near them; no data at: Tigoa
Not covered: - SO: 18/19 cities covered, 4,841 businesses near them; no data at: Bu'ale
Not covered: - SS: 12/14 cities covered, 1,537 businesses near them; no data at: Abyei, Pariang

Same format again:


## Message 17 of 19 - countries
St. Martin (MF), St. Pierre & Miquelon (PM), St. Vincent & Grenadines (VC), Sudan (SD), Suriname (SR), Svalbard & Jan Mayen (SJ), Sweden (SE), Switzerland (CH), Syria (SY), Taiwan (TW), Tajikistan (TJ), Tanzania (TZ), Thailand (TH)

For EACH country above give:
1. every first-level administrative division (state / province / region / governorate ... as it is today),
   with its capital or largest city (kind S);
2. the 10 largest cities of the country by population (kind N) - fewer if the country has fewer.
   A city can appear as both S and N; list it once with kind SN.
Uninhabited territories: one line `CC|-|-|||none`.

Output ONLY one code block, one line per city, pipe-separated, no header, no commentary inside it:
`CC|state|city|lat|lon|kind`
- CC = ISO code above; state and city in English (the name a map would show); lat / lon with 2 decimals.
After the code block: one line per country with any naming caveat (renamed divisions, disputed areas),
then the list of points still open.


---

## ChatGPT (Extra High) - 2026-11-08 21:11 UTC - saved as 17_chatgpt.md

```
MF|Saint Martin|Marigot|18.07|-63.08|SN
MF|Saint Martin|Grand Case|18.10|-63.05|N
MF|Saint Martin|Concordia|18.06|-63.08|N
MF|Saint Martin|Sandy Ground|18.06|-63.10|N
MF|Saint Martin|Quartier d'Orléans|18.07|-63.04|N
MF|Saint Martin|Colombier|18.07|-63.06|N
MF|Saint Martin|Agrément|18.08|-63.08|N
MF|Saint Martin|Oyster Pond|18.06|-63.02|N
MF|Saint Martin|Saint-James|18.06|-63.09|N
PM|Saint-Pierre|Saint-Pierre|46.78|-56.18|SN
PM|Miquelon-Langlade|Miquelon|47.10|-56.38|SN
VC|Charlotte|Georgetown|13.29|-61.12|SN
VC|Grenadines|Port Elizabeth|13.01|-61.24|SN
VC|Saint Andrew|Layou|13.20|-61.27|SN
VC|Saint David|Chateaubelair|13.29|-61.24|SN
VC|Saint George|Kingstown|13.16|-61.22|SN
VC|Saint Patrick|Barrouallie|13.24|-61.27|SN
VC|Saint George|Calliaqua|13.13|-61.20|N
VC|Charlotte|Biabou|13.20|-61.13|N
VC|Saint George|Arnos Vale|13.14|-61.20|N
VC|Charlotte|South Rivers|13.24|-61.12|N
SD|Blue Nile|Ad Damazin|11.79|34.36|S
SD|Central Darfur|Zalingei|12.91|23.47|S
SD|East Darfur|Ed Daein|11.46|26.13|S
SD|Gedaref|Gedaref|14.04|35.38|SN
SD|Gezira|Wad Madani|14.40|33.52|SN
SD|Kassala|Kassala|15.45|36.40|SN
SD|Khartoum|Khartoum|15.59|32.53|SN
SD|North Darfur|El Fasher|13.63|25.35|S
SD|North Kordofan|El Obeid|13.18|30.22|SN
SD|Northern|Dongola|19.17|30.48|S
SD|Red Sea|Port Sudan|19.62|37.22|SN
SD|River Nile|Ed Damer|17.59|33.96|S
SD|Sennar|Singa|13.15|33.93|S
SD|South Darfur|Nyala|12.05|24.88|SN
SD|South Kordofan|Kadugli|11.01|29.72|S
SD|West Darfur|El Geneina|13.45|22.45|S
SD|West Kordofan|El Fula|11.73|28.35|S
SD|White Nile|Rabak|13.18|32.74|S
SD|Khartoum|Omdurman|15.64|32.48|N
SD|Khartoum|Khartoum North|15.63|32.63|N
SD|White Nile|Kosti|13.16|32.66|N
SR|Brokopondo|Brokopondo|5.06|-54.98|S
SR|Commewijne|Nieuw Amsterdam|5.89|-55.09|SN
SR|Coronie|Totness|5.88|-56.33|S
SR|Marowijne|Albina|5.50|-54.06|SN
SR|Nickerie|Nieuw Nickerie|5.95|-56.99|SN
SR|Para|Onverwacht|5.60|-55.19|S
SR|Paramaribo|Paramaribo|5.85|-55.17|SN
SR|Saramacca|Groningen|5.80|-55.47|SN
SR|Sipaliwini|Apoera|5.19|-57.16|S
SR|Wanica|Lelydorp|5.70|-55.23|SN
SR|Marowijne|Moengo|5.62|-54.40|N
SR|Commewijne|Mariënburg|5.87|-55.04|N
SR|Nickerie|Wageningen|5.77|-56.69|N
SR|Brokopondo|Brownsweg|5.02|-55.17|N
SJ|Svalbard|Longyearbyen|78.22|15.65|SN
SJ|Jan Mayen|Olonkinbyen|70.92|-8.72|S
SJ|Svalbard|Barentsburg|78.06|14.23|N
SJ|Svalbard|Ny-Ålesund|78.92|11.93|N
SE|Blekinge|Karlskrona|56.16|15.59|S
SE|Dalarna|Falun|60.61|15.63|S
SE|Gotland|Visby|57.64|18.29|S
SE|Gävleborg|Gävle|60.67|17.14|S
SE|Halland|Halmstad|56.67|12.86|S
SE|Jämtland|Östersund|63.18|14.64|S
SE|Jönköping|Jönköping|57.78|14.16|SN
SE|Kalmar|Kalmar|56.66|16.36|S
SE|Kronoberg|Växjö|56.88|14.81|S
SE|Norrbotten|Luleå|65.58|22.15|S
SE|Skåne|Malmö|55.60|13.00|SN
SE|Stockholm|Stockholm|59.33|18.07|SN
SE|Södermanland|Nyköping|58.75|17.01|S
SE|Uppsala|Uppsala|59.86|17.64|SN
SE|Värmland|Karlstad|59.38|13.50|S
SE|Västerbotten|Umeå|63.83|20.26|S
SE|Västernorrland|Härnösand|62.63|17.94|S
SE|Västmanland|Västerås|59.61|16.54|SN
SE|Västra Götaland|Gothenburg|57.71|11.97|SN
SE|Örebro|Örebro|59.27|15.21|SN
SE|Östergötland|Linköping|58.41|15.63|SN
SE|Skåne|Helsingborg|56.05|12.69|N
SE|Östergötland|Norrköping|58.59|16.18|N
CH|Aargau|Aarau|47.39|8.05|S
CH|Appenzell Ausserrhoden|Herisau|47.39|9.28|S
CH|Appenzell Innerrhoden|Appenzell|47.33|9.41|S
CH|Basel-Landschaft|Liestal|47.48|7.73|S
CH|Basel-Stadt|Basel|47.56|7.59|SN
CH|Bern|Bern|46.95|7.45|SN
CH|Fribourg|Fribourg|46.81|7.16|S
CH|Geneva|Geneva|46.20|6.14|SN
CH|Glarus|Glarus|47.04|9.07|S
CH|Graubünden|Chur|46.85|9.53|S
CH|Jura|Delémont|47.37|7.34|S
CH|Lucerne|Lucerne|47.05|8.31|SN
CH|Neuchâtel|Neuchâtel|46.99|6.93|S
CH|Nidwalden|Stans|46.96|8.37|S
CH|Obwalden|Sarnen|46.90|8.25|S
CH|Schaffhausen|Schaffhausen|47.70|8.63|S
CH|Schwyz|Schwyz|47.02|8.65|S
CH|Solothurn|Solothurn|47.21|7.54|S
CH|St. Gallen|St. Gallen|47.42|9.38|SN
CH|Thurgau|Frauenfeld|47.56|8.90|S
CH|Ticino|Bellinzona|46.19|9.02|S
CH|Uri|Altdorf|46.88|8.64|S
CH|Valais|Sion|46.23|7.36|S
CH|Vaud|Lausanne|46.52|6.63|SN
CH|Zug|Zug|47.17|8.52|S
CH|Zurich|Zurich|47.38|8.54|SN
CH|Zurich|Winterthur|47.50|8.73|N
CH|Ticino|Lugano|46.00|8.95|N
CH|Bern|Biel/Bienne|47.14|7.25|N
SY|Aleppo|Aleppo|36.20|37.16|SN
SY|Al-Hasakah|Al-Hasakah|36.50|40.75|SN
SY|Ar-Raqqa|Raqqa|35.95|39.01|SN
SY|As-Suwayda|As-Suwayda|32.71|36.57|S
SY|Damascus|Damascus|33.51|36.29|SN
SY|Daraa|Daraa|32.62|36.10|S
SY|Deir ez-Zor|Deir ez-Zor|35.34|40.14|SN
SY|Hama|Hama|35.13|36.76|SN
SY|Homs|Homs|34.73|36.71|SN
SY|Idlib|Idlib|35.93|36.63|S
SY|Latakia|Latakia|35.52|35.78|SN
SY|Quneitra|Baath City|33.17|35.87|S
SY|Rif Dimashq|Douma|33.57|36.40|S
SY|Tartus|Tartus|34.89|35.89|S
SY|Al-Hasakah|Qamishli|37.05|41.23|N
SY|Aleppo|Manbij|36.53|37.96|N
TW|Changhua County|Changhua|24.07|120.54|SN
TW|Chiayi City|Chiayi|23.48|120.45|SN
TW|Chiayi County|Taibao|23.46|120.33|S
TW|Hsinchu City|Hsinchu|24.80|120.97|SN
TW|Hsinchu County|Zhubei|24.84|121.01|S
TW|Hualien County|Hualien|23.98|121.60|S
TW|Kaohsiung|Kaohsiung|22.63|120.30|SN
TW|Keelung City|Keelung|25.13|121.74|SN
TW|Kinmen County|Jincheng|24.43|118.32|S
TW|Lienchiang County|Jieshou|26.15|119.94|S
TW|Miaoli County|Miaoli|24.56|120.82|S
TW|Nantou County|Nantou|23.91|120.69|S
TW|New Taipei City|New Taipei City|25.01|121.46|SN
TW|Penghu County|Magong|23.57|119.57|S
TW|Pingtung County|Pingtung|22.67|120.49|S
TW|Taichung|Taichung|24.15|120.67|SN
TW|Tainan|Tainan|22.99|120.20|SN
TW|Taipei|Taipei|25.03|121.57|SN
TW|Taitung County|Taitung|22.76|121.14|S
TW|Taoyuan|Taoyuan|24.99|121.30|SN
TW|Yilan County|Yilan|24.76|121.75|S
TW|Yunlin County|Douliu|23.71|120.54|S
TJ|Districts of Republican Subordination|Vahdat|38.56|69.02|SN
TJ|Dushanbe|Dushanbe|38.56|68.79|SN
TJ|Gorno-Badakhshan|Khorugh|37.49|71.55|S
TJ|Khatlon|Bokhtar|37.84|68.78|SN
TJ|Sughd|Khujand|40.28|69.62|SN
TJ|Khatlon|Kulob|37.91|69.78|N
TJ|Sughd|Istaravshan|39.91|69.00|N
TJ|Districts of Republican Subordination|Tursunzoda|38.51|68.23|N
TJ|Sughd|Isfara|40.13|70.63|N
TJ|Sughd|Konibodom|40.29|70.43|N
TJ|Sughd|Panjakent|39.50|67.61|N
TZ|Arusha|Arusha|-3.39|36.68|SN
TZ|Dar es Salaam|Dar es Salaam|-6.79|39.28|SN
TZ|Dodoma|Dodoma|-6.16|35.75|SN
TZ|Geita|Geita|-2.87|32.23|SN
TZ|Iringa|Iringa|-7.77|35.69|S
TZ|Kagera|Bukoba|-1.33|31.81|S
TZ|Kaskazini Pemba|Wete|-5.06|39.73|S
TZ|Kaskazini Unguja|Mkokotoni|-5.88|39.26|S
TZ|Katavi|Mpanda|-6.34|31.07|S
TZ|Kigoma|Kigoma|-4.88|29.63|S
TZ|Kilimanjaro|Moshi|-3.35|37.34|S
TZ|Kusini Pemba|Chake Chake|-5.25|39.77|S
TZ|Kusini Unguja|Koani|-6.13|39.28|S
TZ|Lindi|Lindi|-10.00|39.72|S
TZ|Manyara|Babati|-4.22|35.75|S
TZ|Mara|Musoma|-1.50|33.80|S
TZ|Mbeya|Mbeya|-8.91|33.46|SN
TZ|Mjini Magharibi|Zanzibar City|-6.16|39.19|SN
TZ|Morogoro|Morogoro|-6.82|37.66|SN
TZ|Mtwara|Mtwara|-10.27|40.18|S
TZ|Mwanza|Mwanza|-2.52|32.90|SN
TZ|Njombe|Njombe|-9.33|34.77|S
TZ|Pwani|Kibaha|-6.77|38.91|S
TZ|Rukwa|Sumbawanga|-7.97|31.62|S
TZ|Ruvuma|Songea|-10.68|35.65|S
TZ|Shinyanga|Shinyanga|-3.66|33.42|S
TZ|Simiyu|Bariadi|-2.79|33.99|S
TZ|Singida|Singida|-4.82|34.74|S
TZ|Songwe|Vwawa|-9.11|32.93|S
TZ|Tabora|Tabora|-5.02|32.80|S
TZ|Tanga|Tanga|-5.07|39.10|SN
TZ|Shinyanga|Kahama|-3.83|32.60|N
TH|Amnat Charoen|Amnat Charoen|15.86|104.63|S
TH|Ang Thong|Ang Thong|14.59|100.46|S
TH|Bangkok|Bangkok|13.75|100.50|SN
TH|Bueng Kan|Bueng Kan|18.36|103.65|S
TH|Buriram|Buriram|14.99|103.10|S
TH|Chachoengsao|Chachoengsao|13.69|101.07|S
TH|Chai Nat|Chai Nat|15.19|100.13|S
TH|Chaiyaphum|Chaiyaphum|15.81|102.03|S
TH|Chanthaburi|Chanthaburi|12.61|102.10|S
TH|Chiang Mai|Chiang Mai|18.79|98.99|SN
TH|Chiang Rai|Chiang Rai|19.91|99.83|S
TH|Chonburi|Chonburi|13.36|100.98|SN
TH|Chumphon|Chumphon|10.50|99.18|S
TH|Kalasin|Kalasin|16.43|103.51|S
TH|Kamphaeng Phet|Kamphaeng Phet|16.48|99.52|S
TH|Kanchanaburi|Kanchanaburi|14.02|99.53|S
TH|Khon Kaen|Khon Kaen|16.44|102.84|SN
TH|Krabi|Krabi|8.06|98.92|S
TH|Lampang|Lampang|18.29|99.49|S
TH|Lamphun|Lamphun|18.58|99.01|S
TH|Loei|Loei|17.49|101.73|S
TH|Lopburi|Lopburi|14.80|100.65|SN
TH|Mae Hong Son|Mae Hong Son|19.30|97.97|S
TH|Maha Sarakham|Maha Sarakham|16.18|103.30|S
TH|Mukdahan|Mukdahan|16.54|104.72|S
TH|Nakhon Nayok|Nakhon Nayok|14.20|101.21|S
TH|Nakhon Pathom|Nakhon Pathom|13.82|100.06|SN
TH|Nakhon Phanom|Nakhon Phanom|17.41|104.78|S
TH|Nakhon Ratchasima|Nakhon Ratchasima|14.98|102.10|SN
TH|Nakhon Sawan|Nakhon Sawan|15.70|100.14|S
TH|Nakhon Si Thammarat|Nakhon Si Thammarat|8.43|99.96|S
TH|Nan|Nan|18.78|100.78|S
TH|Narathiwat|Narathiwat|6.43|101.82|S
TH|Nong Bua Lamphu|Nong Bua Lamphu|17.21|102.44|S
TH|Nong Khai|Nong Khai|17.88|102.74|S
TH|Nonthaburi|Nonthaburi|13.86|100.51|S
TH|Pathum Thani|Pathum Thani|14.02|100.53|S
TH|Pattani|Pattani|6.87|101.25|S
TH|Phang Nga|Phang Nga|8.45|98.53|S
TH|Phatthalung|Phatthalung|7.62|100.08|S
TH|Phayao|Phayao|19.17|99.90|S
TH|Phetchabun|Phetchabun|16.42|101.16|S
TH|Phetchaburi|Phetchaburi|13.11|99.94|S
TH|Phichit|Phichit|16.44|100.35|S
TH|Phitsanulok|Phitsanulok|16.82|100.26|S
TH|Phra Nakhon Si Ayutthaya|Ayutthaya|14.36|100.58|S
TH|Phrae|Phrae|18.14|100.14|S
TH|Phuket|Phuket|7.89|98.40|SN
TH|Prachinburi|Prachinburi|14.05|101.37|S
TH|Prachuap Khiri Khan|Prachuap Khiri Khan|11.81|99.80|S
TH|Ranong|Ranong|9.97|98.63|S
TH|Ratchaburi|Ratchaburi|13.54|99.82|S
TH|Rayong|Rayong|12.68|101.28|S
TH|Roi Et|Roi Et|16.05|103.65|S
TH|Sa Kaeo|Sa Kaeo|13.81|102.07|S
TH|Sakon Nakhon|Sakon Nakhon|17.16|104.15|S
TH|Samut Prakan|Samut Prakan|13.60|100.60|S
TH|Samut Sakhon|Samut Sakhon|13.55|100.27|S
TH|Samut Songkhram|Samut Songkhram|13.41|100.00|S
TH|Saraburi|Saraburi|14.53|100.91|S
TH|Satun|Satun|6.62|100.07|S
TH|Sing Buri|Sing Buri|14.89|100.40|S
TH|Sisaket|Sisaket|15.12|104.33|S
TH|Songkhla|Songkhla|7.20|100.60|S
TH|Sukhothai|Sukhothai|17.01|99.82|S
TH|Suphan Buri|Suphan Buri|14.47|100.12|S
TH|Surat Thani|Surat Thani|9.14|99.33|S
TH|Surin|Surin|14.88|103.49|S
TH|Tak|Tak|16.87|99.13|S
TH|Trang|Trang|7.56|99.61|S
TH|Trat|Trat|12.24|102.52|S
TH|Ubon Ratchathani|Ubon Ratchathani|15.24|104.85|S
TH|Udon Thani|Udon Thani|17.42|102.79|S
TH|Uthai Thani|Uthai Thani|15.38|100.02|S
TH|Uttaradit|Uttaradit|17.62|100.10|S
TH|Yala|Yala|6.54|101.28|S
TH|Yasothon|Yasothon|15.79|104.15|S
TH|Songkhla|Hat Yai|7.01|100.47|N
TH|Chonburi|Pattaya|12.93|100.88|N
```

MF — French Saint Martin is one overseas collectivity, separate from Dutch Sint Maarten (SX). Marigot is its capital; Grand Case, Concordia and the other entries are populated neighborhoods rather than separate municipalities. Nine settlements are listed because only nine have usable population rankings.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://geodatakit.com\&sz=32)

CSV, JSON & GeoJSON · GeoDataKit



PM — Saint Pierre and Miquelon has two communes: Saint-Pierre and Miquelon-Langlade. Miquelon is the principal inhabited settlement of the latter; Langlade has no permanent population.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.saint-pierre-et-miquelon.gouv.fr\&sz=32)

saint-pierre-et-miquelon.gouv.fr



VC — Six parishes. Georgetown is the centre of Charlotte, Kingstown of Saint George, and Port Elizabeth of the Grenadines. Calliaqua, Arnos Vale and Biabou are included as additional populated settlements.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://geotaria.com\&sz=32)

Geotaria



SD — Eighteen states. Al Jazirah is also Gezira; Gedaref is also Al Qadarif; El Obeid is also Al-Ubayyid. Singa is the capital of Sennar State, distinct from Sennar town. Armed conflict since 2023 has caused extensive displacement, making historic population rankings unreliable as current resident counts.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://tran.sudanembassy-kw.com\&sz=32)

tran.sudanembassy-kw\.com+1



SR — Ten districts. Sipaliwini has no capital within the district and is administered from Paramaribo; Apoera is used solely as an in-district geographic reference. Nieuw Nickerie and Nieuw Amsterdam are also written with hyphens.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.opreisdoorsuriname.sr\&sz=32)

Op reis door Suriname+1



SJ — Svalbard and Jan Mayen are separate Arctic components grouped under one ISO code, not ordinary provinces. Longyearbyen is Svalbard's administrative centre; Olonkinbyen is a staffed station on Jan Mayen without a permanent civilian population. Barentsburg and Ny-Ålesund are small inhabited research or industrial settlements.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.regjeringen.no\&sz=32)

Svalbard+1



SE — Twenty-one counties (län). Gothenburg is Göteborg, Malmö retains its Swedish spelling, and Växjö is the seat of Kronoberg County. The ten N entries follow the 2025 municipality population ranking; municipality and continuous urban-area rankings differ.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.scb.se\&sz=32)

Statistikmyndigheten SCB+1



CH — Twenty-six cantons. Basel-Stadt and Basel-Landschaft are separate cantons; Appenzell Innerrhoden and Ausserrhoden are also separate. Graubünden is also Grisons; Valais is also Wallis; Biel/Bienne uses its bilingual name. N entries use the 2025 municipal population ranking.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.thelocal.ch\&sz=32)

The Local Switzerland+1



SY — Fourteen governorates. Rif Dimashq means Rural Damascus; Douma is its administrative centre. Quneitra's historic capital has been largely abandoned, so Baath City is used as the populated administrative reference; territorial control in the Golan Heights remains disputed. Recent estimates place Manbij among the ten largest urban settlements.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://en.wikipedia.org\&sz=32)

Wikipedia+1



TW — Twenty-two first-level local governments: six special municipalities, thirteen counties and three provincial cities. New Taipei City is represented by its Banqiao administrative centre; Jieshou is the administrative locality of Lienchiang County in the Matsu Islands. Taiwan's political status is disputed internationally.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://english.president.gov.tw\&sz=32)

english.president.gov.tw



TJ — Five first-level administrative territories. Bokhtar was formerly Qurghonteppa, and Gorno-Badakhshan is also abbreviated GBAO. The Districts of Republican Subordination are administered centrally from Dushanbe; Vahdat is used as a separate in-region reference so Dushanbe is not duplicated.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.adb.org\&sz=32)

Asian Development Bank+1



TZ — Thirty-one regions, including five in Zanzibar. Pwani is also called Coast Region; its headquarters is Kibaha. Songwe's headquarters is Vwawa, and the Zanzibar regions use the local names Kaskazini, Kusini and Mjini Magharibi. The ten N entries follow the 2022 census ranking, including Kahama and Geita.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://achpr.au.int\&sz=32)

African Human Rights Commission+1



TH — Seventy-six provinces plus Bangkok as a special administrative area. Phra Nakhon Si Ayutthaya is commonly shortened to Ayutthaya; Buriram is also Buri Ram; Sisaket is also Si Sa Ket. Pattaya is a special local administrative city inside Chonburi Province, not a separate province. The ten N entries use the 2026 UN urban-area ranking, which differs from municipal population rankings.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://mpdc.moc.go.th\&sz=32)

mpdc.moc.go.th+1



### Points still open

- Round 11: FM — Tol; MH — Airuk, Jabat, Lib; MR — Guerou; MU — Vingt Cinq, Raphael Island.
- Round 12: NL — The Bottom, Oranjestad.
- Round 13: MP — Agrihan; PW — Ngaramasch, Tobi, Dongosaru.
- Round 14: PA — Gaigirgordub.
- Round 15: RS — Pristina, Gjilan, Peja, Prizren. Check against Kosovo data rather than Serbian coverage.
- Round 16: SB — Tigoa; SO — Bu'ale; SS — Abyei, Pariang.
- Round 17: Compare the new reference points against Overture business data; coverage has not yet been verified.
- Special geographic checks: SJ — Olonkinbyen and Ny-Ålesund; SR — Apoera; VC — smaller Grenadine settlements; TW — Jieshou and offshore counties; TZ — smaller Zanzibar regional headquarters.
- Population consistency: Sudan and Syria require conflict-adjusted population interpretation. Thailand, Sweden and Taiwan require consistent definitions of municipality, city proper and urban area before strict population-ranking validation.


---

## Claude Code - 2026-11-08 21:12 UTC - 18_claude.md - attachments: none

## Check of your message-17 list
Round 17: 272 reference lines, 272 cities, 272 with business data (100 %).

Same format again:


## Message 18 of 19 - countries
Timor-Leste (TL), Togo (TG), Tokelau (TK), Tonga (TO), Trinidad & Tobago (TT), Tunisia (TN), Türkiye (TR), Turkmenistan (TM), Turks & Caicos Islands (TC), Tuvalu (TV), U.S. Outlying Islands (UM), U.S. Virgin Islands (VI), Uganda (UG)

For EACH country above give:
1. every first-level administrative division (state / province / region / governorate ... as it is today),
   with its capital or largest city (kind S);
2. the 10 largest cities of the country by population (kind N) - fewer if the country has fewer.
   A city can appear as both S and N; list it once with kind SN.
Uninhabited territories: one line `CC|-|-|||none`.

Output ONLY one code block, one line per city, pipe-separated, no header, no commentary inside it:
`CC|state|city|lat|lon|kind`
- CC = ISO code above; state and city in English (the name a map would show); lat / lon with 2 decimals.
After the code block: one line per country with any naming caveat (renamed divisions, disputed areas),
then the list of points still open.


---

## ChatGPT (Extra High) - 2026-11-08 21:24 UTC - saved as 18_chatgpt.md

```
TL|Aileu|Aileu|-8.73|125.57|S
TL|Ainaro|Ainaro|-8.99|125.51|SN
TL|Atauro|Vila Maumeta|-8.27|125.61|S
TL|Baucau|Baucau|-8.47|126.46|SN
TL|Bobonaro|Maliana|-8.99|125.22|SN
TL|Cova Lima|Suai|-9.31|125.26|SN
TL|Dili|Dili|-8.56|125.58|SN
TL|Ermera|Gleno|-8.72|125.44|SN
TL|Lautém|Lospalos|-8.52|127.00|SN
TL|Liquiçá|Liquiçá|-8.59|125.34|S
TL|Manatuto|Manatuto|-8.51|126.01|SN
TL|Manufahi|Same|-9.00|125.65|SN
TL|Oecusse|Pante Macassar|-9.20|124.38|SN
TL|Viqueque|Viqueque|-8.86|126.36|S
TG|Centrale|Sokodé|8.98|1.13|SN
TG|Grand Lomé Autonomous District|Lomé|6.13|1.22|SN
TG|Kara|Kara|9.55|1.19|SN
TG|Maritime|Tsévié|6.43|1.21|SN
TG|Plateaux|Atakpamé|7.53|1.13|SN
TG|Savanes|Dapaong|10.86|0.21|SN
TG|Plateaux|Kpalimé|6.90|0.63|N
TG|Plateaux|Anié|7.75|1.20|N
TG|Savanes|Cinkassé|11.10|0.01|N
TG|Plateaux|Notsé|6.95|1.17|N
TK|Atafu|Atafu|-8.55|-172.50|SN
TK|Fakaofo|Fakaofo|-9.37|-171.23|SN
TK|Nukunonu|Nukunonu|-9.20|-171.85|SN
TO|Eua|Ohonua|-21.34|-174.96|S
TO|Ha'apai|Pangai|-19.81|-174.35|S
TO|Niuas|Hihifo|-15.95|-173.77|S
TO|Tongatapu|Nuku'alofa|-21.14|-175.20|SN
TO|Vava'u|Neiafu|-18.65|-173.98|SN
TO|Tongatapu|Haveluloto|-21.15|-175.21|N
TO|Tongatapu|Tofoa-Koloua|-21.16|-175.23|N
TO|Tongatapu|Vaini|-21.19|-175.18|N
TO|Tongatapu|Ha'ateiho|-21.18|-175.23|N
TO|Tongatapu|Popua|-21.15|-175.18|N
TO|Tongatapu|Nukunuku|-21.13|-175.30|N
TO|Tongatapu|Pea|-21.17|-175.24|N
TO|Tongatapu|Lapaha|-21.18|-175.12|N
TT|Arima|Arima|10.64|-61.28|SN
TT|Chaguanas|Chaguanas|10.52|-61.41|SN
TT|Couva-Tabaquite-Talparo|Couva|10.42|-61.45|SN
TT|Diego Martin|Diego Martin|10.72|-61.56|SN
TT|Mayaro-Rio Claro|Rio Claro|10.30|-61.18|S
TT|Penal-Debe|Debe|10.20|-61.45|S
TT|Point Fortin|Point Fortin|10.17|-61.68|SN
TT|Port of Spain|Port of Spain|10.66|-61.52|SN
TT|Princes Town|Princes Town|10.27|-61.38|SN
TT|San Fernando|San Fernando|10.28|-61.47|SN
TT|San Juan-Laventille|San Juan|10.65|-61.45|SN
TT|Sangre Grande|Sangre Grande|10.59|-61.13|S
TT|Siparia|Siparia|10.14|-61.50|S
TT|Tobago|Scarborough|11.18|-60.74|S
TT|Tunapuna-Piarco|Tunapuna|10.65|-61.39|SN
TN|Ariana|Ariana|36.86|10.19|S
TN|Béja|Béja|36.73|9.18|S
TN|Ben Arous|Ben Arous|36.75|10.22|S
TN|Bizerte|Bizerte|37.27|9.87|SN
TN|Gabès|Gabès|33.88|10.10|S
TN|Gafsa|Gafsa|34.43|8.78|S
TN|Jendouba|Jendouba|36.50|8.78|S
TN|Kairouan|Kairouan|35.68|10.10|SN
TN|Kasserine|Kasserine|35.17|8.83|S
TN|Kebili|Kebili|33.70|8.97|S
TN|Kef|El Kef|36.17|8.70|S
TN|Mahdia|Mahdia|35.50|11.06|S
TN|Manouba|Manouba|36.81|10.10|S
TN|Medenine|Medenine|33.35|10.50|S
TN|Monastir|Monastir|35.78|10.83|S
TN|Nabeul|Nabeul|36.46|10.73|S
TN|Sfax|Sfax|34.74|10.76|SN
TN|Sidi Bouzid|Sidi Bouzid|35.04|9.48|S
TN|Siliana|Siliana|36.08|9.37|S
TN|Sousse|Sousse|35.83|10.64|SN
TN|Tataouine|Tataouine|32.93|10.45|S
TN|Tozeur|Tozeur|33.92|8.13|S
TN|Tunis|Tunis|36.81|10.18|SN
TN|Zaghouan|Zaghouan|36.40|10.14|S
TN|Ariana|La Soukra|36.88|10.25|N
TN|Ariana|Raoued|36.95|10.19|N
TN|Tunis|Sidi Hassine|36.75|10.11|N
TN|Ben Arous|El Mourouj|36.73|10.21|N
TN|Ariana|Mnihla|36.86|10.11|N
TR|Adana|Adana|37.00|35.32|S
TR|Adıyaman|Adıyaman|37.76|38.28|S
TR|Afyonkarahisar|Afyonkarahisar|38.76|30.54|S
TR|Ağrı|Ağrı|39.72|43.05|S
TR|Aksaray|Aksaray|38.37|34.03|S
TR|Amasya|Amasya|40.65|35.84|S
TR|Ankara|Ankara|39.93|32.86|SN
TR|Antalya|Antalya|36.90|30.70|SN
TR|Ardahan|Ardahan|41.11|42.70|S
TR|Artvin|Artvin|41.18|41.82|S
TR|Aydın|Aydın|37.84|27.85|S
TR|Balıkesir|Balıkesir|39.65|27.88|S
TR|Bartın|Bartın|41.63|32.34|S
TR|Batman|Batman|37.88|41.13|S
TR|Bayburt|Bayburt|40.26|40.23|S
TR|Bilecik|Bilecik|40.15|29.98|S
TR|Bingöl|Bingöl|38.89|40.50|S
TR|Bitlis|Bitlis|38.40|42.11|S
TR|Bolu|Bolu|40.73|31.61|S
TR|Burdur|Burdur|37.72|30.29|S
TR|Bursa|Bursa|40.19|29.06|SN
TR|Çanakkale|Çanakkale|40.15|26.41|S
TR|Çankırı|Çankırı|40.60|33.62|S
TR|Çorum|Çorum|40.55|34.96|S
TR|Denizli|Denizli|37.78|29.09|S
TR|Diyarbakır|Diyarbakır|37.91|40.23|S
TR|Düzce|Düzce|40.84|31.16|S
TR|Edirne|Edirne|41.68|26.56|S
TR|Elazığ|Elazığ|38.67|39.22|S
TR|Erzincan|Erzincan|39.75|39.49|S
TR|Erzurum|Erzurum|39.90|41.27|S
TR|Eskişehir|Eskişehir|39.77|30.52|SN
TR|Gaziantep|Gaziantep|37.07|37.38|SN
TR|Giresun|Giresun|40.92|38.39|S
TR|Gümüşhane|Gümüşhane|40.46|39.48|S
TR|Hakkâri|Hakkâri|37.58|43.74|S
TR|Hatay|Antakya|36.20|36.16|S
TR|Iğdır|Iğdır|39.92|44.04|S
TR|Isparta|Isparta|37.76|30.55|S
TR|İstanbul|Istanbul|41.01|28.98|SN
TR|İzmir|Izmir|38.42|27.14|SN
TR|Kahramanmaraş|Kahramanmaraş|37.58|36.94|S
TR|Karabük|Karabük|41.20|32.62|S
TR|Karaman|Karaman|37.18|33.22|S
TR|Kars|Kars|40.60|43.09|S
TR|Kastamonu|Kastamonu|41.39|33.78|S
TR|Kayseri|Kayseri|38.72|35.49|SN
TR|Kırıkkale|Kırıkkale|39.85|33.51|S
TR|Kırklareli|Kırklareli|41.74|27.23|S
TR|Kırşehir|Kırşehir|39.15|34.16|S
TR|Kilis|Kilis|36.72|37.12|S
TR|Kocaeli|İzmit|40.77|29.92|S
TR|Konya|Konya|37.87|32.48|SN
TR|Kütahya|Kütahya|39.42|29.98|S
TR|Malatya|Malatya|38.35|38.31|S
TR|Manisa|Manisa|38.61|27.43|S
TR|Mardin|Mardin|37.31|40.74|S
TR|Mersin|Mersin|36.80|34.63|S
TR|Muğla|Muğla|37.22|28.36|S
TR|Muş|Muş|38.74|41.49|S
TR|Nevşehir|Nevşehir|38.62|34.71|S
TR|Niğde|Niğde|37.97|34.68|S
TR|Ordu|Ordu|40.98|37.88|S
TR|Osmaniye|Osmaniye|37.07|36.25|S
TR|Rize|Rize|41.02|40.52|S
TR|Sakarya|Adapazarı|40.78|30.40|S
TR|Samsun|Samsun|41.29|36.33|S
TR|Şanlıurfa|Şanlıurfa|37.16|38.79|S
TR|Siirt|Siirt|37.93|41.94|S
TR|Sinop|Sinop|42.03|35.15|S
TR|Şırnak|Şırnak|37.52|42.46|S
TR|Sivas|Sivas|39.75|37.02|S
TR|Tekirdağ|Tekirdağ|40.98|27.51|S
TR|Tokat|Tokat|40.32|36.55|S
TR|Trabzon|Trabzon|41.00|39.72|S
TR|Tunceli|Tunceli|39.11|39.55|S
TR|Uşak|Uşak|38.68|29.41|S
TR|Van|Van|38.49|43.38|S
TR|Yalova|Yalova|40.66|29.27|S
TR|Yozgat|Yozgat|39.82|34.80|S
TR|Zonguldak|Zonguldak|41.45|31.79|S
TR|Ankara|Sincan|39.97|32.58|N
TM|Ahal|Anau|37.89|58.52|S
TM|Arkadag City|Arkadag|38.06|58.18|S
TM|Ashgabat City|Ashgabat|37.96|58.33|SN
TM|Balkan|Balkanabat|39.51|54.37|SN
TM|Dashoguz|Dashoguz|41.83|59.97|SN
TM|Lebap|Turkmenabat|39.07|63.58|SN
TM|Mary|Mary|37.59|61.83|SN
TM|Balkan|Turkmenbashi|40.02|52.96|N
TM|Ahal|Tejen|37.38|60.50|N
TM|Mary|Bayramaly|37.62|62.17|N
TM|Dashoguz|Köneürgench|42.33|59.16|N
TM|Ahal|Abadan|38.05|58.20|N
TC|Grand Turk|Cockburn Town|21.46|-71.14|SN
TC|Middle Caicos|Conch Bar|21.82|-71.82|S
TC|North Caicos|Kew|21.92|-72.00|SN
TC|Providenciales|Blue Hills|21.80|-72.27|SN
TC|Salt Cay|Balfour Town|21.33|-71.20|S
TC|South Caicos|Cockburn Harbour|21.49|-71.53|SN
TC|Providenciales|Five Cays|21.77|-72.26|N
TC|Providenciales|Wheeland|21.80|-72.32|N
TC|Providenciales|The Bight|21.78|-72.20|N
TC|Grand Turk|Palm Grove|21.48|-71.14|N
TC|North Caicos|Bottle Creek|21.89|-71.92|N
TC|North Caicos|Whitby|21.95|-71.97|N
TV|Funafuti|Vaiaku|-8.53|179.19|SN
TV|Nanumanga|Toga|-6.29|176.32|S
TV|Nanumea|Lolua|-5.67|176.11|S
TV|Nui|Tanrake|-7.25|177.15|S
TV|Niutao|Kulia|-6.11|177.34|SN
TV|Nukufetau|Savave|-8.02|178.31|S
TV|Nukulaelae|Pepesala|-9.37|179.81|S
TV|Vaitupu|Asau|-7.49|178.68|S
TV|Funafuti|Fakaifou|-8.52|179.20|N
TV|Funafuti|Lofeagai|-8.51|179.20|N
TV|Funafuti|Alapi|-8.52|179.20|N
TV|Funafuti|Senala|-8.52|179.20|N
TV|Funafuti|Tekavatoetoe|-8.51|179.20|N
TV|Funafuti|Teone|-8.50|179.20|N
TV|Nukufetau|Aulotu|-8.02|178.31|N
TV|Nui|Alamoni-Maiaki|-7.25|177.15|N
UM|-|-|||none
VI|Saint Croix|Christiansted|17.74|-64.71|SN
VI|Saint John|Cruz Bay|18.32|-64.78|SN
VI|Saint Thomas|Charlotte Amalie|18.34|-64.93|SN
VI|Saint Thomas|Tutu|18.34|-64.89|N
VI|Saint Thomas|Charlotte Amalie West|18.34|-64.96|N
VI|Saint Thomas|Charlotte Amalie East|18.33|-64.92|N
VI|Saint Croix|Frederiksted Southeast|17.70|-64.88|N
VI|Saint John|Coral Bay|18.34|-64.72|N
VI|Saint Croix|Frederiksted|17.71|-64.88|N
VI|Saint Thomas|Red Hook|18.33|-64.85|N
UG|Abim|Abim|2.70|33.66|S
UG|Adjumani|Adjumani|3.37|31.79|S
UG|Agago|Patongo|2.96|33.31|S
UG|Alebtong|Alebtong|2.25|33.30|S
UG|Amolatar|Amolatar|1.63|32.81|S
UG|Amudat|Amudat|1.95|34.94|S
UG|Amuria|Amuria|2.03|33.65|S
UG|Amuru|Amuru|2.81|31.85|S
UG|Apac|Apac|1.98|32.54|S
UG|Arua District|Vurra|3.01|30.94|S
UG|Budaka|Budaka|1.00|33.95|S
UG|Bududa|Bududa|1.01|34.34|S
UG|Bugiri|Bugiri|0.57|33.74|S
UG|Bugweri|Busembatia|0.77|33.60|S
UG|Buhweju|Nsiika|-0.29|30.30|S
UG|Buikwe|Buikwe|0.34|33.00|S
UG|Bukedea|Bukedea|1.35|34.04|S
UG|Bukomansimbi|Bukomansimbi|-0.19|31.60|S
UG|Bukwo|Bukwo|1.28|34.75|S
UG|Bulambuli|Bulambuli|1.17|34.36|S
UG|Buliisa|Buliisa|2.12|31.41|S
UG|Bundibugyo|Bundibugyo|0.70|30.06|S
UG|Bunyangabu|Kibiito|0.32|30.20|S
UG|Bushenyi|Bushenyi|-0.54|30.18|S
UG|Busia|Busia|0.47|34.09|S
UG|Butaleja|Butaleja|0.91|33.95|S
UG|Butambala|Gombe|-0.18|32.12|S
UG|Butebo|Butebo|1.20|33.93|S
UG|Buvuma|Kitamilo|0.23|33.27|S
UG|Buyende|Buyende|1.15|33.15|S
UG|Dokolo|Dokolo|1.92|33.17|S
UG|Gomba|Kanoni|-0.26|31.80|S
UG|Gulu District|Awach|2.87|32.44|S
UG|Hoima District|Kigorobya|1.62|31.31|S
UG|Ibanda|Ibanda|-0.13|30.49|S
UG|Iganga|Iganga|0.61|33.48|S
UG|Isingiro|Isingiro|-0.82|30.83|S
UG|Jinja District|Buwenge|0.62|33.17|S
UG|Kaabong|Kaabong|3.51|34.14|S
UG|Kabale|Kabale|-1.25|29.99|S
UG|Kabarole|Busoro|0.63|30.19|S
UG|Kaberamaido|Kaberamaido|1.76|33.16|S
UG|Kagadi|Kagadi|0.94|30.81|S
UG|Kakumiro|Kakumiro|0.78|31.32|S
UG|Kalaki|Kalaki|1.87|33.31|S
UG|Kalangala|Kalangala|-0.32|32.29|S
UG|Kaliro|Kaliro|0.90|33.50|S
UG|Kalungu|Kalungu|-0.17|31.76|S
UG|Kampala Capital City|Kampala|0.32|32.58|SN
UG|Kamuli|Kamuli|0.95|33.12|S
UG|Kamwenge|Kamwenge|0.19|30.45|S
UG|Kanungu|Kanungu|-0.96|29.79|S
UG|Kapchorwa|Kapchorwa|1.40|34.45|S
UG|Kapelebyong|Kapelebyong|2.23|33.73|S
UG|Karenga|Karenga|3.72|33.78|S
UG|Kasese|Kasese|0.18|30.08|S
UG|Kassanda|Kassanda|0.62|31.82|S
UG|Katakwi|Katakwi|1.91|34.00|S
UG|Kayunga|Kayunga|0.70|32.90|S
UG|Kazo|Kazo|-0.05|30.78|S
UG|Kibaale|Kibaale|0.78|31.06|S
UG|Kiboga|Kiboga|0.92|31.77|S
UG|Kibuku|Kibuku|1.02|33.82|S
UG|Kikuube|Kikuube|1.60|31.17|S
UG|Kiruhura|Kiruhura|-0.20|30.80|S
UG|Kiryandongo|Kiryandongo|1.88|32.07|S
UG|Kisoro|Kisoro|-1.29|29.68|S
UG|Kitagwenda|Ntara|0.05|30.32|S
UG|Kitgum|Kitgum|3.28|32.89|S
UG|Koboko|Koboko|3.41|30.96|S
UG|Kole|Kole|2.41|32.80|S
UG|Kotido|Kotido|2.98|34.13|S
UG|Kumi|Kumi|1.46|33.94|S
UG|Kwania|Aduku|2.06|32.77|S
UG|Kween|Binyiny|1.43|34.66|S
UG|Kyankwanzi|Kyankwanzi|1.13|31.72|S
UG|Kyegegwa|Kyegegwa|0.49|31.05|S
UG|Kyenjojo|Kyenjojo|0.63|30.64|S
UG|Kyotera|Kyotera|-0.62|31.52|S
UG|Lamwo|Lamwo|3.54|32.80|S
UG|Lira District|Erute|2.28|32.93|S
UG|Luuka|Bulongo|0.78|33.30|S
UG|Luwero|Luwero|0.85|32.47|S
UG|Lwengo|Lwengo|-0.42|31.41|S
UG|Lyantonde|Lyantonde|-0.40|31.16|S
UG|Madi-Okollo|Rhino Camp|2.94|31.13|S
UG|Manafwa|Manafwa|0.98|34.32|S
UG|Maracha|Maracha|3.29|30.94|S
UG|Masaka District|Bukakata|-0.32|32.06|S
UG|Masindi|Masindi|1.69|31.71|S
UG|Mayuge|Mayuge|0.46|33.50|S
UG|Mbale District|Busiu|0.97|34.15|S
UG|Mbarara District|Bwizibwera|-0.56|30.58|S
UG|Mitooma|Mitooma|-0.57|30.06|S
UG|Mityana|Mityana|0.40|32.04|S
UG|Moroto|Moroto|2.53|34.67|S
UG|Moyo|Moyo|3.65|31.72|S
UG|Mpigi|Mpigi|0.23|32.32|S
UG|Mubende|Mubende|0.56|31.39|S
UG|Mukono|Mukono|0.35|32.76|SN
UG|Nabilatuk|Nabilatuk|2.05|34.55|S
UG|Nakapiripirit|Nakapiripirit|1.92|34.78|S
UG|Nakaseke|Nakaseke|0.73|32.40|S
UG|Nakasongola|Nakasongola|1.31|32.46|S
UG|Namayingo|Namayingo|0.24|33.88|S
UG|Namisindwa|Bupoto|0.85|34.35|S
UG|Namutumba|Namutumba|0.83|33.69|S
UG|Napak|Lokopo|2.28|34.22|S
UG|Nebbi|Nebbi|2.48|31.09|S
UG|Ngora|Ngora|1.49|33.77|S
UG|Ntoroko|Kanara|1.08|30.54|S
UG|Ntungamo|Ntungamo|-0.88|30.27|S
UG|Nwoya|Anaka|2.64|31.98|S
UG|Obongi|Obongi|3.37|31.58|S
UG|Omoro|Lalogi|2.74|32.63|S
UG|Otuke|Orum|2.63|33.32|S
UG|Oyam|Oyam|2.25|32.38|S
UG|Pakwach|Pakwach|2.46|31.50|S
UG|Pader|Pader|2.80|33.14|S
UG|Pallisa|Pallisa|1.15|33.71|S
UG|Rakai|Rakai|-0.68|31.37|S
UG|Rubanda|Rubanda|-1.18|29.87|S
UG|Rubirizi|Rubirizi|-0.30|30.11|S
UG|Rukiga|Muhanga|-1.13|30.11|S
UG|Rukungiri|Rukungiri|-0.79|29.93|S
UG|Rwampara|Kinoni|-0.52|30.67|S
UG|Sembabule|Sembabule|-0.08|31.46|S
UG|Serere|Serere|1.50|33.55|S
UG|Sheema|Kabwohe|-0.58|30.38|S
UG|Sironko|Sironko|1.24|34.25|S
UG|Soroti District|Katine|1.78|33.69|S
UG|Terego|Leju|3.10|31.17|S
UG|Tororo|Tororo|0.69|34.18|S
UG|Wakiso|Wakiso|0.40|32.46|S
UG|Yumbe|Yumbe|3.47|31.25|S
UG|Zombo|Zombo|2.51|30.90|S
UG|Arua City|Arua|3.02|30.91|SN
UG|Fort Portal City|Fort Portal|0.66|30.28|S
UG|Gulu City|Gulu|2.77|32.30|S
UG|Hoima City|Hoima|1.43|31.35|S
UG|Jinja City|Jinja|0.42|33.20|SN
UG|Lira City|Lira|2.25|32.90|S
UG|Masaka City|Masaka|-0.34|31.74|SN
UG|Mbale City|Mbale|1.08|34.18|SN
UG|Mbarara City|Mbarara|-0.61|30.65|S
UG|Soroti City|Soroti|1.71|33.61|S
UG|Wakiso|Nansana|0.37|32.53|N
UG|Wakiso|Kira|0.40|32.64|N
UG|Wakiso|Makindye-Ssabagabo|0.22|32.57|N
UG|Wakiso|Kyengera|0.30|32.45|N
```

### Naming caveats

TL — Fourteen municipalities, including Atauro, established separately in 2022. Oecusse is the Special Administrative Region of Oe-Cusse Ambeno; Pante Macassar is also Pante Makasar. The ten N entries follow the 2022 census of urban settlements.

TG — Five conventional regions plus the Autonomous District of Greater Lomé, treated as a sixth geographic administrative unit. The ten largest urban localities follow the 2022 census; Cinkassé is also Senkase, and Kara is also Lama-Kara.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://help.fews.net\&sz=32)

FEWS NET Help Center+1



TK — Three inhabited atolls, each with its own village administration. Tokelau has no single permanent national capital; government functions rotate among the atolls.

TO — Five island divisions. Niuas is also called Ongo Niua; Hihifo on Niuatoputapu is used as its principal reference. N entries follow the 2021 village-level census rather than aggregating the Greater Nuku'alofa urban area.

TT — Fourteen municipal corporations in Trinidad plus Tobago's separate administration. Diego Martin and Siparia became boroughs in 2023. Proposals announced in October 2026 would increase Trinidad's corporations to 17, but they are not yet treated as enacted boundaries.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.ttt.live\&sz=32)

TTT News+1



TN — Twenty-four governorates are retained as the practical mapping units. Five larger districts were introduced in September 2023, grouping those governorates, without replacing them as ordinary geographic subdivisions. El Kef is also Le Kef.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://9anoun.tn\&sz=32)

9anoun 🇹🇳



TR — Eighty-one provinces. Hatay's capital is Antakya; Kocaeli's is İzmit; Sakarya's is Adapazarı. Sincan is a major Ankara urban district and appears separately in the UN urban-settlement population ranking. İstanbul and İstanbul Province have overlapping metropolitan boundaries.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://turkishrepublic.org\&sz=32)

turkishrepublic.org+1



TM — Five welaýat provinces plus Ashgabat and Arkadag, both separately administered cities of state importance. Ahal's administrative centre is associated with Arkadag; Anau is used as an in-province geographic reference. Turkmenabat was formerly Chardzhou; Balkanabat was formerly Nebit-Dag.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://ift2026.com\&sz=32)

ift2026.com



TC — Six geographic districts. Cockburn Town is the capital on Grand Turk, whereas Cockburn Harbour is on South Caicos. Providenciales is an island containing several settlements, not a single conventional city; its populated localities are listed separately.

TV — Eight island councils; Niulakita is administered with Niutao rather than being a ninth council. The ten N entries use 2022 census villages, including several neighborhoods of Fongafale. Several coordinates coincide when rounded to two decimals.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://www.geonames.org\&sz=32)

GeoNames UI+1



UM — No permanent civilian population across the U.S. Minor Outlying Islands. Some islands host rotating military, research or conservation personnel, but the uninhabited-territory convention is used.

VI — Three principal island subdivisions: Saint Croix, Saint John and Saint Thomas. Population-ranked entries follow the 2020 census of towns and census-designated places, including Charlotte Amalie East/West and Frederiksted Southeast as separate localities.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://wm-site-staging.cloudflare-47b.workers.dev\&sz=32)

Worldometer



UG — Uganda has 135 districts plus 11 cities, including Kampala, giving 146 district-equivalent local-government units. Districts surrounding separately administered cities use nearby in-district settlements as geographic references where possible. The ten largest N settlements follow the 2024 census, which ranks Nansana, Kira and Makindye-Ssabagabo among the largest urban centres.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://statistics.ubos.org\&sz=32)

UBOS Dissemination Board+1



### Points still open

- Round 11: FM — Tol; MH — Airuk, Jabat, Lib; MR — Guerou; MU — Vingt Cinq, Raphael Island.
- Round 12: NL — The Bottom, Oranjestad.
- Round 13: MP — Agrihan; PW — Ngaramasch, Tobi, Dongosaru.
- Round 14: PA — Gaigirgordub.
- Round 15: RS — Pristina, Gjilan, Peja, Prizren. These are Kosovo localities requiring separate geographic classification.
- Round 16: SB — Tigoa; SO — Bu'ale; SS — Abyei, Pariang.
- Round 17: No outstanding coverage points; all 272 reference cities matched business data.
- Round 18: New reference points await comparison with Overture business data.
- Administrative checks: Confirm Uganda's rural district-headquarters locations, particularly districts separated from newly designated cities; verify Turkmenistan's Ahal–Arkadag administrative relationship; and monitor Trinidad and Tobago's proposed municipal restructuring.
- Sparse-island checks: TK — Atafu, Fakaofo, Nukunonu; TC — Balfour Town and Conch Bar; TV — small island-council settlements. Some may legitimately have few or no Overture business records.
- Population consistency: Türkiye, Tunisia, Trinidad and Tobago, and Uganda use different city-proper versus municipal or urban-agglomeration definitions. Keep those distinctions when interpreting N coverage.


---

## Claude Code - 2026-11-08 21:25 UTC - 19_claude.md - attachments: none

## Check of your message-18 list
Round 18: 367 reference lines, 366 cities, 356 with business data (97 %).
Not covered: - TK: 1/3 cities covered, 2 businesses near them; no data at: Atafu, Fakaofo
Not covered: - TM: 11/12 cities covered, 704 businesses near them; no data at: Tejen
Not covered: - TV: 12/16 cities covered, 236 businesses near them; no data at: Kulia, Savave, Pepesala, Aulotu
Not covered: - UG: 147/150 cities covered, 74,341 businesses near them; no data at: Amuru, Nabilatuk, Lalogi

Last message - same format again:


## Message 19 of 19 - countries
Ukraine (UA), United Arab Emirates (AE), United Kingdom (GB), United States (US), Uruguay (UY), Uzbekistan (UZ), Vanuatu (VU), Vatican City (VA), Venezuela (VE), Vietnam (VN), Wallis & Futuna (WF), Western Sahara (EH), Yemen (YE), Zambia (ZM), Zimbabwe (ZW)

For EACH country above give:
1. every first-level administrative division (state / province / region / governorate ... as it is today),
   with its capital or largest city (kind S);
2. the 10 largest cities of the country by population (kind N) - fewer if the country has fewer.
   A city can appear as both S and N; list it once with kind SN.
Uninhabited territories: one line `CC|-|-|||none`.

Output ONLY one code block, one line per city, pipe-separated, no header, no commentary inside it:
`CC|state|city|lat|lon|kind`
- CC = ISO code above; state and city in English (the name a map would show); lat / lon with 2 decimals.
After the code block: one line per country with any naming caveat (renamed divisions, disputed areas),
then the list of points still open.


---

## ChatGPT (Extra High) - 2026-11-08 21:40 UTC - saved as 19_chatgpt.md

```
UA|Autonomous Republic of Crimea|Simferopol|44.95|34.10|S
UA|Cherkasy Oblast|Cherkasy|49.44|32.06|S
UA|Chernihiv Oblast|Chernihiv|51.50|31.29|S
UA|Chernivtsi Oblast|Chernivtsi|48.29|25.94|S
UA|Dnipropetrovsk Oblast|Dnipro|48.46|35.05|SN
UA|Donetsk Oblast|Donetsk|48.02|37.80|SN
UA|Ivano-Frankivsk Oblast|Ivano-Frankivsk|48.92|24.71|S
UA|Kharkiv Oblast|Kharkiv|49.99|36.23|SN
UA|Kherson Oblast|Kherson|46.64|32.62|S
UA|Khmelnytskyi Oblast|Khmelnytskyi|49.42|26.99|S
UA|Kirovohrad Oblast|Kropyvnytskyi|48.51|32.26|S
UA|Kyiv Oblast|Bila Tserkva|49.80|30.12|S
UA|Kyiv City|Kyiv|50.45|30.52|SN
UA|Luhansk Oblast|Luhansk|48.57|39.31|S
UA|Lviv Oblast|Lviv|49.84|24.03|SN
UA|Mykolaiv Oblast|Mykolaiv|46.98|31.99|SN
UA|Odesa Oblast|Odesa|46.48|30.73|SN
UA|Poltava Oblast|Poltava|49.59|34.55|S
UA|Rivne Oblast|Rivne|50.62|26.25|S
UA|Sevastopol City|Sevastopol|44.61|33.52|SN
UA|Sumy Oblast|Sumy|50.91|34.80|S
UA|Ternopil Oblast|Ternopil|49.55|25.60|S
UA|Vinnytsia Oblast|Vinnytsia|49.23|28.47|S
UA|Volyn Oblast|Lutsk|50.75|25.34|S
UA|Zakarpattia Oblast|Uzhhorod|48.62|22.30|S
UA|Zaporizhzhia Oblast|Zaporizhzhia|47.84|35.14|SN
UA|Zhytomyr Oblast|Zhytomyr|50.25|28.66|S
UA|Dnipropetrovsk Oblast|Kryvyi Rih|47.91|33.39|N
AE|Abu Dhabi|Abu Dhabi|24.45|54.37|SN
AE|Ajman|Ajman|25.41|55.45|SN
AE|Dubai|Dubai|25.20|55.27|SN
AE|Fujairah|Fujairah|25.12|56.33|SN
AE|Ras Al Khaimah|Ras Al Khaimah|25.79|55.94|SN
AE|Sharjah|Sharjah|25.35|55.39|SN
AE|Umm Al Quwain|Umm Al Quwain|25.56|55.56|SN
AE|Abu Dhabi|Al Ain|24.21|55.74|N
AE|Sharjah|Khor Fakkan|25.33|56.34|N
AE|Sharjah|Kalba|25.07|56.35|N
GB|England|London|51.51|-0.13|SN
GB|Northern Ireland|Belfast|54.60|-5.93|SN
GB|Scotland|Edinburgh|55.95|-3.19|SN
GB|Wales|Cardiff|51.48|-3.18|S
GB|England|Birmingham|52.49|-1.89|N
GB|Scotland|Glasgow|55.86|-4.25|N
GB|England|Leeds|53.80|-1.55|N
GB|England|Liverpool|53.41|-2.98|N
GB|England|Sheffield|53.38|-1.47|N
GB|England|Manchester|53.48|-2.24|N
GB|England|Bristol|51.45|-2.59|N
US|Alabama|Montgomery|32.37|-86.30|S
US|Alaska|Juneau|58.30|-134.42|S
US|Arizona|Phoenix|33.45|-112.07|SN
US|Arkansas|Little Rock|34.75|-92.29|S
US|California|Sacramento|38.58|-121.49|S
US|Colorado|Denver|39.74|-104.99|S
US|Connecticut|Hartford|41.76|-72.68|S
US|Delaware|Dover|39.16|-75.52|S
US|District of Columbia|Washington|38.91|-77.04|S
US|Florida|Tallahassee|30.44|-84.28|S
US|Georgia|Atlanta|33.75|-84.39|S
US|Hawaii|Honolulu|21.31|-157.86|S
US|Idaho|Boise|43.62|-116.20|S
US|Illinois|Springfield|39.80|-89.65|S
US|Indiana|Indianapolis|39.77|-86.16|S
US|Iowa|Des Moines|41.59|-93.62|S
US|Kansas|Topeka|39.05|-95.68|S
US|Kentucky|Frankfort|38.20|-84.87|S
US|Louisiana|Baton Rouge|30.45|-91.19|S
US|Maine|Augusta|44.31|-69.78|S
US|Maryland|Annapolis|38.98|-76.49|S
US|Massachusetts|Boston|42.36|-71.06|S
US|Michigan|Lansing|42.73|-84.56|S
US|Minnesota|Saint Paul|44.95|-93.09|S
US|Mississippi|Jackson|32.30|-90.18|S
US|Missouri|Jefferson City|38.58|-92.17|S
US|Montana|Helena|46.59|-112.04|S
US|Nebraska|Lincoln|40.81|-96.68|S
US|Nevada|Carson City|39.16|-119.77|S
US|New Hampshire|Concord|43.21|-71.54|S
US|New Jersey|Trenton|40.22|-74.76|S
US|New Mexico|Santa Fe|35.69|-105.94|S
US|New York|Albany|42.65|-73.76|S
US|North Carolina|Raleigh|35.78|-78.64|S
US|North Dakota|Bismarck|46.81|-100.78|S
US|Ohio|Columbus|39.96|-83.00|S
US|Oklahoma|Oklahoma City|35.47|-97.52|S
US|Oregon|Salem|44.94|-123.03|S
US|Pennsylvania|Harrisburg|40.27|-76.88|S
US|Rhode Island|Providence|41.82|-71.41|S
US|South Carolina|Columbia|34.00|-81.03|S
US|South Dakota|Pierre|44.37|-100.35|S
US|Tennessee|Nashville|36.16|-86.78|S
US|Texas|Austin|30.27|-97.74|S
US|Utah|Salt Lake City|40.76|-111.89|S
US|Vermont|Montpelier|44.26|-72.58|S
US|Virginia|Richmond|37.54|-77.44|S
US|Washington|Olympia|47.04|-122.90|S
US|West Virginia|Charleston|38.35|-81.63|S
US|Wisconsin|Madison|43.07|-89.40|S
US|Wyoming|Cheyenne|41.14|-104.82|S
US|New York|New York City|40.71|-74.01|N
US|California|Los Angeles|34.05|-118.24|N
US|Illinois|Chicago|41.88|-87.63|N
US|Texas|Houston|29.76|-95.37|N
US|Pennsylvania|Philadelphia|39.95|-75.16|N
US|Texas|San Antonio|29.42|-98.49|N
US|California|San Diego|32.72|-117.16|N
US|Texas|Dallas|32.78|-96.80|N
US|Texas|Fort Worth|32.76|-97.33|N
UY|Artigas|Artigas|-30.40|-56.47|SN
UY|Canelones|Canelones|-34.52|-56.28|S
UY|Cerro Largo|Melo|-32.37|-54.18|SN
UY|Colonia|Colonia del Sacramento|-34.47|-57.84|S
UY|Durazno|Durazno|-33.38|-56.52|S
UY|Flores|Trinidad|-33.52|-56.90|S
UY|Florida|Florida|-34.10|-56.21|S
UY|Lavalleja|Minas|-34.38|-55.24|S
UY|Maldonado|Maldonado|-34.90|-54.95|SN
UY|Montevideo|Montevideo|-34.91|-56.19|SN
UY|Paysandú|Paysandú|-32.32|-58.08|SN
UY|Río Negro|Fray Bentos|-33.12|-58.31|S
UY|Rivera|Rivera|-30.90|-55.55|SN
UY|Rocha|Rocha|-34.48|-54.34|S
UY|Salto|Salto|-31.39|-57.96|SN
UY|San José|San José de Mayo|-34.34|-56.71|S
UY|Soriano|Mercedes|-33.25|-58.03|S
UY|Tacuarembó|Tacuarembó|-31.72|-55.98|SN
UY|Treinta y Tres|Treinta y Tres|-33.23|-54.38|S
UY|Canelones|Ciudad de la Costa|-34.82|-55.95|N
UY|Canelones|Las Piedras|-34.73|-56.22|N
UZ|Andijan Region|Andijan|40.78|72.34|SN
UZ|Bukhara Region|Bukhara|39.77|64.43|SN
UZ|Fergana Region|Fergana|40.39|71.79|SN
UZ|Jizzakh Region|Jizzakh|40.12|67.84|S
UZ|Karakalpakstan|Nukus|42.46|59.61|SN
UZ|Kashkadarya Region|Qarshi|38.86|65.79|SN
UZ|Khorezm Region|Urgench|41.55|60.63|S
UZ|Namangan Region|Namangan|40.99|71.67|SN
UZ|Navoi Region|Navoi|40.10|65.38|S
UZ|Samarkand Region|Samarkand|39.65|66.97|SN
UZ|Surkhandarya Region|Termez|37.22|67.28|S
UZ|Syrdarya Region|Gulistan|40.49|68.78|S
UZ|Tashkent Region|Nurafshon|41.04|69.36|S
UZ|Tashkent City|Tashkent|41.30|69.27|SN
UZ|Fergana Region|Kokand|40.53|70.94|N
UZ|Fergana Region|Margilan|40.47|71.72|N
VU|Malampa|Lakatoro|-16.10|167.42|SN
VU|Penama|Saratamata|-15.29|167.99|S
VU|Sanma|Luganville|-15.52|167.16|SN
VU|Shefa|Port Vila|-17.74|168.31|SN
VU|Tafea|Isangel|-19.54|169.28|SN
VU|Torba|Sola|-13.88|167.55|SN
VU|Malampa|Norsup|-16.07|167.40|N
VU|Shefa|Mele|-17.69|168.26|N
VU|Shefa|Erakor|-17.76|168.32|N
VU|Shefa|Pango|-17.78|168.28|N
VU|Sanma|Port Olry|-15.04|167.07|N
VA|Vatican City|Vatican City|41.90|12.45|SN
VE|Amazonas|Puerto Ayacucho|5.66|-67.62|S
VE|Anzoátegui|Barcelona|10.13|-64.72|SN
VE|Apure|San Fernando de Apure|7.89|-67.47|S
VE|Aragua|Maracay|10.25|-67.60|SN
VE|Barinas|Barinas|8.62|-70.21|S
VE|Bolívar|Ciudad Bolívar|8.13|-63.54|S
VE|Carabobo|Valencia|10.16|-68.01|SN
VE|Cojedes|San Carlos|9.66|-68.58|S
VE|Delta Amacuro|Tucupita|9.06|-62.05|S
VE|Capital District|Caracas|10.49|-66.90|SN
VE|Falcón|Coro|11.40|-69.67|S
VE|Federal Dependencies|Gran Roque|11.95|-66.67|S
VE|Guárico|San Juan de los Morros|9.91|-67.36|S
VE|La Guaira|La Guaira|10.60|-66.93|S
VE|Lara|Barquisimeto|10.07|-69.32|SN
VE|Mérida|Mérida|8.59|-71.16|S
VE|Miranda|Los Teques|10.34|-67.04|S
VE|Monagas|Maturín|9.75|-63.18|SN
VE|Nueva Esparta|La Asunción|11.03|-63.86|S
VE|Portuguesa|Guanare|9.04|-69.75|S
VE|Sucre|Cumaná|10.46|-64.17|SN
VE|Táchira|San Cristóbal|7.77|-72.23|S
VE|Trujillo|Trujillo|9.37|-70.43|S
VE|Yaracuy|San Felipe|10.34|-68.74|S
VE|Zulia|Maracaibo|10.64|-71.63|SN
VE|Bolívar|Ciudad Guayana|8.35|-62.65|N
VE|Miranda|Guarenas|10.47|-66.62|N
VN|An Giang|Rach Gia|10.02|105.08|S
VN|Bac Ninh|Bac Giang|21.28|106.19|S
VN|Ca Mau|Ca Mau|9.18|105.15|S
VN|Can Tho|Can Tho|10.05|105.78|SN
VN|Cao Bang|Cao Bang|22.67|106.25|S
VN|Da Nang|Da Nang|16.07|108.22|SN
VN|Dak Lak|Buon Ma Thuot|12.67|108.05|S
VN|Dien Bien|Dien Bien Phu|21.39|103.02|S
VN|Dong Nai|Bien Hoa|10.95|106.82|S
VN|Dong Thap|My Tho|10.36|106.36|SN
VN|Gia Lai|Quy Nhon|13.78|109.22|S
VN|Ha Tinh|Ha Tinh|18.36|105.90|S
VN|Hai Phong|Hai Phong|20.86|106.68|SN
VN|Hanoi|Hanoi|21.03|105.85|SN
VN|Ho Chi Minh City|Ho Chi Minh City|10.82|106.63|SN
VN|Hue|Hue|16.46|107.60|S
VN|Hung Yen|Hung Yen|20.65|106.05|S
VN|Khanh Hoa|Nha Trang|12.24|109.19|SN
VN|Lai Chau|Lai Chau|22.40|103.46|S
VN|Lam Dong|Da Lat|11.94|108.44|S
VN|Lang Son|Lang Son|21.85|106.76|S
VN|Lao Cai|Yen Bai|21.72|104.91|S
VN|Nghe An|Vinh|18.67|105.69|S
VN|Ninh Binh|Ninh Binh|20.25|105.97|S
VN|Phu Tho|Viet Tri|21.31|105.40|S
VN|Quang Ngai|Quang Ngai|15.12|108.80|S
VN|Quang Ninh|Ha Long|20.95|107.08|S
VN|Quang Tri|Dong Hoi|17.47|106.62|S
VN|Son La|Son La|21.33|103.91|S
VN|Tay Ninh|Tan An|10.54|106.41|S
VN|Thai Nguyen|Thai Nguyen|21.59|105.85|S
VN|Thanh Hoa|Thanh Hoa|19.81|105.78|S
VN|Tuyen Quang|Tuyen Quang|21.82|105.21|S
VN|Vinh Long|Vinh Long|10.25|105.97|S
VN|An Giang|Long Xuyen|10.39|105.44|N
VN|Ho Chi Minh City|Vung Tau|10.35|107.08|N
VN|Tay Ninh|Tay Ninh|11.31|106.10|N
WF|Alo|Ono|-14.31|-178.11|SN
WF|Sigave|Leava|-14.29|-178.16|S
WF|Uvea|Mata-Utu|-13.28|-176.17|SN
WF|Uvea|Liku|-13.27|-176.17|N
WF|Uvea|Utufua|-13.34|-176.19|N
WF|Uvea|Falaleu|-13.29|-176.18|N
WF|Uvea|Alele|-13.25|-176.18|N
WF|Uvea|Mala'e|-13.24|-176.19|N
WF|Uvea|Halalo|-13.35|-176.21|N
WF|Uvea|Ahoa|-13.29|-176.24|N
WF|Alo|Taoa|-14.31|-178.13|N
EH|Laayoune-Sakia El Hamra|Laayoune|27.14|-13.19|SN
EH|Dakhla-Oued Ed Dahab|Dakhla|23.68|-15.96|SN
EH|Laayoune-Sakia El Hamra|Smara|26.74|-11.67|N
EH|Laayoune-Sakia El Hamra|Boujdour|26.13|-14.49|N
EH|Laayoune-Sakia El Hamra|El Marsa|27.10|-13.42|N
EH|Laayoune-Sakia El Hamra|Meharrize|26.15|-11.07|N
EH|Dakhla-Oued Ed Dahab|Tichla|21.58|-14.97|N
EH|Dakhla-Oued Ed Dahab|El Aargub|23.61|-15.87|N
EH|Dakhla-Oued Ed Dahab|Bir Ganduz|21.60|-16.45|N
EH|Laayoune-Sakia El Hamra|Amgala|26.29|-11.14|N
YE|Abyan|Zinjibar|13.13|45.38|S
YE|Aden|Aden|12.78|45.04|SN
YE|Al Bayda|Al Bayda|13.99|45.57|S
YE|Al Dhale|Ad Dhale|13.70|44.73|S
YE|Al Hudaydah|Al Hudaydah|14.80|42.95|SN
YE|Al Jawf|Al Hazm|16.17|44.78|S
YE|Al Mahrah|Al Ghaydah|16.21|52.18|S
YE|Al Mahwit|Al Mahwit|15.47|43.54|S
YE|Amran|Amran|15.66|43.94|SN
YE|Dhamar|Dhamar|14.54|44.41|SN
YE|Hadramawt|Mukalla|14.54|49.13|SN
YE|Hajjah|Hajjah|15.69|43.60|S
YE|Ibb|Ibb|13.97|44.18|SN
YE|Lahij|Lahij|13.06|44.88|S
YE|Marib|Marib|15.46|45.33|S
YE|Raymah|Al Jabin|14.71|43.50|S
YE|Saadah|Saadah|16.94|43.76|S
YE|Sana'a Governorate|Sayyan|15.17|44.32|SN
YE|Sana'a City|Sana'a|15.35|44.21|SN
YE|Shabwah|Ataq|14.54|46.83|S
YE|Socotra|Hadibu|12.65|54.02|S
YE|Taiz|Taiz|13.58|44.02|SN
YE|Al Hudaydah|Zabid|14.20|43.32|N
ZM|Central|Kabwe|-14.44|28.45|SN
ZM|Copperbelt|Ndola|-12.96|28.64|SN
ZM|Eastern|Chipata|-13.63|32.65|SN
ZM|Luapula|Mansa|-11.20|28.89|S
ZM|Lusaka|Lusaka|-15.42|28.28|SN
ZM|Muchinga|Chinsali|-10.54|32.08|S
ZM|Northern|Kasama|-10.21|31.18|SN
ZM|North-Western|Solwezi|-12.17|26.39|SN
ZM|Southern|Choma|-16.81|26.98|S
ZM|Western|Mongu|-15.25|23.13|S
ZM|Copperbelt|Kitwe|-12.82|28.21|N
ZM|Copperbelt|Chingola|-12.53|27.86|N
ZM|Copperbelt|Luanshya|-13.14|28.42|N
ZM|Southern|Livingstone|-17.85|25.86|N
ZW|Bulawayo|Bulawayo|-20.15|28.59|SN
ZW|Harare|Harare|-17.83|31.05|SN
ZW|Manicaland|Mutare|-18.97|32.67|SN
ZW|Mashonaland Central|Bindura|-17.30|31.33|S
ZW|Mashonaland East|Marondera|-18.19|31.55|S
ZW|Mashonaland West|Chinhoyi|-17.37|30.19|SN
ZW|Masvingo|Masvingo|-20.07|30.83|S
ZW|Matabeleland North|Lupane|-18.93|27.81|S
ZW|Matabeleland South|Gwanda|-20.94|29.00|S
ZW|Midlands|Gweru|-19.45|29.82|SN
ZW|Harare|Chitungwiza|-18.02|31.07|N
ZW|Harare|Epworth|-17.89|31.15|N
ZW|Midlands|Kwekwe|-18.93|29.82|N
ZW|Mashonaland West|Kadoma|-18.33|29.91|N
ZW|Mashonaland East|Ruwa|-17.89|31.24|N
```

### Naming caveats

UA — Ukraine has 24 oblasts, the Autonomous Republic of Crimea, and the special-status cities Kyiv and Sevastopol. Crimea, Sevastopol and other Russian-occupied Ukrainian territories remain internationally recognized as Ukrainian. Kyiv is the administrative centre of Kyiv Oblast but lies outside that oblast, so Bila Tserkva is used as its in-oblast geographic reference. Kropyvnytskyi was formerly Kirovohrad. Population rankings are historical because wartime displacement makes current comparisons unreliable.

AE — Seven emirates. Ras Al Khaimah is also Ras al-Khaimah; Umm Al Quwain is also Umm al-Quwain. Khor Fakkan and Kalba belong to Sharjah despite their locations on the eastern coast.

GB — Four constituent countries: England, Scotland, Wales and Northern Ireland. These are used as first-level reference units; their internal administrative systems differ. London is the UK capital; Edinburgh, Cardiff and Belfast are the respective national capitals. City-population rankings differ between built-up areas and local-authority boundaries.

US — Fifty states plus Washington, D.C. The federal capital is separate from the 50 states. Puerto Rico, Guam, the US Virgin Islands and other territories have their own ISO entries. Fort Worth is tenth in the US Census Bureau's July 2025 city-population estimates, ahead of Jacksonville.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://cdn.www.census.gov\&sz=32)

Census.gov



UY — Nineteen departments. Ciudad de la Costa and Las Piedras are in Canelones Department. Maldonado and nearby Punta del Este form a larger urban area, but Maldonado is used as the city reference.

UZ — Twelve regions, the autonomous Republic of Karakalpakstan and independently administered Tashkent City. Tashkent Region's administrative centre is Nurafshon. Qarshi is also Karshi; Kokand is also Qo'qon; Urgench is also Urganch.

VU — Six provinces. Lakatoro is the administrative centre of Malampa, while nearby Norsup is another important settlement. Penama consists of Pentecost, Ambae and Maewo; Saratamata is its administrative centre. The additional N entries represent populated villages rather than ten conventional incorporated cities.

VA — Vatican City is a single sovereign city-state, without separate first-level administrative divisions. Vatican City is therefore the only SN entry.

VE — Twenty-three established states, the Capital District and Federal Dependencies are used. La Guaira was previously Vargas State. Gran Roque is a populated reference for the Federal Dependencies, not a conventional state capital. Venezuela also claims Guayana Esequiba, territory administered by Guyana; the disputed claim is excluded from these rows.

VN — Thirty-four provincial-level jurisdictions following the July 2025 consolidation. By 2026, nine are centrally governed cities, including the newly designated Dong Nai, Quang Ninh and Bac Ninh. The merged Lao Cai administration is centred in Yen Bai, Quang Tri in Dong Hoi, and Tay Ninh in Tan An. Older map datasets may still use the pre-merger provincial names.&#x20;

[image](https://www.google.com/s2/favicons?domain=https://en.baochinhphu.vn\&sz=32)

en.baochinhphu.vn+1



WF — Wallis and Futuna has three traditional administrative districts: Uvea on Wallis, and Alo and Sigave on Futuna. Mata-Utu is the territorial capital. The N entries are villages rather than conventional cities; names such as Mala'e can occur in more than one district.

EH — Western Sahara has disputed sovereignty and no universally accepted first-level administrative system. Laayoune-Sakia El Hamra and Dakhla-Oued Ed Dahab are Moroccan administrative designations used here for geographic matching only. This does not imply recognition of Moroccan sovereignty over the territory. Population data for smaller settlements are sparse.

YE — Twenty-two governorate-level units, including Socotra and separately administered Sana'a City. Sana'a Governorate surrounds, but excludes, Sana'a City; Sayyan is used as an in-governorate reference rather than a separate governorate capital. Hadramawt is also Hadhramaut, and Al Hudaydah is also Hodeidah. Population estimates are affected by prolonged conflict and displacement.

ZM — Ten provinces. Southern Province's administrative centre is Choma, having moved from Livingstone. Muchinga's is Chinsali. Ndola is the Copperbelt provincial capital, while Kitwe is another major city in the same province.

ZW — Eight provinces plus two metropolitan provinces, Harare and Bulawayo. Lupane is the administrative centre of Matabeleland North. Chitungwiza and Epworth are separate urban areas within Harare Province; Ruwa is in Mashonaland East.

### Points still open

- Round 11: FM — Tol; MH — Airuk, Jabat, Lib; MR — Guerou; MU — Vingt Cinq, Raphael Island. Seven unmatched points.
- Round 12: NL — The Bottom, Oranjestad. Two unmatched points.
- Round 13: MP — Agrihan; PW — Ngaramasch, Tobi, Dongosaru. Four unmatched points.
- Round 14: PA — Gaigirgordub. One unmatched point.
- Round 15: RS — Pristina, Gjilan, Peja, Prizren. Four unmatched points in Kosovo; check their country assignment separately.
- Round 16: SB — Tigoa; SO — Bu'ale; SS — Abyei, Pariang. Four unmatched points.
- Round 17: No unmatched points; all 272 reference cities had business data.
- Round 18: TK — Atafu, Fakaofo; TM — Tejen; TV — Kulia, Savave, Pepesala, Aulotu; UG — Amuru, Nabilatuk, Lalogi. Ten unmatched points.
- Round 19: 295 reference rows prepared across 15 ISO entries. Overture business-data coverage is pending.
- Cumulative unresolved before Round 19: 32 reference points reported without business data across Rounds 11–18. These are not necessarily extraction failures; isolated settlements, coordinate precision, aliases and disputed country assignments may explain some.
- Final validation priorities: Check Vietnam's merged provincial boundaries, Ukraine's occupied territories, Venezuela/Western Sahara territorial classifications, small settlements in Wallis and Futuna and Vanuatu, and Yemen's conflict-affected place records.
- Population methodology: Top-ten N entries should be treated as geographic reference targets, not a uniform global population ranking, because countries use different municipal, urban-area and census definitions.
