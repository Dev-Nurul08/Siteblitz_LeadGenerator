// 04 Outreach — honest, human-sent contact; signature "Evidence threads" (fact ↔ sentence).
import { useCallback, useEffect, useLayoutEffect, useMemo, useRef, useState } from 'react'
import { motion } from 'motion/react'
import { Ban, Check, Copy, ExternalLink, Info, Mail, MessageCircle, Phone, Send } from 'lucide-react'
import api from '../services/api'
import { go } from '../lib/router'
import { refreshStats } from '../lib/stats'
import { date } from '../lib/format'
import { TitleBlock } from '../components/TitleBlock'
import { DelayedSkeleton, ErrorBanner, StateBlock, TierChip } from '../components/ui'
import { ease, ms } from '../motion'

const OUTCOMES = [['interested', 'Interested'], ['not_now', 'Not now'], ['no_reply', 'No reply'], ['other', 'Other']]
const CHANNELS = [['phone', 'Phone'], ['email', 'Email'], ['social', 'Social message'], ['form', 'Contact form'], ['visit', 'Visit']]

// Facts come only from stored evidence; every sentence lists the facts it relies on.
function buildDraft(detail) {
  const b = detail.business
  const a = detail.assessment || {}
  const checks = detail.checks || []
  const facts = []
  const fact = (id, text, when) => { facts.push({ id, text, when }); return id }
  const lastOf = (type) => [...checks].reverse().find((c) => c.type === type)
  const platforms = Object.keys(b.social_urls || {})
  const sentences = [{ text: `Hi ${b.name} team,`, facts: [] }]
  const searched = lastOf('MANUAL_SEARCH') || lastOf('DOMAIN_GUESS')
  if (a.website_verdict === 'NO_SITE_VERIFIED') {
    const f = fact('nosite', `No website found (${checks.filter((c) => c.type === 'DOMAIN_GUESS').length} domain checks${lastOf('MANUAL_SEARCH') ? ' + your search' : ''})`, searched?.observed_at)
    sentences.push({ text: `I looked for ${b.name}${b.city ? ` in ${b.city}` : ''} online and could not find a website for it.`, facts: [f] })
  } else if (a.website_verdict === 'SOCIAL_ONLY_VERIFIED') {
    const f1 = fact('social', `Social profile: ${platforms.join(', ')}`, lastOf('SOCIAL_LINK')?.observed_at)
    const f2 = fact('nosite', 'No website of its own found', searched?.observed_at)
    sentences.push({ text: `I found ${b.name} on ${platforms.join(' and ')}, but not a website of your own.`, facts: [f1, f2] })
  } else if (a.website_verdict === 'SITE_DOWN_CONFIRMED') {
    const f = fact('down', `Listed website ${b.website_url || ''} failed on separate checks`, lastOf('SITE_FETCH')?.observed_at)
    sentences.push({ text: `The website listed for ${b.name} did not open when I checked it on different days.`, facts: [f] })
  } else if (a.website_verdict === 'OWN_SITE_VERIFIED') {
    const fetch = lastOf('SITE_FETCH')
    if (fetch?.detail?.has_viewport === false) {
      const f = fact('mobile', 'Website has no mobile viewport setting', fetch.observed_at)
      sentences.push({ text: `Your website ${b.website_url || ''} does not adapt to phone screens.`, facts: [f] })
    }
    if (fetch?.detail?.has_ssl === false) {
      const f = fact('https', 'Website opens without HTTPS', fetch.observed_at)
      sentences.push({ text: 'Browsers mark it as "Not secure" because it has no HTTPS.', facts: [f] })
    }
  }
  if (b.category) {
    const f = fact('category', `Category: ${b.category}`)
    sentences.push({ text: `SiteBlitz builds websites for businesses like yours (${b.category.toLowerCase()}), and I would be glad to show you what one for ${b.name} could look like.`, facts: [f] })
  } else {
    sentences.push({ text: `SiteBlitz builds websites for local businesses, and I would be glad to show you what one for ${b.name} could look like.`, facts: [] })
  }
  sentences.push({ text: 'Would a 10-minute call this week work for you?', facts: [] })
  sentences.push({ text: '— [your name], SiteBlitz', facts: [] })
  return { facts, sentences }
}

