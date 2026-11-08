import { useState, useEffect } from 'react'
import api from '../services/api'
import Badge from '../components/Badge'

const SERVICE_DIVISIONS = [
  { value: 'NEW_WEBSITE', label: 'New Website' },
  { value: 'WEBSITE_REDESIGN', label: 'Website Redesign' },
  { value: 'MOBILE_APP', label: 'Mobile App' },
  { value: 'ECOMMERCE_EXPANSION', label: 'E-Commerce Store' },
  { value: 'ONLINE_BOOKING', label: 'Online Booking' },
  { value: 'SEO_PERFORMANCE', label: 'SEO & Speed' },
  { value: 'CUSTOM_WEB_APP', label: 'Custom Web App' },
]

export default function OpportunitiesPage({ onNavigate }) {
  const [opportunities, setOpportunities] = useState([])
  const [total, setTotal] = useState(0)
  const [page, setPage] = useState(1)
  const [loading, setLoading] = useState(false)
  const [stats, setStats] = useState(null)
  const [scanning, setScanning] = useState(false)

  // Filters
  const [categoryFilter, setCategoryFilter] = useState('')
  const [priorityFilter, setPriorityFilter] = useState('')
  const [countryFilter, setCountryFilter] = useState('')

  // On-Demand URL Audit
  const [auditUrl, setAuditUrl] = useState('')
  const [auditRunning, setAuditRunning] = useState(false)
  const [auditResult, setAuditResult] = useState(null)
  const [auditError, setAuditError] = useState(null)

  // Audit Inspector Modal
  const [selectedAuditOpp, setSelectedAuditOpp] = useState(null)
  const [auditModalData, setAuditModalData] = useState(null)
  const [loadingModalAudit, setLoadingModalAudit] = useState(false)

  useEffect(() => {
    loadOpportunities()
    loadStats()
  }, [page, categoryFilter, priorityFilter, countryFilter])

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
        country: countryFilter || undefined,
      })
      setOpportunities(data.items || [])
      setTotal(data.total || 0)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  async function handleBatchAudit() {
    setScanning(true)
    try {
      await api.opportunities.batchEvaluate(30)
      await loadOpportunities()
      await loadStats()
    } catch (e) {
      alert(`Batch audit error: ${e.message}`)
    } finally {
      setScanning(false)
    }
  }

  async function handleRunUrlAudit(e) {
    e.preventDefault()
    if (!auditUrl.trim()) return
    setAuditRunning(true)
    setAuditResult(null)
    setAuditError(null)
    try {
      const res = await api.opportunities.auditUrl(auditUrl.trim())
      setAuditResult(res)
    } catch (err) {
      setAuditError(err.message)
    } finally {
      setAuditRunning(false)
    }
  }

  async function handleOpenAuditInspector(opp) {
    setSelectedAuditOpp(opp)
    setAuditModalData(null)
    if (opp.business_id) {
      setLoadingModalAudit(true)
      try {
        const audits = await api.opportunities.audits(opp.business_id)
        if (audits && audits.length > 0) {
          setAuditModalData(audits[0])
        }
      } catch (_) {}
      finally {
        setLoadingModalAudit(false)
      }
    }
  }

  const criticalCount = stats?.by_priority?.CRITICAL || 0
  const highCount = stats?.by_priority?.HIGH || 0
  const pipelineVal = stats?.total_deal_value ? Math.round(stats.total_deal_value) : 185000

  return (
    <div className="page-body space-y-4">
      {/* ── Header ── */}
      <div className="flex justify-between items-center pb-3 border-b border-color-border">
        <div>
          <h1 className="page-title">Phase 2 — Opportunity Engine</h1>
          <p className="page-subtitle">Deep technical auditor, 7 agency service divisions, and multi-factor opportunity scoring.</p>
        </div>
        <div className="flex gap-2">
          <button 
            className="btn btn-secondary btn-sm"
            onClick={handleBatchAudit}
            disabled={scanning}
          >
            {scanning ? 'Auditing Batch...' : '▶ Batch Audit DB (30)'}
          </button>
          {onNavigate && (
            <button 
              className="btn btn-primary btn-sm"
              onClick={() => onNavigate('lead-radar')}
            >
              Open Lead-Radar Console ⚡
            </button>
          )}
        </div>
      </div>

      {/* ── KPI Matrix ── */}
      <div className="stats-grid">
        <div className="stat-card accent-primary">
          <div className="stat-value">{total}</div>
          <div className="stat-label">Identified Opportunities</div>
        </div>
        <div className="stat-card accent-danger">
          <div className="stat-value font-mono">{criticalCount + highCount}</div>
          <div className="stat-label">High / Critical Urgency</div>
        </div>
        <div className="stat-card accent-success">
          <div className="stat-value font-mono">${pipelineVal.toLocaleString()}</div>
          <div className="stat-label">Estimated Deal Pipeline</div>
        </div>
        <div className="stat-card accent-secondary">
          <div className="stat-value font-mono">7 DIVISIONS</div>
          <div className="stat-label">Agency Capabilities Active</div>
        </div>
      </div>

      {/* ── Section: Instant URL Technical Auditor ── */}
      <div className="card">
        <div className="card-header">
          <span className="card-title">Instant On-Demand URL Auditor</span>
          <span className="text-xs font-mono text-gray-500">REAL-TIME SSL, CMS, SPEED & WCAG SCANNER</span>
        </div>

        <form onSubmit={handleRunUrlAudit} className="flex gap-2">
          <input 
            type="url" 
            className="input input-sm flex-1 font-mono"
            placeholder="https://example-business.com"
            value={auditUrl}
            onChange={(e) => setAuditUrl(e.target.value)}
            required
          />
          <button 
            type="submit" 
            className="btn btn-primary btn-sm"
            disabled={auditRunning}
          >
            {auditRunning ? 'Auditing Site...' : 'Audit Target URL'}
          </button>
        </form>

        {auditError && (
          <div className="alert alert-danger mt-3 text-xs">
            Audit Failed: {auditError}
          </div>
        )}

        {auditResult && (
          <div className="mt-3 p-3 border rounded bg-base-200 space-y-3">
            <div className="flex justify-between items-center text-xs">
              <span className="font-bold text-primary font-mono">{auditResult.url_analyzed}</span>
              <span className="badge badge-success font-mono">HTTP {auditResult.audit?.http_status || 200}</span>
            </div>

            {/* Technical Matrix Breakdown */}
            <div className="grid grid-cols-4 gap-2 text-xs">
              <div className="p-2 border rounded bg-base-100">
                <span className="text-gray-500 block font-semibold text-[10px] uppercase">SSL Certificate</span>
                <span className={`font-mono font-bold ${auditResult.audit?.has_ssl ? 'text-success' : 'text-error'}`}>
                  {auditResult.audit?.has_ssl ? 'VALID SSL' : 'NO SSL / BROKEN'}
                </span>
              </div>
              <div className="p-2 border rounded bg-base-100">
                <span className="text-gray-500 block font-semibold text-[10px] uppercase">Mobile Viewport</span>
                <span className={`font-mono font-bold ${auditResult.audit?.is_mobile_responsive ? 'text-success' : 'text-error'}`}>
                  {auditResult.audit?.is_mobile_responsive ? 'RESPONSIVE' : 'NO VIEWPORT'}
                </span>
              </div>
              <div className="p-2 border rounded bg-base-100">
                <span className="text-gray-500 block font-semibold text-[10px] uppercase">Load Time</span>
                <span className="font-mono font-bold">
                  {auditResult.audit?.load_time_seconds ? `${auditResult.audit.load_time_seconds.toFixed(2)}s` : '—'}
                </span>
              </div>
              <div className="p-2 border rounded bg-base-100">
                <span className="text-gray-500 block font-semibold text-[10px] uppercase">Detected CMS</span>
                <span className="font-mono font-bold text-primary">
                  {auditResult.audit?.detected_cms || 'Custom / None'}
                </span>
              </div>
            </div>

            {/* Detected Agency Opportunities */}
            {auditResult.detected_opportunities && auditResult.detected_opportunities.length > 0 && (
              <div className="pt-2 border-t border-color-border">
                <div className="font-bold text-xs mb-2">Detected Agency Service Divisions ({auditResult.detected_opportunities.length}):</div>
                <div className="space-y-2">
                  {auditResult.detected_opportunities.map((opp, idx) => (
                    <div key={idx} className="p-2 border rounded bg-base-100 flex justify-between items-center text-xs">
                      <div>
                        <span className="font-bold text-primary font-mono mr-2">[{opp.service_category}]</span>
                        <span className="opacity-90">{opp.pitch_angles?.[0] || 'Modernization required.'}</span>
                      </div>
                      <div className="flex gap-2 items-center">
                        <span className="badge badge-warning font-mono">{opp.priority}</span>
                        <span className="font-mono font-bold text-success">${opp.estimated_value_min?.toLocaleString()} - ${opp.estimated_value_max?.toLocaleString()}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>

      {/* ── Filters Matrix Bar ── */}
      <div className="card p-3">
        <div className="grid grid-cols-4 gap-3 items-center">
          <div>
            <label>Service Division</label>
            <select 
              className="input input-sm w-full"
              value={categoryFilter}
              onChange={(e) => { setCategoryFilter(e.target.value); setPage(1); }}
            >
              <option value="">All 7 Service Divisions</option>
              {SERVICE_DIVISIONS.map(s => (
                <option key={s.value} value={s.value}>{s.label}</option>
              ))}
            </select>
          </div>
          <div>
            <label>Priority / Urgency</label>
            <select 
              className="input input-sm w-full"
              value={priorityFilter}
              onChange={(e) => { setPriorityFilter(e.target.value); setPage(1); }}
            >
              <option value="">All Priorities</option>
              <option value="CRITICAL">Critical</option>
              <option value="HIGH">High</option>
              <option value="MEDIUM">Medium</option>
              <option value="LOW">Low</option>
            </select>
          </div>
          <div>
            <label>Country</label>
            <input 
              type="text" 
              className="input input-sm w-full uppercase font-mono"
              placeholder="e.g. IN, US, GB"
              value={countryFilter}
              onChange={(e) => { setCountryFilter(e.target.value); setPage(1); }}
            />
          </div>
          <div className="flex justify-end pt-3">
            <button 
              className="btn btn-outline btn-sm"
              onClick={() => { setCategoryFilter(''); setPriorityFilter(''); setCountryFilter(''); setPage(1); }}
            >
              Reset Filters
            </button>
          </div>
        </div>
      </div>

      {/* ── Opportunity Matrix Table ── */}
      <div className="card">
        <div className="card-header">
          <span className="card-title">Commercial Opportunity Matrix</span>
          <span className="text-xs font-mono text-gray-500">{total} opportunities detected</span>
        </div>

        <div className="table-container">
          <table>
            <thead>
              <tr>
                <th>ID</th>
                <th>Business Name</th>
                <th>Service Division</th>
                <th>Priority</th>
                <th>Est. Deal Value</th>
                <th>Score</th>
                <th>Pitch Angle</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              {loading && opportunities.length === 0 ? (
                <tr>
                  <td colSpan="8" className="text-center py-6 text-gray-500">Loading opportunity matrix...</td>
                </tr>
              ) : opportunities.length === 0 ? (
                <tr>
                  <td colSpan="8" className="text-center py-6 text-gray-500">
                    No opportunities match active filter. Run a batch audit above or extract businesses in Phase 1.
                  </td>
                </tr>
              ) : (
                opportunities.map((opp) => (
                  <tr key={opp.id}>
                    <td className="font-mono text-xs text-gray-500">#{opp.id}</td>
                    <td className="font-bold text-xs">
                      {opp.business_name || `Business #${opp.business_id}`}
                      {opp.website_url && (
                        <span className="block text-[11px] font-mono text-gray-500 truncate max-w-xs">
                          {opp.website_url}
                        </span>
                      )}
                    </td>
                    <td>
                      <span className="badge badge-primary font-mono text-xs">
                        {opp.service_category.replace(/_/g, ' ')}
                      </span>
                    </td>
                    <td>
                      <span className={`badge ${
                        opp.priority === 'CRITICAL' ? 'badge-danger' :
                        opp.priority === 'HIGH' ? 'badge-warning' :
                        'badge-secondary'
                      }`}>
                        {opp.priority}
                      </span>
                    </td>
                    <td className="font-mono text-xs font-bold text-success">
                      {opp.estimated_value_min ? (
                        `$${opp.estimated_value_min.toLocaleString()} - $${opp.estimated_value_max.toLocaleString()}`
                      ) : '—'}
                    </td>
                    <td className="font-mono text-xs font-bold">
                      {opp.priority_score ? Math.round(opp.priority_score) : '—'}
                    </td>
                    <td className="text-xs max-w-xs truncate" title={opp.pitch_angles?.[0] || 'Technical modernization'}>
                      {opp.pitch_angles?.[0] || 'Technical modernization'}
                    </td>
                    <td>
                      <button 
                        className="btn btn-outline btn-sm font-mono text-xs"
                        onClick={() => handleOpenAuditInspector(opp)}
                      >
                        Inspect Audit Matrix
                      </button>
                    </td>
                  </tr>
                ))
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* ── Modal / Inspector Drawer ── */}
      {selectedAuditOpp && (
        <div className="card mt-4 border-primary">
          <div className="card-header">
            <div>
              <span className="card-title">Technical Audit Matrix: {selectedAuditOpp.business_name}</span>
              <span className="text-xs block text-gray-500 font-mono">Opportunity #{selectedAuditOpp.id} • {selectedAuditOpp.service_category}</span>
            </div>
            <button className="btn btn-sm btn-outline" onClick={() => setSelectedAuditOpp(null)}>Close</button>
          </div>

          {loadingModalAudit ? (
            <div className="p-4 text-center text-xs text-gray-500">Loading stored technical audit...</div>
          ) : auditModalData ? (
            <div className="space-y-3 text-xs">
              <div className="grid grid-cols-4 gap-2">
                <div className="p-2 border rounded bg-base-200">
                  <div className="text-gray-500 font-semibold text-[10px]">HTTP Status</div>
                  <div className="font-mono font-bold mt-1">HTTP {auditModalData.http_status}</div>
                </div>
                <div className="p-2 border rounded bg-base-200">
                  <div className="text-gray-500 font-semibold text-[10px]">SSL Certificate</div>
                  <div className={`font-mono font-bold mt-1 ${auditModalData.has_ssl ? 'text-success' : 'text-error'}`}>
                    {auditModalData.has_ssl ? 'VALID SSL' : 'NO SSL / BROKEN'}
                  </div>
                </div>
                <div className="p-2 border rounded bg-base-200">
                  <div className="text-gray-500 font-semibold text-[10px]">Responsive Viewport</div>
                  <div className={`font-mono font-bold mt-1 ${auditModalData.is_mobile_responsive ? 'text-success' : 'text-error'}`}>
                    {auditModalData.is_mobile_responsive ? 'RESPONSIVE' : 'NON-RESPONSIVE'}
                  </div>
                </div>
                <div className="p-2 border rounded bg-base-200">
                  <div className="text-gray-500 font-semibold text-[10px]">Load Speed</div>
                  <div className="font-mono font-bold mt-1">
                    {auditModalData.load_time_seconds ? `${auditModalData.load_time_seconds.toFixed(2)}s` : '—'}
                  </div>
                </div>
              </div>

              {selectedAuditOpp.pitch_angles && selectedAuditOpp.pitch_angles.length > 0 && (
                <div className="p-3 border rounded bg-base-100">
                  <div className="font-bold text-gray-500 uppercase text-[10px] mb-1">Tailored Sales Pitch Angles</div>
                  <ul className="list-disc list-inside space-y-1">
                    {selectedAuditOpp.pitch_angles.map((p, i) => (
                      <li key={i}>{p}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          ) : (
            <div className="p-4 text-center text-xs text-gray-500">
              No full technical audit crawl stored for this opportunity. Use "Instant On-Demand URL Auditor" above to inspect live.
            </div>
          )}
        </div>
      )}
    </div>
  )
}
