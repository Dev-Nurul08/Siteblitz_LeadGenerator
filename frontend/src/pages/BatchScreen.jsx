// 04 Outreach — email batch (email engine v2, phase E3): today's allowance, pauses, founder checks, the eligible
// list, Write (T1–T3 by the AI writer + validator), the READY / HOLD review with evidence, approve / reject, and
// the scheduled result. Nothing here sends mail: approved sequences go to the E2 worker's supervised windows.
import { useCallback, useEffect, useMemo, useState } from 'react'
import { motion } from 'motion/react'
import {
  Ban, CalendarClock, Check, CircleCheck, CirclePause, ExternalLink, Inbox, ListChecks, PenLine, RotateCw,
  ShieldCheck, TriangleAlert, UserCheck,
} from 'lucide-react'
import api from '../services/api'
import { date } from '../lib/format'
import { DelayedSkeleton, ErrorBanner, Segmented, Spinner, StateBlock, Ticker } from '../components/ui'
import { ease, ms } from '../motion'

const OBSERVATION = {
  SOCIAL_ONLY: 'Instagram bio, no website link',
  SITE_DOWN: 'Website did not load',
  NO_VIEWPORT: 'Homepage zoomed-out on a phone',
}
const STATE_CHIP = {
  READY: ['Ready', 'chip-lead'], HOLD: ['Hold', 'chip-review'], APPROVED: ['Approved', 'chip-lead'],
  REJECTED: ['Rejected', 'chip-outline'], PENDING: ['Waiting', 'chip-outline'], WRITING: ['Writing', 'chip-running'],
}
const WINDOW_TEXT = { '09:00-11:30': '09:00–11:30', '14:00-16:30': '14:00–16:30' }
const dayText = (iso) => (iso ? new Intl.DateTimeFormat('en-IN', { weekday: 'short', day: 'numeric', month: 'short' }).format(new Date(`${iso}T00:00:00`)) : '—')
const timeText = (iso) => (iso ? new Intl.DateTimeFormat('en-IN', { hour: '2-digit', minute: '2-digit', hour12: false, timeZone: 'Asia/Kolkata' }).format(new Date(iso)) : '')
const plural = (n, word) => `${n} ${word}${n === 1 ? '' : 's'}`

function useFounderName() {
  const [name, setName] = useState(() => localStorage.getItem('sb.founderName') || '')
  useEffect(() => { localStorage.setItem('sb.founderName', name) }, [name])
  return [name, setName]
}

function StateChip({ state }) {
  const [label, cls] = STATE_CHIP[state] || [state, 'chip-outline']
  return <span className={`chip ${cls}`}>{state === 'WRITING' && <Spinner label="Writing" />}{label}</span>
}

// ─── header: ramp, allowance, mailboxes, pauses ───────────────────────────────

function PauseBanner({ pause, who, onCleared }) {
  const [open, setOpen] = useState(false)
  const [note, setNote] = useState('')
  const [error, setError] = useState(null)
  async function clear() {
    setError(null)
    try { await api.outreach.clearPause({ pause_id: pause.id, cleared_by: who, note }); setOpen(false); onCleared() } catch (e) { setError(e.message) }
  }
  const scope = pause.scope.toLowerCase().replace('_', ' ')
  return (
    <div className="banner banner-error pause-banner" role="status">
      <CirclePause size={16} strokeWidth={1.75} aria-hidden="true" />
      <div style={{ flex: 1, minWidth: 0 }}>
        <div><b>{pause.level === 'STOP' ? 'Stopped' : 'Paused'}: {pause.reason_code}</b> · {scope}{pause.scope_value ? ` ${pause.scope_value}` : ''} · since <span className="mono">{date(pause.created_at)}</span></div>
        {pause.detail && <div className="pause-detail">{pause.detail}</div>}
        {pause.blocks_new_contacts && <div className="pause-detail">New first contacts are blocked until a person clears this.</div>}
        {open && (
          <div className="row" style={{ marginTop: 8 }}>
            <input className="input" style={{ flex: 1, minWidth: 180 }} placeholder="What was checked and fixed" value={note} onChange={(e) => setNote(e.target.value)} aria-label="Note" />
            <button className="btn btn-sm" disabled={!who || note.trim().length < 3} onClick={clear}>Clear pause</button>
            {!who && <span className="hint">Enter your name first.</span>}
          </div>
        )}
        {error && <div className="pause-detail" role="alert">{error}</div>}
      </div>
      {!open && <button className="btn btn-sm" onClick={() => setOpen(true)}>Resolve</button>}
    </div>
  )
}