function Threads({ draft, hover, setHover }) {
  const grid = useRef(null)
  const [line, setLine] = useState(null)
  useLayoutEffect(() => {
    if (!hover || !grid.current || window.innerWidth < 768) { setLine(null); return }
    const box = grid.current.getBoundingClientRect()
    const f = grid.current.querySelector(`[data-fact="${hover}"]`)
    const s = grid.current.querySelector(`[data-uses~="${hover}"]`)
    if (!f || !s) { setLine(null); return }
    const a = f.getBoundingClientRect(), b = s.getBoundingClientRect()
    setLine({ x1: a.right - box.left, y1: a.top + a.height / 2 - box.top, x2: b.left - box.left, y2: b.top + b.height / 2 - box.top })
  }, [hover])
  const unlinked = draft.sentences.filter((s) => s.facts.length === 0).length
  return (
    <div className="draft-grid" ref={grid}>
      <div className="facts" aria-label="Facts used">
        <div className="label">Facts used</div>
        {draft.facts.map((f) => (
          <div key={f.id} data-fact={f.id} className={`fact ${hover === f.id ? 'lit' : ''}`} tabIndex={0}
            onMouseEnter={() => setHover(f.id)} onMouseLeave={() => setHover(null)} onFocus={() => setHover(f.id)} onBlur={() => setHover(null)}>
            {f.text}{f.when && <div className="mono muted" style={{ fontSize: 13 }}>{date(f.when)}</div>}
          </div>
        ))}
        {draft.facts.length === 0 && <div className="muted" style={{ fontSize: 14 }}>No stored facts for this lead yet.</div>}
      </div>
      <div>
        <div className="paper" id="draft-text">
          {draft.sentences.map((s, i) => (
            <p key={i} style={{ margin: '0 0 12px' }}>
              <span data-uses={s.facts.join(' ')} className={`sentence ${s.facts.length ? 'linked' : 'muted-p'} ${s.facts.includes(hover) ? 'lit' : ''}`}
                onMouseEnter={() => s.facts[0] && setHover(s.facts[0])} onMouseLeave={() => setHover(null)}>{s.text}</span>
            </p>
          ))}
        </div>
        <div className="hint" style={{ marginTop: 8 }}>{unlinked} sentence{unlinked === 1 ? '' : 's'} have no linked fact (greeting, offer, question, sign-off).</div>
      </div>
      {line && (
        <svg style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', pointerEvents: 'none', overflow: 'visible' }} aria-hidden="true">
          <motion.path d={`M${line.x1} ${line.y1} C ${line.x1 + 24} ${line.y1}, ${line.x2 - 24} ${line.y2}, ${line.x2} ${line.y2}`}
            fill="none" stroke="var(--accent)" strokeWidth="1" initial={{ pathLength: 0 }} animate={{ pathLength: 1 }} transition={{ duration: 0.24, ease: ease.entrance }} />
        </svg>
      )}
    </div>
  )
}

