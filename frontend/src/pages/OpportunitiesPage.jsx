import { useState, useEffect } from 'react'
import PageHeader from '../components/PageHeader'
import StatCard from '../components/StatCard'
import Badge from '../components/Badge'
import api from '../services/api'

const SERVICE_META = {
  NEW_WEBSITE: { icon: '🌐', label: 'New Website', color: 'badge-danger' },
  WEBSITE_REDESIGN: { icon: '🔄', label: 'Website Redesign', color: 'badge-warning' },
  MOBILE_APP: { icon: '📱', label: 'Mobile App', color: 'badge-purple' },
  ECOMMERCE_EXPANSION: { icon: '🛒', label: 'E-Commerce Store', color: 'badge-success' },
  ONLINE_BOOKING: { icon: '📅', label: 'Online Booking', color: 'badge-info' },
  SEO_PERFORMANCE: { icon: '⚡', label: 'SEO & Speed', color: 'badge-neutral' },
  CUSTOM_WEB_APP: { icon: '💻', label: 'Custom Web App', color: 'badge-purple' },
}

const PRIORITY_META = {
  CRITICAL: { icon: '🔴', label: 'Critical', color: 'badge-danger' },
  HIGH: { icon: '🟠', label: 'High', color: 'badge-warning' },
  MEDIUM: { icon: '🟡', label: 'Medium', color: 'badge-info' },
  LOW: { icon: '⚪', label: 'Low', color: 'badge-neutral' },
}

