// 02 Review — website verdicts with evidence; signature "The row becomes its evidence".
import { Fragment, lazy, Suspense, useCallback, useEffect, useMemo, useState } from 'react'
import { LayoutGroup, motion } from 'motion/react'
import { CircleCheck, CircleDashed, CircleX, ExternalLink, ListChecks, MapPin, RefreshCw, Search, TriangleAlert } from 'lucide-react'
import api from '../services/api'
import { go } from '../lib/router'
import { refreshStats } from '../lib/stats'
import { ago, coord, dateSeconds, num } from '../lib/format'
import { TitleBlock } from '../components/TitleBlock'
import { ConfidenceChip, DelayedSkeleton, Drawer, ErrorBanner, Segmented, Spinner, StateBlock, VerdictChip } from '../components/ui'
import { ease, ms } from '../motion'

const MapView = lazy(() => import('../components/MapView'))
const VERDICT_FILTERS = [
  ['', 'All'], ['UNKNOWN', 'Needs review'], ['UNCHECKED', 'Not checked yet'], ['NO_SITE_VERIFIED', 'No website found'],
  ['SOCIAL_ONLY_VERIFIED', 'Social media only'], ['SITE_DOWN_CONFIRMED', 'Website down'],
  ['OWN_SITE_VERIFIED', 'Has own website'], ['SKIP', 'Skipped'],
]
const CHECK_NAMES = {
  SKIP_RULE: 'Exclusion rules (chains, ATMs, closed…)', SOURCE_TAG: 'Website field in the source data',
  SOCIAL_LINK: 'Social profile', LINK_IN_BIO: 'Link-in-bio page', SITE_FETCH: 'Open the website',
  DOMAIN_GUESS: 'Domain guess', SEARCH: 'Web search', MANUAL_SEARCH: 'Your web search', MANUAL_ACTIVITY: 'Open / closed',
}
const LABELS = { CORRECT: 'Correct', WRONG: 'Wrong', UNSURE: 'Not sure' }
const WRONG_PARTS = [['ownership', 'Website ownership'], ['activity', 'Open or closed'], ['identity', 'Wrong business'], ['exclusion', 'Should (not) be skipped'], ['need', 'Need / score']]

function checkView(c) {
  const d = c.detail || {}
  const positive = ['found', 'ok', 'protected', 'matched', 'links', 'pass', 'active']
  const negative = ['none', 'no_match', 'failed', 'inactive', 'skip', 'social']
  let Icon = CircleCheck, cls = 'ok-ico'
  if (negative.includes(c.outcome)) { Icon = CircleX; cls = 'bad-ico' }
  if (c.outcome === 'not_checked') { Icon = CircleDashed; cls = 'dim-ico' }
  if (['error', 'blocked'].includes(c.outcome)) { Icon = TriangleAlert; cls = 'mid-ico' }
  if (!positive.includes(c.outcome) && !negative.includes(c.outcome) && Icon === CircleCheck) cls = 'dim-ico'
  const result = {
    SITE_FETCH: { ok: `Opened (HTTP ${d.http_status})`, protected: `Exists — blocks robots (HTTP ${d.http_status}), not counted as down`,
      failed: d.note || `Failed (${d.http_status ? `HTTP ${d.http_status}` : d.error || 'no answer'})`, social: 'Redirects to a social page', blocked: d.error || 'Blocked (private address)' }[c.outcome],
    DOMAIN_GUESS: { none: d.note || 'Domain does not exist', no_match: 'Exists, but it is another business', matched: `This business's site (${(d.signals || []).join(', ')})` }[c.outcome],
    SOURCE_TAG: { found: 'Listed', none: 'No website listed in any source' }[c.outcome],
    LINK_IN_BIO: { not_checked: d.note, links: `Links: ${(d.links || []).join(', ')}`, none: 'No external links' }[c.outcome],
    MANUAL_SEARCH: { none: 'You found no website', found: 'You found its website' }[c.outcome],
    MANUAL_ACTIVITY: { active: `Open (${d.method})`, inactive: `Closed (${d.method})` }[c.outcome],
    SKIP_RULE: { pass: 'Not excluded', skip: d.reason }[c.outcome],
  }[c.type] || c.outcome
  return { Icon, cls, name: CHECK_NAMES[c.type] || c.type, result }
}

