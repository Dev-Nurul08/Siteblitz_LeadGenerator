import { useState, useEffect } from 'react'
import PageHeader from '../components/PageHeader'
import StatCard from '../components/StatCard'
import Badge from '../components/Badge'
import api from '../services/api'

const ROLE_META = {
  EXECUTIVE: { label: 'Executive', color: 'badge-secondary', icon: '👑' },
  MANAGEMENT: { label: 'Management', color: 'badge-secondary', icon: '💼' },
  TECHNICAL: { label: 'Technical', color: 'badge-secondary', icon: '💻' },
  MARKETING: { label: 'Marketing', color: 'badge-success', icon: '📈' },
  STAFF: { label: 'Staff', color: 'badge-secondary', icon: '👤' },
  GENERAL_INBOX: { label: 'General Inbox', color: 'badge-warning', icon: '📥' },
}

const STATUS_META = {
  VERIFIED: { label: 'Verified', variant: 'success', icon: '✓' },
  RISKY: { label: 'Risky', variant: 'warning', icon: '⚠️' },
  ROLE_BASED: { label: 'Role Inbox', variant: 'secondary', icon: '🏢' },
  DISPOSABLE: { label: 'Disposable', variant: 'danger', icon: '🚫' },
  UNDELIVERABLE: { label: 'Undeliverable', variant: 'danger', icon: '❌' },
  UNVERIFIED: { label: 'Unverified', variant: 'secondary', icon: '⏳' },
}