function AllowanceHeader({ allowance, who, setWho, onChanged }) {
  const a = allowance
  return (
    <section className="panel" aria-labelledby="allow-h">
      <div className="panel-head">
        <h2 id="allow-h">Sending day: {a.send_date_text}</h2>
        <label className="row who" style={{ gap: 8 }}>
          <span className="label">Your name</span>
          <input className="input" style={{ width: 180 }} value={who} onChange={(e) => setWho(e.target.value)} placeholder="Recorded on approvals" aria-label="Your name" />
        </label>
      </div>
      {a.pauses.length > 0 && <div className="stack" style={{ gap: 8, marginBottom: 16 }}>{a.pauses.map((p) => <PauseBanner key={p.id} pause={p} who={who} onCleared={onChanged} />)}</div>}
      <div className="tickers batch-tickers">
        <div className="ticker"><div className="label">Ramp stage</div><div className="stat"><Ticker value={a.ramp_stage} /></div><div className="hint">{a.daily_limit} new a day</div></div>
        <div className="ticker"><div className="label">New contacts left</div><div className="stat"><Ticker value={a.left} /></div><div className="hint">of {a.daily_limit} for {dayText(a.send_date)}</div></div>
        <div className="ticker"><div className="label">Scheduled</div><div className="stat"><Ticker value={a.scheduled_new} /></div><div className="hint">{a.reserved_by_batches} held by unapproved leads</div></div>
        <div className="ticker"><div className="label">Mailboxes</div><div className="stat"><Ticker value={a.mailboxes.filter((m) => !m.paused.length).length} /></div><div className="hint">of {a.mailboxes.length} can send</div></div>
      </div>
      <p className="hint" style={{ margin: '0 0 12px' }}>{a.message}</p>
      {a.mailboxes.length > 0 && (
        <div className="scroll-x"><table className="data mbx-table">
          <thead><tr><th>Mailbox</th><th className="num">Campaign</th><th className="num">All mail</th><th>State</th></tr></thead>
          <tbody>{a.mailboxes.map((m) => (
            <tr key={m.mailbox_id}>
              <td><span className="mono">{m.address}</span><div className="muted" style={{ fontSize: 13 }}>{m.display_name}</div></td>
              <td className="num">{m.campaign_reserved} / {m.campaign_limit}</td>
              <td className="num">{m.total_reserved} / {m.daily_ceiling}</td>
              <td>{m.paused.length ? <span className="chip chip-error">Paused</span> : <span className="chip chip-lead">Ready</span>}</td>
            </tr>
          ))}</tbody>
        </table></div>
      )}
    </section>
  )
}

// ─── founder checks (SOCIAL_ONLY, spec row 4) ──────────────────────────────────

