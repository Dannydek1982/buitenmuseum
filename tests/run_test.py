"""Automatische test van het Buitenmuseum-prototype.

Start een lokale server, opent de app in Chrome met een nepcamera en nagebootste
bewegingssensoren, doorloopt vastleggen -> vertalen -> bekijken -> uitlijnen -> afspelen,
en bewaart screenshots in tests/out/.

Gebruik:  pip install playwright && playwright install chromium
          python3 tests/run_test.py
(optioneel CHROME_PATH=/pad/naar/chrome)
"""
import asyncio, json, subprocess, sys, time, os
from playwright.async_api import async_playwright

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'out')
os.makedirs(OUT, exist_ok=True)
PHOTO = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'testfoto-oud.jpg')

async def hold(page, alpha, beta, gamma, n=30):
    for _ in range(n):
        await page.evaluate("""([a,b,g]) => {
            const type = ('ondeviceorientationabsolute' in window) ? 'deviceorientationabsolute' : 'deviceorientation';
            window.dispatchEvent(new DeviceOrientationEvent(type, {alpha:a, beta:b, gamma:g, absolute:true}));
        }""", [alpha, beta, gamma])
        await page.wait_for_timeout(16)

STATE = """() => ({
  chip: document.querySelector('#chip').textContent,
  chipOk: document.querySelector('#chip').classList.contains('ok'),
  guide: document.querySelector('#guide').className,
  arrows: ['arL','arR','arU','arD','arRot'].filter(id => document.getElementById(id).classList.contains('on')),
  op: document.querySelector('#photoLayer').style.opacity,
  locked: window.__bm.locked, playing: window.__bm.playing
})"""