export default function ContactsPage() {
  const [contacts, setContacts] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [pages, setPages] = useState(1)
  const [loading, setLoading] = useState(false)
  const [stats, setStats] = useState(null)
  const [enriching, setEnriching] = useState(false)

  // Filters
  const [search, setSearch] = useState('')
  const [roleFilter, setRoleFilter] = useState('')
  const [statusFilter, setStatusFilter] = useState('')

  // Standalone Verification Modal
  const [showVerifyModal, setShowVerifyModal] = useState(false)
  const [verifyEmailInput, setVerifyEmailInput] = useState('')
  const [verifyLoading, setVerifyLoading] = useState(false)
  const [verifyResult, setVerifyResult] = useState(null)
  const [verifyError, setVerifyError] = useState(null)

  useEffect(() => {
    loadContacts()
    loadStats()
  }, [page, roleFilter, statusFilter])

  async function loadStats() {
    try {
      const data = await api.contacts.stats()
      setStats(data)
    } catch (_) {}
  }

  async function loadContacts() {
    setLoading(true)
    try {
      const data = await api.contacts.list({
        page,
        pageSize: 25,
        roleLevel: roleFilter || undefined,
        emailStatus: statusFilter || undefined,
        search: search || undefined,
      })
      setContacts(data.items || [])
      setTotal(data.total || 0)
      setPages(data.pages || 1)
    } catch (e) {
      console.error('Failed to load contacts:', e)
    } finally {
      setLoading(false)
    }
  }

  function handleSearchSubmit(e) {
    e.preventDefault()
    setPage(1)
    loadContacts()
  }

  async function handleBatchEnrich() {
    setEnriching(true)
    try {
      await api.contacts.batchEnrich(25)
      await loadContacts()
      await loadStats()
    } catch (e) {
      alert(`Batch enrichment error: ${e.message}`)
    } finally {
      setEnriching(false)
    }
  }

  async function handleRunStandaloneVerify(e) {
    e.preventDefault()
    if (!verifyEmailInput.trim()) return
    setVerifyLoading(true)
    setVerifyResult(null)
    setVerifyError(null)
    try {
      const res = await api.contacts.verifyEmail(verifyEmailInput.trim())
      setVerifyResult(res)
    } catch (err) {
      setVerifyError(err.message || 'Verification failed')
    } finally {
      setVerifyLoading(false)
    }
  }

  return (
    <div className="page-container">
      <PageHeader
        title="Contacts & Deliverability"
        subtitle="Phase 3: B2B Contact Discovery, MX Deliverability Verification & Role Classification"
        actions={
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button
              className="btn btn-secondary"
              onClick={() => {
                setShowVerifyModal(true)
                setVerifyResult(null)
                setVerifyError(null)
              }}
            >
              <span style={{ marginRight: '6px' }}>🔬</span>
              Email Verifier Sandbox
            </button>
            <button
              className="btn btn-primary"
              onClick={handleBatchEnrich}
              disabled={enriching}
            >
              {enriching ? (
                <>
                  <span className="spinner" style={{ marginRight: '8px' }} />
                  Discovering Contacts...
                </>
              ) : (
                <>
                  <span style={{ marginRight: '6px' }}>⚡</span>
                  Batch Enrich Businesses (25)
                </>
              )}
            </button>
          </div>
        }
      />

      {/* KPI Stats */}
      <div className="stats-grid" style={{ marginBottom: '1.5rem' }}>
        <StatCard
          title="Total Contacts"
          value={stats?.total_contacts?.toLocaleString() || '0'}
          subValue="Discovered across businesses"
          icon="👥"
          trend="neutral"
        />
        <StatCard
          title="Verified Deliverability"
          value={`${stats?.verified_rate || 0}%`}
          subValue="Valid MX & Clean syntax"
          icon="🛡️"
          trend="up"
        />
        <StatCard
          title="Key Decision Makers"
          value={((stats?.by_role?.EXECUTIVE || 0) + (stats?.by_role?.MANAGEMENT || 0)).toLocaleString()}
          subValue={`${stats?.by_role?.EXECUTIVE || 0} Executives, ${stats?.by_role?.MANAGEMENT || 0} Managers`}
          icon="👑"
          trend="up"
        />
        <StatCard
          title="Direct Inboxes"
          value={((stats?.by_role?.TECHNICAL || 0) + (stats?.by_role?.MARKETING || 0) + (stats?.by_role?.STAFF || 0)).toLocaleString()}
          subValue={`${stats?.by_status?.ROLE_BASED || 0} general inboxes filtered`}
          icon="📬"
          trend="neutral"
        />
      </div>

      {/* Filter and Search Bar */}
      <div className="card" style={{ marginBottom: '1.5rem', padding: '1rem' }}>
        <form onSubmit={handleSearchSubmit} style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'center' }}>
          <div style={{ flex: '1 1 250px' }}>
            <input
              type="text"
              className="input-field"
              placeholder="Search by name, email, or business..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
          </div>
          <div style={{ width: '180px' }}>
            <select
              className="input-field"
              value={roleFilter}
              onChange={(e) => {
                setRoleFilter(e.target.value)
                setPage(1)
              }}
            >
              <option value="">All Role Levels</option>
              <option value="EXECUTIVE">👑 Executive / Owner</option>
              <option value="MANAGEMENT">💼 Management</option>
              <option value="TECHNICAL">💻 Technical / CTO</option>
              <option value="MARKETING">📈 Marketing / CMO</option>
              <option value="STAFF">👤 Staff / General</option>
              <option value="GENERAL_INBOX">📥 Role / General Inbox</option>
            </select>
          </div>
          <div style={{ width: '180px' }}>
            <select
              className="input-field"
              value={statusFilter}
              onChange={(e) => {
                setStatusFilter(e.target.value)
                setPage(1)
              }}
            >
              <option value="">All Deliverability</option>
              <option value="VERIFIED">✓ Verified</option>
              <option value="RISKY">⚠️ Risky</option>
              <option value="ROLE_BASED">🏢 Role Based</option>
              <option value="DISPOSABLE">🚫 Disposable</option>
              <option value="UNDELIVERABLE">❌ Undeliverable</option>
              <option value="UNVERIFIED">⏳ Unverified</option>
            </select>
          </div>
          <button type="submit" className="btn btn-secondary">
            Filter
          </button>
          {(roleFilter || statusFilter || search) && (
            <button
              type="button"
              className="btn btn-ghost"
              onClick={() => {
                setSearch('')
                setRoleFilter('')
                setStatusFilter('')
                setPage(1)
              }}
            >
              Reset
            </button>
          )}
        </form>
      </div>

      {/* Contacts Table */}
      <div className="card" style={{ overflow: 'hidden' }}>
        <div className="table-responsive">
          <table className="data-table">
            <thead>
              <tr>
                <th>Contact</th>
                <th>Role & Title</th>
                <th>Business</th>
                <th>Email Address</th>
                <th>Deliverability</th>
                <th>Score</th>
                <th>Source Provenance</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={7} style={{ textAlign: 'center', padding: '3rem' }}>
                    <div className="spinner" style={{ margin: '0 auto 1rem' }} />
                    <div style={{ color: 'var(--color-text-secondary)' }}>Loading verified contacts...</div>
                  </td>
                </tr>
              ) : contacts.length === 0 ? (
                <tr>
                  <td colSpan={7} style={{ textAlign: 'center', padding: '3.5rem 1rem' }}>
                    <div style={{ fontSize: '2.5rem', marginBottom: '0.75rem' }}>📭</div>
                    <div style={{ fontWeight: 600, fontSize: '1.1rem', marginBottom: '0.5rem' }}>No Contacts Found</div>
                    <p style={{ color: 'var(--color-text-secondary)', maxWidth: '400px', margin: '0 auto 1.5rem' }}>
                      Run batch discovery or select individual businesses to crawl websites for email addresses and decision makers.
                    </p>
                    <button className="btn btn-primary" onClick={handleBatchEnrich} disabled={enriching}>
                      {enriching ? 'Enriching...' : 'Batch Enrich Now'}
                    </button>
                  </td>
                </tr>
              ) : (
                contacts.map((c) => {
                  const roleMeta = ROLE_META[c.role_level] || ROLE_META.STAFF
                  const statusMeta = STATUS_META[c.email_status] || STATUS_META.UNVERIFIED
                  const scorePct = Math.round((c.verification_score || 0) * 100)

                  return (
                    <tr key={c.id}>
                      <td>
                        <div style={{ fontWeight: 600, color: 'var(--color-text-primary)' }}>
                          {c.full_name || 'Anonymous Contact'}
                        </div>
                        {c.phone && (
                          <div style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>
                            📞 {c.phone}
                          </div>
                        )}
                      </td>
                      <td>
                        <span className={`badge ${roleMeta.color}`} style={{ marginBottom: '4px', display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                          <span>{roleMeta.icon}</span>
                          <span>{roleMeta.label}</span>
                        </span>
                        {c.job_title && (
                          <div style={{ fontSize: '0.8rem', color: 'var(--color-text-secondary)', maxWidth: '160px', overflow: 'hidden', textOverflow: 'ellipsis', whiteSpace: 'nowrap' }}>
                            {c.job_title}
                          </div>
                        )}
                      </td>
                      <td>
                        <div style={{ fontWeight: 500 }}>{c.business_name || `Business #${c.business_id}`}</div>
                        <div style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>
                          {c.business_country || 'Global'}
                        </div>
                      </td>
                      <td>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                          <span style={{ fontFamily: 'var(--font-mono)', fontSize: '0.88rem', color: 'var(--color-accent-secondary)' }}>
                            {c.email}
                          </span>
                          <button
                            title="Copy email"
                            style={{ background: 'none', border: 'none', cursor: 'pointer', opacity: 0.6, fontSize: '0.85rem' }}
                            onClick={() => navigator.clipboard?.writeText(c.email)}
                          >
                            📋
                          </button>
                        </div>
                        {c.is_role_based && (
                          <div style={{ fontSize: '0.75rem', color: 'var(--color-accent-warning)' }}>
                            ⚠️ General mailbox (e.g. info@)
                          </div>
                        )}
                      </td>
                      <td>
                        <Badge variant={statusMeta.variant} label={`${statusMeta.icon} ${statusMeta.label}`} />
                        {c.has_valid_mx && (
                          <div style={{ fontSize: '0.75rem', color: 'var(--color-accent-success)', marginTop: '2px' }}>
                            MX Verified
                          </div>
                        )}
                      </td>
                      <td>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <div
                            style={{
                              width: '48px',
                              height: '6px',
                              background: 'var(--color-bg-tertiary)',
                              borderRadius: '3px',
                              overflow: 'hidden',
                            }}
                          >
                            <div
                              style={{
                                width: `${scorePct}%`,
                                height: '100%',
                                background:
                                  scorePct >= 80
                                    ? 'var(--color-accent-success)'
                                    : scorePct >= 50
                                    ? 'var(--color-accent-warning)'
                                    : 'var(--color-accent-danger)',
                              }}
                            />
                          </div>
                          <span style={{ fontSize: '0.82rem', fontFamily: 'var(--font-mono)', fontWeight: 600 }}>
                            {scorePct}%
                          </span>
                        </div>
                      </td>
                      <td>
                        <div style={{ fontSize: '0.82rem', color: 'var(--color-text-secondary)' }}>
                          {c.source_method || 'Direct'}
                        </div>
                        {c.source_url && (
                          <a
                            href={c.source_url}
                            target="_blank"
                            rel="noreferrer"
                            style={{ fontSize: '0.75rem', color: 'var(--color-accent-primary)', textDecoration: 'none' }}
                          >
                            Source Link ↗
                          </a>
                        )}
                      </td>
                    </tr>
                  )
                })
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination footer */}
        {total > 0 && (
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              padding: '1rem',
              borderTop: '1px solid var(--color-border)',
              fontSize: '0.88rem',
              color: 'var(--color-text-secondary)',
            }}
          >
            <div>
              Showing {contacts.length} of {total} contacts (Page {page} of {pages})
            </div>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <button
                className="btn btn-secondary"
                disabled={page <= 1}
                onClick={() => setPage((p) => Math.max(1, p - 1))}
                style={{ padding: '0.4rem 0.8rem', fontSize: '0.85rem' }}
              >
                Previous
              </button>
              <button
                className="btn btn-secondary"
                disabled={page >= pages}
                onClick={() => setPage((p) => Math.min(pages, p + 1))}
                style={{ padding: '0.4rem 0.8rem', fontSize: '0.85rem' }}
              >
                Next
              </button>
            </div>
          </div>
        )}
      </div>

      {/* Standalone Email Verifier Sandbox Modal */}
      {showVerifyModal && (
        <div className="modal-backdrop" onClick={() => setShowVerifyModal(false)}>
          <div className="modal-card" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '580px', width: '100%' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ fontSize: '1.5rem' }}>🔬</span>
                <h3 style={{ margin: 0, fontSize: '1.25rem' }}>DNS & Deliverability Sandbox</h3>
              </div>
              <button
                className="btn btn-ghost"
                onClick={() => setShowVerifyModal(false)}
                style={{ padding: '0.25rem 0.5rem' }}
              >
                ✕
              </button>
            </div>

            <p style={{ color: 'var(--color-text-secondary)', fontSize: '0.88rem', marginBottom: '1.25rem' }}>
              Execute live RFC-5322 regex parsing, disposable provider lookup, and live DNS MX resolution to verify inbox deliverability before outreach.
            </p>

            <form onSubmit={handleRunStandaloneVerify} style={{ display: 'flex', gap: '0.75rem', marginBottom: '1.5rem' }}>
              <input
                type="email"
                required
                className="input-field"
                placeholder="Enter email address (e.g. contact@domain.com)..."
                value={verifyEmailInput}
                onChange={(e) => setVerifyEmailInput(e.target.value)}
                style={{ flex: 1 }}
              />
              <button type="submit" className="btn btn-primary" disabled={verifyLoading}>
                {verifyLoading ? 'Auditing...' : 'Verify DNS'}
              </button>
            </form>

            {verifyError && (
              <div style={{ padding: '0.75rem', background: 'rgba(239, 68, 68, 0.1)', border: '1px solid var(--color-accent-danger)', borderRadius: '8px', color: 'var(--color-accent-danger)', fontSize: '0.88rem', marginBottom: '1rem' }}>
                ❌ {verifyError}
              </div>
            )}

            {verifyResult && (
              <div style={{ background: 'var(--color-bg-primary)', border: '1px solid var(--color-border)', borderRadius: '10px', padding: '1.25rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem', borderBottom: '1px solid var(--color-border)', paddingBottom: '0.75rem' }}>
                  <div>
                    <div style={{ fontWeight: 600, fontSize: '1.05rem', color: 'var(--color-text-primary)' }}>
                      {verifyResult.email}
                    </div>
                    <div style={{ fontSize: '0.82rem', color: 'var(--color-text-secondary)' }}>
                      Domain: {verifyResult.domain || 'N/A'}
                    </div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <Badge variant={STATUS_META[verifyResult.status]?.variant || 'secondary'} label={verifyResult.status} />
                    <div style={{ fontSize: '0.85rem', fontFamily: 'var(--font-mono)', fontWeight: 700, marginTop: '4px', color: 'var(--color-accent-secondary)' }}>
                      Score: {Math.round(verifyResult.verification_score * 100)}%
                    </div>
                  </div>
                </div>

                <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '0.75rem', fontSize: '0.85rem' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <span>{verifyResult.is_valid_syntax ? '✅' : '❌'}</span>
                    <span>RFC 5322 Syntax Valid</span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <span>{verifyResult.has_valid_mx ? '✅' : '❌'}</span>
                    <span>Active MX DNS Record</span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <span>{verifyResult.is_disposable ? '⚠️ Yes (Blocked)' : '✅ No'}</span>
                    <span>Disposable / Burner Email</span>
                  </div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <span>{verifyResult.is_role_based ? '⚠️ Yes (Generic)' : '✅ Personal Inbox'}</span>
                    <span>Role-Based Address</span>
                  </div>
                </div>

                {verifyResult.mx_records && verifyResult.mx_records.length > 0 && (
                  <div style={{ marginTop: '1rem', borderTop: '1px solid var(--color-border)', paddingTop: '0.75rem' }}>
                    <div style={{ fontSize: '0.78rem', color: 'var(--color-text-muted)', marginBottom: '4px' }}>
                      Discovered MX Hosts:
                    </div>
                    <div style={{ fontFamily: 'var(--font-mono)', fontSize: '0.8rem', color: 'var(--color-text-secondary)', background: 'var(--color-bg-secondary)', padding: '0.5rem', borderRadius: '6px' }}>
                      {verifyResult.mx_records.join(', ')}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}
