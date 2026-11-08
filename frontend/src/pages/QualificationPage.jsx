import { useState, useEffect } from 'react'
import PageHeader from '../components/PageHeader'
import StatCard from '../components/StatCard'
import Badge from '../components/Badge'
import api from '../services/api'

const LEAD_STATUS_META = {
  READY_FOR_OUTREACH: { label: 'Ready for Outreach', variant: 'success', icon: '🚀' },
  QUALIFIED: { label: 'Qualified', variant: 'info', icon: '✅' },
  NEEDS_REVIEW: { label: 'Needs Review', variant: 'warning', icon: '⚠️' },
  DISQUALIFIED: { label: 'Disqualified', variant: 'danger', icon: '🚫' },
  CONTACTED: { label: 'Contacted', variant: 'secondary', icon: '📨' },
  CONVERTED: { label: 'Converted', variant: 'success', icon: '🎉' },
}

const FRAMEWORK_META = {
  CAN_SPAM: { label: 'US CAN-SPAM', icon: '🇺🇸', color: 'badge-secondary' },
  GDPR_UK: { label: 'UK PECR/GDPR', icon: '🇬🇧', color: 'badge-secondary' },
  GDPR_EU: { label: 'EU GDPR', icon: '🇪🇺', color: 'badge-warning' },
  CASL: { label: 'Canada CASL', icon: '🇨🇦', color: 'badge-danger' },
  AUSTRALIA_SPAM_ACT: { label: 'AU Spam Act', icon: '🇦🇺', color: 'badge-secondary' },
  GENERAL_B2B: { label: 'General B2B', icon: '🌐', color: 'badge-secondary' },
}

