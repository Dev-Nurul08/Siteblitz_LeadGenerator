import { useState, useEffect } from 'react'
import PageHeader from '../components/PageHeader'
import Badge from '../components/Badge'
import api from '../services/api'

const LICENSE_INFO = {
  OPEN_LICENSE: { icon: '✅', label: 'Open License', description: 'Freely reusable with attribution (e.g., ODbL)' },
  LICENSED_COMMERCIAL: { icon: '💼', label: 'Commercial License', description: 'Reusable under paid/commercial agreement' },
  API_RESTRICTED: { icon: '⚠️', label: 'API Restricted', description: 'Limited storage — cannot be cached permanently' },
  MANUAL_OR_OPT_IN: { icon: '📝', label: 'Manual / Opt-in', description: 'User-submitted or consent-based data' },
}

export default function SourcesPage() {
  const [sources, setSources] = useState([])
  const [loading, setLoading] = useState(true)
  const [showCreate, setShowCreate] = useState(false)

  useEffect(() => {
    loadSources()
  }, [])

  async function loadSources() {
    setLoading(true)
    try {
      const data = await api.sources.list()
      setSources(data || [])
    } catch {
      // API offline
    } finally {
      setLoading(false)
    }
  }

  // Pre-defined adapters for quick setup
  const BUILT_IN_ADAPTERS = [
    {
      name: 'OpenStreetMap',
      slug: 'openstreetmap',
      license_type: 'OPEN_LICENSE',
      adapter_class: 'backend.app.engines.discovery.osm.OSMAdapter',
      license_url: 'https://www.openstreetmap.org/copyright',
      attribution_required: true,
      attribution_text: '© OpenStreetMap contributors',
      allows_commercial_storage: true,
      allows_contact_enrichment: true,
      allows_marketing_use: false,
      rate_limit_rpm: 10,
    },
    {
      name: 'CSV / XLSX Import',
      slug: 'csv_import',
      license_type: 'MANUAL_OR_OPT_IN',
      adapter_class: 'backend.app.engines.discovery.csv_import.CSVImportAdapter',
      attribution_required: false,
      allows_commercial_storage: true,
      allows_contact_enrichment: true,
      allows_marketing_use: true,
      rate_limit_rpm: 1000,
    },
  ]

  async function registerAdapter(adapter) {
    try {
      await api.sources.create(adapter)
      await loadSources()
    } catch (e) {
      alert(e.message)
    }
  }

  const existingSlugs = sources.map(s => s.slug)

  return (
    <>
      <PageHeader
        title="Data Sources"
        subtitle="Manage source adapters, licenses, and permissions"
        actions={
          <div className="flex gap-3">
            <button className="btn btn-ghost btn-sm" onClick={loadSources}>↻ Refresh</button>
          </div>
        }
      />

      <div className="page-body animate-fadeIn">

        {/* Source Classification Reference */}
        <div className="card" style={{ marginBottom: '24px' }}>
          <div className="card-header">
            <div className="card-title">Source Classifications</div>
            <div className="card-description">Every data source must have a documented reuse classification before data enters the database</div>
          </div>
          <div className="grid-4" style={{ gap: '12px' }}>
            {Object.entries(LICENSE_INFO).map(([key, info]) => (
              <div key={key} style={{
                padding: '14px', background: 'var(--color-bg-tertiary)',
                borderRadius: 'var(--radius-md)', border: '1px solid var(--color-border)',
              }}>
                <div style={{ fontSize: '1.2rem', marginBottom: '6px' }}>{info.icon}</div>
                <div style={{ fontWeight: 600, fontSize: '0.82rem', marginBottom: '4px' }}>{info.label}</div>
                <div style={{ fontSize: '0.72rem', color: 'var(--color-text-muted)' }}>{info.description}</div>
                <div style={{ marginTop: '8px' }}>
                  <Badge status={key} />
                </div>
              </div>
            ))}
          </div>
          <div style={{ marginTop: '16px', padding: '10px 14px', background: 'rgba(239, 68, 68, 0.07)', borderRadius: 'var(--radius-md)', fontSize: '0.78rem', color: 'var(--color-text-secondary)' }}>
            ⚠️ <strong>Important:</strong> API_RESTRICTED sources cannot be stored permanently. A source permitting viewing is not the same as permitting commercial reuse. Google Places is not a permanent database foundation.
          </div>
        </div>

        {/* Built-in Adapters */}
        <div className="card" style={{ marginBottom: '24px' }}>
          <div className="card-header">
            <div className="card-title">Built-in Source Adapters</div>
          </div>
          <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
            {BUILT_IN_ADAPTERS.map(adapter => {
              const alreadyRegistered = existingSlugs.includes(adapter.slug)
              const info = LICENSE_INFO[adapter.license_type]
              return (
                <div key={adapter.slug} style={{
                  display: 'flex', alignItems: 'center', gap: '16px',
                  padding: '16px', background: 'var(--color-bg-tertiary)',
                  borderRadius: 'var(--radius-md)', border: '1px solid var(--color-border)',
                }}>
                  <div style={{ fontSize: '1.5rem' }}>{info.icon}</div>
                  <div style={{ flex: 1 }}>
                    <div style={{ fontWeight: 600, fontSize: '0.9rem' }}>{adapter.name}</div>
                    <div style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)', marginTop: '2px' }}>
                      {info.description}
                      {adapter.attribution_text && ` — Attribution: ${adapter.attribution_text}`}
                    </div>
                    <div style={{ display: 'flex', gap: '6px', marginTop: '6px', flexWrap: 'wrap' }}>
                      <Badge status={adapter.license_type} />
                      {adapter.allows_commercial_storage && <Badge label="Storage ✓" variant="success" />}
                      {adapter.allows_marketing_use && <Badge label="Marketing ✓" variant="success" />}
                      {!adapter.allows_marketing_use && <Badge label="No Marketing" variant="warning" />}
                      <Badge label={`${adapter.rate_limit_rpm} req/min`} variant="secondary" />
                    </div>
                  </div>
                  {alreadyRegistered ? (
                    <Badge label="Registered" variant="success" />
                  ) : (
                    <button className="btn btn-primary btn-sm" onClick={() => registerAdapter(adapter)}>
                      Register
                    </button>
                  )}
                </div>
              )
            })}
          </div>
        </div>

        {/* Registered Sources */}
        <div className="card">
          <div className="card-header">
            <div className="card-title">Registered Sources</div>
            <span style={{ fontSize: '0.8rem', color: 'var(--color-text-muted)' }}>{sources.length} source{sources.length !== 1 ? 's' : ''}</span>
          </div>

          {loading ? (
            <div style={{ display: 'flex', justifyContent: 'center', padding: '40px' }}>
              <div className="spinner spinner-lg" />
            </div>
          ) : sources.length === 0 ? (
            <div className="empty-state" style={{ padding: '40px 20px' }}>
              <div style={{ fontSize: '2.5rem', marginBottom: '12px' }}>🗄️</div>
              <div className="empty-state-title">No sources registered</div>
              <div className="empty-state-description">Register the built-in adapters above to start discovering businesses</div>
            </div>
          ) : (
            <div className="table-container">
              <table>
                <thead>
                  <tr>
                    <th>Source</th>
                    <th>License</th>
                    <th>Storage</th>
                    <th>Marketing</th>
                    <th>Rate Limit</th>
                    <th>Status</th>
                    <th>Attribution</th>
                  </tr>
                </thead>
                <tbody>
                  {sources.map(src => (
                    <tr key={src.id}>
                      <td>
                        <div style={{ fontWeight: 600, color: 'var(--color-text-primary)', fontSize: '0.85rem' }}>{src.name}</div>
                        <div style={{ fontSize: '0.72rem', color: 'var(--color-text-muted)' }}>{src.slug}</div>
                      </td>
                      <td><Badge status={src.license_type} /></td>
                      <td>
                        <span style={{ color: src.allows_commercial_storage ? 'var(--color-accent-success)' : 'var(--color-accent-danger)' }}>
                          {src.allows_commercial_storage ? '✓' : '✗'}
                        </span>
                      </td>
                      <td>
                        <span style={{ color: src.allows_marketing_use ? 'var(--color-accent-success)' : 'var(--color-accent-danger)' }}>
                          {src.allows_marketing_use ? '✓' : '✗'}
                        </span>
                      </td>
                      <td style={{ fontSize: '0.78rem' }}>{src.rate_limit_rpm}/min</td>
                      <td><Badge status={src.status} /></td>
                      <td>
                        {src.attribution_required ? (
                          <span style={{ fontSize: '0.75rem', color: 'var(--color-accent-warning)' }}>Required</span>
                        ) : (
                          <span style={{ fontSize: '0.75rem', color: 'var(--color-text-muted)' }}>Not required</span>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>
    </>
  )
}
