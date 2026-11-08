// Numbers and dates — spec row 23 (en-IN grouping, "8 Nov 2026, 15:42", mono everywhere).
const nf = new Intl.NumberFormat('en-IN')
export const num = (n) => (n === null || n === undefined ? '—' : nf.format(n))
const df = new Intl.DateTimeFormat('en-IN', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', hour12: false })
const dfs = new Intl.DateTimeFormat('en-IN', { day: 'numeric', month: 'short', year: 'numeric', hour: '2-digit', minute: '2-digit', second: '2-digit', hour12: false })
export const date = (iso) => (iso ? df.format(new Date(iso)) : '—')
export const dateSeconds = (iso) => (iso ? dfs.format(new Date(iso)) : '—')
export function ago(iso) {
  if (!iso) return '—'
  const minutes = Math.round((Date.now() - new Date(iso).getTime()) / 60000)
  if (minutes < 1) return 'just now'
  if (minutes < 60) return `${minutes} min ago`
  if (minutes < 24 * 60) return `${Math.round(minutes / 60)} h ago`
  return date(iso)
}
export const coord = (v) => (v === null || v === undefined ? '—' : Number(v).toFixed(5))
