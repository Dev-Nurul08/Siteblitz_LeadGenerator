/**
 * Sidebar navigation component
 */

const NAV_ITEMS = [
  {
    section: 'Overview',
    items: [
      { id: 'dashboard', label: 'Dashboard', icon: '📊' },
      { id: 'lead-radar', label: 'Lead Radar ⚡', icon: '📡', badge: 'STRATEGY' },
    ]
  },
  {
    section: 'Discovery Engine',
    items: [
      { id: 'discovery', label: 'Run Discovery', icon: '🔍' },
      { id: 'sources', label: 'Data Sources', icon: '🗄️' },
      { id: 'businesses', label: 'Businesses', icon: '🏢' },
    ]
  },
  {
    section: 'Opportunity Engine',
    items: [
      { id: 'opportunities', label: 'Opportunities', icon: '🎯' },
    ]
  },
  {
    section: 'Enrichment Engine',
    items: [
      { id: 'contacts', label: 'Contacts', icon: '👤' },
    ]
  },
  {
    section: 'Qualification Engine',
    items: [
      { id: 'compliance', label: 'Compliance & Leads', icon: '🛡️' },
    ]
  },
  {
    section: 'Conversion Engine',
    items: [
      { id: 'campaigns', label: 'Campaigns & CRM', icon: '📧', badge: 'ACTIVE' },
    ]
  }
]

export default function Sidebar({ currentPage, onNavigate }) {
  return (
    <aside className="sidebar">
      <div className="sidebar-header">
        <div className="sidebar-logo">SB</div>
        <div>
          <div className="sidebar-title">SiteBlitz</div>
          <div className="sidebar-subtitle">Lead Intelligence OS</div>
        </div>
      </div>

      <nav className="sidebar-nav">
        {NAV_ITEMS.map(({ section, items }) => (
          <div key={section} className="nav-section">
            <div className="nav-section-title">{section}</div>
            {items.map(item => (
              <button
                key={item.id}
                className={`nav-item ${currentPage === item.id ? 'active' : ''} ${item.locked ? 'locked' : ''}`}
                onClick={() => !item.locked && onNavigate(item.id)}
                title={item.locked ? 'Available after Phase 1 gate' : item.label}
                style={{ opacity: item.locked ? 0.4 : 1, cursor: item.locked ? 'not-allowed' : 'pointer' }}
              >
                <span style={{ fontSize: '1rem' }}>{item.icon}</span>
                <span>{item.label}</span>
                {item.badge && (
                  <span className="nav-badge">{item.badge}</span>
                )}
                {item.locked && (
                  <span style={{ marginLeft: 'auto', fontSize: '0.7rem', opacity: 0.5 }}>🔒</span>
                )}
              </button>
            ))}
          </div>
        ))}
      </nav>

      {/* Phase progress */}
      <div className="phase-indicator">
        <div className="phase-dot active" title="Phase 1 — Active" />
        <div className="phase-connector" />
        <div className="phase-dot pending" title="Phase 2 — Pending" />
        <div className="phase-connector" />
        <div className="phase-dot locked" title="Phase 3 — Locked" />
        <div className="phase-connector" />
        <div className="phase-dot locked" title="Phase 4 — Locked" />
        <div className="phase-connector" />
        <div className="phase-dot locked" title="Phase 5 — Locked" />
      </div>

      <div style={{ padding: '12px 16px', borderTop: '1px solid var(--color-border)' }}>
        <div style={{ fontSize: '0.7rem', color: 'var(--color-text-muted)', marginBottom: '4px' }}>
          CURRENT PHASE
        </div>
        <div style={{ fontSize: '0.8rem', color: 'var(--color-accent-success)', fontWeight: 600 }}>
          ● Phase 1 — Discovery
        </div>
        <div style={{ fontSize: '0.7rem', color: 'var(--color-text-muted)', marginTop: '2px' }}>
          Build & test before Phase 2
        </div>
      </div>
    </aside>
  )
}