function Evidence({ id, onLabelled, onChanged }) {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  const [busy, setBusy] = useState(null)
  const [foundUrl, setFoundUrl] = useState('')
  const [wrongPart, setWrongPart] = useState('')
  const [labelError, setLabelError] = useState(null)
  const load = useCallback(() => {
    setError(null)
    api.intelligence.detail(id).then(setData).catch((e) => setError(e.message))
  }, [id])
  useEffect(() => { setData(null); setWrongPart(''); setFoundUrl(''); load() }, [load])

  async function act(name, fn) {
    setBusy(name)
    try { setData(await fn()); onChanged(); refreshStats() } catch (e) { setError(e.message) } finally { setBusy(null) }
  }
  async function label(value) {
    if (value === 'WRONG' && !wrongPart) { setLabelError('Pick what was wrong first.'); return }
    setLabelError(null)
    try {
      const res = await api.intelligence.label(id, { label: value, wrong_part: value === 'WRONG' ? wrongPart : undefined })
      setData(res); refreshStats(); onLabelled(value)
    } catch (e) { setLabelError(e.message) }
  }
  useEffect(() => {
    const onKey = (e) => {
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes(e.target.tagName)) return
      if (e.key === '1') label('CORRECT'); if (e.key === '2') label('WRONG'); if (e.key === '3') label('UNSURE')
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  })

  const a = data?.assessment
  const b = data?.business
  return (
    <>
      <div className="drawer-head">
        <motion.h2 id="drawer-title" layoutId={`name-${id}`} style={{ paddingRight: 48 }}>{b?.name || '…'}</motion.h2>
        <div className="row">
          <VerdictChip verdict={a?.website_verdict || 'UNCHECKED'} layoutId={`verdict-${id}`} />
          {a && <><span className="label">Confidence</span><ConfidenceChip value={a.evidence_confidence} /></>}
        </div>
        {a?.summary && <p className="ink2" style={{ margin: 0, fontSize: 14 }}>{a.summary}</p>}
      </div>
      <div className="drawer-body">
        {error && <ErrorBanner message={error} onRetry={load} />}
        {!data && !error && <DelayedSkeleton rows={5} />}
        {data && !a && (
          <StateBlock icon={ListChecks} title="Not checked yet" text="Run every website check for this business."
            action={<button className="btn btn-primary" disabled={!!busy} onClick={() => act('assess', () => api.intelligence.assess(id))}>
              {busy === 'assess' ? <><Spinner />Checking…</> : 'Check this business'}</button>} />
        )}
        {data && data.checks.length > 0 && (
          <section aria-labelledby="checks-h">
            <div className="panel-head" style={{ marginBottom: 8 }}><h3 id="checks-h">Checks, in the order they ran</h3>
              <button className="btn btn-sm" disabled={!!busy} onClick={() => act('assess', () => api.intelligence.assess(id))}>
                {busy === 'assess' ? <Spinner /> : <RefreshCw size={16} />}Check again</button></div>
            {data.checks.map((c, i) => {
              const v = checkView(c)
              return (
                <motion.div key={c.id} className="check-row"
                  initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }}
                  transition={{ duration: 0.24, delay: Math.min(i * ms.checksStagger, ms.checksBudget - 240) / 1000, ease: ease.entrance }}>
                  <v.Icon size={16} strokeWidth={1.75} className={v.cls} aria-hidden="true" style={{ marginTop: 4 }} />
                  <div>
                    <div>{v.name}{c.target && <span className="mono muted"> · {c.target}</span>}</div>
                    <div className="ink2" style={{ fontSize: 14 }}>{v.result}</div>
                    <div className="when">{dateSeconds(c.observed_at)}</div>
                  </div>
                </motion.div>
              )
            })}
          </section>
        )}
        {b && (
          <section aria-labelledby="facts-h">
            <h3 id="facts-h" style={{ marginBottom: 8 }}>What the sources say</h3>
            <dl className="kv">
              <dt>Category</dt><dd>{b.category || '—'}</dd>
              <dt>Address</dt><dd>{[b.address, b.city, b.country_code].filter(Boolean).join(', ') || '—'}</dd>
              <dt>Phone</dt><dd className="mono">{b.phone || '—'}</dd>
              <dt>Email</dt><dd className="mono">{b.email || '—'}</dd>
              <dt>Website</dt><dd className="mono">{b.website_url || '—'}</dd>
              {Object.entries(b.social_urls).map(([k, url]) => (
                <Fragment key={k}><dt>{k}</dt><dd><a href={url} target="_blank" rel="noreferrer noopener">{url}</a></dd></Fragment>
              ))}
              <dt>Coordinates</dt><dd className="mono">{coord(b.lat)}, {coord(b.lon)} {b.lat !== null && <a href={`#/review?view=map&business=${b.id}`}><MapPin size={14} /> Show on map</a>}</dd>
            </dl>
          </section>
        )}
        {a && a.website_verdict !== 'SKIP' && b && (
          <section aria-labelledby="you-h" className="stack" style={{ gap: 12 }}>
            <h3 id="you-h">Your checks</h3>
            <div className="row">
              <a className="btn btn-sm" target="_blank" rel="noreferrer noopener"
                href={`https://www.google.com/search?q=${encodeURIComponent(`${b.name} ${b.city || ''}`)}`}><Search size={16} />Search “{b.name}” <ExternalLink size={14} /></a>
              <button className="btn btn-sm" disabled={!!busy} onClick={() => act('nosite', () => api.intelligence.manualSearch(id, {}))}>I found no website</button>
            </div>
            <div className="row">
              <input className="input" style={{ flex: 1, minWidth: 180 }} placeholder="Website you found" value={foundUrl} onChange={(e) => setFoundUrl(e.target.value)} aria-label="Website you found" maxLength={1000} />
              <button className="btn btn-sm" disabled={!foundUrl || !!busy} onClick={() => act('found', () => api.intelligence.manualSearch(id, { found_url: foundUrl }))}>Save website</button>
            </div>
            <div className="row">
              <button className="btn btn-sm" disabled={!!busy} onClick={() => act('open', () => api.intelligence.activity(id, { active: true, method: 'call' }))}>Confirmed open (call)</button>
              <button className="btn btn-sm" disabled={!!busy} onClick={() => act('closed', () => api.intelligence.activity(id, { active: false, method: 'call' }))}>It is closed</button>
            </div>
          </section>
        )}
      </div>
      {a && (
        <div className="drawer-foot">
          <div className="row" style={{ justifyContent: 'space-between' }}>
            <span className="label">Is this verdict right?</span>
            {a.label && <motion.span key={a.label} className="chip chip-outline" initial={{ scale: 1.08, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} transition={{ duration: ms.stamp / 1000 }}>You: {LABELS[a.label]}</motion.span>}
          </div>
          <div className="row">
            {Object.entries(LABELS).map(([value, text], i) => (
              <button key={value} className="btn btn-sm" aria-pressed={a.label === value} onClick={() => label(value)}>{text} <span className="mono muted">{i + 1}</span></button>
            ))}
            <select className="input" style={{ width: 'auto', height: 32 }} value={wrongPart} onChange={(e) => setWrongPart(e.target.value)} aria-label="What was wrong">
              <option value="">If wrong: what?</option>
              {WRONG_PARTS.map(([v, t]) => <option key={v} value={v}>{t}</option>)}
            </select>
          </div>
          {labelError && <div style={{ color: 'var(--error)', fontSize: 13 }}>{labelError}</div>}
          <div className="hint">1 2 3 to label · J K to move · Esc to close</div>
        </div>
      )}
    </>
  )
}

