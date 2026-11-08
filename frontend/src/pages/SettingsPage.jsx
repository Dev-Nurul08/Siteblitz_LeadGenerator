// Settings — live source check (each row resolves in real response order) + do-not-contact list.
import { useCallback, useEffect, useState } from 'react'
import { AnimatePresence, motion } from 'motion/react'
import { Ban } from 'lucide-react'
import api from '../services/api'
import { date } from '../lib/format'
import { TitleBlock } from '../components/TitleBlock'
import { DelayedSkeleton, ErrorBanner, Spinner, StateBlock } from '../components/ui'

const SOURCES = [
  { slug: 'overture', name: 'Overture Places (default)', needs: 'Internet + DuckDB; reads public map data by city' },
  { slug: 'openstreetmap', name: 'OpenStreetMap', needs: 'Internet (Overpass API)' },
  { slug: 'csv_import', name: 'CSV file', needs: 'A UTF-8 CSV with a name column' },
]
const STATIC_ROWS = [
  { name: 'Google Places', needs: 'An API key and a licensing check', status: ['Not built yet', 'chip-outline'] },
  { name: 'Email provider', needs: 'Connect one before the app can send', status: ['Not connected', 'chip-review'] },
]
const STATUS = { ready: ['Ready', 'chip-lead'], unreachable: ['Not reachable', 'chip-error'], not_configured: ['Not set up', 'chip-review'] }

function HealthCell({ slug }) {
  const [res, setRes] = useState(null)
  useEffect(() => {
    let alive = true
    api.sourceHealth(slug).then((r) => alive && setRes(r)).catch((e) => alive && setRes({ status: 'unreachable', detail: e.message }))
    return () => { alive = false }
  }, [slug])
  return (
    <AnimatePresence mode="wait" initial={false}>
      {!res ? <motion.span key="s" exit={{ opacity: 0 }} transition={{ duration: 0.15 }}><Spinner label="Checking" /></motion.span> : (
        <motion.span key="r" initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.15 }}>
          <span className={`chip ${STATUS[res.status][1]}`}>{STATUS[res.status][0]}</span>
          {res.detail && <span className="mono muted" style={{ fontSize: 13, marginLeft: 8 }}>{res.detail}</span>}
        </motion.span>
      )}
    </AnimatePresence>
  )
}

export default function SettingsPage({ entrance }) {
  const [optOuts, setOptOuts] = useState(null)
  const [error, setError] = useState(null)
  const [form, setForm] = useState({ email: '', reason: '' })
  const [formError, setFormError] = useState(null)
  const load = useCallback(() => {
    setError(null)
    api.qualification.listOptOuts({ page: 1, pageSize: 100 }).then((r) => setOptOuts(r.items)).catch((e) => setError(e.message))
  }, [])
  useEffect(() => { load() }, [load])
  async function add(e) {
    e.preventDefault()
    setFormError(null)
    try {
      await api.qualification.addOptOut({ email: form.email, reason: form.reason || 'Do-not-contact (manual)', source: 'MANUAL' })
      setForm({ email: '', reason: '' }); load()
    } catch (err) { setFormError(err.message) }
  }
  return (
    <>
      <TitleBlock title="Settings" entrance={entrance} text="Where the data comes from, and who must never be contacted." />
      <section className="stack">
        <div>
          <div className="panel-head"><h2>Data sources</h2></div>
          <div className="table-wrap" style={{ maxHeight: 'none' }}>
            <table className="data"><thead><tr><th>Source</th><th className="hide-sm">What it needs</th><th>Status</th></tr></thead>
              <tbody>
                {SOURCES.map((s) => <tr key={s.slug} style={{ cursor: 'default' }}><td>{s.name}</td><td className="hide-sm ink2">{s.needs}</td><td><HealthCell slug={s.slug} /></td></tr>)}
                {STATIC_ROWS.map((s) => <tr key={s.name} style={{ cursor: 'default' }}><td>{s.name}</td><td className="hide-sm ink2">{s.needs}</td><td><span className={`chip ${s.status[1]}`}>{s.status[0]}</span></td></tr>)}
              </tbody></table>
          </div>
          <p className="hint">Keys are set in the backend .env file. This page only shows whether something is ready; it never shows or stores a key.</p>
        </div>
        <div>
          <div className="panel-head"><h2>Do-not-contact list</h2></div>
          <form className="row" onSubmit={add} style={{ marginBottom: 12 }}>
            <input className="input" style={{ width: 280 }} required type="email" maxLength={255} placeholder="Email address" aria-label="Email address" value={form.email} onChange={(e) => setForm({ ...form, email: e.target.value })} />
            <input className="input" style={{ flex: 1, minWidth: 160 }} maxLength={255} placeholder="Reason (optional)" aria-label="Reason" value={form.reason} onChange={(e) => setForm({ ...form, reason: e.target.value })} />
            <button className="btn" type="submit"><Ban size={16} />Add to list</button>
          </form>
          {formError && <ErrorBanner message={formError} />}
          {error && <ErrorBanner message={`Could not load the list. ${error}`} onRetry={load} />}
          {!optOuts && !error && <DelayedSkeleton rows={3} />}
          {optOuts && optOuts.length === 0 && <div className="panel"><StateBlock icon={Ban} title="No one is on the do-not-contact list" /></div>}
          {optOuts && optOuts.length > 0 && (
            <div className="table-wrap"><table className="data"><thead><tr><th>Email / domain</th><th>Reason</th><th className="hide-sm">Added</th></tr></thead>
              <tbody>{optOuts.map((o) => <tr key={o.id} style={{ cursor: 'default' }}><td className="mono">{o.email}</td><td>{o.reason}</td><td className="mono hide-sm">{date(o.created_at)}</td></tr>)}</tbody></table></div>
          )}
          <p className="hint">Phone-only businesses are blocked from the Outreach screen ("Add to do-not-contact list"), which also blocks them here in the app.</p>
        </div>
      </section>
    </>
  )
}