export default function OpportunitiesPage() {
  const [opportunities, setOpportunities] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [pages, setPages] = useState(1)
  const [loading, setLoading] = useState(false)
  const [stats, setStats] = useState(null)
  const [scanning, setScanning] = useState(false)
  const [selectedOpp, setSelectedOpp] = useState(null)
  const [auditDetails, setAuditDetails] = useState(null)
  const [loadingAudit, setLoadingAudit] = useState(false)

  // Filters
  const [categoryFilter, setCategoryFilter] = useState('')
  const [priorityFilter, setPriorityFilter] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [countryFilter, setCountryFilter] = useState('')

  useEffect(() => {
    loadOpportunities()
    loadStats()
  }, [page, categoryFilter, priorityFilter, statusFilter, countryFilter])

  async function loadStats() {
    try {
      const data = await api.opportunities.stats()
      setStats(data)
    } catch (_) {}
  }

  async function loadOpportunities() {
    setLoading(true)
    try {
      const data = await api.opportunities.list({
        page,
        page_size: 25,
        service_category: categoryFilter || undefined,
        priority: priorityFilter || undefined,
        status: statusFilter || undefined,
        country: countryFilter || undefined,
      })
      setOpportunities(data.items || [])
      setTotal(data.total || 0)
      setPages(data.pages || 1)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  async function handleBatchScan() {
    setScanning(true)
    try {
      await api.opportunities.batchEvaluate(30)
      await loadOpportunities()
      await loadStats()
    } catch (e) {
      alert(`Scan failed: ${e.message}`)
    } finally {
      setScanning(false)
    }
  }

  async function handleViewEvidence(opp) {
    setSelectedOpp(opp)
    setAuditDetails(null)
    if (opp.business_id) {
      setLoadingAudit(true)
      try {
        const audits = await api.opportunities.audits(opp.business_id)
        if (audits && audits.length > 0) {
          setAuditDetails(audits[0])
        }
      } catch (_) {}
      finally {
        setLoadingAudit(false)
      }
    }
  }

  async function handleUpdateStatus(oppId, newStatus) {
    try {
      await api.opportunities.update(oppId, { status: newStatus })
      setOpportunities(prev =>
        prev.map(o => (o.id === oppId ? { ...o, status: newStatus } : o))
      )
      if (selectedOpp && selectedOpp.id === oppId) {
        setSelectedOpp(prev => ({ ...prev, status: newStatus }))
      }
      loadStats()
    } catch (e) {
      alert(`Update failed: ${e.message}`)
    }
  }

  return (
    <div className="page-container animate-fade-in">
      <div className="page-header-row flex items-center justify-between mb-6">
        <PageHeader
          title="Sales Opportunities"
          description="Qualified digital-service needs matched to agency capabilities and prioritized by urgency."
        />
        <button
          onClick={handleBatchScan}
          disabled={scanning}
          className="btn btn-primary flex items-center gap-2"
        >
          {scanning ? (
            <>
              <span className="spinner spinner-sm"></span>
              Scanning Businesses…
            </>
          ) : (
            <>
              <span>⚡</span>
              Scan Unaudited Leads
            </>
          )}
        </button>
      </div>

      {/* KPI Stats */}
      {stats && (
        <div className="grid grid-cols-4 gap-4 mb-6">
          <StatCard
            label="Total Opportunities"
            value={stats.total_opportunities || 0}
            icon="🎯"
            color="primary"
          />
          <StatCard
            label="Critical Urgency"
            value={stats.by_priority?.CRITICAL || 0}
            icon="🔴"
            color="danger"
          />
          <StatCard
            label="High Priority"
            value={stats.by_priority?.HIGH || 0}
            icon="🟠"
            color="warning"
          />
          <StatCard
            label="Avg. Need Score"
            value={`${stats.average_score || 0}/100`}
            icon="⭐"
            color="success"
          />
        </div>
      )}

      {/* Filter Bar */}
      <div className="card mb-6 flex flex-wrap gap-4 items-center">
        <div className="form-group flex-1 min-w-[180px]">
          <label className="form-label text-xs">Service Category</label>
          <select
            className="form-input text-sm"
            value={categoryFilter}
            onChange={e => {
              setCategoryFilter(e.target.value)
              setPage(1)
            }}
          >
            <option value="">All Services</option>
            {Object.entries(SERVICE_META).map(([key, meta]) => (
              <option key={key} value={key}>
                {meta.icon} {meta.label}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group flex-1 min-w-[140px]">
          <label className="form-label text-xs">Priority</label>
          <select
            className="form-input text-sm"
            value={priorityFilter}
            onChange={e => {
              setPriorityFilter(e.target.value)
              setPage(1)
            }}
          >
            <option value="">All Priorities</option>
            <option value="CRITICAL">🔴 Critical</option>
            <option value="HIGH">🟠 High</option>
            <option value="MEDIUM">🟡 Medium</option>
            <option value="LOW">⚪ Low</option>
          </select>
        </div>

        <div className="form-group flex-1 min-w-[140px]">
          <label className="form-label text-xs">Stage</label>
          <select
            className="form-input text-sm"
            value={statusFilter}
            onChange={e => {
              setStatusFilter(e.target.value)
              setPage(1)
            }}
          >
            <option value="">All Stages</option>
            <option value="IDENTIFIED">Identified</option>
            <option value="EVALUATING">Evaluating</option>
            <option value="QUALIFIED">Qualified</option>
            <option value="DISQUALIFIED">Disqualified</option>
            <option value="CONVERTED">Converted</option>
          </select>
        </div>

        <div className="form-group w-32">
          <label className="form-label text-xs">Country</label>
          <input
            type="text"
            className="form-input text-sm uppercase"
            placeholder="e.g. GB"
            maxLength={2}
            value={countryFilter}
            onChange={e => {
              setCountryFilter(e.target.value)
              setPage(1)
            }}
          />
        </div>

        {(categoryFilter || priorityFilter || statusFilter || countryFilter) && (
          <button
            onClick={() => {
              setCategoryFilter('')
              setPriorityFilter('')
              setStatusFilter('')
              setCountryFilter('')
              setPage(1)
            }}
            className="btn btn-secondary text-xs mt-4"
          >
            Clear Filters
          </button>
        )}
      </div>

      {/* Opportunities Table */}
      <div className="card">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-base font-semibold text-white">
            Target Leads ({total})
          </h3>
          <span className="text-xs text-text-muted">
            Page {page} of {pages}
          </span>
        </div>

        {loading ? (
          <div className="flex justify-center items-center py-12">
            <span className="spinner spinner-lg"></span>
          </div>
        ) : opportunities.length === 0 ? (
          <div className="text-center py-12 text-text-muted">
            <p className="text-4xl mb-2">🔍</p>
            <p className="text-base font-medium text-white mb-1">
              No opportunities match current criteria
            </p>
            <p className="text-xs">
              Try importing more businesses or running the automated scanner.
            </p>
          </div>
        ) : (
          <div className="table-responsive">
            <table className="table">
              <thead>
                <tr>
                  <th>Business</th>
                  <th>Service Opportunity</th>
                  <th>Urgency Score</th>
                  <th>Priority</th>
                  <th>Stage</th>
                  <th className="text-right">Action</th>
                </tr>
              </thead>
              <tbody>
                {opportunities.map(opp => {
                  const sMeta = SERVICE_META[opp.service_category] || {
                    icon: '🎯',
                    label: opp.service_category,
                    color: 'badge-info',
                  }
                  const pMeta = PRIORITY_META[opp.priority] || {
                    icon: '⚪',
                    label: opp.priority,
                    color: 'badge-neutral',
                  }

                  return (
                    <tr key={opp.id} className="hover:bg-surface-raised transition-colors">
                      <td>
                        <div className="font-medium text-white">
                          {opp.business_name}
                        </div>
                        <div className="text-xs text-text-muted flex items-center gap-2 mt-0.5">
                          {opp.business_country && (
                            <span className="badge badge-neutral text-2xs uppercase">
                              {opp.business_country}
                            </span>
                          )}
                          {opp.business_website ? (
                            <a
                              href={opp.business_website}
                              target="_blank"
                              rel="noreferrer"
                              className="text-primary hover:underline truncate max-w-[200px]"
                            >
                              {opp.business_website.replace(/^https?:\/\//, '')}
                            </a>
                          ) : (
                            <span className="text-accent-red">No Website</span>
                          )}
                        </div>
                      </td>

                      <td>
                        <span className={`badge ${sMeta.color} inline-flex items-center gap-1.5`}>
                          <span>{sMeta.icon}</span>
                          <span>{sMeta.label}</span>
                        </span>
                        <div className="text-xs text-text-muted line-clamp-1 mt-1 max-w-xs">
                          {opp.title}
                        </div>
                      </td>

                      <td className="w-36">
                        <div className="flex items-center justify-between text-xs font-semibold mb-1">
                          <span
                            className={
                              opp.score >= 80
                                ? 'text-accent-red font-bold'
                                : opp.score >= 65
                                ? 'text-accent-amber'
                                : 'text-primary'
                            }
                          >
                            {opp.score}/100
                          </span>
                        </div>
                        <div className="w-full bg-surface-overlay rounded-full h-1.5 overflow-hidden">
                          <div
                            className={`h-full rounded-full ${
                              opp.score >= 80
                                ? 'bg-accent-red'
                                : opp.score >= 65
                                ? 'bg-accent-amber'
                                : 'bg-primary'
                            }`}
                            style={{ width: `${Math.min(opp.score, 100)}%` }}
                          />
                        </div>
                      </td>

                      <td>
                        <span className={`badge ${pMeta.color} inline-flex items-center gap-1`}>
                          <span>{pMeta.icon}</span>
                          <span>{pMeta.label}</span>
                        </span>
                      </td>

                      <td>
                        <select
                          className="form-input text-xs py-1 px-2 w-28 bg-surface-overlay"
                          value={opp.status}
                          onChange={e => handleUpdateStatus(opp.id, e.target.value)}
                        >
                          <option value="IDENTIFIED">Identified</option>
                          <option value="EVALUATING">Evaluating</option>
                          <option value="QUALIFIED">Qualified</option>
                          <option value="DISQUALIFIED">Disqualified</option>
                          <option value="CONVERTED">Converted</option>
                        </select>
                      </td>

                      <td className="text-right">
                        <button
                          onClick={() => handleViewEvidence(opp)}
                          className="btn btn-secondary text-xs px-2.5 py-1"
                        >
                          Pitch & Evidence ↗
                        </button>
                      </td>
                    </tr>
                  )
                })}
              </tbody>
            </table>
          </div>
        )}

        {/* Pagination */}
        {pages > 1 && (
          <div className="flex items-center justify-between mt-4 pt-4 border-t border-border">
            <button
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
              className="btn btn-secondary text-xs"
            >
              Previous
            </button>
            <span className="text-xs text-text-muted">
              Page {page} of {pages}
            </span>
            <button
              onClick={() => setPage(p => Math.min(pages, p + 1))}
              disabled={page === pages}
              className="btn btn-secondary text-xs"
            >
              Next
            </button>
          </div>
        )}
      </div>

      {/* Intelligence & Pitch Evidence Modal */}
      {selectedOpp && (
        <div className="modal-backdrop" onClick={() => setSelectedOpp(null)}>
          <div
            className="modal-card max-w-2xl w-full p-6"
            onClick={e => e.stopPropagation()}
          >
            <div className="flex items-start justify-between border-b border-border pb-4 mb-4">
              <div>
                <span className="badge badge-purple text-2xs uppercase mb-1">
                  Sales Intelligence
                </span>
                <h3 className="text-lg font-bold text-white">
                  {selectedOpp.title}
                </h3>
                <p className="text-xs text-text-muted mt-0.5">
                  Business: <strong className="text-white">{selectedOpp.business_name}</strong>{' '}
                  ({selectedOpp.business_country || 'Global'})
                </p>
              </div>
              <button
                onClick={() => setSelectedOpp(null)}
                className="text-text-muted hover:text-white text-lg p-1"
              >
                ✕
              </button>
            </div>

            {/* Summary */}
            <div className="p-3 bg-surface-raised rounded-lg border border-border mb-4 text-xs text-text-muted leading-relaxed">
              <strong className="text-white block mb-1">Diagnosis:</strong>
              {selectedOpp.summary}
            </div>

            {/* Score Breakdown */}
            {selectedOpp.evidence?.score_breakdown && (
              <div className="mb-4">
                <h4 className="text-xs font-semibold text-text-muted uppercase tracking-wider mb-2">
                  Multi-Factor Score Composition ({selectedOpp.score}/100)
                </h4>
                <div className="grid grid-cols-4 gap-2 text-center text-xs">
                  <div className="p-2 bg-surface-overlay rounded border border-border">
                    <div className="text-text-muted text-2xs">Need Severity</div>
                    <div className="font-bold text-accent-red mt-0.5">
                      {selectedOpp.evidence.score_breakdown.need_severity}/40
                    </div>
                  </div>
                  <div className="p-2 bg-surface-overlay rounded border border-border">
                    <div className="text-text-muted text-2xs">Agency Fit</div>
                    <div className="font-bold text-primary mt-0.5">
                      {selectedOpp.evidence.score_breakdown.service_fit}/25
                    </div>
                  </div>
                  <div className="p-2 bg-surface-overlay rounded border border-border">
                    <div className="text-text-muted text-2xs">Category Tier</div>
                    <div className="font-bold text-accent-amber mt-0.5">
                      {selectedOpp.evidence.score_breakdown.market_viability}/20
                    </div>
                  </div>
                  <div className="p-2 bg-surface-overlay rounded border border-border">
                    <div className="text-text-muted text-2xs">Reachability</div>
                    <div className="font-bold text-accent-green mt-0.5">
                      {selectedOpp.evidence.score_breakdown.contactability}/15
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Pitch Angles */}
            {selectedOpp.pitch_angles?.angles && (
              <div className="mb-4">
                <h4 className="text-xs font-semibold text-text-muted uppercase tracking-wider mb-2">
                  Agency Talking Points & Value Proposition
                </h4>
                <ul className="space-y-1.5 text-xs text-text">
                  {selectedOpp.pitch_angles.angles.map((angle, idx) => (
                    <li key={idx} className="flex items-start gap-2">
                      <span className="text-primary font-bold">✓</span>
                      <span>{angle}</span>
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Technical Audit Findings if available */}
            {auditDetails && (
              <div className="mb-4 pt-3 border-t border-border">
                <h4 className="text-xs font-semibold text-text-muted uppercase tracking-wider mb-2">
                  Technical Audit Metrics
                </h4>
                <div className="grid grid-cols-3 gap-2 text-xs">
                  <div className="p-2 bg-surface-overlay rounded">
                    <span className="text-text-muted text-2xs block">Mobile Viewport</span>
                    <span className={auditDetails.is_mobile_responsive ? 'text-accent-green' : 'text-accent-red font-bold'}>
                      {auditDetails.is_mobile_responsive ? '✅ Responsive' : '❌ Non-Responsive'}
                    </span>
                  </div>
                  <div className="p-2 bg-surface-overlay rounded">
                    <span className="text-text-muted text-2xs block">SSL Security</span>
                    <span className={auditDetails.has_ssl ? 'text-accent-green' : 'text-accent-red font-bold'}>
                      {auditDetails.has_ssl ? '✅ HTTPS' : '❌ Insecure HTTP'}
                    </span>
                  </div>
                  <div className="p-2 bg-surface-overlay rounded">
                    <span className="text-text-muted text-2xs block">CMS / Platform</span>
                    <span className="text-white font-medium">
                      {auditDetails.detected_cms || 'Custom/Unknown'}
                    </span>
                  </div>
                  <div className="p-2 bg-surface-overlay rounded">
                    <span className="text-text-muted text-2xs block">E-Commerce</span>
                    <span>{auditDetails.has_ecommerce ? '✅ Present' : '❌ None'}</span>
                  </div>
                  <div className="p-2 bg-surface-overlay rounded">
                    <span className="text-text-muted text-2xs block">Online Booking</span>
                    <span>{auditDetails.has_online_booking ? '✅ Present' : '❌ None'}</span>
                  </div>
                  <div className="p-2 bg-surface-overlay rounded">
                    <span className="text-text-muted text-2xs block">Page Load</span>
                    <span>{auditDetails.load_time_seconds ? `${auditDetails.load_time_seconds}s` : 'N/A'}</span>
                  </div>
                </div>
              </div>
            )}

            <div className="flex items-center justify-between pt-4 border-t border-border mt-6">
              <div className="flex items-center gap-2">
                <span className="text-xs text-text-muted">Set Stage:</span>
                <button
                  onClick={() => handleUpdateStatus(selectedOpp.id, 'QUALIFIED')}
                  className={`btn text-xs py-1 px-3 ${
                    selectedOpp.status === 'QUALIFIED' ? 'btn-primary' : 'btn-secondary'
                  }`}
                >
                  Mark Qualified
                </button>
                <button
                  onClick={() => handleUpdateStatus(selectedOpp.id, 'DISQUALIFIED')}
                  className={`btn text-xs py-1 px-3 ${
                    selectedOpp.status === 'DISQUALIFIED' ? 'btn-danger' : 'btn-secondary'
                  }`}
                >
                  Disqualify
                </button>
              </div>
              <button
                onClick={() => setSelectedOpp(null)}
                className="btn btn-secondary text-xs"
              >
                Close
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  )
}