function Workspace({ id, onChanged }) {
  const [detail, setDetail] = useState(null)
  const [error, setError] = useState(null)
  const [hover, setHover] = useState(null)
  const [checked, setChecked] = useState(false)
  const [copied, setCopied] = useState(false)
  const [log, setLog] = useState({ channel: 'phone', outcome: 'no_reply', note: '' })
  const [logError, setLogError] = useState(null)
  const [confirmDnc, setConfirmDnc] = useState(false)
  const load = useCallback(() => api.intelligence.detail(id).then(setDetail).catch((e) => setError(e.message)), [id])
  useEffect(() => { setDetail(null); setChecked(false); load() }, [load])
  const draft = useMemo(() => (detail ? buildDraft(detail) : null), [detail])
  if (error) return <ErrorBanner message={error} onRetry={load} />
  if (!detail) return <DelayedSkeleton rows={10} />
  const b = detail.business
  const blocked = detail.assessment?.outreach_readiness === 'BLOCKED'
  const digits = (b.phone || '').replace(/\D/g, '')

  async function copy() {
    await navigator.clipboard.writeText(draft.sentences.map((s) => s.text).join('\n\n'))
    setCopied(true); setTimeout(() => setCopied(false), ms.copyHold)
  }
  async function saveLog(extra = {}) {
    setLogError(null)
    try {
      const res = await api.intelligence.contactLog(id, { ...log, note: log.note || undefined, ...extra })
      setDetail(res); setLog((l) => ({ ...l, note: '' })); refreshStats(); onChanged()
    } catch (e) { setLogError(e.message) }
  }
  async function doNotContact() {
    await saveLog({ outcome: 'do_not_contact', note: 'Added to do-not-contact list' })
    if (b.email) await api.qualification.addOptOut({ email: b.email, reason: 'Do-not-contact (outreach)', source: 'MANUAL' }).catch(() => {})
    setConfirmDnc(false)
  }
  return (
    <div className="stack">
      {blocked && <div className="banner banner-error" role="status"><Ban size={16} />On the do-not-contact list — every action is off.</div>}
      <section className="panel" aria-labelledby="routes-h">
        <div className="panel-head"><h2 id="routes-h">{b.name}</h2><TierChip tier={detail.assessment?.tier} /></div>
        <div className="scroll-x"><table className="data" style={{ fontSize: 14 }}><tbody>
          <tr><td><Phone size={16} /> Phone</td><td className="mono">{b.phone || '—'}</td>
            <td>{b.phone && !blocked && <a className="btn btn-sm" href={`tel:${b.phone}`}>Call</a>} {digits && !blocked && <a className="btn btn-sm" href={`https://wa.me/${digits}`} target="_blank" rel="noreferrer noopener"><MessageCircle size={16} />Open chat</a>}</td></tr>
          <tr><td><Mail size={16} /> Email</td><td className="mono">{b.email || '—'}</td>
            <td>{b.email && !blocked && <button className="btn btn-sm" onClick={() => navigator.clipboard.writeText(b.email)}><Copy size={16} />Copy email</button>}</td></tr>
          {Object.entries(b.social_urls).map(([k, url]) => (
            <tr key={k}><td>{k}</td><td className="mono" style={{ overflowWrap: 'anywhere' }}>{url}</td>
              <td>{!blocked && <a className="btn btn-sm" href={url} target="_blank" rel="noreferrer noopener"><ExternalLink size={16} />Open profile</a>}</td></tr>
          ))}
        </tbody></table></div>
        <p className="hint" style={{ marginBottom: 0 }}>WhatsApp: business messages need the person's opt-in, so chats are opened by you, by hand — never sent automatically.</p>
      </section>

      <section className="panel" aria-labelledby="draft-h">
        <div className="panel-head"><h2 id="draft-h">Draft</h2></div>
        <Threads draft={draft} hover={hover} setHover={setHover} />
        <label className="switch" style={{ margin: '16px 0 8px' }}><input type="checkbox" checked={checked} onChange={(e) => setChecked(e.target.checked)} />I checked every fact in this draft</label>
        <div className="row">
          <button className="btn btn-primary" disabled={!checked || blocked} onClick={copy}>
            <motion.span key={copied ? 'y' : 'n'} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: 0.15 }} style={{ display: 'inline-flex' }}>{copied ? <Check size={16} /> : <Copy size={16} />}</motion.span>
            {copied ? 'Copied' : 'Copy draft'}</button>
          {!checked && <span className="hint">Tick the box first.</span>}
          <button className="btn" aria-disabled="true" onClick={(e) => e.preventDefault()}><Send size={16} />Send email</button>
          <span className="hint">Sending is off</span>
        </div>
      </section>

      <section className="panel" aria-labelledby="log-h">
        <div className="panel-head"><h2 id="log-h">Log contact</h2></div>
        <div className="row">
          <select className="input" style={{ width: 'auto' }} value={log.channel} onChange={(e) => setLog({ ...log, channel: e.target.value })} aria-label="Channel" disabled={blocked}>
            {CHANNELS.map(([v, l]) => <option key={v} value={v}>{l}</option>)}</select>
          <select className="input" style={{ width: 'auto' }} value={log.outcome} onChange={(e) => setLog({ ...log, outcome: e.target.value })} aria-label="Outcome" disabled={blocked}>
            {OUTCOMES.map(([v, l]) => <option key={v} value={v}>{l}</option>)}</select>
          <input className="input" style={{ flex: 1, minWidth: 160 }} placeholder="Note" value={log.note} onChange={(e) => setLog({ ...log, note: e.target.value })} aria-label="Note" disabled={blocked} />
          <button className="btn" disabled={blocked} onClick={() => saveLog()}>Save log</button>
        </div>
        {logError && <div style={{ color: 'var(--error)', fontSize: 13, marginTop: 8 }}>{logError}</div>}
        <ul style={{ listStyle: 'none', padding: 0, margin: '16px 0 0' }}>
          {detail.contact_log.map((l) => (
            <li key={l.id} className="check-row" style={{ gridTemplateColumns: '160px 1fr' }}>
              <span className="mono muted">{date(l.logged_at)}</span>
              <span>{CHANNELS.find((c) => c[0] === l.channel)?.[1]} · {l.outcome.replace(/_/g, ' ')}{l.note && <span className="muted"> — {l.note}</span>}</span>
            </li>
          ))}
          {detail.contact_log.length === 0 && <li className="muted" style={{ fontSize: 14 }}>Not contacted yet.</li>}
        </ul>
        <div style={{ marginTop: 16 }}>
          {!confirmDnc ? <button className="btn btn-sm" disabled={blocked} onClick={() => setConfirmDnc(true)}><Ban size={16} />Add to do-not-contact list</button> : (
            <div className="row"><span className="ink2" style={{ fontSize: 14 }}>Never contact {b.name} again?</span>
              <button className="btn btn-sm" onClick={doNotContact}>Yes, add</button><button className="btn btn-sm" onClick={() => setConfirmDnc(false)}>Cancel</button></div>
          )}
        </div>
      </section>
    </div>
  )
}

