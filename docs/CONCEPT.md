# Buitenmuseum: concept, onderzoek en beslissingen

Samenvatting van het gesprek tussen Danny en Claude (16 november 2026) waarin dit prototype ontstond.

## Het idee (Danny, al jaren)

- **Wat:** een online geschiedenismuseum voor de buitenruimte van een stad of dorp.
- **Marker:** op een specifieke plek ligt een teken: een stoeptegel met QR-code of een paaltje met NFC-chip. Die opent een webapp.
- **Ervaring:** je ziet de omgeving live in liggende stand. Een oude foto, gemaakt vanaf exact die plek, ligt precies over het live beeld, zodat je de verschillen één op één ziet.
- **Eén manier van kijken:** de foto is maar op één manier goed te zien.
- **Museum:** meerdere punten in de stad samen vormen het museum.

## Wat er al bestaat (onderzoek)

- **Streetmuseum (Museum of London, 2010):** legde historische foto's over het live camerabeeld. Het bureau erachter rekende op ongeveer 5.000 downloads en kreeg er ruim een half miljoen, plus grote reclameprijzen. De app is nu niet meer beschikbaar, omdat hij door veranderingen in de besturingssystemen van telefoons niet meer werkte.
- **Historypin:** had een overlay met instelbare transparantie. De apps zijn in 2015 gestopt: onderhoud voor nieuwe telefoons kostte te veel, en ze kozen voor het webplatform.
- **WhatWasThere** en vergelijkbare apps: de overlays klopten vaak niet goed, omdat ze op GPS of Street View leunden.
- **Onderzoek MIT (computational rephotography):** ongetrainde gebruikers konden het standpunt van een referentiefoto niet goed nadoen.
- **Nederland:**
  - UAR (NAi, Rotterdam): een architectuur-app met AR;
  - Koloniaal Rotterdam: AR op 27 plekken;
  - Street Museum NL (MediaMonks, Noord-Holland);
  - De Verhalen van Groningen: weinig gebruikt.
- **Patroon:** een eenmalig project. Een museum of archief laat een bureau een app bouwen, er komt een lancering met persaandacht, en daarna onderhoudt niemand de app. Het grote publiek kent ze niet.

**Conclusie:** het effect is bewezen. Het onderscheid van dit concept zit in de **fysieke marker**. Die lost het standpuntprobleem op, waar de anderen op vastliepen, en die is zichtbaar op straat, terwijl een app in een store onzichtbaar blijft.

## Precedent in Rotterdam: de Brandgrens

- **Wat:** in 2010 liet de gemeente de grens van de brand na het bombardement van 14 mei 1940 markeren met grondlampen in de straat.
- **Ontwerp:** West 8. Het gaat om 127 rode lampen langs een route van ongeveer 12 km, met informatiezuilen en een website.
- **Eigendom:** de gemeente was opdrachtgever én eigenaar. Dat is ook een goed model voor het Buitenmuseum: Danny ontwerpt en levert, de eigenaar onderhoudt.
- **Gevolg voor de punten:** binnen de brandgrens is het stratenplan na de oorlog opnieuw getekend. Alleen de Laurenskerk, het Witte Huis, de Beurs, het Postkantoor, het Raadhuis en het Schielandshuis bleven staan.

## Kritische discussie en Danny's antwoorden

