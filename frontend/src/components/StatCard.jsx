/**
 * Reusable StatCard component
 */
export default function StatCard({ value, label, accent = 'primary', change, changeLabel }) {
  return (
    <div className={`card stat-card accent-${accent}`}>
      <div className="stat-value">{value ?? '—'}</div>
      <div className="stat-label">{label}</div>
      {change !== undefined && (
        <div className={`stat-change ${change >= 0 ? 'positive' : 'negative'}`}>
          {change >= 0 ? '▲' : '▼'} {Math.abs(change)}{changeLabel || ''}
        </div>
      )}
    </div>
  )
}