export default function OutreachPage({ params, entrance }) {
  const [queue, setQueue] = useState(null)
  const [error, setError] = useState(null)
  const [selected, setSelected] = useState(params.lead ? Number(params.lead) : null)
  const load = useCallback(async () => {
    setError(null)
    try {
      const [hot, warm] = await Promise.all([api.intelligence.leads({ tier: 'HOT', page_size: 100 }), api.intelligence.leads({ tier: 'WARM', page_size: 100 })])
      const items = [...hot.items, ...warm.items]
      setQueue(items)
      setSelected((s) => s ?? items[0]?.id ?? null)
    } catch (e) { setError(e.message) }
  }, [])
  useEffect(() => { load() }, [load])
  return (
    <>
      <TitleBlock index="04" title="Outreach" entrance={entrance} text="Step 4 of 4. Contact a lead yourself and log what happened." />
      <div className="banner banner-info"><Info size={16} /><span style={{ flex: 1 }}>Sending is off: no email provider is connected. Copy the draft, send it yourself, then log it here.</span><a href="#/settings">Settings</a></div>
      {error && <ErrorBanner message={`Could not load leads. ${error}`} onRetry={load} />}
      {!queue && !error && <DelayedSkeleton />}
      {queue && queue.length === 0 && (
        <div className="panel"><StateBlock icon={Send} title="No leads in outreach yet" text="Hot and warm leads appear here." action={<button className="btn btn-primary" onClick={() => go('leads')}>See hot leads</button>} /></div>
      )}
      {queue && queue.length > 0 && (
        <div className="outreach-grid">
          <nav className="panel" aria-label="Lead queue" style={{ padding: 8, maxHeight: '75vh', overflow: 'auto' }}>
            {queue.map((x) => (
              <div key={x.id} className="queue-item" role="button" tabIndex={0} aria-selected={selected === x.id}
                onClick={() => setSelected(x.id)} onKeyDown={(e) => e.key === 'Enter' && setSelected(x.id)}>
                <span>{x.name}<div className="muted" style={{ fontSize: 13 }}>{x.city || '—'}</div></span><TierChip tier={x.tier} />
              </div>
            ))}
          </nav>
          {selected !== null && <motion.div key={selected} initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ duration: ms.indicator / 1000, ease: ease.ui }}>
            <Workspace id={selected} onChanged={load} /></motion.div>}
        </div>
      )}
    </>
  )
}
