// 03 Hot leads — ranked leads; signature "The score builds from its reasons".
import { Fragment, useCallback, useEffect, useState } from 'react'
import { motion, useReducedMotion } from 'motion/react'
import { AtSign, Flame, Mail, Phone, Send } from 'lucide-react'
import NumberFlow from '@number-flow/react'
import api from '../services/api'
import { go } from '../lib/router'
import { num } from '../lib/format'
import { TitleBlock } from '../components/TitleBlock'
import { ConfidenceChip, DelayedSkeleton, Drawer, ErrorBanner, Segmented, StateBlock, TierChip, VerdictChip } from '../components/ui'
import { ease } from '../motion'

const TIERS = [['HOT', 'Hot'], ['WARM', 'Warm'], ['COLD', 'Cold'], ['REVIEW', 'Review'], ['SKIP', 'Skip']]
const PART_NAMES = { website_gap: 'Website gap', business_problem: 'Business problem', activity: 'Activity', service_fit: 'Service fit' }
// Segment colours are tokens only (spec row 2–7): the gap is the heat, the rest stay neutral.
const PART_COLOUR = { website_gap: 'var(--accent)', business_problem: 'var(--warm)', activity: 'var(--dot-lead)', service_fit: 'var(--ink-3)' }
const READINESS = { READY: 'Can be contacted', RESEARCH: 'Find a phone or email first', BLOCKED: 'Do not contact' }

function Routes({ x }) {
  const r = [[Phone, x.phone, 'Phone'], [Mail, x.email, 'Email'], [AtSign, x.social_platforms?.length, 'Social profile']]
  return (
    <span className="routes">
      {r.map(([Icon, on, label]) => <Icon key={label} size={16} strokeWidth={1.75} className={on ? '' : 'off'} aria-label={`${label}: ${on ? 'found' : 'not found'}`} />)}
    </span>
  )
}

function ScoreBuild({ assessment }) {
  const reduce = useReducedMotion()
  const reasons = (assessment.reasons || []).filter((r) => r.points > 0)
  const step = Math.min(120, 900 / Math.max(1, reasons.length))
  const [lit, setLit] = useState(reduce ? reasons.length : 0)
  useEffect(() => {
    if (reduce) return undefined
    const timers = reasons.map((_, i) => setTimeout(() => setLit(i + 1), (i + 1) * step))
    return () => timers.forEach(clearTimeout)
  }, [assessment]) // eslint-disable-line react-hooks/exhaustive-deps
  return (
    <section aria-labelledby="why-h">
      <div className="row" style={{ justifyContent: 'space-between', alignItems: 'flex-end' }}>
        <h3 id="why-h">Why it scores</h3>
        <div className="stat"><NumberFlow value={lit >= reasons.length ? assessment.need_score ?? 0 : reasons.slice(0, lit).reduce((s, r) => s + r.points, 0)} locales="en-IN" /><span className="muted" style={{ fontSize: 16 }}>/100</span></div>
      </div>
      <div className="score-bar" role="img" aria-label={`Need score ${assessment.need_score} of 100`} style={{ margin: '8px 0 12px' }}>
        {reasons.map((r, i) => (
          <motion.i key={r.part} style={{ width: `${r.points}%`, background: PART_COLOUR[r.part] }}
            initial={{ scaleX: reduce ? 1 : 0 }} animate={{ scaleX: i < lit ? 1 : 0 }} transition={{ duration: step / 1000, ease: ease.entrance }} />
        ))}
      </div>
      {reasons.map((r, i) => (
        <div key={r.part} className="reason" style={{ color: i < lit ? 'var(--ink)' : 'var(--ink-3)' }}>
          <span><span className="label" style={{ color: 'inherit' }}>{PART_NAMES[r.part]}</span> — {r.text}
            {r.check_ids?.length > 0 && <> · <a href={`#/review?business=${assessment.business_id}`}>See evidence</a></>}</span>
          <span className="mono">+{r.points}</span>
        </div>
      ))}
    </section>
  )
}