export default function QualificationPage() {
  const [leads, setLeads] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [pages, setPages] = useState(1)
  const [loading, setLoading] = useState(false)
  const [stats, setStats] = useState(null)
  const [qualifying, setQualifying] = useState(false)

  // Filters
  const [statusFilter, setStatusFilter] = useState('')
  const [countryFilter, setCountryFilter] = useState('')
  const [minScoreFilter, setMinScoreFilter] = useState('')
  const [search, setSearch] = useState('')

  // Review Modal State
  const [selectedLead, setSelectedLead] = useState(null)
  const [updatingStatus, setUpdatingStatus] = useState(false)

  // Suppression Registry Modal State
  const [showSuppressionModal, setShowSuppressionModal] = useState(false)
  const [optOuts, setOptOuts] = useState([])
  const [newOptOutEmail, setNewOptOutEmail] = useState('')
  const [newOptOutReason, setNewOptOutReason] = useState('User requested unsubscribe')
  const [addingOptOut, setAddingOptOut] = useState(false)

  useEffect(() => {
    loadLeads()
    loadStats()
  }, [page, statusFilter, countryFilter, minScoreFilter])

  async function loadStats() {
    try {
      const data = await api.qualification.stats()
      setStats(data)
    } catch (_) {}
  }

  async function loadLeads() {
    setLoading(true)
    try {
      const data = await api.qualification.listLeads({
        page,
        pageSize: 25,
        status: statusFilter || undefined,
        country: countryFilter || undefined,
        minScore: minScoreFilter || undefined,
        search: search || undefined,
      })
      setLeads(data.items || [])
      setTotal(data.total || 0)
      setPages(data.pages || 1)
    } catch (e) {
      console.error('Failed to load qualified leads:', e)
    } finally {
      setLoading(false)
    }
  }

  function handleSearchSubmit(e) {
    e.preventDefault()
    setPage(1)
    loadLeads()
  }

  async function handleBatchQualify() {
    setQualifying(true)
    try {
      await api.qualification.batchQualify(25)
      await loadLeads()
      await loadStats()
    } catch (e) {
      alert(`Batch qualification error: ${e.message}`)
    } finally {
      setQualifying(false)
    }
  }

  async function handleUpdateLeadStatus(leadId, newStatus) {
    setUpdatingStatus(true)
    try {
      await api.qualification.updateStatus(leadId, { status: newStatus })
      if (selectedLead && selectedLead.id === leadId) {
        setSelectedLead({ ...selectedLead, lead_status: newStatus })
      }
      await loadLeads()
      await loadStats()
    } catch (e) {
      alert(`Error updating lead status: ${e.message}`)
    } finally {
      setUpdatingStatus(false)
    }
  }

  async function loadOptOuts() {
    try {
      const data = await api.qualification.listOptOuts({ page: 1, pageSize: 50 })
      setOptOuts(data.items || [])
    } catch (_) {}
  }

  async function handleAddOptOut(e) {
    e.preventDefault()
    if (!newOptOutEmail.trim()) return
    setAddingOptOut(true)
    try {
      await api.qualification.addOptOut({
        email: newOptOutEmail.trim(),
        reason: newOptOutReason,
        source: 'OPERATOR_MANUAL',
      })
      setNewOptOutEmail('')
      await loadOptOuts()
      await loadLeads()
      await loadStats()
    } catch (err) {
      alert(`Suppression error: ${err.message}`)
    } finally {
      setAddingOptOut(false)
    }
  }

  return (
    <div className="page-container">
      <PageHeader
        title="Qualification & Compliance"
        subtitle="Phase 4: Multi-jurisdiction Compliance Engine, Composite Lead Scoring, AI Pitch Synthesis & Suppression Registry"
        actions={
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button
              className="btn btn-secondary"
              onClick={() => {
                setShowSuppressionModal(true)
                loadOptOuts()
              }}
            >
              <span style={{ marginRight: '6px' }}>🛡️</span>
              Suppression Registry ({stats?.opt_out_count || 0})
            </button>
            <button
              className="btn btn-primary"
              onClick={handleBatchQualify}
              disabled={qualifying}
            >
              {qualifying ? (
                <>
                  <span className="spinner" style={{ marginRight: '8px' }} />
                  Evaluating Leads...
                </>
              ) : (
                <>
                  <span style={{ marginRight: '6px' }}>⚡</span>
                  Batch Qualify Leads (25)
                </>
              )}
            </button>
          </div>
        }
      />

      {/* KPI Cards */}
      <div className="stats-grid" style={{ marginBottom: '1.5rem' }}>
        <StatCard
          title="Total Evaluated"
          value={stats?.total_leads?.toLocaleString() || '0'}
          subValue="Audited through compliance engine"
          icon="📊"
          trend="neutral"
        />
        <StatCard
          title="Ready for Outreach"
          value={stats?.ready_for_outreach_count?.toLocaleString() || '0'}
          subValue="Passed opportunity & compliance gates"
          icon="🚀"
          trend="up"
        />
        <StatCard
          title="Review Queue"
          value={(stats?.by_status?.NEEDS_REVIEW || 0).toLocaleString()}
          subValue="Requires human operator sign-off"
          icon="⚠️"
          trend={stats?.by_status?.NEEDS_REVIEW > 0 ? 'down' : 'neutral'}
        />
        <StatCard
          title="Average Quality Score"
          value={`${stats?.avg_composite_score || 0}%`}
          subValue="Weighted opportunity + deliverability"
          icon="🎯"
          trend="up"
        />
      </div>

      {/* Filters */}
      <div className="card" style={{ marginBottom: '1.5rem', padding: '1rem' }}>
        <form onSubmit={handleSearchSubmit} style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'center' }}>
          <div style={{ flex: '1 1 250px' }}>
            <input
              type="text"
              className="input-field"
              placeholder="Search by business, email, or contact name..."
              value={search}
              onChange={(e) => setSearch(e.target.value)}
            />
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
              <option value="">All Statuses</option>
              <option value="READY_FOR_OUTREACH">🚀 Ready for Outreach</option>
              <option value="QUALIFIED">✅ Qualified</option>
              <option value="NEEDS_REVIEW">⚠️ Needs Review</option>
              <option value="DISQUALIFIED">🚫 Disqualified</option>
            </select>
          </div>
          <div style={{ width: '140px' }}>
            <select
              className="input-field"
              value={countryFilter}
              onChange={(e) => {
                setCountryFilter(e.target.value)
                setPage(1)
              }}
            >
              <option value="">All Countries</option>
              <option value="US">🇺🇸 United States</option>
              <option value="GB">🇬🇧 United Kingdom</option>
              <option value="CA">🇨🇦 Canada</option>
              <option value="AU">🇦🇺 Australia</option>
              <option value="DE">🇩🇪 Germany</option>
              <option value="FR">🇫🇷 France</option>
            </select>
          </div>
          <button type="submit" className="btn btn-secondary">
            Filter
          </button>
          {(statusFilter || countryFilter || minScoreFilter || search) && (
            <button
              type="button"
              className="btn btn-ghost"
              onClick={() => {
                setSearch('')
                setStatusFilter('')
                setCountryFilter('')
                setMinScoreFilter('')
                setPage(1)
              }}
            >
              Reset
            </button>
          )}
        </form>
      </div>

      {/* Leads Table */}
      <div className="card" style={{ overflow: 'hidden' }}>
        <div className="table-responsive">
          <table className="data-table">
            <thead>
              <tr>
                <th>Lead / Company</th>
                <th>Service Opportunity</th>
                <th>Contact Person</th>
                <th>Jurisdiction & Mode</th>
                <th>Composite Score</th>
                <th>Status</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {loading ? (
                <tr>
                  <td colSpan={7} style={{ textAlign: 'center', padding: '3rem' }}>
                    <div className="spinner" style={{ margin: '0 auto 1rem' }} />
                    <div style={{ color: 'var(--color-text-secondary)' }}>Loading qualified leads...</div>
                  </td>
                </tr>
              ) : leads.length === 0 ? (
                <tr>
                  <td colSpan={7} style={{ textAlign: 'center', padding: '3.5rem 1rem' }}>
                    <div style={{ fontSize: '2.5rem', marginBottom: '0.75rem' }}>🎯</div>
                    <div style={{ fontWeight: 600, fontSize: '1.1rem', marginBottom: '0.5rem' }}>No Qualified Leads Yet</div>
                    <p style={{ color: 'var(--color-text-secondary)', maxWidth: '400px', margin: '0 auto 1.5rem' }}>
                      Run batch qualification to evaluate discovered businesses, verify compliance legality, and generate AI personalized sales copy.
                    </p>
                    <button className="btn btn-primary" onClick={handleBatchQualify} disabled={qualifying}>
                      {qualifying ? 'Evaluating...' : 'Batch Qualify Now'}
                    </button>
                  </td>
                </tr>
              ) : (
                leads.map((lead) => {
                  const statusMeta = LEAD_STATUS_META[lead.lead_status] || LEAD_STATUS_META.QUALIFIED
                  const fwMeta = FRAMEWORK_META[lead.legal_framework] || FRAMEWORK_META.GENERAL_B2B
                  const scorePct = Math.round(lead.composite_score)

                  return (
                    <tr key={lead.id}>
                      <td>
                        <div style={{ fontWeight: 600, color: 'var(--color-text-primary)' }}>
                          {lead.business_name}
                        </div>
                        <div style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>
                          {lead.business_city ? `${lead.business_city}, ` : ''}{lead.business_country || 'Global'}
                        </div>
                      </td>
                      <td>
                        <span className="badge badge-secondary">
                          {lead.opportunity_service?.replace(/_/g, ' ') || 'Digital Need'}
                        </span>
                      </td>
                      <td>
                        <div style={{ fontWeight: 500 }}>{lead.contact_name || 'Business Contact'}</div>
                        <div style={{ fontSize: '0.8rem', fontFamily: 'var(--font-mono)', color: 'var(--color-accent-secondary)' }}>
                          {lead.contact_email}
                        </div>
                      </td>
                      <td>
                        <span className={`badge ${fwMeta.color}`} style={{ marginBottom: '3px', display: 'inline-flex', alignItems: 'center', gap: '4px' }}>
                          <span>{fwMeta.icon}</span>
                          <span>{fwMeta.label}</span>
                        </span>
                        <div style={{ fontSize: '0.75rem', color: lead.outreach_mode === 'AUTOMATED' ? 'var(--color-accent-success)' : 'var(--color-accent-warning)' }}>
                          {lead.outreach_mode === 'AUTOMATED' ? '⚡ Auto Sequence' : '👤 Manual Review'}
                        </div>
                      </td>
                      <td>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                          <div
                            style={{
                              width: '45px',
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
                                    : scorePct >= 60
                                    ? 'var(--color-accent-warning)'
                                    : 'var(--color-accent-danger)',
                              }}
                            />
                          </div>
                          <span style={{ fontSize: '0.85rem', fontFamily: 'var(--font-mono)', fontWeight: 700 }}>
                            {scorePct}%
                          </span>
                        </div>
                      </td>
                      <td>
                        <Badge variant={statusMeta.variant} label={`${statusMeta.icon} ${statusMeta.label}`} />
                        {lead.validation_passed && (
                          <div style={{ fontSize: '0.72rem', color: 'var(--color-accent-success)', marginTop: '2px' }}>
                            ✓ Safety Verified
                          </div>
                        )}
                      </td>
                      <td>
                        <button
                          className="btn btn-secondary"
                          style={{ padding: '0.35rem 0.75rem', fontSize: '0.82rem' }}
                          onClick={() => setSelectedLead(lead)}
                        >
                          👁️ Review & Pitch
                        </button>
                      </td>
                    </tr>
                  )
                })
              )}
            </tbody>
          </table>
        </div>

        {/* Pagination */}
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
              Showing {leads.length} of {total} leads (Page {page} of {pages})
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

      {/* Lead Review & Pitch Modal */}
      {selectedLead && (
        <div className="modal-backdrop" onClick={() => setSelectedLead(null)}>
          <div className="modal-card" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '680px', width: '100%' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', borderBottom: '1px solid var(--color-border)', paddingBottom: '0.75rem' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <h3 style={{ margin: 0, fontSize: '1.3rem' }}>{selectedLead.business_name}</h3>
                  <Badge variant={LEAD_STATUS_META[selectedLead.lead_status]?.variant || 'secondary'} label={selectedLead.lead_status} />
                </div>
                <div style={{ fontSize: '0.82rem', color: 'var(--color-text-secondary)', marginTop: '4px' }}>
                  Target: {selectedLead.contact_name} ({selectedLead.contact_email}) • {selectedLead.business_country || 'Global'}
                </div>
              </div>
              <button className="btn btn-ghost" onClick={() => setSelectedLead(null)} style={{ padding: '0.25rem 0.5rem' }}>
                ✕
              </button>
            </div>

            {/* AI Personalized Pitch Preview */}
            <div style={{ marginBottom: '1.25rem' }}>
              <div style={{ fontWeight: 600, fontSize: '0.9rem', marginBottom: '0.4rem', color: 'var(--color-text-secondary)' }}>
                Subject Line:
              </div>
              <input
                type="text"
                readOnly
                className="input-field"
                value={selectedLead.personalized_subject || 'No subject synthesized'}
                style={{ fontFamily: 'var(--font-family)', fontWeight: 500 }}
              />
            </div>

            <div style={{ marginBottom: '1.25rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
                <span style={{ fontWeight: 600, fontSize: '0.9rem', color: 'var(--color-text-secondary)' }}>
                  Personalized Outreach Copy:
                </span>
                <span style={{ fontSize: '0.75rem', color: 'var(--color-accent-success)' }}>
                  ✓ FTC & CAN-SPAM Compliant
                </span>
              </div>
              <div
                style={{
                  background: 'var(--color-bg-primary)',
                  border: '1px solid var(--color-border)',
                  borderRadius: '8px',
                  padding: '1rem',
                  fontFamily: 'var(--font-family)',
                  fontSize: '0.88rem',
                  lineHeight: '1.6',
                  whiteSpace: 'pre-wrap',
                  maxHeight: '260px',
                  overflowY: 'auto',
                  color: 'var(--color-text-primary)',
                }}
              >
                {selectedLead.personalized_pitch || 'No pitch body generated.'}
              </div>
            </div>

            {/* Regulatory Checklist & Diagnostics */}
            <div style={{ background: 'var(--color-bg-secondary)', border: '1px solid var(--color-border)', borderRadius: '8px', padding: '0.85rem', marginBottom: '1.5rem', fontSize: '0.82rem' }}>
              <div style={{ fontWeight: 600, marginBottom: '6px', color: 'var(--color-text-secondary)' }}>
                Compliance & Quality Safeguards:
              </div>
              <div style={{ display: 'grid', gridTemplateColumns: 'repeat(2, 1fr)', gap: '6px' }}>
                <div>✅ Lawful Basis: {selectedLead.legal_framework || 'B2B Legitimate Interest'}</div>
                <div>✅ Unsubscribe Token Present</div>
                <div>✅ Physical Postal Address Included</div>
                <div>✅ Deliverability Verified</div>
              </div>
            </div>

            {/* Operator Actions */}
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px solid var(--color-border)', paddingTop: '1rem' }}>
              <button
                className="btn btn-secondary"
                onClick={() => handleUpdateLeadStatus(selectedLead.id, 'DISQUALIFIED')}
                disabled={updatingStatus}
                style={{ color: 'var(--color-accent-danger)' }}
              >
                Disqualify Lead
              </button>
              <div style={{ display: 'flex', gap: '0.75rem' }}>
                <button
                  className="btn btn-secondary"
                  onClick={() => setSelectedLead(null)}
                >
                  Close
                </button>
                {selectedLead.lead_status !== 'READY_FOR_OUTREACH' && (
                  <button
                    className="btn btn-primary"
                    onClick={() => handleUpdateLeadStatus(selectedLead.id, 'READY_FOR_OUTREACH')}
                    disabled={updatingStatus}
                  >
                    {updatingStatus ? 'Updating...' : '🚀 Approve for Phase 5 Outreach'}
                  </button>
                )}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Suppression Registry Modal */}
      {showSuppressionModal && (
        <div className="modal-backdrop" onClick={() => setShowSuppressionModal(false)}>
          <div className="modal-card" onClick={(e) => e.stopPropagation()} style={{ maxWidth: '620px', width: '100%' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                <span style={{ fontSize: '1.5rem' }}>🛡️</span>
                <h3 style={{ margin: 0, fontSize: '1.25rem' }}>Global Suppression Registry</h3>
              </div>
              <button className="btn btn-ghost" onClick={() => setShowSuppressionModal(false)} style={{ padding: '0.25rem 0.5rem' }}>
                ✕
              </button>
            </div>

            <p style={{ color: 'var(--color-text-secondary)', fontSize: '0.88rem', marginBottom: '1.25rem' }}>
              Addresses and domains listed here are strictly blocked across all campaigns, evaluations, and schedulers to ensure zero contact with opted-out parties.
            </p>

            <form onSubmit={handleAddOptOut} style={{ display: 'flex', gap: '0.75rem', marginBottom: '1.5rem' }}>
              <input
                type="email"
                required
                className="input-field"
                placeholder="Email address to suppress (e.g. user@domain.com)..."
                value={newOptOutEmail}
                onChange={(e) => setNewOptOutEmail(e.target.value)}
                style={{ flex: 1 }}
              />
              <button type="submit" className="btn btn-primary" disabled={addingOptOut}>
                {addingOptOut ? 'Adding...' : 'Add to Registry'}
              </button>
            </form>

            <div style={{ maxHeight: '240px', overflowY: 'auto', border: '1px solid var(--color-border)', borderRadius: '8px' }}>
              <table className="data-table" style={{ fontSize: '0.82rem' }}>
                <thead>
                  <tr>
                    <th>Suppressed Email</th>
                    <th>Reason</th>
                    <th>Source</th>
                  </tr>
                </thead>
                <tbody>
                  {optOuts.length === 0 ? (
                    <tr>
                      <td colSpan={3} style={{ textAlign: 'center', padding: '1.5rem', color: 'var(--color-text-secondary)' }}>
                        No suppressed records in registry.
                      </td>
                    </tr>
                  ) : (
                    optOuts.map((o) => (
                      <tr key={o.id}>
                        <td style={{ fontFamily: 'var(--font-mono)', color: 'var(--color-accent-danger)' }}>
                          {o.email}
                        </td>
                        <td>{o.reason}</td>
                        <td>
                          <span className="badge badge-secondary">{o.source}</span>
                        </td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