| Kritiekpunt (Claude) | Antwoord (Danny) | Uitkomst |
|---|---|---|
| De mooiste voor-en-na-plekken passen het slechtst, omdat er zoveel veranderd is | Neem de mooiste punten mee en laat sommige liggen | Tegel + sensoren bepalen al de plek, dus herkenning is niet nodig om goed te staan. Er zijn twee soorten punten: **herkenning** (iets bleef staan) en **verdwijning** ("hier stond een straat"). Kies punten op het verhaal dat ze vertellen. |
| Een ervaring van 30 seconden, daarna lopen mensen door | Direct informatie tonen of vertellen, in alle talen | ▶-knop met voorlezen + ondertiteling, 5 talen. Laat gevoelige onderwerpen (1940) in de hoofdtalen door een mens nalezen. |
| Donker, regen en een drukke stoep | Dan doe je de route ook niet | Klopt grotendeels. Donker blijft een specifiek probleem voor een camerabeeld, opgelost met een **nachtmodus** (daglichtbeeld). |
| Wie betaalt jaar 3? (onderhoud, vergunningen, vandalisme) | Dat moet mee in de deal, met technologische innovatie als uitgangspunt | Let op: innovatiebudget en beheerbudget zijn bij gemeentes vaak verschillende potjes. Zet onderhoud als **vast jaarbedrag per punt** in de deal; de klant wordt eigenaar van het object. |
| Is de app nodig? Een geëtste glasplaat doet hetzelfde | Glas is veel duurder. Juist het instapniveau en de lage kosten maken het schaalbaar | Terecht. De schaalbaarheid zit dan wel in het **werk per punt** (foto, rechten, standpunt, vastleggen, tekst, vergunning). Dat moet een vaste, snelle werkwijze worden. |

**Het product** is dus een set: tegel/paaltje + webapp + vaste werkwijze om punten te maken + jaarabonnement. Je verkoopt het aan eigenaren (gemeente, stadsarchief, ondernemersvereniging), niet als consumentenapp.

**Open vraag om te meten:** hoeveel uur kost één punt van begin tot eind?

## Wensen van Danny voor de beleving (verwerkt in v0.2–v0.3)

- Het mag niet te moeilijk worden: er moet speling zijn en de app moet duidelijk aangeven wat je moet doen.
- Een digitaal kader in beeld, met pijlen: een pijl omhoog en een pijl naar rechts betekent dat je de telefoon omhoog en naar rechts beweegt.
- Niet op de mm nauwkeurig, anders zijn mensen alleen maar met kalibreren bezig.
- Tijdens het zoeken staat de oude foto half doorzichtig in beeld, zodat je makkelijk de juiste hoek vindt. Een groen kader betekent: precies goed.
- Knoppen op het scherm om de oude foto helemaal naar voren te halen, en een ▶-knop die de foto laat zien en direct het verhaal vertelt.

## Bronnen

- Museum of London over zijn apps: https://museumoflondon.org.uk/discover/museum-london-apps
- Streetmuseum, resultaten van het bureau: https://lbbonline.com/news/brothers-sisters-13-in-13-the-museum-of-london
- Streetmuseum in 2010: https://petapixel.com/2010/05/24/museum-of-london-releases-augmented-reality-app-for-historical-photos
- Historypin (Wikipedia): https://en.wikipedia.org/wiki/Historypin
- Historypin, app gestopt: https://groups.google.com/g/historypin/c/BmOh-XIBBEo
- Historypin overlay (iCulture): https://www.iculture.nl/apps/historypin-voor-iphone-zie-meteen-de-geschiedenis-van-jouw-straat/
- WhatWasThere: https://www.geographyrealm.com/whatwasthere-augmented-reality/
- MIT, computational rephotography: https://people.csail.mit.edu/soonmin/rephoto/rephoto.pdf
- UAR Rotterdam (iCulture): https://www.iculture.nl/apps/ontdek-rotterdam-met-de-rotterdam-city-guide-en-uar-voor-iphone/
- Brandgrens, West 8 (Dutch Design Awards): https://dutchdesignawards.nl/en/gallery/permanent-marking-of-the-brandgrens-rotterdam
- Brandgrens (BKOR): https://www.bkor.nl/en/beeld/brandgrens/
- Brandgrens, 127 lampen (VoiceMap): https://voicemap.me/tour/rotterdam/stadswandeling-rotterdam-van-een-dam-in-de-rotte-naar-een-moderne-metropool/sites/de-brandgrens-van-14-mei-1940
- Wederopbouw Rotterdam (TU Delft): https://repository.tudelft.nl/file/File_cbf7a8c9-3372-4bf4-926e-cb02f3ae3674?preview=1
- Stadsarchief Rotterdam, jaaroverzicht 2024 (beeldbank, auteursrecht): https://stadsarchief.rotterdam.nl/sites/default/files/2025-07/jaaroverzicht-2024-stadsarchief-rotterdam-digitaal-1.pdf