export default function ReviewPage({ params, entrance, stats }) {
  const [verdict, setVerdict] = useState(params.verdict || '')
  const [search, setSearch] = useState('')
  const [view, setView] = useState(params.view === 'map' ? 'map' : 'table')
  const [page, setPage] = useState(1)
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  const [selected, setSelected] = useState(params.business ? Number(params.business) : null)
  const [points, setPoints] = useState([])
  const [batch, setBatch] = useState(null)
  const job = params.job ? Number(params.job) : undefined

  const load = useCallback(() => {
    setError(null)
    api.intelligence.leads({ verdict, search, job_id: job, page }).then(setData).catch((e) => setError(e.message))
  }, [verdict, search, job, page])
  useEffect(() => { const id = setTimeout(load, search ? 250 : 0); return () => clearTimeout(id) }, [load, search])
  useEffect(() => { setPage(1) }, [verdict, search, job])
  useEffect(() => { if (view === 'map') api.points({ job_id: job }).then((r) => setPoints(r.points)).catch(() => {}) }, [view, job, data])

  const items = useMemo(() => data?.items || [], [data])
  const move = useCallback((delta) => {
    if (!items.length) return
    const i = items.findIndex((x) => x.id === selected)
    const next = items[Math.min(items.length - 1, Math.max(0, (i < 0 ? -1 : i) + delta))]
    if (next) setSelected(next.id)
  }, [items, selected])
  useEffect(() => {
    const onKey = (e) => {
      if (['INPUT', 'TEXTAREA', 'SELECT'].includes(e.target.tagName)) return
      if (e.key === 'j' || e.key === 'J') move(1)
      if (e.key === 'k' || e.key === 'K') move(-1)
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [move])

  async function checkBatch() {
    setBatch({ running: true })
    try {
      const res = await api.intelligence.assessBatch({ job_id: job, limit: 25 })
      setBatch({ running: false, ...res }); load(); refreshStats()
    } catch (e) { setBatch({ running: false, error: e.message }) }
  }
  // Label "stamp" then open the next unlabelled row after 240 ms (spec v2 Review signature).
  const onLabelled = () => {
    load()
    const i = items.findIndex((x) => x.id === selected)
    const next = items.slice(i + 1).find((x) => !x.label && x.website_verdict !== 'UNCHECKED')
    if (next) setTimeout(() => setSelected(next.id), ms.autoAdvance)
  }

  const counts = data?.verdict_counts || {}
  const labels = stats?.labels || {}
  return (
    <>
      <TitleBlock index="02" title="Review website checks" entrance={entrance}
        text="Step 2 of 4. See what was found about each business's website, and mark each verdict right or wrong."
        actions={<>
          {job && <span className="chip chip-outline">Search #{job} <a href="#/review" aria-label="Show all searches" style={{ color: 'var(--ink-3)' }}>×</a></span>}
          <button className="btn" onClick={checkBatch} disabled={batch?.running}>{batch?.running ? <><Spinner />Checking 25…</> : <><ListChecks size={16} />Check websites for 25 businesses</>}</button>
        </>} />
      {batch && !batch.running && !batch.error && <div className="banner banner-info">Checked {num(batch.assessed)} · {num(batch.remaining_unassessed)} still not checked.</div>}
      {batch?.error && <ErrorBanner message={batch.error} onRetry={checkBatch} />}
      <div className="row" style={{ justifyContent: 'space-between', marginBottom: 12 }}>
        <div className="row">
          <input className="input" style={{ width: 280 }} placeholder="Search by name" value={search} onChange={(e) => setSearch(e.target.value)} aria-label="Search by name" maxLength={500} />
          <Segmented id="view" value={view} onChange={setView} options={[{ value: 'table', label: 'Table' }, { value: 'map', label: 'Map' }]} />
        </div>
        <div className="ink2" style={{ fontSize: 13 }}>
          Your labels: <span className="num">{num(stats?.labeled ?? 0)}</span> of 200 · <span className="num">{num(labels.CORRECT ?? 0)}</span> correct · <span className="num">{num(labels.WRONG ?? 0)}</span> wrong · <span className="num">{num(labels.UNSURE ?? 0)}</span> not sure
        </div>
      </div>
      <div style={{ marginBottom: 12 }}>
        <Segmented id="verdict" value={verdict} onChange={setVerdict}
          options={VERDICT_FILTERS.map(([v, l]) => ({ value: v, label: l, count: v ? counts[v] ?? 0 : undefined }))} />
      </div>
      <p className="hint" style={{ margin: '0 0 12px' }}>Green: a possible lead (no real website). Yellow: needs your check. Grey: not a lead.</p>

      {error && <ErrorBanner message={`Could not load businesses. ${error}`} onRetry={load} />}
      {view === 'map' ? (
        <Suspense fallback={<div className="map-frame" />}><MapView points={points} animate={false} onSelect={setSelected} /></Suspense>
      ) : (
        <LayoutGroup>
          {!data && !error && <DelayedSkeleton />}
          {data && items.length === 0 && (
            <div className="panel">
              {search || verdict ? <StateBlock title="No businesses match these filters" action={<button className="btn" onClick={() => { setSearch(''); setVerdict('') }}>Clear filters</button>} />
                : <StateBlock icon={Search} title="No businesses yet" text="Search a city first; the results appear here." action={<button className="btn btn-primary" onClick={() => go('find')}>Start a search</button>} />}
            </div>
          )}
          {items.length > 0 && (
            <div className="table-wrap">
              <table className="data">
                <thead><tr><th>Business</th><th className="hide-sm">Category</th><th className="hide-sm">City</th><th>Website verdict</th><th className="hide-sm">Checked</th><th className="hide-sm">Your label</th></tr></thead>
                <tbody>
                  {items.map((x) => (
                    <tr key={x.id} aria-selected={selected === x.id} tabIndex={0}
                      onClick={() => setSelected(x.id)} onKeyDown={(e) => e.key === 'Enter' && setSelected(x.id)}>
                      <td>{selected === x.id ? x.name : <motion.span layoutId={`name-${x.id}`} style={{ display: 'inline-block' }}>{x.name}</motion.span>}</td>
                      <td className="hide-sm">{x.category || '—'}</td>
                      <td className="hide-sm">{x.city || '—'}</td>
                      <td>{selected === x.id ? <VerdictChip verdict={x.website_verdict} /> : <VerdictChip verdict={x.website_verdict} layoutId={`verdict-${x.id}`} />}</td>
                      <td className="mono hide-sm" title={x.assessed_at || ''}>{ago(x.assessed_at)}</td>
                      <td className="hide-sm">{x.label ? LABELS[x.label] : <span className="muted">—</span>}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
          {data && data.pages > 1 && (
            <div className="pager">
              <span>{num((page - 1) * data.page_size + 1)}–{num(Math.min(page * data.page_size, data.total))} of {num(data.total)}</span>
              <span className="row"><button className="btn btn-sm" disabled={page <= 1} onClick={() => setPage(page - 1)}>Previous</button>
                <button className="btn btn-sm" disabled={page >= data.pages} onClick={() => setPage(page + 1)}>Next</button></span>
            </div>
          )}
          <Drawer open={selected !== null} onClose={() => setSelected(null)} labelledBy="drawer-title">
            {selected !== null && <Evidence key={selected} id={selected} onLabelled={onLabelled} onChanged={load} />}
          </Drawer>
        </LayoutGroup>
      )}
      {view === 'map' && (
        <Drawer open={selected !== null} onClose={() => setSelected(null)} labelledBy="drawer-title">
          {selected !== null && <Evidence key={selected} id={selected} onLabelled={load} onChanged={load} />}
        </Drawer>
      )}
    </>
  )
}