function FounderCheck({ item, onSaved }) {
  const [opened, setOpened] = useState(false)
  const [link, setLink] = useState(null)
  const [email, setEmail] = useState('')
  const [error, setError] = useState(null)
  async function save() {
    setError(null)
    try {
      await api.outreach.confirm({ business_id: item.business_id, profile_url: item.profile_url, checked_at: new Date().toISOString(), website_link_present: link === 'yes', email_seen: email.trim() || null })
      onSaved()
    } catch (e) { setError(e.message) }
  }
  return (
    <li className="check-item">
      <div className="check-item-head">
        <span><b>{item.business_name}</b><span className="muted"> · {item.city || '—'}{item.vertical ? ` · ${item.vertical.replace('_', ' ')}` : ''}</span></span>
        <a className="btn btn-sm" href={item.profile_url} target="_blank" rel="noreferrer noopener" onClick={() => setOpened(true)}><ExternalLink size={16} strokeWidth={1.75} />Open profile</a>
      </div>
      <fieldset className="check-form" disabled={!opened}>
        <legend className="sr-only">Check of {item.business_name}</legend>
        <span className="label">Website link in the bio?</span>
        <label className="switch"><input type="radio" name={`link-${item.business_id}`} checked={link === 'yes'} onChange={() => setLink('yes')} />Yes</label>
        <label className="switch"><input type="radio" name={`link-${item.business_id}`} checked={link === 'no'} onChange={() => setLink('no')} />No</label>
        <input className="input" style={{ flex: 1, minWidth: 180 }} placeholder="Email seen in the bio (optional)" value={email} onChange={(e) => setEmail(e.target.value)} aria-label="Email seen in the bio" />
        <button className="btn btn-sm" disabled={!link} onClick={save}><Check size={16} strokeWidth={1.75} />Save check</button>
      </fieldset>
      {!opened && <div className="hint">Open the profile first; the form unlocks after that.</div>}
      {error && <div className="hint" style={{ color: 'var(--error)' }} role="alert">{error}</div>}
    </li>
  )
}

function FounderChecks({ pending, onSaved }) {
  if (!pending) return null
  return (
    <section className="panel" aria-labelledby="checks-h">
      <div className="panel-head"><h2 id="checks-h">Founder checks</h2><span className="chip chip-outline">{plural(pending.total, 'profile')} to check</span></div>
      {pending.items.length === 0
        ? <p className="hint" style={{ margin: 0 }}>No Instagram profile is waiting for a check.</p>
        : <ul className="check-list">{pending.items.slice(0, 5).map((item) => <FounderCheck key={item.business_id} item={item} onSaved={onSaved} />)}</ul>}
      {pending.items.length > 5 && <p className="hint" style={{ marginBottom: 0 }}>Showing 5 of {pending.total}. The next ones appear after these are saved.</p>}
    </section>
  )
}

// ─── the eligible list ────────────────────────────────────────────────────────

