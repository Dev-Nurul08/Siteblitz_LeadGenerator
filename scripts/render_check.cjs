// Email engine v2, phase E1 - rendered phone check of a homepage (docs/spec/email-engine-v2.md row 4).
//
// Usage: PW_PATH=<path to the playwright package> node scripts/render_check.cjs <jobs.json>
//   jobs.json = [{"key": "<business id>", "url": "https://...", "screenshot": "E:/.../evidence/<date>/x.png"}]
// Prints one JSON line per job:
//   {"key", "url", "checked_at", "result": "ZOOMED_OUT" | "FITS" | "ERROR", "inner_width", "final_url",
//    "screenshot", "load_timeout", "error"}
//
// Chromium emulates a phone: isMobile, touch, 390 x 844, deviceScaleFactor 3. After the page loads (12 s
// navigation timeout), window.innerWidth >= 900 means the page has no working viewport tag and the browser fell
// back to a desktop-width layout, so the page opens zoomed-out. One viewport screenshot is kept as evidence.
// Only URLs that the Python side checked with the SSRF guard are passed in; requests to localhost or a private
// IP literal are aborted here as a second line of defence. Nothing is clicked, typed or submitted.

const fs = require('fs');
const path = require('path');

const { chromium } = require(process.env.PW_PATH || 'playwright');

const NAV_TIMEOUT_MS = 12000;
const ZOOMED_OUT_MIN_INNER_WIDTH = 900;
const USER_AGENT = 'Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) '
  + 'Chrome/140.0.0.0 Mobile Safari/537.36 SiteBlitzEnricher/1.0';

function isPrivateHost(host) {
  const h = (host || '').toLowerCase().replace(/^\[|\]$/g, '');
  if (h === 'localhost' || h.endsWith('.localhost') || h === '0.0.0.0') return true;
  const v4 = h.match(/^(\d+)\.(\d+)\.(\d+)\.(\d+)$/);
  if (v4) {
    const [a, b] = [Number(v4[1]), Number(v4[2])];
    return a === 10 || a === 127 || a === 0 || (a === 169 && b === 254) || (a === 192 && b === 168)
      || (a === 172 && b >= 16 && b <= 31) || (a === 100 && b >= 64 && b <= 127);
  }
  return h === '::1' || h.startsWith('fc') || h.startsWith('fd') || h.startsWith('fe80');
}

async function renderOne(browser, job) {
  const out = { key: job.key, url: job.url, checked_at: new Date().toISOString() };
  const context = await browser.newContext({
    isMobile: true, hasTouch: true, viewport: { width: 390, height: 844 }, deviceScaleFactor: 3,
    userAgent: USER_AGENT,
  });
  try {
    const page = await context.newPage();
    await page.route('**/*', (route) => {
      let host = '';
      try { host = new URL(route.request().url()).hostname; } catch (e) { return route.abort(); }
      return isPrivateHost(host) ? route.abort() : route.continue();
    });
    let loadTimeout = false;
    try {
      await page.goto(job.url, { waitUntil: 'load', timeout: NAV_TIMEOUT_MS });
    } catch (e) {
      // A slow image or script can keep "load" from firing; the layout viewport is already known once the
      // document is there. Nothing loaded at all = an error, not a result.
      if (page.url() === 'about:blank') throw e;
      loadTimeout = true;
    }
    const innerWidth = await page.evaluate(() => window.innerWidth);
    fs.mkdirSync(path.dirname(job.screenshot), { recursive: true });
    await page.screenshot({ path: job.screenshot, fullPage: false });
    Object.assign(out, {
      result: innerWidth >= ZOOMED_OUT_MIN_INNER_WIDTH ? 'ZOOMED_OUT' : 'FITS',
      inner_width: innerWidth, final_url: page.url(), screenshot: job.screenshot, load_timeout: loadTimeout,
    });
  } catch (e) {
    out.result = 'ERROR';
    out.error = String((e && e.message) || e).split('\n')[0].slice(0, 300);
  } finally {
    await context.close().catch(() => {});
  }
  return out;
}

(async () => {
  const jobs = JSON.parse(fs.readFileSync(process.argv[2], 'utf8'));
  const browser = await chromium.launch({ headless: true });
  try {
    for (const job of jobs) {
      process.stdout.write(JSON.stringify(await renderOne(browser, job)) + '\n');
    }
  } finally {
    await browser.close();
  }
})().catch((e) => {
  process.stderr.write(String((e && e.stack) || e) + '\n');
  process.exit(1);
});