function LeadDetail({ id }) {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  useEffect(() => { api.intelligence.detail(id).then(setData).catch((e) => setError(e.message)) }, [id])
  if (error) return <div className="drawer-body"><ErrorBanner message={error} /></div>
  if (!data) return <div className="drawer-body"><DelayedSkeleton rows={6} /></div>
  const a = { ...data.assessment, business_id: id }
  const b = data.business
  return (
    <>
      <div className="drawer-head">
        <h2 id="lead-title" style={{ paddingRight: 48 }}>{b.name}</h2>
        <div className="row"><TierChip tier={a.tier} /><VerdictChip verdict={a.website_verdict} /></div>
      </div>
      <div className="drawer-body">
        <div className="indicators">
          <div className="indicator"><div className="label">Website need</div><div className="mono" style={{ fontSize: 22 }}>{a.need_score ?? '—'}<span className="muted">/100</span></div></div>
          <div className="indicator"><div className="label">Evidence confidence</div><ConfidenceChip value={a.evidence_confidence} /></div>
          <div className="indicator"><div className="label">Outreach readiness</div><div style={{ fontSize: 14 }}>{READINESS[a.outreach_readiness]}</div></div>
        </div>
        {a.need_score !== null && <ScoreBuild assessment={a} />}
        <section>
          <h3 style={{ marginBottom: 8 }}>Contact routes</h3>
          <dl className="kv">
            <dt>Phone</dt><dd className="mono">{b.phone ? <a href={`tel:${b.phone}`}>{b.phone}</a> : '—'}</dd>
            <dt>Email</dt><dd className="mono">{b.email || '—'}</dd>
            {Object.entries(b.social_urls).map(([k, url]) => <Fragment key={k}><dt>{k}</dt><dd><a href={url} target="_blank" rel="noreferrer noopener">{url}</a></dd></Fragment>)}
          </dl>
        </section>
        {a.next_actions?.length > 0 && (
          <section><h3 style={{ marginBottom: 8 }}>Before it can be Hot</h3>
            <ul style={{ margin: 0, paddingLeft: 18, color: 'var(--ink-2)' }}>{a.next_actions.map((n) => <li key={n}>{n}</li>)}</ul>
            <a className="btn btn-sm" style={{ marginTop: 12 }} href={`#/review?business=${id}`}>Check in Review</a></section>
        )}
      </div>
      <div className="drawer-foot">
        <button className="btn btn-primary" onClick={() => go('outreach', { lead: id })}><Send size={16} />Start outreach</button>
      </div>
    </>
  )
}

export default function HotLeadsPage({ entrance }) {
  const [tier, setTier] = useState('HOT')
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  const [selected, setSelected] = useState(null)
  const load = useCallback(() => {
    setError(null)
    api.intelligence.leads({ tier, page_size: 100 }).then(setData).catch((e) => setError(e.message))
  }, [tier])
  useEffect(() => { load() }, [load])
  const counts = data?.tier_counts || {}
  const items = data?.items || []
  return (
    <>
      <TitleBlock index="03" title="Hot leads" entrance={entrance}
        text="Step 3 of 4. Businesses ranked by how much they need a website, with the reasons. Hot needs: no real website (checked), a search, confirmed open, and a way to reach them." />
      <div style={{ marginBottom: 16 }}>
        <Segmented id="tier" value={tier} onChange={setTier} options={TIERS.map(([v, l]) => ({ value: v, label: l, count: counts[v] ?? 0 }))} />
      </div>
      {error && <ErrorBanner message={`Could not load leads. ${error}`} onRetry={load} />}
      {!data && !error && <DelayedSkeleton />}
      {data && items.length === 0 && (
        <div className="panel">
          <StateBlock icon={Flame} title={tier === 'HOT' ? 'No hot leads yet' : `No ${tier.toLowerCase()} leads`}
            text={tier === 'HOT' ? 'Warm leads become Hot after you record a search for them and confirm they are open (in Review).' : undefined}
            action={<button className="btn btn-primary" onClick={() => go('review')}>Review {num(counts.WARM ?? 0)} warm leads</button>} />
        </div>
      )}
      {items.length > 0 && (
        <div className="table-wrap">
          <table className="data">
            <thead><tr><th className="num">#</th><th>Business</th><th className="hide-sm">Category</th><th>Tier</th><th className="num">Need</th>
              <th className="hide-sm">Confidence</th><th className="hide-sm">Routes</th><th className="hide-lg">Website verdict</th></tr></thead>
            <motion.tbody layout transition={{ duration: 0.28, ease: ease.ui }}>
              {items.map((x, i) => (
                <motion.tr layout key={x.id} aria-selected={selected === x.id} tabIndex={0}
                  onClick={() => setSelected(x.id)} onKeyDown={(e) => e.key === 'Enter' && setSelected(x.id)}>
                  <td className="num">{i + 1}</td>
                  <td>{x.name}<div className="muted" style={{ fontSize: 13 }}>{x.city}</div></td>
                  <td className="hide-sm">{x.category || '—'}</td>
                  <td><TierChip tier={x.tier} /></td>
                  <td className="num">{x.need_score ?? '—'}<span className={`need-bar ${x.tier === 'HOT' ? 'hot' : ''}`}><i style={{ transform: `scaleX(${(x.need_score || 0) / 100})` }} /></span></td>
                  <td className="hide-sm"><ConfidenceChip value={x.evidence_confidence} /></td>
                  <td className="hide-sm"><Routes x={x} /></td>
                  <td className="hide-lg"><VerdictChip verdict={x.website_verdict} /></td>
                </motion.tr>
              ))}
            </motion.tbody>
          </table>
        </div>
      )}
      <Drawer open={selected !== null} onClose={() => setSelected(null)} labelledBy="lead-title">
        {selected !== null && <LeadDetail key={selected} id={selected} />}
      </Drawer>
    </>
  )
}