function CandidateList({ data, allowance, filter, setFilter, reason, setReason, selected, setSelected, who, onWrite, writing, error }) {
  const left = allowance.left
  const atCap = left > 0 && selected.size >= left
  const reasons = Object.entries(data.counts.by_hold_reason)
  const [blockedClick, setBlockedClick] = useState(false)
  function toggle(id) {
    const next = new Set(selected)
    if (next.has(id)) next.delete(id)
    else if (next.size >= left) { setBlockedClick(true); return }
    else next.add(id)
    setBlockedClick(false)
    setSelected(next)
  }
  const items = data.items
  return (
    <section className="panel" aria-labelledby="cand-h">
      <div className="panel-head">
        <h2 id="cand-h">Leads</h2>
        <Segmented id="cand" value={filter} onChange={(v) => { setFilter(v); setReason('') }} options={[
          { value: 'eligible', label: 'Eligible', count: data.counts.selectable },
          { value: 'hold', label: 'On hold', count: data.counts.hold },
        ]} />
      </div>
      {filter === 'hold' && (
        <div className="row" style={{ marginBottom: 12 }}>
          <label className="label" htmlFor="reason">Reason</label>
          <select id="reason" className="input" style={{ width: 'auto' }} value={reason} onChange={(e) => setReason(e.target.value)}>
            <option value="">All reasons</option>
            {reasons.map(([code, n]) => <option key={code} value={code}>{code} ({n})</option>)}
          </select>
        </div>
      )}
      {filter === 'eligible' && left === 0 && (
        <div className="banner banner-error" role="status"><Ban size={16} strokeWidth={1.75} />No new first contact can be added. {allowance.message}</div>
      )}
      {filter === 'eligible' && (atCap || blockedClick) && left > 0 && (
        <div className="banner banner-error" role="alert"><Ban size={16} strokeWidth={1.75} />Cap reached: {selected.size} of {left} new first contacts selected for {allowance.send_date_text}. The ramp allows {allowance.daily_limit} a day, so no more can be added.</div>
      )}
      {error && <ErrorBanner message={error} />}
      {filter === 'eligible' && data.counts.busy > 0 && <p className="hint" style={{ margin: '0 0 12px' }}>{plural(data.counts.busy, 'eligible lead')} not listed: already in a sequence or a batch waiting for review.</p>}
      {items.length === 0 ? (
        <p className="hint" style={{ margin: 0 }}>{filter === 'eligible' ? 'No eligible lead is waiting.' : 'No lead on hold for this reason.'}</p>
      ) : (
        <div className="table-wrap" style={{ maxHeight: 520 }}>
          <table className="data cand-table">
            <thead><tr>{filter === 'eligible' && <th style={{ width: 44 }}><span className="sr-only">Select</span></th>}<th>Business</th><th className="hide-sm">Observation</th><th className="hide-sm">Address</th><th className="hide-sm">{filter === 'eligible' ? 'Verified' : 'Hold reasons'}</th></tr></thead>
            <tbody>
              {items.map((c) => {
                const busy = c.busy
                const checked = selected.has(c.id)
                const disabled = filter !== 'eligible' || !!busy || (!checked && selected.size >= left)
                return (
                  <tr key={c.id} aria-selected={checked} onClick={() => !busy && filter === 'eligible' && toggle(c.id)}>
                    {filter === 'eligible' && <td><input type="checkbox" checked={checked} disabled={disabled} onChange={() => toggle(c.id)} onClick={(e) => e.stopPropagation()} aria-label={`Select ${c.business_name}`} /></td>}
                    <td><b style={{ fontWeight: 500 }}>{c.business_name}</b><div className="muted" style={{ fontSize: 13 }}>{(c.vertical || 'other').replace('_', ' ')}{busy ? ` · ${busy.code === 'IN_SEQUENCE' ? 'already in a sequence' : busy.message}` : ''}</div>
                      <div className="show-sm cand-sm">
                        {c.observation && <span className="chip chip-lead">{OBSERVATION[c.observation.type] || c.observation.type}</span>}
                        {filter !== 'eligible' && <span className="reason-chips">{c.hold_reasons.map((r) => <span key={r} className="chip chip-review">{r}</span>)}</span>}
                        <span className="mono muted" style={{ fontSize: 13, overflowWrap: 'anywhere' }}>{c.email}</span>
                      </div></td>
                    <td className="hide-sm">{c.observation ? <span className="chip chip-lead">{OBSERVATION[c.observation.type] || c.observation.type}</span> : <span className="muted">—</span>}</td>
                    <td className="hide-sm mono" style={{ fontSize: 13 }}>{c.email}</td>
                    <td className="hide-sm">{filter === 'eligible'
                      ? <span className="chip chip-lead"><ShieldCheck size={16} strokeWidth={1.75} />{c.verification_status}</span>
                      : <span className="reason-chips">{c.hold_reasons.map((r) => <span key={r} className="chip chip-review">{r}</span>)}</span>}</td>
                  </tr>
                )
              })}
            </tbody>
          </table>
        </div>
      )}
      {filter === 'eligible' && (
        <div className="select-bar">
          <span><span className="num">{selected.size}</span> of <span className="num">{left}</span> selected for {allowance.send_date_text}</span>
          <span className="row">
            {!who && <span className="hint">Enter your name first.</span>}
            {selected.size > 0 && <button className="btn" onClick={() => setSelected(new Set())}>Clear</button>}
            <button className="btn btn-primary" disabled={!selected.size || !who || writing} onClick={onWrite}>
              {writing ? <Spinner label="Starting" /> : <PenLine size={16} strokeWidth={1.75} />}Write {selected.size ? plural(selected.size, 'lead') : ''}
            </button>
          </span>
        </div>
      )}
    </section>
  )
}

