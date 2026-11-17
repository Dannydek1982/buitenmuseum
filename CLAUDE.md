# Buitenmuseum (prototype-webapp)

Een online geschiedenismuseum in de buitenruimte. De bezoeker gaat op een fysieke marker staan: een stoeptegel met QR-code of een paaltje met NFC-chip, precies op het standpunt van een historische foto. De webapp opent de camera in liggende stand. De oude foto valt dan precies over het live beeld, zodat je toen en nu één op één vergelijkt. Meerdere punten in een stad samen vormen het museum.

Eigenaar: **Danny** (Rotterdam), conceptontwikkelaar en ontwerper (Integrated Product Design, TU Delft).
- **Taal:** communiceer in het Nederlands.
- **Stijl:** hij wil concrete, specifieke voorstellen en vragen, geen algemene stellingen.
- **Rol:** kritisch meedenken wordt gewaardeerd.

Achtergrond, onderzoek en de kritische discussie staan in `docs/CONCEPT.md`.

## Huidige stand: v0.3 (16 november 2026)

Alles staat in **`index.html`**: vanilla HTML, CSS en JS, zonder build-stap en zonder dependencies. De enige externe bron is qrcodejs via cdnjs, en die wordt pas geladen bij "QR".

**Beheerkant** (Nederlands):
- **Punt vastleggen:** kies een oude foto, ga op het standpunt staan, tik op de ontspanknop. Daarbij leg je vast:
  - het camerabeeld (dat wordt het daglichtbeeld voor de nachtmodus);
  - de stand van de telefoon (richting, kanteling, horizon, gemiddeld over 0,5 s).
- **Foto uitlijnen:** op het bevroren beeld de oude foto schuiven, knijpen en draaien tot hij past.
- **Gegevens per punt:** naam, jaar, bron, richtpunt ("kijk naar…") en verhaal.
- **Bewerk:** vertalingen per taal (NL, EN, DE, FR, ES).
- **Overige functies:** QR per punt (`?p=<id>`), export en import als JSON, speling (Ruim/Normaal/Precies), Testinfo-overlay.

**Bezoekerskant** (5 talen, standaard de taal van de telefoon):
- **Startscherm:** de oude foto, een kijkrichting ("Kijk richting noordoost, naar de toren van de Laurenskerk") en 3 stappen.
- **Zoeken:**
  - de oude foto staat **45% doorzichtig** in beeld en schuift mee met de wereld;
  - een **wit kader** rond de oude foto en **4 vaste hoeken** geven aan waar het kader moet landen;
  - **oranje pijlen** per as, ook twee tegelijk (bijvoorbeeld links + omhoog), plus een tekstaanwijzing.
- **Bijna goed:** het kader wordt **oranje**.
- **Goed:** het kader wordt **groen**, met "Precies goed! Druk op ▶" en een trilsignaal op Android.
- **Knoppen onderin:**
  - **Half / Toen / Schuif** (Schuif = een toen/nu-lijn die je met de vinger sleept);
  - **▶**: de foto fadet langzaam naar 100% en het verhaal wordt voorgelezen (Web Speech API) met ondertiteling per zin. Zonder stem: alleen ondertitels op leestempo.
- **Nachtmodus:** is het camerabeeld te donker (lichtmeter), dan schakelt de app automatisch naar het daglichtbeeld. Het maantje wisselt handmatig.
- **Info-knop:** het volledige verhaal, met een taalkeuze.

## Ontwerpprincipes (met Danny afgesproken, niet zomaar veranderen)

1. **Niet op de mm.** Mensen mogen niet bezig zijn met kalibreren, want dat gaat ten koste van het concept.
   - Standaard speling is "ruim": ±20° draaien, ±8° kantelen, ±10° horizon.
   - Binnen de speling staat de foto stil.
   - Na vastklikken mag je 1,5× verder afwijken (`HOLD`), en pas na 500 ms buiten de marge laat hij los (`LEAVE_MS`).
2. **Duidelijke cues:** half doorzichtige foto + kader + pijlen + tekst. Wit → oranje (bijna) → groen (goed).
3. **De tegel/het paaltje bepaalt het standpunt.** Daardoor hoeft de app geen positie te bepalen; GPS is te grof. Sensoren regelen alleen de kijkrichting.
4. **Webapp, geen app store.** Streetmuseum (Londen) en Historypin sneuvelden op het onderhoud van hun native apps.
5. **Instap en lage kosten, daardoor schaalbaar.** Onderhoud gaat mee in de deal met de eigenaar (gemeente, archief).

## Architectuur van `index.html` (secties in het script)

- **instellingen:**
  - `LEVELS` (speling per niveau);
  - `HOLD`, `ENTER_MS`, `LEAVE_MS`;
  - `GHOST` (doorzichtigheid tijdens zoeken);
  - localStorage-sleutels.
- **talen:**
  - `LANGS` (inclusief TTS-codes) en `STR` (alle bezoekersteksten);
  - `t()` en `field(p, key)` (tekst van een punt in de gekozen taal, met terugval op NL);
  - `moveMsg()` (zinnen als "naar links en omhoog").
- **opslag:**
  - IndexedDB `buitenmuseum` → store `kv` → key `points`;
  - terugval op localStorage (`buitenmuseum.points.v1`);
  - in het geheugen: `POINTS`, `loadPoints()` en `savePoints()`.
