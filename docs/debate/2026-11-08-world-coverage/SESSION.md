

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