// ─── the review ───────────────────────────────────────────────────────────────

function Schedule({ lead }) {
  const s = lead.schedule
  if (!s) return <p className="hint" style={{ margin: 0 }}>No slot planned.</p>
  return (
    <div>
      <div className="label" style={{ marginBottom: 4 }}>{lead.schedule_kind === 'scheduled' ? 'Scheduled' : 'Proposed'} · <span className="mono">{s.mailbox}</span></div>
      <table className="data sched-table"><tbody>
        {s.steps.map((st) => (
          <tr key={st.step}><td className="mono">T{st.step}</td><td>{dayText(st.local_date)}</td><td className="mono">{WINDOW_TEXT[st.window] || st.window}</td><td className="num">{timeText(st.scheduled_for)}</td></tr>
        ))}
      </tbody></table>
    </div>
  )
}

function Evidence({ lead }) {
  const e = lead.evidence || {}
  const o = e.observation || {}, p = e.provenance || {}, v = e.verification || {}
  return (
    <dl className="kv evidence">
      <dt>Observation</dt>
      <dd>{o.text}<div className="muted mono" style={{ fontSize: 13 }}>checked {date(o.checked_at)}</div>
        {o.evidence_url && <a href={o.evidence_url} target="_blank" rel="noreferrer noopener" className="ev-link"><ExternalLink size={14} strokeWidth={1.75} />{o.type === 'SOCIAL_ONLY' ? 'Open profile' : 'Open website'}</a>}
        {o.evidence_path && <div className="mono muted" style={{ fontSize: 13 }}>Screenshot: {o.evidence_path}</div>}</dd>
      <dt>Address found</dt>
      <dd><span className="mono">{e.email}</span><div className="muted" style={{ fontSize: 13 }}>{(p.method || '').replace('_', ' ')} · captured <span className="mono">{date(p.captured_at)}</span></div>
        {p.source_url && <a href={p.source_url} target="_blank" rel="noreferrer noopener" className="ev-link"><ExternalLink size={14} strokeWidth={1.75} />Source page</a>}
        {p.excerpt && <blockquote className="excerpt">{p.excerpt}</blockquote>}</dd>
      <dt>Verified</dt>
      <dd><span className="chip chip-lead"><ShieldCheck size={16} strokeWidth={1.75} />{v.status}</span> <span className="muted" style={{ fontSize: 13 }}>{v.provider} · <span className="mono">{date(v.verified_at)}</span></span></dd>
    </dl>
  )
}

function Texts({ lead }) {
  const [tab, setTab] = useState('t1')
  const subject = tab === 't1' ? lead.subject : `Re: ${lead.subject}`
  return (
    <div>
      <Segmented id={`t-${lead.id}`} value={tab} onChange={setTab} options={[
        { value: 't1', label: 'Day 1' }, { value: 't2', label: 'Day 6' }, { value: 't3', label: 'Day 14' },
      ]} />
      <div className="paper mail-sheet">
        <div className="mail-subject"><span className="paper-label">Subject</span>{subject}</div>
        <pre className="mail-body">{lead.texts[tab]}</pre>
      </div>
    </div>
  )
}