- **sensoren:** `orientFrom(alpha, beta, gamma, screenAngle)` gebruikt de W3C-rotatiematrix en geeft `heading`, `pitch` en `roll` terug, gerekend vanuit het scherm. Daardoor maakt de liggende stand niet uit.
  - **iOS:** gyroscoop (`alpha`) gecombineerd met `webkitCompassHeading` via een langzaam bijgestelde offset.
  - **Android:** `deviceorientationabsolute`.
- **camera:** `startDevices()` start bewegingstoestemming, fullscreen/landscape-lock en camera in één tik. Lichtmeter: `meterLight()`.
- **foto + kader:**
  - transformatie `T = {x, y, s, r}`, met x/y als fractie van de viewport;
  - `applyTransform(offX, offY, rotD)` wordt toegepast op `#photo` én `#frame`;
  - `layoutGuide()` zet de vaste hoeken en de pijlposities.
- **modes:** `home | cal-live | cal-adjust | view` via `setMode()`.
- **bezoeker:**
  - `updateView(now)` draait elke frame: residuen buiten de speling, lock met hysterese, pijlen, chip-tekst, afvlakken (`D`) en fade (`D.vis`);
  - `playStory()`, `stopStory()`, `endStory()`.
- **gebaren:**
  - **pinch/drag/rotate:** in `cal-adjust`, rond het middelpunt tussen de vingers;
  - **schuiflijn:** wordt in `view` met Schuif gesleept.
- **testhaak:** `window.__bm` (status, sensoren, punten).

**Tekenconventies:**
- **Richting:** te ver naar rechts gekeken (dH > 0) → beeld schuift naar links → pijl links.
- **Kanteling:** te hoog gericht (dP > 0) → beeld lager → pijl omlaag.
- **Horizon:** met de klok mee gekanteld (dR > 0) → draai tegen de klok in.

**Puntmodel (JSON):**
`{ id, img (dataURL), nowImg (dataURL daglichtbeeld), created, name, year, source, aim, text, i18n: { en: {name, aim, text}, … }, t: {x,y,s,r}, orient: {ok, heading, pitch, roll, abs, angle} }`

## Draaien en testen

- **Camera en bewegingssensoren werken alleen via https** (of `localhost`). Ze werken **niet** in een Claude-artifact, omdat de sandbox camera en sensoren blokkeert.
- **Lokaal op desktop:** `python3 -m http.server 8000` en open dan http://localhost:8000. Je ziet de webcam, maar zonder sensoren werkt de uitlijnhulp niet.
- **Op de telefoon:** zet de map op een https-adres (Netlify Drop, GitHub Pages, of een tunnel als `cloudflared tunnel --url http://localhost:8000`).
- **Automatische test:**

  ```
  pip install playwright && playwright install chromium
  python3 tests/run_test.py
  ```

  - **Wat hij doet:** nepcamera, nagebootste `deviceorientation`, de hele flow inclusief uitlijnen, trillende hand, afspelen, schuif, nacht en EN.
  - **Uitvoer:** screenshots in `tests/out/`, status en fouten in de terminal.
  - **Eerste test:** gebruikt `tests/testfoto-oud.jpg`.
- **iOS-valkuil:** `DeviceOrientationEvent.requestPermission()` en het eerste voorlezen moeten **direct vanuit een tik** gebeuren. Daarom wordt `startDevices()` en `primeSpeech()` aangeroepen vóór de eerste `await` in `startView()`/`startCalibration()`. Laat die volgorde intact.

## Bekende beperkingen

- Nog **niet getest op een echte telefoon** (iOS Safari, Android Chrome). Alleen headless met nagebootste sensoren.
- Het kompas wijkt in de stad 5–15° af. Daarom is de horizontale speling ruim, en kanteling en horizon (via zwaartekracht) zijn nauwkeurig.
- Wat `webkitCompassHeading` precies meet bij liggend vasthouden is onzeker. Het is consistent binnen één platform, maar iOS-kalibratie tegen Android-bezoeker kan afwijken.
- `HFOV = 62°` is een aanname. Andere telefoons (beeldhoek, beeldverhouding) kunnen iets anders uitvallen dan het toestel waarmee is vastgelegd.
- Punten staan **lokaal per toestel**. Een QR-code werkt dus alleen op een toestel waar het punt al op staat. Overzetten gaat via export/import.
- Vertalingen vul je handmatig in via Bewerk. Er is geen automatische vertaling.

## Volgende stappen

1. **Hosten op https en buiten testen.**
   - Eén punt waar iets bleef staan (bijv. bij de Laurenskerk = "herkenning").
   - Eén punt waar niets meer staat ("verdwijning").
   - Meet hoeveel uur één punt kost, van foto tot rechten tot vastleggen tot tekst.
2. **Speling afstellen** met Testinfo aan (graden en licht in beeld).
3. **Centrale opslag + beheeromgeving,** zodat QR-codes op elk toestel werken. Daarna eventueel automatische vertaling.
4. **Mockup van tegel/paaltje,** bijvoorbeeld met een uitsparing waarin je de telefoon liggend legt. Die legt hoogte, richting en kanteling fysiek vast.
