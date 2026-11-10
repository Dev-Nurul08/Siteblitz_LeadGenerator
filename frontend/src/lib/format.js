// Numbers and dates — spec row 23 (en-IN grouping, "8 Nov 2026, 15:42", mono everywhere).
const nf = new Intl.NumberFormat('en-IN')
export const num = (n) => (n === null || n === undefined ? '—' : nf.format(n))
const df = new Intl.DateTimeFormat('en-IN', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false })
const dfs = new Intl.DateTimeFormat('en-IN', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false })
// The API stores UTC, but SQLite returns it without an offset ("2026-11-08T14:35:11"), which the
// browser reads as local time — 5 h 30 min early in India. A timestamp with no offset is UTC.
const NO_OFFSET = /^\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}(:\d{2}(\.\d+)?)?$/
const toDate = (iso) => new Date(typeof iso === 'string' && NO_OFFSET.test(iso) ? `${iso.replace(' ', 'T')}Z` : iso)
export const date = (iso) => (iso ? df.format(toDate(iso)) : '—')
export const dateSeconds = (iso) => (iso ? dfs.format(toDate(iso)) : '—')
export function ago(iso) {
  if (!iso) return '—'
  const minutes = Math.round((Date.now() - toDate(iso).getTime()) / 60000)
  if (minutes < 1) return 'just now'
  if (minutes < 60) return `${minutes} min ago`
  if (minutes < 24 * 60) return `${Math.round(minutes / 60)} h ago`
  return date(iso)
}
export const coord = (v) => (v === null || v === undefined ? '—' : Number(v).toFixed(5))