function LeadCard({ lead, chosen, toggle, who, batchId, onChanged }) {
  const [rejecting, setRejecting] = useState(false)
  const [reason, setReason] = useState('')
  const [error, setError] = useState(null)
  async function reject() {
    setError(null)
    try { await api.outreach.reject(batchId, { lead_ids: [lead.id], reason, rejected_by: who }); setRejecting(false); onChanged() } catch (e) { setError(e.message) }
  }
  const ready = lead.state === 'READY'
  const written = !!lead.texts.t1
  return (
    <motion.article className={`lead-card state-${lead.state.toLowerCase()}`} initial={{ opacity: 0, y: 6 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: ms.indicator / 1000, ease: ease.entrance }}>
      <header className="lead-head">
        {ready && <input type="checkbox" checked={chosen} onChange={toggle} aria-label={`Choose ${lead.business_name}`} />}
        <h3>{lead.business_name}</h3>
        <StateChip state={lead.state} />
        <span className="muted lead-sender">{lead.sender_name ? `from ${lead.sender_name}` : ''}</span>
      </header>
      {lead.state === 'HOLD' && (
        <div className="hold-box" role="status">
          <span className="reason-chips">{lead.hold_reasons.map((r) => <span key={r} className="chip chip-review">{r}</span>)}</span>
          {lead.hold_detail.length > 0 && <ul>{lead.hold_detail.slice(0, 4).map((d, i) => <li key={i}>{d}</li>)}</ul>}
        </div>
      )}
      {lead.approval_refusal && lead.state === 'READY' && (
        <div className="banner banner-error" role="status" style={{ margin: 0 }}><TriangleAlert size={16} strokeWidth={1.75} />Not approved: {lead.approval_refusal.code}. {lead.approval_refusal.message}</div>
      )}
      {lead.state === 'APPROVED' && <div className="approved-line"><CircleCheck size={16} strokeWidth={1.75} /><span>Approved by {lead.approved_by} · <span className="mono">{date(lead.approved_at)}</span></span></div>}
      {lead.state === 'REJECTED' && <div className="approved-line muted"><Ban size={16} strokeWidth={1.75} /><span>Rejected by {lead.rejected_by}: {lead.reject_reason}</span></div>}
      <div className="lead-grid">
        <div className="stack" style={{ gap: 16 }}>
          <Evidence lead={lead} />
          <Schedule lead={lead} />
        </div>
        <div>{written ? <Texts lead={lead} /> : <p className="hint" style={{ margin: 0 }}>{lead.state === 'HOLD' ? 'No text: a held lead is never given a made-up message.' : 'Waiting for the writer.'}</p>}</div>
      </div>
      {(ready || lead.state === 'HOLD') && (
        <footer className="lead-foot">
          {!rejecting ? <button className="btn btn-sm" onClick={() => setRejecting(true)}><Ban size={16} strokeWidth={1.75} />Reject</button> : (
            <div className="row" style={{ flex: 1 }}>
              <input className="input" style={{ flex: 1, minWidth: 200 }} placeholder="Why (kept with the lead)" value={reason} onChange={(e) => setReason(e.target.value)} aria-label="Reason" />
              <button className="btn btn-sm" disabled={!who || reason.trim().length < 3} onClick={reject}>Reject lead</button>
              <button className="btn btn-sm" onClick={() => setRejecting(false)}>Cancel</button>
            </div>
          )}
          {error && <span className="hint" style={{ color: 'var(--error)' }} role="alert">{error}</span>}
        </footer>
      )}
    </motion.article>
  )
}

