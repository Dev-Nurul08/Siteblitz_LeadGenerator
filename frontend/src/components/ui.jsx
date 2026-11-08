// Shared UI pieces — chips (spec rows 5–7), state blocks (row 22), tickers (row 23), drawer (row 15).
import { useEffect, useRef, useState } from 'react'
import { motion, AnimatePresence } from 'motion/react'
import NumberFlow from '@number-flow/react'
import {
  AtSign, CircleHelp, CircleMinus, CircleOff, Flame, Globe, LoaderCircle, ServerCrash, X,
} from 'lucide-react'
import { ms, t } from '../motion'

export const VERDICT = {
  NO_SITE_VERIFIED: { label: 'No website found', cls: 'chip-lead', Icon: CircleOff, dot: 'lead' },
  SOCIAL_ONLY_VERIFIED: { label: 'Social media only', cls: 'chip-lead', Icon: AtSign, dot: 'lead' },
  SITE_DOWN_CONFIRMED: { label: 'Website down', cls: 'chip-lead', Icon: ServerCrash, dot: 'lead' },
  UNKNOWN: { label: 'Needs review', cls: 'chip-review', Icon: CircleHelp, dot: 'review' },
  OWN_SITE_VERIFIED: { label: 'Has own website', cls: 'chip-notlead', Icon: Globe, dot: 'notlead' },
  SKIP: { label: 'Skipped', cls: 'chip-skip', Icon: CircleMinus, dot: 'notlead' },
  UNCHECKED: { label: 'Not checked yet', cls: 'chip-outline', Icon: LoaderCircle, dot: 'unchecked' },
}
export const TIER = {
  HOT: { label: 'Hot', cls: 'chip-hot', Icon: Flame },
  WARM: { label: 'Warm', cls: 'chip-warm' },
  COLD: { label: 'Cold', cls: 'chip-cold' },
  REVIEW: { label: 'Review', cls: 'chip-review' },
  SKIP: { label: 'Skip', cls: 'chip-skip' },
}
const CONFIDENCE = { HIGH: ['High', 'chip-lead'], MEDIUM: ['Medium', 'chip-review'], LOW: ['Low', 'chip-error'] }
const JOB = {
  PENDING: ['Queued', 'chip-outline'], RUNNING: ['Running', 'chip-running'], COMPLETED: ['Done', 'chip-lead'],
  PARTIAL: ['Partial', 'chip-review'], FAILED: ['Failed', 'chip-error'], CANCELLED: ['Cancelled', 'chip-outline'],
}

export function VerdictChip({ verdict, layoutId }) {
  const v = VERDICT[verdict] || VERDICT.UNCHECKED
  const Icon = v.Icon
  return (
    <motion.span layoutId={layoutId} className={`chip ${v.cls}`}>
      <Icon size={16} strokeWidth={1.75} aria-hidden="true" />{v.label}
    </motion.span>
  )
}
export function TierChip({ tier }) {
  if (!tier) return <span className="chip chip-outline">Not scored</span>
  const v = TIER[tier]
  return <span className={`chip ${v.cls}`}>{v.Icon && <v.Icon size={16} strokeWidth={1.75} aria-hidden="true" />}{v.label}</span>
}
export function ConfidenceChip({ value }) {
  if (!value) return <span className="muted">—</span>
  const [label, cls] = CONFIDENCE[value]
  return <span className={`chip ${cls}`}>{label}</span>
}
export function JobChip({ status }) {
  const [label, cls] = JOB[status] || [status, 'chip-outline']
  return <span className={`chip ${cls}`}>{status === 'RUNNING' && <Spinner />}{label}</span>
}

export function Spinner({ label }) {
  return <LoaderCircle className="spinner" size={16} strokeWidth={1.75} aria-label={label || 'Loading'} />
}

// Rolling count (NumberFlow keeps en-IN grouping and honours reduced motion by default).
export function Ticker({ value, className = 'num' }) {
  return <NumberFlow className={className} value={value ?? 0} locales="en-IN" transformTiming={{ duration: ms.countRoll, easing: 'cubic-bezier(.2,.8,.2,1)' }} />
}

export function StateBlock({ icon: Icon = CircleHelp, title, text, action, details }) {
  return (
    <div className="state" role="status" aria-live="polite">
      <div className="state-glyph"><Icon size={20} strokeWidth={1.75} aria-hidden="true" /></div>
      <h3>{title}</h3>
      {text && <p>{text}</p>}
      {action}
      {details && (
        <details><summary>Technical details</summary><pre>{details}</pre></details>
      )}
    </div>
  )
}

// Skeleton shown only after 300 ms, so fast loads never flash (spec row 22).
export function DelayedSkeleton({ rows = 8 }) {
  const [show, setShow] = useState(false)
  useEffect(() => { const id = setTimeout(() => setShow(true), 300); return () => clearTimeout(id) }, [])
  if (!show) return null
  return (
    <div aria-hidden="true" style={{ display: 'grid', gap: 18, padding: '16px 12px' }}>
      {Array.from({ length: rows }, (_, i) => <div key={i} className="skeleton" style={{ width: `${60 + ((i * 17) % 35)}%` }} />)}
    </div>
  )
}

export function Segmented({ value, onChange, options, id }) {
  return (
    <div className="segmented" role="group">
      {options.map((o) => (
        <button key={o.value} type="button" aria-pressed={value === o.value} onClick={() => onChange(o.value)}>
          {value === o.value && <motion.i className="seg-bg" layoutId={`seg-${id}`} transition={t('indicator')} />}
          <span>{o.label}</span>
          {o.count !== undefined && <span className="num muted">{o.count}</span>}
        </button>
      ))}
    </div>
  )
}

// Right-side drawer: non-modal ≥ 1024 px, modal with scrim below (CSS), Esc closes, focus returns.
export function Drawer({ open, onClose, labelledBy, children }) {
  const returnFocus = useRef(null)
  useEffect(() => {
    if (!open) return undefined
    returnFocus.current = document.activeElement
    const onKey = (e) => { if (e.key === 'Escape') onClose() }
    window.addEventListener('keydown', onKey)
    return () => {
      window.removeEventListener('keydown', onKey)
      if (returnFocus.current && returnFocus.current.focus) returnFocus.current.focus()
    }
  }, [open, onClose])
  return (
    <AnimatePresence>
      {open && (
        <>
          <motion.div className="scrim" onClick={onClose} initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }} transition={t('menu')} />
          <motion.aside className="drawer" role="dialog" aria-labelledby={labelledBy}
            initial={{ opacity: 0, x: 24 }} animate={{ opacity: 1, x: 0 }} exit={{ opacity: 0, x: 24 }}
            transition={{ duration: ms.drawer / 1000, ease: [0.22, 1, 0.36, 1] }}>
            <button className="btn btn-sm" style={{ position: 'absolute', top: 16, right: 16 }} onClick={onClose} aria-label="Close">
              <X size={16} strokeWidth={1.75} />
            </button>
            {children}
          </motion.aside>
        </>
      )}
    </AnimatePresence>
  )
}

export function ErrorBanner({ message, onRetry }) {
  return (
    <div className="banner banner-error" role="alert">
      <span style={{ flex: 1 }}>{message}</span>
      {onRetry && <button className="btn btn-sm" onClick={onRetry}>Retry</button>}
    </div>
  )
}
