import { useState, useEffect } from 'react'
import PageHeader from '../components/PageHeader'
import Badge from '../components/Badge'
import api from '../services/api'

export default function BusinessesPage() {
  // A Discovery job card can open this page filtered to that job (see DiscoveryPage).
  const [jobId, setJobId] = useState(() => sessionStorage.getItem('sb.jobFilter') || '')
  const [businesses, setBusinesses] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [pages, setPages] = useState(1)
  const [loading, setLoading] = useState(true)
  const [selected, setSelected] = useState(null)

  // Filters
  const [filters, setFilters] = useState({
    country: '',
    status: '',
    website_status: '',
    category: '',
    search: '',
  })
  const activeFilters = { ...Object.fromEntries(Object.entries(filters).filter(([, v]) => v)), ...(jobId ? { job_id: jobId } : {}) }

  function clearJobFilter() {
    sessionStorage.removeItem('sb.jobFilter')
    setJobId('')
  }
  const [auditLoading, setAuditLoading] = useState(false)
  const [auditResult, setAuditResult] = useState(null)

  useEffect(() => {
    setAuditResult(null)
  }, [selected])

  useEffect(() => {
    setPage(1)
  }, [filters])

  useEffect(() => {
    loadBusinesses()
  }, [page, filters, jobId])

  async function loadBusinesses() {
    setLoading(true)
    try {
      const data = await api.businesses.list({
        page,
        page_size: 25,
        ...activeFilters,
      })
      setBusinesses(data.items || [])
      setTotal(data.total || 0)
      setPages(data.pages || 1)
    } catch (e) {
      // Silently handle API offline
    } finally {
      setLoading(false)
    }
  }

  function websiteStatusIcon(status) {
    const icons = {
      NOT_FOUND: '❌',
      SOCIAL_ONLY: '📱',
      FOUND: '✅',
      BROKEN: '⚠️',
      UNDER_CONSTRUCTION: '🚧',
      UNKNOWN: '❓',
    }
    return icons[status] || '❓'
  }

  return (
    <>
      <PageHeader
        title="Businesses"
        subtitle={`${total.toLocaleString()} discovered businesses${jobId ? ` · found by job #${jobId}` : ''}`}
        actions={
          <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
            {jobId && <button className="btn btn-ghost btn-sm" onClick={clearJobFilter}>Show all jobs ✕</button>}
            <a className="btn btn-ghost btn-sm" href={api.businesses.exportUrl(activeFilters, 'csv')} download>Export CSV</a>
            <a className="btn btn-ghost btn-sm" href={api.businesses.exportUrl(activeFilters, 'pdf')} download>Export PDF</a>
            <button className="btn btn-ghost btn-sm" onClick={loadBusinesses}>↻ Refresh</button>
          </div>
        }
      />

      <div className="page-body animate-fadeIn">

        {/* Filters */}
        <div className="card" style={{ marginBottom: '20px' }}>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(160px, 1fr))', gap: '12px' }}>
            <div>
              <label className="input-label">Search</label>
              <input
                className="input"
                placeholder="Business name…"
                value={filters.search}
                onChange={e => setFilters(p => ({ ...p, search: e.target.value }))}
              />
            </div>
            <div>
              <label className="input-label">Country</label>
              <select className="input" value={filters.country} onChange={e => setFilters(p => ({ ...p, country: e.target.value }))}>
                <option value="">All countries</option>
                {['GB', 'US', 'AU', 'CA', 'DE', 'FR', 'IN', 'AE', 'SG', 'NZ'].map(c => (
                  <option key={c} value={c}>{c}</option>
                ))}
              </select>
            </div>
            <div>
              <label className="input-label">Status</label>
              <select className="input" value={filters.status} onChange={e => setFilters(p => ({ ...p, status: e.target.value }))}>
                <option value="">All statuses</option>
                <option value="DISCOVERED">Discovered</option>
                <option value="ACTIVE">Active</option>
                <option value="INACTIVE">Inactive</option>
              </select>
            </div>
            <div>
              <label className="input-label">Website</label>
              <select className="input" value={filters.website_status} onChange={e => setFilters(p => ({ ...p, website_status: e.target.value }))}>
                <option value="">All websites</option>
                <option value="NOT_FOUND">No Website ❌</option>
                <option value="SOCIAL_ONLY">Social Only 📱</option>
                <option value="FOUND">Has Website ✅</option>
                <option value="BROKEN">Broken ⚠️</option>
                <option value="UNKNOWN">Unknown ❓</option>
              </select>
            </div>
            <div>
              <label className="input-label">Category</label>
              <input
                className="input"
                placeholder="restaurant, hotel…"
                value={filters.category}
                onChange={e => setFilters(p => ({ ...p, category: e.target.value }))}
              />
            </div>
            <div style={{ display: 'flex', alignItems: 'flex-end' }}>
              <button className="btn btn-secondary" style={{ width: '100%' }} onClick={() => setFilters({ country: '', status: '', website_status: '', category: '', search: '' })}>
                Clear Filters
              </button>
            </div>
          </div>
        </div>

        <div className={`grid-2`} style={{ gap: '20px', alignItems: 'start' }}>

          {/* Table */}
          <div className="card" style={{ gridColumn: selected ? '1' : '1 / -1', padding: 0, overflow: 'hidden' }}>
            {loading ? (
              <div style={{ display: 'flex', justifyContent: 'center', padding: '60px' }}>
                <div className="spinner spinner-lg" />
              </div>
            ) : businesses.length === 0 ? (
              <div className="empty-state">
                <div style={{ fontSize: '3rem', marginBottom: '16px' }}>🏢</div>
                <div className="empty-state-title">No businesses found</div>
                <div className="empty-state-description">
                  Run a discovery first, or adjust your filters
                </div>
              </div>
            ) : (
              <>
                <div className="table-container">
                  <table>
                    <thead>
                      <tr>
                        <th>Business</th>
                        <th>Country</th>
                        <th>Category</th>
                        <th>Website</th>
                        <th>Status</th>
                        <th>Discovered</th>
                      </tr>
                    </thead>
                    <tbody>
                      {businesses.map(biz => (
                        <tr
                          key={biz.id}
                          onClick={() => setSelected(selected?.id === biz.id ? null : biz)}
                          style={{ cursor: 'pointer', background: selected?.id === biz.id ? 'rgba(99,102,241,0.06)' : undefined }}
                        >
                          <td>
                            <div style={{ fontWeight: 600, color: 'var(--color-text-primary)', fontSize: '0.85rem' }}>
                              {biz.name}
                            </div>
                            {biz.locations?.[0]?.city && (
                              <div style={{ fontSize: '0.73rem', color: 'var(--color-text-muted)' }}>
                                📍 {biz.locations[0].city}
                              </div>
                            )}
                          </td>
                          <td>
                            <span style={{ fontWeight: 600 }}>{biz.country_code || '—'}</span>
                          </td>
                          <td>
                            {biz.categories?.[0] ? (
                              <Badge label={biz.categories[0].industry_group || biz.categories[0].category_name} variant="secondary" />
                            ) : '—'}
                          </td>
                          <td>
                            <span title={biz.website_status}>
                              {websiteStatusIcon(biz.website_status)}{' '}
                            </span>
                            {biz.website_url ? (
                              <a href={biz.website_url} target="_blank" rel="noopener noreferrer"
                                style={{ fontSize: '0.75rem', color: 'var(--color-accent-secondary)' }}
                                onClick={e => e.stopPropagation()}>
                                {new URL(biz.website_url).hostname}
                              </a>
                            ) : (
                              <span style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
                                <Badge status={biz.website_status} />
                              </span>
                            )}
                          </td>
                          <td><Badge status={biz.status} /></td>
                          <td style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>
                            {new Date(biz.discovered_at).toLocaleDateString()}
                          </td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                </div>

                {/* Pagination */}
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', padding: '12px 16px', borderTop: '1px solid var(--color-border)' }}>
                  <span style={{ fontSize: '0.78rem', color: 'var(--color-text-muted)' }}>
                    {total.toLocaleString()} total · Page {page} of {pages}
                  </span>
                  <div className="flex gap-2">
                    <button className="btn btn-secondary btn-sm" disabled={page === 1} onClick={() => setPage(p => p - 1)}>← Prev</button>
                    <button className="btn btn-secondary btn-sm" disabled={page === pages} onClick={() => setPage(p => p + 1)}>Next →</button>
                  </div>
                </div>
              </>
            )}
          </div>

          {/* Detail Panel */}
          {selected && (
            <div className="card animate-slideIn" style={{ position: 'sticky', top: '84px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', marginBottom: '16px' }}>
                <div>
                  <div style={{ fontWeight: 700, fontSize: '1rem', color: 'var(--color-text-primary)' }}>{selected.name}</div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', marginTop: '2px' }}>ID #{selected.id}</div>
                </div>
                <button className="btn btn-ghost btn-sm btn-icon" onClick={() => setSelected(null)}>✕</button>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '14px' }}>
                <DetailRow label="Status">
                  <Badge status={selected.status} />
                </DetailRow>
                <DetailRow label="Country">{selected.country_code || '—'}</DetailRow>
                <DetailRow label="Website">
                  <Badge status={selected.website_status} />
                </DetailRow>
                {selected.website_url && (
                  <DetailRow label="URL">
                    <a href={selected.website_url} target="_blank" rel="noopener noreferrer" style={{ color: 'var(--color-accent-secondary)', fontSize: '0.8rem', wordBreak: 'break-all' }}>
                      {selected.website_url}
                    </a>
                  </DetailRow>
                )}
                {selected.phone && <DetailRow label="Phone">{selected.phone}</DetailRow>}
                {selected.email && <DetailRow label="Email">{selected.email}</DetailRow>}
                {selected.locations?.length > 0 && (
                  <DetailRow label="Location">
                    {[selected.locations[0].address_line_1, selected.locations[0].city, selected.locations[0].state_province, selected.locations[0].postal_code].filter(Boolean).join(', ')}
                  </DetailRow>
                )}
                {selected.categories?.length > 0 && (
                  <DetailRow label="Categories">
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                      {selected.categories.map(c => (
                        <Badge key={c.id} label={c.category_name} variant="secondary" />
                      ))}
                    </div>
                  </DetailRow>
                )}
                {selected.social_urls && Object.keys(selected.social_urls).length > 0 && (
                  <DetailRow label="Social">
                    <div style={{ display: 'flex', flexWrap: 'wrap', gap: '4px' }}>
                      {Object.keys(selected.social_urls).map(k => (
                        <Badge key={k} label={k} variant="info" />
                      ))}
                    </div>
                  </DetailRow>
                )}
                <DetailRow label="Discovered">{new Date(selected.discovered_at).toLocaleString()}</DetailRow>
              </div>

              {/* Opportunity Signals & Audit */}
              <div style={{ marginTop: '20px', padding: '12px', background: 'rgba(99, 102, 241, 0.06)', borderRadius: 'var(--radius-md)', border: '1px solid rgba(99, 102, 241, 0.12)' }}>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '8px' }}>
                  <div style={{ fontSize: '0.72rem', fontWeight: 700, color: 'var(--color-text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
                    Opportunity Engine
                  </div>
                  <button
                    onClick={async () => {
                      setAuditLoading(true)
                      try {
                        const res = await api.opportunities.evaluate(selected.id)
                        setAuditResult(res)
                      } catch (err) {
                        alert(err.message)
                      } finally {
                        setAuditLoading(false)
                      }
                    }}
                    disabled={auditLoading}
                    className="btn btn-primary"
                    style={{ fontSize: '0.72rem', padding: '3px 8px' }}
                  >
                    {auditLoading ? 'Auditing…' : '⚡ Audit Now'}
                  </button>
                </div>
                {auditResult ? (
                  <div>
                    <div style={{ fontSize: '0.75rem', fontWeight: 600, color: 'var(--color-text)', marginBottom: '4px' }}>
                      {auditResult.opportunities?.length || 0} Opportunities Detected:
                    </div>
                    {auditResult.opportunities?.map((o, idx) => (
                      <div key={idx} style={{ fontSize: '0.75rem', color: 'var(--color-accent-primary)', marginBottom: '3px' }}>
                        ● {o.title} — <strong>{o.score}/100</strong> ({o.priority})
                      </div>
                    ))}
                  </div>
                ) : (
                  <div>
                    {selected.website_status === 'NOT_FOUND' && (
                      <div style={{ fontSize: '0.8rem', color: 'var(--color-accent-primary)', marginBottom: '4px' }}>● No official website found → Business website opportunity</div>
                    )}
                    {selected.website_status === 'SOCIAL_ONLY' && (
                      <div style={{ fontSize: '0.8rem', color: 'var(--color-accent-warning)', marginBottom: '4px' }}>● Social media only → Website + social integration</div>
                    )}
                    {selected.website_status === 'BROKEN' && (
                      <div style={{ fontSize: '0.8rem', color: 'var(--color-accent-danger)', marginBottom: '4px' }}>● Broken website → Website repair/redesign</div>
                    )}
                    {selected.website_status === 'FOUND' && (
                      <div style={{ fontSize: '0.78rem', color: 'var(--color-text-muted)' }}>Click Audit Now to run deep technical inspection and opportunity detection.</div>
                    )}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </>
  )
}

function DetailRow({ label, children }) {
  return (
    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', gap: '12px', fontSize: '0.82rem' }}>
      <span style={{ color: 'var(--color-text-muted)', flexShrink: 0, minWidth: '80px' }}>{label}</span>
      <span style={{ color: 'var(--color-text-secondary)', textAlign: 'right' }}>{children}</span>
    </div>
  )
}