function BatchReview({ batch, who, onChanged, onNew }) {
  const [chosen, setChosen] = useState(new Set())
  const [busy, setBusy] = useState(false)
  const [message, setMessage] = useState(null)
  const [error, setError] = useState(null)
  const counts = batch.counts
  const total = batch.total
  const done = total - (counts.PENDING || 0) - (counts.WRITING || 0)
  const readyIds = batch.leads.filter((l) => l.state === 'READY').map((l) => l.id)
  async function approve(ids) {
    setBusy(true); setError(null); setMessage(null)
    try {
      const res = await api.outreach.approve(batch.id, { lead_ids: ids, approved_by: who })
      setMessage(`${plural(res.approved.length, 'lead')} approved and scheduled${res.refused.length ? `, ${res.refused.length} refused (see the cards)` : ''}.`)
      setChosen(new Set()); onChanged()
    } catch (e) { setError(e.message) } finally { setBusy(false) }
  }
  async function resume() {
    setError(null)
    try { await api.outreach.continueWriting(batch.id); onChanged() } catch (e) { setError(e.message) }
  }
  const writing = batch.status === 'WRITING'
  return (
    <section className="panel" aria-labelledby="batch-h">
      <div className="panel-head">
        <div>
          <h2 id="batch-h">Batch {batch.id} · for {batch.send_date_text}</h2>
          <div className="hint">Written by the AI writer ({batch.writer_model}, templates {batch.template_version}) for {batch.created_by} · <span className="mono">{date(batch.created_at)}</span></div>
        </div>
        <div className="row">
          {['READY', 'HOLD', 'APPROVED', 'REJECTED'].filter((s) => counts[s]).map((s) => <span key={s} className={`chip ${STATE_CHIP[s][1]}`}>{STATE_CHIP[s][0]} {counts[s]}</span>)}
          {batch.status === 'DONE' && <button className="btn btn-sm" onClick={onNew}><ListChecks size={16} strokeWidth={1.75} />New batch</button>}
        </div>
      </div>
      {writing && (
        <div className="writing" role="status" aria-live="polite">
          <div className="row" style={{ justifyContent: 'space-between' }}>
            <span>{batch.writing_active ? <Spinner label="Writing" /> : <TriangleAlert size={16} strokeWidth={1.75} />} {batch.writing_active ? 'Writing' : 'Writing stopped'}: <span className="num">{done}</span> of <span className="num">{total}</span> leads done. Each lead gets three emails (Day 1, 6, 14), each checked by the validator.</span>
            {!batch.writing_active && <button className="btn btn-sm" onClick={resume}><RotateCw size={16} strokeWidth={1.75} />Continue writing</button>}
          </div>
          <div className="progress"><motion.i initial={false} animate={{ scaleX: total ? done / total : 0 }} transition={{ duration: ms.indicator / 1000, ease: ease.ui }} /></div>
        </div>
      )}
      {error && <ErrorBanner message={error} />}
      {message && <div className="banner banner-info" role="status"><CalendarClock size={16} strokeWidth={1.75} />{message}</div>}
      {readyIds.length > 0 && !writing && (
        <div className="select-bar" style={{ marginTop: 0, marginBottom: 16 }}>
          <span>{plural(readyIds.length, 'lead')} ready. Approving creates the sequence: Day 1 now scheduled, Day 6 and Day 14 approved with their texts.</span>
          <span className="row">
            {!who && <span className="hint">Enter your name first.</span>}
            <button className="btn" disabled={!chosen.size || !who || busy} onClick={() => approve([...chosen])}>Approve selected ({chosen.size})</button>
            <button className="btn btn-primary" disabled={!who || busy} onClick={() => approve('all_ready')}><UserCheck size={16} strokeWidth={1.75} />Approve all ready ({readyIds.length})</button>
          </span>
        </div>
      )}
      <div className="stack" style={{ gap: 16 }}>
        {batch.leads.map((lead) => (
          <LeadCard key={lead.id} lead={lead} batchId={batch.id} who={who} onChanged={onChanged}
            chosen={chosen.has(lead.id)} toggle={() => setChosen((c) => { const n = new Set(c); if (n.has(lead.id)) n.delete(lead.id); else n.add(lead.id); return n })} />
        ))}
      </div>
    </section>
  )
}

// ─── the screen ───────────────────────────────────────────────────────────────

