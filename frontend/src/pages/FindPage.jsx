// 01 Find — new search, live status, map signature "Businesses land on the map", past searches.
import { lazy, Suspense, useCallback, useEffect, useRef, useState } from 'react'
import { motion } from 'motion/react'
import { Download, FileText, Pause, Play, Search, Upload } from 'lucide-react'
import api from '../services/api'
import { go } from '../lib/router'
import { refreshStats } from '../lib/stats'
import { date, num } from '../lib/format'
import { TitleBlock } from '../components/TitleBlock'
import { DelayedSkeleton, ErrorBanner, JobChip, Spinner, StateBlock, Ticker } from '../components/ui'
import { ease, ms } from '../motion'

const MapView = lazy(() => import('../components/MapView'))

// Same country list the old Discovery page offered; any ISO code can be typed in "Other".
const COUNTRIES = [['IN', 'India'], ['GB', 'United Kingdom'], ['US', 'United States'], ['AU', 'Australia'],
  ['CA', 'Canada'], ['DE', 'Germany'], ['FR', 'France'], ['AE', 'United Arab Emirates'], ['SG', 'Singapore'], ['NZ', 'New Zealand']]
const CATEGORIES = ['dentist', 'salon', 'hairdresser', 'cafe', 'restaurant', 'gym', 'clinic', 'hotel', 'school',
  'lawyer', 'accountant', 'estate_agent', 'car_repair', 'plumber', 'electrician', 'bakery', 'shop']
const SOURCES = [
  { id: 'all_sources', name: 'All sources (default)', note: 'Overture Places + OpenStreetMap together, duplicates merged — the most businesses per search' },
  { id: 'overture', name: 'Overture Places', note: 'Free · map position, phone and social links for most businesses' },
  { id: 'openstreetmap', name: 'OpenStreetMap', note: 'Free · volunteer-mapped, thin in small cities' },
  { id: 'google', name: 'Google Places', note: 'Not available yet — needs an API key and a licensing check', disabled: true },
  { id: 'csv', name: 'CSV file', note: 'Your own list · UTF-8, up to 15 MB / 5,000 rows' },
]
// 100 = the API's batch limit; checks inside a batch run concurrently (~40 s per 100).
const CHECK_BATCH = 100

function FlowDiagram() {
  const [paused, setPaused] = useState(false)
  const lane = (y, label, color) => (
    <g>
      <path className="pulse" d={`M330 120 C 380 120, 380 ${y}, 430 ${y}`} />
      <rect x="430" y={y - 18} width="170" height="36" rx="6" fill="var(--surface)" stroke={color} />
      <text x="515" y={y + 5} textAnchor="middle">{label}</text>
      <path className="pulse" d={`M600 ${y} C 640 ${y}, 640 120, 680 120`} />
    </g>
  )
  return (
    <div className="lanes">
      <style>{`.flow text{fill:var(--ink-2);font:13px var(--font)} .flow .pulse{fill:none;stroke:var(--line-strong);stroke-width:1.5;stroke-dasharray:6 10;animation:flow ${ms.diagramCycle}ms linear infinite} .flow.paused .pulse{animation-play-state:paused} @keyframes flow{to{stroke-dashoffset:-64}}`}</style>
      <svg className={`flow ${paused ? 'paused' : ''}`} viewBox="0 0 860 240" width="100%" style={{ maxWidth: 860 }} role="img"
        aria-label="How it works: search a city, check every website, sort into leads, then hot leads">
        <rect x="20" y="102" width="150" height="36" rx="6" fill="var(--accent-tint)" stroke="var(--accent)" />
        <text x="95" y="125" textAnchor="middle">Search: cafés in Udaipur</text>
        <path className="pulse" d="M170 120 H 200" />
        <rect x="200" y="102" width="130" height="36" rx="6" fill="var(--surface)" stroke="var(--line-strong)" />
        <text x="265" y="125" textAnchor="middle">Website checks</text>
        {lane(50, 'A lead (no real website)', 'var(--dot-lead)')}
        {lane(120, 'Needs your review', 'var(--dot-review)')}
        {lane(190, 'Not a lead (has a site)', 'var(--dot-notlead)')}
        <rect x="680" y="102" width="150" height="36" rx="6" fill="var(--surface)" stroke="var(--accent)" />
        <text x="755" y="125" textAnchor="middle">Hot leads</text>
      </svg>
      <button className="btn btn-sm" style={{ position: 'absolute', right: 12, top: 12, width: 32, padding: 0 }}
        onClick={() => setPaused((p) => !p)} aria-label={paused ? 'Play diagram' : 'Pause diagram'}>
        {paused ? <Play size={16} /> : <Pause size={16} />}
      </button>
    </div>
  )
}

