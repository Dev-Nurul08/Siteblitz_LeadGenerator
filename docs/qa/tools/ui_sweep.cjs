// QA UI sweep: every route at 1280 and 390, captures console errors, page errors, failed/5xx requests.
const { chromium } = require(process.env.PW_PATH);
const OUT = process.argv[2];
const ROUTES = ['find', 'review', 'leads', 'outreach', 'settings', 'radar'];
(async () => {
  const browser = await chromium.launch();
  const report = [];
  for (const width of (process.env.WIDTHS || '1280,390').split(',').map(Number)) {
    const ctx = await browser.newContext({ viewport: { width, height: width === 390 ? 844 : 800 }, reducedMotion: 'reduce' });
    for (const r of ROUTES) {
      const page = await ctx.newPage();
      const errs = [];
      page.on('console', m => { if (m.type() === 'error' || m.type() === 'warning') errs.push(`console.${m.type()}: ${m.text().slice(0, 300)}`); });
      page.on('pageerror', e => errs.push(`pageerror: ${String(e).slice(0, 300)}`));
      page.on('response', res => { if (res.status() >= 400) errs.push(`http ${res.status()} ${res.request().method()} ${res.url()}`); });
      page.on('requestfailed', req => errs.push(`requestfailed ${req.url()} ${req.failure()?.errorText}`));
      await page.goto(`http://localhost:5173/#/${r}`, { waitUntil: 'domcontentloaded' });
      await page.waitForTimeout(r === 'find' || r === 'review' ? 6000 : 3500);
      const file = `${OUT}/${process.env.PREFIX || ""}${width}-${r}.png`;
      await page.screenshot({ path: file, fullPage: false });
      const h1 = await page.locator('h1, h2').first().textContent().catch(() => null);
      const bodyText = (await page.locator('body').innerText().catch(() => '')).slice(0, 200).replace(/\s+/g, ' ');
      const overflowX = await page.evaluate(() => document.documentElement.scrollWidth > window.innerWidth);
      report.push({ width, route: r, heading: h1 && h1.trim(), overflowX, errors: errs, text: bodyText, file });
      await page.close();
    }
    await ctx.close();
  }
  await browser.close();
  console.log(JSON.stringify(report, null, 1));
})().catch(e => { console.error('SWEEP FAILED', e); process.exit(1); });
