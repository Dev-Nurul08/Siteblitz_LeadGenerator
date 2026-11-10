"""Hit every GET route on the running QA backend and report status codes (no external calls)."""
import json, sys, urllib.request, urllib.error, sqlite3
BASE = "http://127.0.0.1:8000"
db = sqlite3.connect(r"E:/tmp/_qa_scratch/qa_runtime.db")
def one(sql):
    try:
        r = db.execute(sql).fetchone(); return r[0] if r else None
    except Exception as e:
        return None
ids = {
  "source_id": one("select id from sources limit 1") or one("select id from data_sources limit 1"),
  "business_id": one("select id from businesses limit 1"),
  "job_id": one("select id from source_jobs order by rowid desc limit 1"),
  "opportunity_id": one("select id from opportunities limit 1"),
  "lead_id": one("select id from qualified_leads limit 1"),
  "campaign_id": one("select id from campaigns limit 1"),
  "slug": "overture", "city": "Surat",
}
print("ids:", ids)
routes = [l.split() for l in open(r"E:/tmp/_qa_scratch/routes.txt") if l.startswith("GET")]
for _, path in routes:
    p = path
    for k, v in ids.items():
        p = p.replace("{%s}" % k, str(v))
    try:
        with urllib.request.urlopen(BASE + p, timeout=30) as r:
            code, body = r.status, r.read()
    except urllib.error.HTTPError as e:
        code, body = e.code, e.read()
    except Exception as e:
        code, body = "EXC", str(e).encode()
    print(code, p, body[:160].decode("utf-8", "replace").replace("\n", " ") if code != 200 else len(body))
