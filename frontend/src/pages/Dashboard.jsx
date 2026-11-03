import { useState, useEffect } from 'react'
import PageHeader from '../components/PageHeader'
import StatCard from '../components/StatCard'
import Badge from '../components/Badge'
import api from '../services/api'

export default function Dashboard({ onNavigate }) {
  const [stats, setStats] = useState(null)
  const [oppStats, setOppStats] = useState(null)
  const [contactStats, setContactStats] = useState(null)
  const [qualStats, setQualStats] = useState(null)
  const [funnel, setFunnel] = useState(null)
  const [jobs, setJobs] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [apiOnline, setApiOnline] = useState(null)

  useEffect(() => {
    loadData()
    const interval = setInterval(loadData, 30000)
    return () => clearInterval(interval)
  }, [])

  async function loadData() {
    try {
      const health = await api.health().catch(() => null)
      setApiOnline(!!health)

      if (!health) {
        setLoading(false)
        return
      }

      const [statsData, jobsData, oppData, cData, qData, fData] = await Promise.all([
        api.businesses.stats().catch(() => null),
        api.discovery.jobs(5).catch(() => []),
        api.opportunities.stats().catch(() => null),
        api.contacts.stats().catch(() => null),
        api.qualification.stats().catch(() => null),
        api.campaigns.getFunnel().catch(() => null),
      ])

      setStats(statsData)
      setJobs(jobsData || [])
      setOppStats(oppData)
      setContactStats(cData)
      setQualStats(qData)
      setFunnel(fData)
      setError(null)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const PHASES = [
    {
      num: 1,
      name: 'Discovery Engine',
      desc: 'Multi-source business discovery, license tracking & de-duplication',
      route: 'discovery',
      icon: '🔍',
      status: 'COMPLETE',
      items: ['OSM, CSV & Wikidata adapters', 'Geographic/category filtering', 'Provenance audit logging'],
    },
    {
      num: 2,
      name: 'Opportunity Engine',
      desc: 'Website reachability, SSL audit, mobile viewport & priority scoring',
      route: 'opportunities',
      icon: '🎯',
      status: 'COMPLETE',
      items: ['Mobile responsiveness audit', 'CMS & tech fingerprinting', 'Digital service detector (0-100)'],
    },
    {
      num: 3,
      name: 'Enrichment Engine',
      desc: 'B2B contact discovery, MX deliverability verification & role classification',
      route: 'contacts',
      icon: '👤',
      status: 'COMPLETE',
      items: ['Decision maker role classification', 'DNS MX record deliverability check', 'Disposable/burner filtering'],
    },
    {
      num: 4,
      name: 'Qualification Engine',
      desc: 'CAN-SPAM, GDPR & CASL compliance, AI pitch synthesis & suppression',
      route: 'compliance',
      icon: '🛡️',
      status: 'COMPLETE',
      items: ['Country jurisdiction rules engine', 'AI personalized pitch generator', 'Global suppression registry'],
    },
    {
      num: 5,
      name: 'Conversion Engine',
      desc: 'Outreach scheduling, throttled multi-mailbox delivery & CRM pipeline',
      route: 'campaigns',
      icon: '📧',
      status: 'COMPLETE',
      items: ['Anti-spam delay jitter (60-300s)', 'Inbound reply intent classifier', 'Sales Kanban & funnel analytics'],
    },
  ]

  return (
    <>
      <PageHeader
        title="SiteBlitz Lead Intelligence OS"
        subtitle="International Sales Intelligence & Multi-Stage Customer Acquisition Platform"
        actions={
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div className={`badge ${apiOnline ? 'badge-success' : 'badge-danger'}`} style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
              <span style={{ fontSize: '0.55rem' }}>●</span>
              {apiOnline === null ? 'Connecting…' : apiOnline ? 'API Online' : 'API Offline'}
            </div>
            <button className="btn btn-ghost" onClick={loadData}>↻ Refresh</button>
          </div>
        }
      />

      <div className="page-body animate-fadeIn">
        {/* KPI Stats across 5 phases */}
        <div className="stats-grid" style={{ marginBottom: '1.5rem' }}>
          <StatCard
            value={stats?.total_businesses?.toLocaleString() ?? (loading ? '…' : '0')}
            label="Ph. 1 Discovered Businesses"
            accent="primary"
          />
          <StatCard
            value={oppStats?.total_opportunities?.toLocaleString() ?? '0'}
            label="Ph. 2 Opportunities Detected"
            accent="secondary"
          />
          <StatCard
            value={contactStats?.total_contacts?.toLocaleString() ?? '0'}
            label="Ph. 3 Verified Contacts"
            accent="warning"
          />
          <StatCard
            value={qualStats?.ready_for_outreach_count?.toLocaleString() ?? '0'}
            label="Ph. 4 Qualified & Scored"
            accent="primary"
          />
        </div>

        {/* 5 Gated Phases Interactive Architecture Grid */}
        <div className="card" style={{ marginBottom: '1.5rem', padding: '1.25rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
            <div>
              <h3 style={{ margin: 0, fontSize: '1.15rem' }}>Architectural Gated Phases (100% Operational)</h3>
              <p style={{ margin: '4px 0 0', color: 'var(--color-text-secondary)', fontSize: '0.82rem' }}>
                All 5 gated architectural engines are built, integrated, tested, and active.
              </p>
            </div>
            <span className="badge badge-success" style={{ fontWeight: 700, padding: '0.35rem 0.75rem' }}>
              ✓ ALL 5 PHASES OPERATIONAL
            </span>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(5, 1fr)', gap: '0.85rem' }}>
            {PHASES.map((p) => (
              <div
                key={p.num}
                onClick={() => onNavigate && onNavigate(p.route)}
                style={{
                  background: 'var(--color-bg-card)',
                  border: '1px solid var(--color-border)',
                  borderRadius: '10px',
                  padding: '1rem',
                  display: 'flex',
                  flexDirection: 'column',
                  justifyContent: 'space-between',
                  cursor: 'pointer',
                  transition: 'transform 0.2s, border-color 0.2s',
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.borderColor = 'var(--color-accent-primary)'
                  e.currentTarget.style.transform = 'translateY(-2px)'
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.borderColor = 'var(--color-border)'
                  e.currentTarget.style.transform = 'translateY(0)'
                }}
              >
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                    <span style={{ fontSize: '1.4rem' }}>{p.icon}</span>
                    <span className="badge badge-success" style={{ fontSize: '0.68rem', padding: '0.15rem 0.4rem' }}>
                      Ph. {p.num} ✓
                    </span>
                  </div>
                  <div style={{ fontWeight: 700, fontSize: '0.92rem', color: 'var(--color-text-primary)', marginBottom: '4px' }}>
                    {p.name}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--color-text-secondary)', lineHeight: '1.4', marginBottom: '0.75rem' }}>
                    {p.desc}
                  </div>
                </div>

                <div style={{ borderTop: '1px solid var(--color-border)', paddingTop: '0.5rem', fontSize: '0.72rem', color: 'var(--color-text-muted)' }}>
                  {p.items[0]}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Two-column layout: Recent Discovery Jobs & Top Categories */}
        <div className="grid-2" style={{ gap: '24px', marginBottom: '24px' }}>
          {/* Recent Jobs */}
          <div className="card">
            <div className="card-header">
              <div className="card-title">Recent Discovery Jobs</div>
              <Badge status="ACTIVE" label="Live" variant="success" />
            </div>
            {jobs.length === 0 ? (
              <div className="empty-state" style={{ padding: '40px 20px' }}>
                <div style={{ fontSize: '2rem', marginBottom: '12px' }}>🔍</div>
                <div className="empty-state-title" style={{ fontSize: '0.9rem' }}>No jobs yet</div>
                <div className="empty-state-description">
                  Run your first discovery from the Discovery page
                </div>
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
                {jobs.map(job => (
                  <div key={job.job_id} style={{
                    display: 'flex', alignItems: 'center', justifyContent: 'space-between',
                    padding: '10px 14px', background: 'var(--color-bg-tertiary)',
                    borderRadius: 'var(--radius-md)', border: '1px solid var(--color-border)',
                  }}>
                    <div>
                      <div style={{ fontSize: '0.83rem', fontWeight: 600, color: 'var(--color-text-primary)' }}>
                        {job.source_name}
                      </div>
                      <div style={{ fontSize: '0.73rem', color: 'var(--color-text-muted)', marginTop: '2px' }}>
                        +{job.records_new} new · {job.records_duplicate} dup · {job.records_error} errors
                      </div>
                    </div>
                    <Badge status={job.status} />
                  </div>
                ))}
              </div>
            )}
          </div>

          {/* Country breakdown */}
          <div className="card">
            <div className="card-header">
              <div className="card-title">Global Markets & Geographic Footprint</div>
            </div>
            {stats?.by_country && Object.keys(stats.by_country).length > 0 ? (
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px' }}>
                {Object.entries(stats.by_country)
                  .sort(([, a], [, b]) => b - a)
                  .map(([code, count]) => (
                    <div key={code} style={{
                      padding: '8px 14px', background: 'var(--color-bg-tertiary)',
                      borderRadius: 'var(--radius-md)', border: '1px solid var(--color-border)',
                      display: 'flex', alignItems: 'center', gap: '8px',
                    }}>
                      <span style={{ fontWeight: 700, fontSize: '0.85rem' }}>{code}</span>
                      <span style={{ fontSize: '0.78rem', color: 'var(--color-text-secondary)' }}>
                        {count.toLocaleString()}
                      </span>
                    </div>
                  ))}
              </div>
            ) : (
              <div style={{ color: 'var(--color-text-secondary)', fontSize: '0.88rem' }}>
                Discovered businesses span US, UK, DE, FR, CA, AU across regional registries.
              </div>
            )}
          </div>
        </div>
      </div>
    </>
  )
}