export default function BatchScreen() {
  const [who, setWho] = useFounderName()
  const [allowance, setAllowance] = useState(null)
  const [candidates, setCandidates] = useState(null)
  const [pending, setPending] = useState(null)
  const [batch, setBatch] = useState(null)
  const [filter, setFilter] = useState('eligible')
  const [reason, setReason] = useState('')
  const [selected, setSelected] = useState(new Set())
  const [writing, setWriting] = useState(false)
  const [error, setError] = useState(null)
  const [writeError, setWriteError] = useState(null)

  // The batch shown: one still being written or reviewed, else the latest one (its scheduled result) until the
  // founder starts a new batch.
  const [dismissed, setDismissed] = useState(() => Number(sessionStorage.getItem('sb.batchDismissed')) || 0)
  const loadBatch = useCallback(async (id) => { if (id) setBatch(await api.outreach.batch(id)) }, [])
  const load = useCallback(async () => {
    setError(null)
    try {
      const [a, c, p, list] = await Promise.all([
        api.outreach.allowance(), api.outreach.candidates({ status: filter, reason, limit: 300 }),
        api.outreach.pendingConfirmations(), api.outreach.batches(),
      ])
      setAllowance(a); setCandidates(c); setPending(p)
      const shown = list.items.find((b) => b.status !== 'DONE') || list.items.find((b) => b.id > dismissed) || null
      if (shown) await loadBatch(shown.id)
      else setBatch(null)
    } catch (e) { setError(e.message) }
  }, [filter, reason, loadBatch, dismissed])
  function newBatch() {
    if (batch) { sessionStorage.setItem('sb.batchDismissed', String(batch.id)); setDismissed(batch.id) }
    setBatch(null)
  }
  useEffect(() => { load() }, [load])

  // While the writer works, the batch is polled; the list and allowance refresh when it ends.
  useEffect(() => {
    if (!batch || batch.status !== 'WRITING' || !batch.writing_active) return undefined
    const id = setInterval(async () => {
      const next = await api.outreach.batch(batch.id).catch(() => null)
      if (next) { setBatch(next); if (next.status !== 'WRITING') load() }
    }, 1500)
    return () => clearInterval(id)
  }, [batch, load])

  async function write() {
    setWriting(true); setWriteError(null)
    try {
      const created = await api.outreach.createBatch({ eligibility_ids: [...selected], send_date: allowance.send_date, created_by: who })
      setSelected(new Set()); setBatch(created)
      const [a, c] = await Promise.all([api.outreach.allowance(), api.outreach.candidates({ status: filter, reason, limit: 300 })])
      setAllowance(a); setCandidates(c)
    } catch (e) {
      setWriteError(e.message)
      if (e.detail?.code === 'CAP_REACHED') api.outreach.allowance().then(setAllowance).catch(() => {})
    } finally { setWriting(false) }
  }
  const refresh = useCallback(async () => { await load(); if (batch) await loadBatch(batch.id) }, [load, loadBatch, batch])
  const nothingEligible = useMemo(() => candidates && candidates.counts.eligible === 0, [candidates])

  if (error) return <ErrorBanner message={`Could not load the email batch. ${error}`} onRetry={load} />
  if (!allowance || !candidates) return <DelayedSkeleton rows={10} />
  return (
    <div className="stack">
      <AllowanceHeader allowance={allowance} who={who} setWho={setWho} onChanged={refresh} />
      {batch && <BatchReview batch={batch} who={who} onChanged={refresh} onNew={newBatch} />}
      {nothingEligible ? (
        <div className="panel"><StateBlock icon={Inbox} title="No eligible leads yet"
          text="A lead appears here once the eligibility check finds an address on the business's own page or profile, a VALID verifier result and a checked observation (Instagram bio, website down, or a phone screenshot). Instagram profiles waiting for your check are listed below." /></div>
      ) : (!batch || batch.status === 'DONE') && (
        <CandidateList data={candidates} allowance={allowance} filter={filter} setFilter={setFilter} reason={reason} setReason={setReason}
          selected={selected} setSelected={setSelected} who={who} onWrite={write} writing={writing} error={writeError} />
      )}
      <FounderChecks pending={pending} onSaved={refresh} />
    </div>
  )
}