async def main():
    srv = subprocess.Popen([sys.executable, '-m', 'http.server', '8771', '--bind', '127.0.0.1'], cwd=ROOT,
                           stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(0.8)
    errors = []
    async with async_playwright() as p:
        browser = await p.chromium.launch(executable_path=os.environ.get('CHROME_PATH') or None, args=[
            '--use-fake-ui-for-media-stream', '--use-fake-device-for-media-stream', '--no-sandbox'])
        ctx = await browser.new_context(viewport={'width': 390, 'height': 844}, device_scale_factor=2, is_mobile=True,
                                        has_touch=True, permissions=['camera','accelerometer','gyroscope','magnetometer'], locale='nl-NL')
        page = await ctx.new_page()
        page.on('console', lambda m: errors.append(f'console.{m.type}: {m.text}') if m.type in ('error',) else None)
        page.on('pageerror', lambda e: errors.append(f'pageerror: {e}'))
        await page.goto('http://127.0.0.1:8771/index.html')
        await page.wait_for_function('window.__bm && window.__bm.ready')
        await page.screenshot(path=f'{OUT}/01_home.png')

        # --- vastleggen ---
        await page.click('#btnNew'); await page.wait_for_timeout(150)
        await page.set_input_files('#photoFile', PHOTO)
        await page.wait_for_selector('[data-act=startcal]')
        await page.set_viewport_size({'width': 844, 'height': 390})
        await page.click('[data-act=startcal]')
        await page.wait_for_timeout(1000)
        await hold(page, 330, 90, 0)
        await page.click('#btnShutter'); await page.wait_for_timeout(250)
        await page.mouse.move(420, 200); await page.mouse.down(); await page.mouse.move(460, 214, steps=6); await page.mouse.up()
        await page.click('#btnNext'); await page.wait_for_timeout(150)
        await page.fill('#fName', 'Hoogstraat bij de Markthal')
        await page.fill('#fYear', '1938')
        await page.fill('#fSrc', 'Stadsarchief Rotterdam')
        await page.fill('#fAim', 'de toren van de Laurenskerk')
        await page.fill('#fText', 'Voor het bombardement van mei 1940 was dit een drukke winkelstraat. Kijk naar de gevels links: daar zat een bakkerij. Na de brand bleef alleen de kerk staan.')
        await page.click('[data-act=save]'); await page.wait_for_timeout(400)

        # --- vertaling toevoegen ---
        await page.set_viewport_size({'width': 390, 'height': 844}); await page.wait_for_timeout(200)
        await page.click('[data-act=edit]'); await page.wait_for_timeout(150)
        await page.click('[data-act=etab][data-l=en]'); await page.wait_for_timeout(100)
        await page.fill('#eName', 'Hoogstraat near the Markthal')
        await page.fill('#eAim', 'the tower of the Laurenskerk')
        await page.fill('#eText', 'Before the bombing of May 1940 this was a busy shopping street. Look at the facades on the left: there was a bakery. After the fire only the church remained.')
        await page.screenshot(path=f'{OUT}/02_edit_en.png')
        await page.click('[data-act=esave]'); await page.wait_for_timeout(300)
        await page.screenshot(path=f'{OUT}/03_home_list.png')
        pts = await page.evaluate("() => window.__bm.loadPoints().map(p => ({name:p.name, i18n:Object.keys(p.i18n||{}), now: !!p.nowImg, t:p.t}))")
        print('POINTS', json.dumps(pts))

        # --- bezoeker: startscherm in EN ---
        await page.set_viewport_size({'width': 844, 'height': 390}); await page.wait_for_timeout(150)
        await page.click('[data-act=entry]'); await page.wait_for_timeout(200)
        await page.click('[data-act=lang][data-l=en]'); await page.wait_for_timeout(200)
        await page.screenshot(path=f'{OUT}/04_entry_en.png')
        await page.click('[data-act=lang][data-l=nl]'); await page.wait_for_timeout(150)
        await page.screenshot(path=f'{OUT}/04b_entry_nl.png')
        await page.click('[data-act=startview]'); await page.wait_for_timeout(900)

        cases = [
            ('05_ver_weg', 260, 90),      # 70 graden te ver naar rechts
            ('06_links', 300, 90),        # 30 graden
            ('07_omhoog', 330, 78),       # 12 graden te laag
            ('08_diagonaal', 300, 78),    # beide
            ('09_goed', 326, 88),         # binnen de speling
        ]
        for name, a, b in cases:
            await hold(page, a, b, 0, n=45)
            await page.wait_for_timeout(300)
            st = await page.evaluate(STATE)
            print(name.upper(), json.dumps(st, ensure_ascii=False))
            await page.screenshot(path=f'{OUT}/{name}.png')

        # trillende hand: korte uitschieter mag niet loslaten
        await hold(page, 326, 79, 0, n=12)   # 9 graden: buiten 8, binnen 12 (hold)
        print('TRIL', json.dumps(await page.evaluate(STATE), ensure_ascii=False))
        await hold(page, 326, 88, 0, n=20)

        # --- play ---
        await page.click('#btnPlay'); await hold(page, 326, 88, 0, n=110)
        print('PLAY', json.dumps(await page.evaluate(STATE), ensure_ascii=False),
              await page.evaluate("() => document.querySelector('#storyLine').textContent"))
        await page.screenshot(path=f'{OUT}/10_play.png')
        await page.click('#btnPlay'); await page.wait_for_timeout(300)

        # --- schuif ---
        await page.click('[data-vm=wipe]'); await page.wait_for_timeout(200)
        await page.mouse.move(300, 200); await page.mouse.down(); await page.mouse.move(520, 200, steps=6); await page.mouse.up()
        await hold(page, 326, 88, 0, n=40)
        await page.screenshot(path=f'{OUT}/11_schuif.png')

        # --- nacht ---
        await page.click('[data-vm=half]')
        await page.click('#btnNight'); await page.wait_for_timeout(1200)
        print('NACHT', json.dumps(await page.evaluate(STATE), ensure_ascii=False))
        await page.screenshot(path=f'{OUT}/12_nacht.png')
        await page.click('#btnNight')

        # --- info in EN ---
        await page.click('#btnInfo'); await page.wait_for_timeout(200)
        await page.click('[data-act=lang][data-l=en]'); await page.wait_for_timeout(200)
        await page.screenshot(path=f'{OUT}/13_info_en.png')
        await page.click('[data-act=close]')
        await hold(page, 260, 90, 0, n=30)
        print('EN CHIP', json.dumps(await page.evaluate(STATE), ensure_ascii=False))
        await hold(page, 300, 78, 0, n=30)
        print('EN DIAG', json.dumps(await page.evaluate(STATE), ensure_ascii=False))
        await page.set_viewport_size({'width': 390, 'height': 844}); await page.wait_for_timeout(200)
        await page.screenshot(path=f'{OUT}/14_rotate_en.png')

        # --- herladen: blijft opgeslagen (IndexedDB) ---
        await page.goto('http://127.0.0.1:8771/index.html')
        await page.wait_for_function('window.__bm && window.__bm.ready')
        print('AFTER RELOAD', await page.evaluate("() => window.__bm.loadPoints().length"))

        await browser.close()
    srv.terminate()
    print('ERRORS', json.dumps(errors, indent=1))

asyncio.run(main())
