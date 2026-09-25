// Esporta ogni slide di carousels.html come PNG 1080×1350.
// Uso: node social/render.js   (richiede Playwright con Chromium)
const path = require("path");
const fs = require("fs");

let playwright;
try { playwright = require("playwright"); } catch (e) {
  playwright = require("/opt/node22/lib/node_modules/playwright");
}

(async () => {
  const src = path.join(__dirname, "carousels.html");
  const browser = await playwright.chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1350 } });
  await page.goto("file://" + src);
  await page.evaluate(() => document.body.classList.add("render"));
  await page.evaluate(() => document.fonts.ready);

  const slides = await page.$$(".slide");
  for (const slide of slides) {
    const file = await slide.getAttribute("data-file");
    const out = path.join(__dirname, file);
    fs.mkdirSync(path.dirname(out), { recursive: true });
    await slide.screenshot({ path: out });
    console.log("✓", file);
  }
  await browser.close();
})();
