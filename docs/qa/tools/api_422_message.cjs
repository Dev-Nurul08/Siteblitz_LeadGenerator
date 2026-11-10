// Reproduce: what message does the frontend API client throw for a FastAPI 422 (detail is an array)?
const { chromium } = require(process.env.PW_PATH);
(async () => {
  const b = await chromium.launch(); const p = await b.newPage();
  await p.goto('http://localhost:5173/#/settings', { waitUntil: 'domcontentloaded' });
  const out = await p.evaluate(async () => {
    const { api } = await import('/src/services/api.js');
    const res = {};
    try { await api.businesses.list({ page_size: -1 }); res.list422 = 'no error'; } catch (e) { res.list422 = e.message; }
    try { await api.businesses.get(999999); res.get404 = 'no error'; } catch (e) { res.get404 = e.message; }
    return res;
  });
  console.log(JSON.stringify(out)); await b.close();
})();
