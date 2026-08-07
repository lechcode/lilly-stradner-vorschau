/**
 * Beweis-Screenshots · lilly-stradner — 390 px und 1440 px, DPR 2.
 *
 * Warum projekteigen: pipeline/bin/qa-tools/aldo-shots.mjs traegt noch die
 * Seitenliste des vorigen Projekts (siehe README-aldo-messungen.md).
 *
 * Wichtig: Die Seite blendet Abschnitte beim Scrollen ein. Fuer einen
 * fullPage-Screenshot muss deshalb einmal durchgescrollt werden, sonst
 * sind untere Abschnitte auf dem Bild unsichtbar.
 *
 * Aufruf (Server muss laufen):
 *   node qa-shots.mjs http://localhost:8018 ./beweise/nachher
 */
// Playwright liegt zentral in pipeline/bin/qa-tools/. Relativ aufgeloest,
// damit im oeffentlichen Vorschau-Repo kein lokaler Benutzerpfad steht.
import { createRequire } from 'node:module';
const { chromium } = createRequire(
  new URL('../../../pipeline/bin/qa-tools/', import.meta.url)
)('playwright');

const BASIS = process.argv[2] || 'http://localhost:8018';
const AUS   = process.argv[3] || './beweise/nachher';

const SEITEN = [
  ['startseite',      'index.html'],
  ['startseite-en',   'en.html'],
  ['richtungB',       'hell.html'],      // Pergament-Fassung
  ['richtungB-en',    'hell-en.html'],
  ['vorschau',        'vorschau.html'],
  ['impressum',       'impressum.html'],
  ['datenschutz',     'datenschutz.html'],
  ['agb',             'agb.html'],
  ['impressum-en',    'impressum-en.html'],
  ['datenschutz-en',  'datenschutz-en.html'],
  ['agb-en',          'agb-en.html'],
  ['404',             '404.html'],
];

const GROESSEN = [['mobil-390', 390, 844], ['desktop-1440', 1440, 900]];

const browser = await chromium.launch();

for (const [name, datei] of SEITEN) {
  for (const [label, w, h] of GROESSEN) {
    const ctx  = await browser.newContext({ viewport: { width: w, height: h }, deviceScaleFactor: 2 });
    const page = await ctx.newPage();
    await page.goto(`${BASIS}/${datei}`, { waitUntil: 'networkidle' });

    // Erster Viewport, bevor gescrollt wird — zeigt, was ohne Zutun sichtbar ist.
    if (name.startsWith('startseite') || name.startsWith('richtungB')) {
      await page.waitForTimeout(350);
      await page.screenshot({ path: `${AUS}/erster-viewport-${name}-${label}.png` });
    }

    // Einmal durchscrollen, damit alle Reveals ausgeloest sind.
    await page.evaluate(async () => {
      const schritt = window.innerHeight * 0.8;
      for (let y = 0; y < document.body.scrollHeight; y += schritt) {
        window.scrollTo(0, y);
        await new Promise(r => setTimeout(r, 110));
      }
      window.scrollTo(0, 0);
      await new Promise(r => setTimeout(r, 250));
    });

    await page.screenshot({ path: `${AUS}/${name}-${label}.png`, fullPage: true });
    console.log(`  ${name}-${label}`);
    await ctx.close();
  }
}

await browser.close();
console.log(`\n${SEITEN.length * GROESSEN.length + 4} Screenshots · DPR 2 · ${AUS}`);