function ExportLinks({ jobId }) {
  return (
    <>
      <button className="btn btn-sm" onClick={() => go('review', { job: jobId })}>View businesses</button>
      <a className="btn btn-sm" href={api.businesses.exportUrl({ job_id: jobId }, 'csv')} download><Download size={16} />Export CSV</a>
      <a className="btn btn-sm" href={api.businesses.exportUrl({ job_id: jobId }, 'pdf')} download><FileText size={16} />Export PDF</a>
    </>
  )
}

export default function FindPage({ entrance }) {
  const [form, setForm] = useState({ source: 'all_sources', country: 'IN', city: '', category: '', max: 500, franchises: false })
  const [csvFile, setCsvFile] = useState(null)
  const [jobs, setJobs] = useState(null)
  const [jobsError, setJobsError] = useState(null)
  const [current, setCurrent] = useState({ phase: 'idle' })
  const [points, setPoints] = useState([])
  const [checking, setChecking] = useState(null) // { done, remaining, running }
  const stopChecks = useRef(false)
  const alive = useRef(true)
  // Set on every mount: React StrictMode mounts twice in development, and a ref that is only
  // ever cleared would silently drop every later state update.
  useEffect(() => { alive.current = true; return () => { alive.current = false; stopChecks.current = true } }, [])

  const loadJobs = useCallback(async () => {
    try { setJobs(await api.discovery.jobs(20)); setJobsError(null) } catch (e) { setJobsError(e.message) }
  }, [])
  useEffect(() => { loadJobs() }, [loadJobs])

  // Default map: the last finished job's businesses.
  useEffect(() => {
    if (current.phase === 'idle' && jobs && jobs.length) {
      api.points({ job_id: jobs[0].job_id }).then((r) => alive.current && setPoints(r.points)).catch(() => {})
    }
  }, [jobs, current.phase])

  const set = (k) => (e) => setForm((f) => ({ ...f, [k]: e.target.type === 'checkbox' ? e.target.checked : e.target.value }))

  async function runChecks(jobId) {
    stopChecks.current = false
    let done = 0
    for (;;) {
      if (stopChecks.current || !alive.current) break
      setChecking((c) => ({ done, remaining: c ? c.remaining : null, running: true }))
      let res
      try { res = await api.intelligence.assessBatch({ job_id: jobId, limit: CHECK_BATCH, include_franchises: form.franchises }) }
      catch { break }
      done += res.assessed
      if (!alive.current) return
      setChecking({ done, remaining: res.remaining_unassessed, running: res.remaining_unassessed > 0 })
      const pts = await api.points({ job_id: jobId }).catch(() => null)
      if (pts && alive.current) setPoints(pts.points)
      refreshStats()
      if (res.assessed === 0 || res.remaining_unassessed === 0) break
    }
    if (alive.current) setChecking((c) => (c ? { ...c, running: false } : c))
  }

  async function start(e) {
    e.preventDefault()
    setCurrent({ phase: 'queued', search: `${form.category || 'All businesses'} in ${form.city || '—'}, ${form.country}` })
    setChecking(null)
    setPoints([])
    try {
      setCurrent((c) => ({ ...c, phase: 'running' }))
      const res = form.source === 'csv'
        ? await api.discovery.importCsv(csvFile, form.country)
        : await api.discovery.run({ source_slug: form.source, country_code: form.country, city: form.city.trim(),
          category: form.category.trim() || undefined, max_results: Number(form.max) })
      if (!alive.current) return
      setCurrent((c) => ({ ...c, phase: 'done', job: res }))
      loadJobs()
      refreshStats()
      const pts = await api.points({ job_id: res.job_id }).catch(() => ({ points: [] }))
      if (alive.current) setPoints(pts.points)
      if (res.new + res.duplicate > 0) runChecks(res.job_id)
    } catch (err) {
      if (alive.current) setCurrent((c) => ({ ...c, phase: 'error', error: err.message }))
    }
  }

  const job = current.job
  const zero = job && job.found === 0
  const csv = form.source === 'csv'
  const firstRun = jobs && jobs.length === 0 && current.phase === 'idle'
  const phaseIndex = { idle: -1, queued: 0, running: 1, done: 2, error: 2 }[current.phase]

  return (
    <>
      <TitleBlock index="01" title="Find businesses" entrance={entrance}
        text="Step 1 of 4. Search one city for one kind of business. Every result gets its website checked, then goes to Review." />
      <div className="grid-find">
        <div className="stack">
          <form className="panel" onSubmit={start} aria-labelledby="new-search">
            <div className="panel-head"><h2 id="new-search">New search</h2></div>
            <div className="source-cards" role="radiogroup" aria-label="Source">
              {SOURCES.map((s) => (
                <button type="button" key={s.id} role="radio" className="source-card" aria-checked={form.source === s.id}
                  aria-disabled={s.disabled || undefined} onClick={() => !s.disabled && setForm((f) => ({ ...f, source: s.id }))}>
                  <span><b>{s.name}</b><span>{s.note}</span></span>
                </button>
              ))}
            </div>
            <div className="field">
              <label className="label" htmlFor="country">Country</label>
              <select id="country" className="input" value={form.country} onChange={set('country')}>
                {COUNTRIES.map(([code, name]) => <option key={code} value={code}>{name} ({code})</option>)}
              </select>
            </div>
            {!csv && (
              <>
                <div className="field">
                  <label className="label" htmlFor="city">City</label>
                  <input id="city" className="input" required maxLength={200} value={form.city} onChange={set('city')} placeholder="Udaipur" />
                </div>
                <div className="field">
                  <label className="label" htmlFor="category">Kind of business</label>
                  <input id="category" className="input" list="categories" maxLength={200} value={form.category} onChange={set('category')} placeholder="cafe" />
                  <datalist id="categories">{CATEGORIES.map((c) => <option key={c} value={c} />)}</datalist>
                </div>
                <div className="field">
                  <label className="label" htmlFor="max">Max results</label>
                  <select id="max" className="input" value={form.max} onChange={set('max')}>
                    {[50, 100, 200, 500, 1000, 2000, 5000].map((n) => <option key={n} value={n}>{n}</option>)}
                  </select>
                </div>
              </>
            )}
            {csv && (
              <label className="dropzone" htmlFor="csvfile">
                <Upload size={20} aria-hidden="true" /><br />
                {csvFile ? `${csvFile.name} · ${num(Math.round(csvFile.size / 1024))} KB` : 'Choose a CSV file (name column required)'}
                <input id="csvfile" type="file" accept=".csv,.txt" className="sr-only" onChange={(e) => setCsvFile(e.target.files[0])} />
              </label>
            )}
            <label className="switch" style={{ margin: '16px 0' }}>
              <input type="checkbox" checked={form.franchises} onChange={set('franchises')} />
              Include franchises and chains
            </label>
            <button className="btn btn-primary" style={{ width: '100%' }} type="submit"
              disabled={['queued', 'running'].includes(current.phase) || (csv && !csvFile)}>
              {['queued', 'running'].includes(current.phase) ? <><Spinner label="Starting" />Searching…</> : <><Search size={16} />Start search</>}
            </button>
          </form>

          <section className="panel" aria-labelledby="current-search" aria-live="polite">
            <div className="panel-head"><h2 id="current-search">Current search</h2>{job && <JobChip status={job.status} />}</div>
            {current.phase === 'idle' ? <p className="muted" style={{ margin: 0 }}>No search running.</p> : (
              <>
                <div className="ink2">{current.search}</div>
                <div className="statusline">
                  {['Queued', 'Running', 'Finished'].map((label, i) => (
                    <span key={label} className={`dotstep ${phaseIndex >= i ? 'on' : ''}`}><i />{label}{i < 2 && <span aria-hidden="true"> —</span>}</span>
                  ))}
                </div>
                {job && job.available != null && (
                  <p className="ink2" style={{ margin: '0 0 8px', fontSize: 14 }}>
                    The sources have <span className="num">{num(job.available)}</span> matching businesses here; this search took{' '}
                    <span className="num">{num(job.found)}</span>{job.available > job.found ? ' — raise Max results to get more.' : ' — all of them.'}
                  </p>
                )}
                <div className="tickers">
                  {[['Found', job?.found], ['New', job?.new], ['Duplicates', job?.duplicate], ['Errors', job?.errors]].map(([label, value]) => (
                    <div className="ticker" key={label}><div className="label">{label}</div><div className="stat"><Ticker value={value ?? 0} /></div></div>
                  ))}
                </div>
                {current.phase === 'error' && <ErrorBanner message={current.error} onRetry={() => setCurrent({ phase: 'idle' })} />}
                {(zero || job?.error) && (
                  <div className="banner banner-error" role="alert">
                    <span style={{ flex: 1 }}>{zero ? 'The source returned 0 businesses. ' : ''}<span className="mono">{job.error || ''}</span></span>
                    <button className="btn btn-sm" onClick={start}>Retry search</button>
                  </div>
                )}
                {checking && (
                  <div className="row" style={{ marginBottom: 12 }}>
                    {checking.running ? <Spinner label="Checking websites" /> : null}
                    <span className="ink2" style={{ fontSize: 14 }}>
                      Website checks: <span className="num">{num(checking.done)}</span> done
                      {checking.remaining !== null && <> · <span className="num">{num(checking.remaining)}</span> left</>}
                    </span>
                    {checking.running && <button className="btn btn-sm" onClick={() => { stopChecks.current = true }}>Stop checking</button>}
                  </div>
                )}
                {job && !zero && <div className="row"><ExportLinks jobId={job.job_id} /></div>}
              </>
            )}
          </section>
        </div>

        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: ms.indicator / 1000, ease: ease.ui }}>
          {firstRun ? (
            <div className="map-frame"><FlowDiagram /></div>
          ) : (
            <Suspense fallback={<div className="map-frame" />}>
              <MapView points={points} onSelect={(id) => go('review', { business: id })} />
            </Suspense>
          )}
        </motion.div>
      </div>

      <section style={{ marginTop: 32 }} aria-labelledby="past">
        <div className="panel-head"><h2 id="past">Past searches</h2></div>
        {jobsError && <ErrorBanner message={`Could not load past searches. ${jobsError}`} onRetry={loadJobs} />}
        {!jobs && !jobsError && <DelayedSkeleton rows={5} />}
        {jobs && jobs.length === 0 && (
          <div className="panel"><StateBlock icon={Search} title="No searches yet" text="Your first search fills the map and the list."
            action={<button className="btn btn-primary" onClick={() => document.getElementById('city')?.focus()}>Start your first search</button>} /></div>
        )}
        {jobs && jobs.length > 0 && (
          <div className="table-wrap">
            <table className="data">
              <thead><tr>
                <th>Started</th><th>Search</th><th className="hide-sm">Source</th><th>Status</th>
                <th className="num">Found</th><th className="num">New</th><th className="num hide-sm">Duplicates</th><th className="num hide-sm">Errors</th><th>Data</th>
              </tr></thead>
              <tbody>
                {jobs.map((j) => (
                  <tr key={j.job_id} onClick={() => go('review', { job: j.job_id })} tabIndex={0}
                    onKeyDown={(e) => e.key === 'Enter' && go('review', { job: j.job_id })}>
                    <td className="mono">{date(j.started_at)}</td>
                    <td>{[j.category, j.city, j.country_code].filter(Boolean).join(' · ') || '—'}
                      {j.error_message && <div className="mono" style={{ fontSize: 13, color: 'var(--error)' }}>{j.error_message}</div>}</td>
                    <td className="hide-sm">{j.source_name}</td>
                    <td><JobChip status={j.status} /></td>
                    <td className="num">{num(j.records_found)}{j.available != null && j.available > j.records_found && <div className="muted" style={{ fontSize: 13 }}>of {num(j.available)}</div>}</td>
                    <td className="num">{num(j.records_new)}</td>
                    <td className="num hide-sm">{num(j.records_duplicate)}</td>
                    <td className="num hide-sm">{num(j.records_error)}</td>
                    <td onClick={(e) => e.stopPropagation()}><div className="row" style={{ flexWrap: 'nowrap' }}><ExportLinks jobId={j.job_id} /></div></td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </>
  )
}
